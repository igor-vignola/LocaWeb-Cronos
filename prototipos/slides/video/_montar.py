# -*- coding: utf-8 -*-
"""Monta deck.html a partir do estilo compartilhado e dos blocos de slide.

Cada bloco em blocos/NN-nome.html traz um <style> com o CSS só dos slides dele,
prefixado pela classe do slide, e um ou mais <section class="slide ...">. Este
script ordena pelo NN, junta os <style> depois do _estilo.css e concatena as
<section> na ordem. O palco, o chrome de navegação e o JS moram aqui.

Uso:
    .venv/Scripts/python.exe prototipos/slides/video/_montar.py
"""
from __future__ import annotations

import re
from pathlib import Path

AQUI = Path(__file__).parent
ESTILO = AQUI / "_estilo.css"
BLOCOS = AQUI / "blocos"
SAIDA = AQUI / "deck.html"

CABECA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cronos · Deck do vídeo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600\
&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* GERADO POR _montar.py — NÃO EDITE ESTE ARQUIVO À MÃO.
   O estilo compartilhado está em _estilo.css e cada slide em blocos/NN-nome.html. */
"""

MEIO = """</style>
</head>
<body>
<div id="fit"><div id="stage">
"""

RODAPE = """
</div></div>

<div id="chrome">
  <div id="dots"></div>
  <span><kbd>&rarr;</kbd> avança &nbsp; <kbd>&larr;</kbd> volta &nbsp;
  <kbd>R</kbd> repete a animação &nbsp; <kbd>H</kbd> esconde isto &nbsp;
  <kbd>F</kbd> tela cheia</span>
</div>

<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll(".slide"));
  var stage=document.getElementById("stage");
  var dots=document.getElementById("dots");
  var chromeBar=document.getElementById("chrome");
  var i=0, timers=[];

  slides.forEach(function(){ dots.appendChild(document.createElement("i")); });
  var marks=[].slice.call(dots.children);

  function fit(){
    stage.style.transform="scale("+Math.min(window.innerWidth/1600,
      window.innerHeight/900)+")";
  }
  window.addEventListener("resize",fit); fit();

  /* numero que conta: data-to e o alvo, data-delay o atraso, data-dec as decimais */
  function contar(el){
    var alvo=parseFloat(el.getAttribute("data-to").replace(",","."));
    var dec=parseInt(el.getAttribute("data-dec")||"0",10);
    var dur=820, t0=performance.now();
    (function passo(t){
      var p=Math.min((t-t0)/dur,1);
      var v=alvo*(1-Math.pow(1-p,3));
      el.textContent=dec?v.toFixed(dec).replace(".",","):String(Math.round(v));
      if(p<1) requestAnimationFrame(passo);
    })(performance.now());
  }

  function play(n){
    timers.forEach(clearTimeout); timers=[];
    slides.forEach(function(s,k){ s.classList.toggle("is-active",k===n); });
    marks.forEach(function(m,k){ m.classList.toggle("on",k===n); });
    [].forEach.call(slides[n].querySelectorAll(".ct"),function(el){
      var dec=parseInt(el.getAttribute("data-dec")||"0",10);
      el.textContent=dec?"0,0":"0";
      timers.push(setTimeout(function(){ contar(el); },
        parseInt(el.getAttribute("data-delay"),10)||0));
    });
  }
  function replay(){
    var s=slides[i];
    s.classList.remove("is-active");
    void s.offsetWidth;              /* reflow reinicia a cascata inteira */
    play(i);
  }
  function go(n){ i=(n+slides.length)%slides.length; play(i); }

  window.addEventListener("keydown",function(e){
    var k=e.key.toLowerCase();
    if(e.key==="ArrowRight"||e.key===" "||e.key==="PageDown"){e.preventDefault();go(i+1);}
    else if(e.key==="ArrowLeft"||e.key==="PageUp"){e.preventDefault();go(i-1);}
    else if(k==="r"){replay();}
    else if(k==="h"){chromeBar.classList.toggle("hidden");}
    else if(k==="f"){ document.fullscreenElement?document.exitFullscreen()
      :document.documentElement.requestFullscreen(); }
    else if(k>="1"&&k<="9"){go(parseInt(k,10)-1);}
  });
  document.getElementById("fit").addEventListener("click",function(){ go(i+1); });

  play(0);
})();
</script>
</body>
</html>
"""

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r'(<section class="slide.*?</section>)', re.S)
# os blocos moram em blocos/, um nível mais fundo que o deck.html, então todo
# caminho relativo escrito lá tem um ../ sobrando quando vem para cá
RE_SUBIR = re.compile(r'((?:src|href)=")\.\./')


def reancora(texto: str) -> str:
    """Remove um nível de ../ dos caminhos relativos, de blocos/ para a raiz do deck."""
    return RE_SUBIR.sub(r"\1", texto)


def main() -> int:
    blocos = sorted(p for p in BLOCOS.glob("[0-9][0-9]-*.html"))
    if not blocos:
        print("nenhum bloco em blocos/NN-nome.html")
        return 1

    estilos = [ESTILO.read_text(encoding="utf-8")]
    secoes: list[str] = []

    for b in blocos:
        texto = b.read_text(encoding="utf-8")
        css = RE_STYLE.findall(texto)
        achadas = RE_SECTION.findall(texto)
        if not achadas:
            print(f"  AVISO  {b.name} nao tem <section class=\"slide ...\">")
            continue
        estilos.append(
            f"\n/* ───── {b.name} ───── */\n"
            + "\n".join(reancora(c.strip()) for c in css)
        )
        reancoradas = [reancora(s) for s in achadas]
        secoes.extend(reancoradas)
        subidas = sum(len(RE_SUBIR.findall(s)) for s in achadas)
        print(f"  {b.name}: {len(achadas)} slide(s), "
              f"{sum(len(c) for c in css)} chars de CSS, {subidas} caminho(s) reancorado(s)")

    # o primeiro slide entra ativo; os outros o JS liga
    secoes[0] = secoes[0].replace('class="slide', 'class="is-active slide', 1)

    SAIDA.write_text(
        CABECA + "\n".join(estilos) + MEIO + "\n\n".join(secoes) + RODAPE,
        encoding="utf-8",
    )
    print(f"\n{len(secoes)} slides em {SAIDA.name} ({SAIDA.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
