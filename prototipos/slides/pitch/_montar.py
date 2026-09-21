# -*- coding: utf-8 -*-
"""Monta o deck do vídeo pitch recortando o deck da banca.

Quase nada é desenhado aqui: cada slide sai inteiro de
prototipos/slides/ao-vivo/deck.html, com o mesmo HTML, o mesmo CSS e a mesma
animação que passaram na banca de 15/09. O que este script faz é escolher quais
entram e em que ordem.

A exceção são os blocos próprios do vídeo, em blocos/NN-nome.html, para o que a
banca não tinha. Eles seguem o mesmo contrato dos blocos de lá: um <style> com o
CSS prefixado e uma <section> por composição, com data-slide, data-var e
data-quem. O visualizador alterna as composições com as setas de cima e de baixo.

Uso:
    .venv/Scripts/python.exe prototipos/slides/pitch/_montar.py
"""
from __future__ import annotations

import re
from pathlib import Path

AQUI = Path(__file__).parent
FONTE = AQUI.parent / "ao-vivo" / "deck.html"
BLOCOS = AQUI / "blocos"
SAIDA = AQUI / "deck.html"

EQUIPE = {
    "igor": ("Igor", "../../../brand/equipe/igor.png"),
    "ana": ("Ana", "../../../brand/equipe/ana-beatriz.png"),
    "hygor": ("Hygor", "../../../brand/equipe/hygor.png"),
}

# ── o recorte ───────────────────────────────────────────────────────────────
# int  = número do slide no deck da banca, reaproveitado inteiro
# str  = bloco próprio do vídeo, em blocos/NN-<nome>.html
ORDEM: list[int | str] = [
    1,              # Capa
    2,              # Quem apresenta
    4,              # O prazo de cada incidente
    5,              # As quebras de OLA em 2025
    6,              # Por que é difícil ver chegando
    "objetivo",     # Objetivo do projeto (três composições, A B C)
    16,             # Divisória · Previsão de volume
    17,             # Os próximos sete dias (Prophet)
    18,             # Comparação do erro com os baselines
    19,             # Divisória · Risco de OLA
    20,             # Quebras encontradas por tamanho da fila
    22,             # Divisória · Morning Brief
    23,             # Morning Brief
    24,             # Divisória · Projeção da meta e saúde
    26,             # A meta do ano vai fechar
    27,             # Saúde por produto
    28,             # Divisória · Arquitetura da solução
    29,             # Como o Cronos antecipa o resultado do ano
    31,             # A demonstração (entra a gravação da tela)
    32,             # Obrigado
    33,             # Abra o Cronos · QR e endereço
]

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r'(<section class="slide.*?</section>)', re.S)
RE_ATRIB = re.compile(r'data-(slide|var|quem)="([^"]+)"')
RE_FT = re.compile(r'(<div class="ft">)', re.S)


def marcador(quem: str) -> str:
    nome, foto = EQUIPE[quem]
    return f'<span class="apres"><img src="{foto}" alt=""><b>{nome}</b></span>'


def secoes_de(texto: str) -> dict[int, list[tuple[str, str]]]:
    achadas: dict[int, list[tuple[str, str]]] = {}
    for s in RE_SECTION.findall(texto):
        atrib = dict(RE_ATRIB.findall(s))
        achadas.setdefault(int(atrib["slide"]), []).append((atrib.get("var", "a"), s))
    return achadas


