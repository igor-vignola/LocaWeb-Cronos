# -*- coding: utf-8 -*-
"""Monta o deck da banca ao vivo (15/09/2026) a partir dos blocos.

Cada bloco em blocos/NN-nome.html traz um <style> com o CSS só dos slides dele
e duas <section> por slide, uma por variação. O script ordena pelo NN, junta os
estilos depois do _estilo.css, injeta o marcador de quem apresenta e escreve o
visualizador.

Contrato do bloco:
  <section class="slide light xx" data-slide="3" data-var="a" data-quem="igor">
    ...
    <div class="ft"><span>procedência do dado</span></div>
  </section>

  data-slide  número do slide, igual nas duas variações
  data-var    "a" ou "b"
  data-quem   igor | ana | hygor, e o marcador é injetado no rodapé
  O rodapé leva UM span, com a procedência. O marcador entra antes dele.

Navegação do visualizador:
  seta direita e esquerda   troca de slide
  seta baixo e cima         alterna a variação do slide atual
  R  repete a animação      H  esconde a ajuda      F  tela cheia

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_montar.py
"""
from __future__ import annotations

import re
from pathlib import Path

AQUI = Path(__file__).parent
ESTILO = AQUI / "_estilo.css"
BLOCOS = AQUI / "blocos"
SAIDA = AQUI / "deck.html"

EQUIPE = {
    "igor": ("Igor", "../../../brand/equipe/igor.png"),
    "ana": ("Ana", "../../../brand/equipe/ana-beatriz.png"),
    "hygor": ("Hygor", "../../../brand/equipe/hygor.png"),
}

# ── ordem do deck ───────────────────────────────────────────────────────────
# Um arquivo por slide, em blocos/NN-nome.html, e o NN é a ordem. Cada arquivo
# traz duas <section>: data-var="a" e data-var="b", que são o MESMO dado em duas
# formas de mostrar. O REMAP existiu enquanto vários agentes numeravam a partir
# do próprio recorte; agora que a numeração nasce do nome do arquivo ele fica
# vazio, e é o gancho para reordenar sem tocar em bloco nenhum.
REMAP: dict[tuple[str, int, str], tuple[int, str, str | None]] = {}

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r"(<section class=\"slide.*?</section>)", re.S)
RE_SUBIR = re.compile(r'((?:src|href)=")\.\./')
RE_ATRIB = re.compile(r'data-(slide|var|quem)="([^"]+)"')
RE_FT = re.compile(r'(<div class="ft">)', re.S)


def reancora(texto: str) -> str:
    """Os blocos moram um nível mais fundo que o deck, então sobra um ../ neles."""
    return RE_SUBIR.sub(r"\1", texto)


def marcador(quem: str) -> str:
    nome, foto = EQUIPE[quem]
    return (
        f'<span class="apres"><img src="{foto}" alt="">'
        f"<b>{nome}</b> apresenta</span>"
    )


def injeta_marcador(secao: str, quem: str) -> str:
    if quem not in EQUIPE:
        raise SystemExit(f'data-quem="{quem}" não é igor, ana nem hygor')
    if '<div class="ft">' not in secao:
        raise SystemExit(f'seção de {quem} sem <div class="ft">, o marcador não tem onde ir')
    return RE_FT.sub(r"\1" + marcador(quem), secao, count=1)