def main() -> int:
    if not FONTE.exists():
        print(f"não achei {FONTE}")
        return 1

    texto = FONTE.read_text(encoding="utf-8")
    m = RE_STYLE.search(texto)
    if not m:
        print("o deck da banca não tem <style>")
        return 1

    estilos = [m.group(1)]
    banca = secoes_de(texto)

    # os blocos próprios do vídeo, indexados pelo nome
    proprios: dict[str, list[tuple[str, str]]] = {}
    for b in sorted(BLOCOS.glob("[0-9][0-9]-*.html")) if BLOCOS.exists() else []:
        conteudo = b.read_text(encoding="utf-8")
        nome = b.stem.split("-", 1)[1]
        estilos.append(f"\n/* ───── bloco próprio · {b.name} ───── */\n"
                       + "\n".join(c.strip() for c in RE_STYLE.findall(conteudo)))
        achadas = secoes_de(conteudo)
        if len(achadas) != 1:
            print(f"{b.name}: esperava um data-slide só, achei {sorted(achadas)}")
            return 1
        proprios[nome] = next(iter(achadas.values()))
        print(f"  bloco próprio '{nome}': {len(proprios[nome])} composições")

    faltando = [i for i in ORDEM
                if (isinstance(i, int) and i not in banca)
                or (isinstance(i, str) and i not in proprios)]
    if faltando:
        print(f"não encontrei: {faltando}")
        return 1

    partes: list[str] = []
    for novo, item in enumerate(ORDEM, start=1):
        if isinstance(item, str):
            for var, s in sorted(proprios[item]):
                s = RE_FT.sub(r"\1" + marcador(dict(RE_ATRIB.findall(s))["quem"]), s, count=1)
                s = re.sub(r'data-slide="\d+"', f'data-slide="{novo}"', s, count=1)
                partes.append(s)
            print(f"  {novo:>2}  próprio '{item}' · {len(proprios[item])} composições")
            continue

        var, s = sorted(banca[item])[0]        # a composição aprovada, "a" na frente
        # as figuras moram na pasta do deck da banca, e este deck está ao lado dela
        s = s.replace('src="figs/', 'src="../ao-vivo/figs/')
        s = s.replace('src="_png/', 'src="../ao-vivo/_png/')
        s = s.replace("url(figs/", "url(../ao-vivo/figs/")
        s = re.sub(r'data-slide="\d+"', f'data-slide="{novo}"', s, count=1)
        partes.append(s)
        print(f"  {novo:>2}  banca {item:>2}{var}  reaproveitado inteiro")

    html = CABECA + "\n".join(estilos) + MEIO + "\n\n".join(partes) + RODAPE
    SAIDA.write_text(html, encoding="utf-8")
    reais = sum(1 for i in ORDEM if isinstance(i, int))
    print(f"\n{len(ORDEM)} quadros: {reais} da banca, {len(ORDEM) - reais} próprios "
          f"· {len(partes)} composições · {SAIDA.stat().st_size // 1024} KB")
    return 0


CABECA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cronos · Vídeo pitch</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600\
&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* GERADO POR _montar.py — NÃO EDITE ESTE ARQUIVO À MÃO.
   Os slides saem inteiros do deck da banca (../ao-vivo/deck.html); os quadros
   próprios do vídeo moram em blocos/NN-nome.html. Para mudar o recorte, mexa na
   lista ORDEM do _montar.py e rode de novo. */
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
  <span><kbd>&larr;</kbd><kbd>&rarr;</kbd> slide &nbsp; <kbd>&uarr;</kbd><kbd>&darr;</kbd> versão
  &nbsp; <kbd>R</kbd> repete &nbsp; <kbd>H</kbd> esconde &nbsp; <kbd>F</kbd> tela cheia</span>
</div>

<script>
(function(){
  var todas=[].slice.call(document.querySelectorAll(".slide"));
  var stage=document.getElementById("stage");
  var chromeBar=document.getElementById("chrome");
  var pos=document.getElementById("pos");
  var timers=[];

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

  var i=0, escolha={};
  ordem.forEach(function(n){ escolha[n]=0; });

  var caixa=document.getElementById("fit");
  function fit(){
    var r=caixa.getBoundingClientRect();
    var l=Math.min(document.documentElement.clientWidth,r.width);
    var a=Math.min(document.documentElement.clientHeight,r.height);
    if(!l||!a) return;
    stage.style.transform="translate(-50%,-50%) scale("+Math.min(l/1600,a/900)+")";
  }
  if(window.ResizeObserver) new ResizeObserver(fit).observe(caixa);
  window.addEventListener("resize",fit);
  window.addEventListener("load",fit);
  document.addEventListener("fullscreenchange",fit);
  fit();

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
    var h="quadro "+n+" de "+ordem[ordem.length-1];
    if(qtd>1){
      h+=' <b class="vr"><u>&uarr;&darr;</u>'+qtd+' versões &middot; vendo a '+letra
        +'</b><span class="vp">';
      for(var k=0;k<qtd;k++) h+="<i"+(k===escolha[n]?' class="on"':"")+"></i>";
      h+="</span>";
    } else {
      h+=' <span class="vu">versão única</span>';
    }
    pos.innerHTML=h;
    if(qtd>1){ pos.classList.remove("bate"); void pos.offsetWidth; pos.classList.add("bate"); }
  }
  function replay(){
    var a=atual(); a.classList.remove("is-active"); void a.offsetWidth; play();
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
  });
  document.getElementById("fit").addEventListener("click",function(){ vaiSlide(1); });

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