def main() -> int:
    blocos = sorted(p for p in BLOCOS.glob("[0-9][0-9]-*.html"))
    if not blocos:
        print("nenhum bloco em blocos/NN-nome.html")
        return 1

    estilos = [ESTILO.read_text(encoding="utf-8")]
    secoes: list[tuple[int, str, str]] = []  # (slide, var, html)
    problemas: list[str] = []

    for b in blocos:
        texto = b.read_text(encoding="utf-8")
        css = RE_STYLE.findall(texto)
        achadas = RE_SECTION.findall(texto)
        if not achadas:
            problemas.append(f"{b.name}: nenhuma <section class=\"slide ...\">")
            continue

        estilos.append(
            f"\n/* ───── {b.name} ───── */\n"
            + "\n".join(reancora(c.strip()) for c in css)
        )

        for s in achadas:
            atrib = dict(RE_ATRIB.findall(s))
            faltando = [k for k in ("slide", "var", "quem") if k not in atrib]
            if faltando:
                problemas.append(f"{b.name}: seção sem data-{', data-'.join(faltando)}")
                continue
            origem = (b.name, int(atrib["slide"]), atrib["var"])
            slide, var, dono = REMAP.get(
                origem, (int(atrib["slide"]), atrib["var"], None)
            )
            s = injeta_marcador(reancora(s), dono or atrib["quem"])
            if origem in REMAP:
                # o data-var do HTML tem que bater com a posição final, senão o
                # visualizador ordena as candidatas pelo valor antigo
                s = re.sub(r'data-slide="\d+"', f'data-slide="{slide}"', s, count=1)
                s = re.sub(r'data-var="[^"]+"', f'data-var="{var}"', s, count=1)
                if dono:
                    # o atributo também, senão o HTML montado diz um dono e o
                    # marcador injetado mostra outro, e quem for ler se perde
                    s = re.sub(r'data-quem="[^"]+"', f'data-quem="{dono}"', s, count=1)
                troca = f", dono {atrib['quem']} -> {dono}" if dono and dono != atrib["quem"] else ""
                print(f"    remapeado  slide {origem[1]}{origem[2]} -> {slide}{var}{troca}")
            secoes.append((slide, var, s))

        print(f"  {b.name}: {len(achadas)} seção(ões), {sum(len(c) for c in css)} chars de CSS")

    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print(f"  {p}")
        return 1

    secoes.sort(key=lambda t: (t[0], t[1]))
    numeros = sorted({n for n, _, _ in secoes})
    for n in numeros:
        vars_do_slide = sorted(v for m, v, _ in secoes if m == n)
        # slide já aprovado fica com uma forma só: as descartadas saem do arquivo.
        # Slide ainda em escolha tem duas, para o dono do projeto alternar e decidir.
        if len(set(vars_do_slide)) != len(vars_do_slide):
            print(f"  AVISO  slide {n} tem data-var repetido: {vars_do_slide}")

    corpo = "\n\n".join(s for _, _, s in secoes)
    html = CABECA + "\n".join(estilos) + MEIO + corpo + RODAPE
    SAIDA.write_text(html, encoding="utf-8")

    print(f"\n{len(numeros)} slides, {len(secoes)} composições, {SAIDA.stat().st_size // 1024} KB")
    return 0


CABECA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cronos · Banca 15/09</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600\
&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* GERADO POR _montar.py — NÃO EDITE ESTE ARQUIVO À MÃO.
   Estilo compartilhado em _estilo.css, cada slide em blocos/NN-nome.html. */
"""

MEIO = """</style>
</head>
<body>
<div id="fit"><div id="stage">
"""

RODAPE = """
</div></div>

<div id="chrome">
  <span id="pos"></span>
  <span><kbd>&larr;</kbd><kbd>&rarr;</kbd> slide &nbsp; <kbd>&uarr;</kbd><kbd>&darr;</kbd> variação
  &nbsp; <kbd>R</kbd> repete &nbsp; <kbd>H</kbd> esconde &nbsp; <kbd>F</kbd> tela cheia</span>
</div>

<script>
(function(){
  var todas=[].slice.call(document.querySelectorAll(".slide"));
  var stage=document.getElementById("stage");
  var chromeBar=document.getElementById("chrome");
  var pos=document.getElementById("pos");
  var timers=[];

  /* agrupa as composições por slide, na ordem do data-slide */
  var mapa={}, ordem=[];
  todas.forEach(function(s){
    var n=parseInt(s.getAttribute("data-slide"),10);
    if(!mapa[n]){ mapa[n]=[]; ordem.push(n); }
    mapa[n].push(s);
  });
  ordem.sort(function(a,b){return a-b;});
  ordem.forEach(function(n){
    mapa[n].sort(function(a,b){
      return a.getAttribute("data-var").localeCompare(b.getAttribute("data-var"));
    });
  });

  var i=0;                                   /* índice do slide na ordem */
  var escolha={};                             /* variação escolhida por slide */
  ordem.forEach(function(n){ escolha[n]=0; });

  /* a escala sai da caixa que de fato existe, não de window.innerHeight: ao
     abrir o arquivo direto no navegador a barra de favoritos e a de abas ainda
     não tinham entrado na conta e o slide saía cortado embaixo até entrar em
     tela cheia. O ResizeObserver cobre todo o resto: zoom, devtools, F11. */
  var caixa=document.getElementById("fit");
  function fit(){
    var r=caixa.getBoundingClientRect();
    if(!r.width||!r.height) return;
    stage.style.transform="scale("+Math.min(r.width/1600,r.height/900)+")";
  }
  if(window.ResizeObserver) new ResizeObserver(fit).observe(caixa);
  window.addEventListener("resize",fit);
  window.addEventListener("load",fit);
  window.addEventListener("orientationchange",fit);
  document.addEventListener("fullscreenchange",fit);
  fit();

  /* pt-BR: ponto como separador de milhar, senão 21561 aparece cru na tela */
  function fmt(n){ return n.toLocaleString("pt-BR"); }

  function contar(el){
    var alvo=parseFloat(el.getAttribute("data-to").replace(",","."));
    var dec=parseInt(el.getAttribute("data-dec")||"0",10);
    var dur=820, t0=performance.now();
    (function passo(t){
      var p=Math.min((t-t0)/dur,1);
      var v=alvo*(1-Math.pow(1-p,3));
      el.textContent=dec?v.toFixed(dec).replace(".",","):fmt(Math.round(v));
      if(p<1) requestAnimationFrame(passo);
    })(performance.now());
  }

  function atual(){ var n=ordem[i]; return mapa[n][escolha[n]]; }

  function play(){
    timers.forEach(clearTimeout); timers=[];
    var alvo=atual();
    todas.forEach(function(s){ s.classList.toggle("is-active",s===alvo); });
    [].forEach.call(alvo.querySelectorAll(".ct"),function(el){
      var dec=parseInt(el.getAttribute("data-dec")||"0",10);
      el.textContent=dec?"0,0":"0";
      timers.push(setTimeout(function(){ contar(el); },
        parseInt(el.getAttribute("data-delay"),10)||0));
    });
    var n=ordem[i], qtd=mapa[n].length;
    var letra=alvo.getAttribute("data-var").toUpperCase();
    /* o indicador diz, sem apertar seta, se aquele slide tem outra composição:
       pílula azul com as bolinhas quando tem, cinza apagado quando é único. */
    var h="slide "+n+" de "+ordem[ordem.length-1];
    if(qtd>1){
      h+=' <b class="vr"><u>&uarr;&darr;</u>'+qtd+' versões &middot; vendo a '+letra
        +'</b><span class="vp">';
      for(var k=0;k<qtd;k++) h+="<i"+(k===escolha[n]?' class="on"':"")+"></i>";
      h+="</span>";
    } else {
      h+=' <span class="vu">versão única</span>';
    }
    pos.innerHTML=h;
    /* a pílula pisca uma vez ao chegar num slide que tem outra versão */
    if(qtd>1){ pos.classList.remove("bate"); void pos.offsetWidth;
      pos.classList.add("bate"); }
  }
  function replay(){
    var a=atual();
    a.classList.remove("is-active");
    void a.offsetWidth;                      /* reflow reinicia a cascata */
    play();
  }
  function vaiSlide(d){ i=(i+d+ordem.length)%ordem.length; play(); }
  function vaiVar(d){
    var n=ordem[i], qtd=mapa[n].length;
    escolha[n]=(escolha[n]+d+qtd)%qtd;
    play();
  }

  window.addEventListener("keydown",function(e){
    var k=e.key.toLowerCase();
    if(e.key==="ArrowRight"||e.key===" "||e.key==="PageDown"){e.preventDefault();vaiSlide(1);}
    else if(e.key==="ArrowLeft"||e.key==="PageUp"){e.preventDefault();vaiSlide(-1);}
    else if(e.key==="ArrowDown"){e.preventDefault();vaiVar(1);}
    else if(e.key==="ArrowUp"){e.preventDefault();vaiVar(-1);}
    else if(k==="r"){replay();}
    else if(k==="h"){chromeBar.classList.toggle("hidden");}
    else if(k==="f"){ document.fullscreenElement?document.exitFullscreen()
      :document.documentElement.requestFullscreen(); }
    else if(k>="1"&&k<="9"){
      var n=parseInt(k,10), j=ordem.indexOf(n);
      if(j>=0){ i=j; play(); }
    }
  });
  document.getElementById("fit").addEventListener("click",function(){ vaiSlide(1); });

  /* gancho para o _verifica.py navegar sem depender de tecla: a navegação por
     número no teclado só cobre 1 a 9, e o deck passou de nove slides. */
  window.cronosIr=function(slide,varIdx){
    var j=ordem.indexOf(slide);
    if(j<0) return false;
    i=j;
    if(typeof varIdx==="number"){
      var qtd=mapa[slide].length;
      escolha[slide]=Math.min(Math.max(varIdx,0),qtd-1);
    }
    play();
    return true;
  };

  play();
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
