# -*- coding: utf-8 -*-
"""Captura os prints da aplicação Django para o PPT da Sprint 3.

A entrega da Sprint 3 mostra a aplicação por print, e não no ar. Este script existe para
que o print seja reproduzível: mesma largura, mesma densidade de pixel e mesmo estado de
tela toda vez que rodar. Sem ele, cada captura manual sai num zoom diferente e o deck fica
com telas de tamanhos que não conversam.

Uso (com o servidor já no ar em outra janela):

    .venv/Scripts/python webapp/manage.py runserver 8765 --noreload
    .venv/Scripts/python scripts/captura_telas.py

Saída: `sprints/sprint-3/prints/*.png`, em 2× (retina) para não borrar ao projetar.

Requer o Chrome do sistema — o browser do Playwright não baixa nesta máquina, então o
`channel="chrome"` aponta para a instalação local.
"""
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://127.0.0.1:8765"
RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "sprints" / "sprint-3" / "prints"

# 1600 é a largura em que o painel foi desenhado para respirar: abaixo disso os pares de
# cartão P2/P3 empilham, e o print deixaria de mostrar as duas prioridades lado a lado.
LARGURA = 1600
ALTURA_JANELA = 1000
ESCALA = 2

# Uma entrada por aba, capturada no tamanho da janela — não a página inteira. O slide reserva
# um retângulo 16:10 para o print, e captura de página inteira sai retrato: encolhida para caber
# na altura do slide, ficaria estreita demais para alguém ler um número.
#
# `rolagem` é o quanto descer antes de disparar, em px de CSS. A barra de navegação é `sticky`,
# então ela continua no print mesmo rolado, e a tela segue reconhecível como a aplicação.
# Só a Saúde precisa disso: o ranking dos 15 produtos é o conteúdo da aba, e no topo aparecem
# quatro linhas dele.
TELAS = [
    ("01-panorama", "/", 0),
    ("02-previsao", "/previsao/", 0),
    ("03-projecao", "/projecao/", 0),
    ("04-fila", "/fila/", 0),
    ("05-saude", "/saude/", 300),
    ("06-causas", "/causas/", 0),
]

# Modais que valem print: cada um responde a uma exigência do desafio que a tela de fundo
# sozinha não responde. `gatilho` é o seletor do que abre; `espera`, o que confirma que o
# fragmento chegou do servidor.
MODAIS = [
    (
        "07-modal-briefing",
        "/",
        None,  # o briefing abre sozinho na primeira visita da sessão
        "#brov .brf",
    ),
    (
        "08-modal-escore",
        "/fila/",
        '[data-mod="incidente"]',
        "#mc .md-h",
    ),
    (
        "09-modal-produto",
        "/saude/",
        '[data-mod="produto"]',
        "#mc .md-h",
    ),
    (
        "10-modal-meta",
        "/projecao/",
        '[data-mod="meta"]',
        "#mc",
    ),
]

# Animação de entrada e cursor piscando entram no print como borrão ou como estado pela
# metade. A captura precisa do quadro final, não do caminho até ele.
CONGELA_ANIMACAO = """
* , *::before, *::after {
  animation-duration: 0s !important;
  animation-delay: 0s !important;
  transition-duration: 0s !important;
  transition-delay: 0s !important;
}
::-webkit-scrollbar { display: none !important; }
"""


def _prepara(page: Page, rota: str) -> None:
    """Abre a rota e espera a tela assentar (fontes, gráficos e fetch pendente)."""
    page.goto(f"{BASE_URL}{rota}", wait_until="networkidle")
    page.add_style_tag(content=CONGELA_ANIMACAO)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(700)


def captura_telas(page: Page) -> None:
    """Um print por aba, com o briefing dispensado para não cobrir o Panorama."""
    for nome, rota, rolagem in TELAS:
        _prepara(page, rota)
        # O briefing é modal de entrada e cobre o Panorama inteiro. Ele tem print próprio
        # mais abaixo; aqui a aba precisa aparecer limpa.
        page.evaluate("document.getElementById('brov')?.setAttribute('hidden','')")
        if rolagem:
            page.evaluate(f"window.scrollTo(0, {rolagem})")
        page.wait_for_timeout(400)

        page.screenshot(path=SAIDA / f"{nome}.png")
        print(f"  {nome}.png")


def captura_modais(page: Page) -> None:
    """Um print por modal, no enquadramento da janela — é assim que ele aparece em uso."""
    for nome, rota, gatilho, espera in MODAIS:
        _prepara(page, rota)

        if gatilho is not None:
            page.evaluate("document.getElementById('brov')?.setAttribute('hidden','')")
            page.locator(gatilho).first.click()
        page.wait_for_selector(espera, timeout=15_000)
        page.wait_for_timeout(900)

        page.screenshot(path=SAIDA / f"{nome}.png")
        print(f"  {nome}.png")


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel="chrome")
        contexto = navegador.new_context(
            viewport={"width": LARGURA, "height": ALTURA_JANELA},
            device_scale_factor=ESCALA,
        )
        # O briefing marca em `sessionStorage` que já foi visto e não reabre. Zerar antes de
        # cada navegação mantém toda captura partindo do mesmo estado de primeira visita.
        contexto.add_init_script("sessionStorage.clear()")
        page = contexto.new_page()

        print(f"Capturando em {SAIDA}")
        captura_telas(page)
        captura_modais(page)

        navegador.close()
    print("Fim.")


if __name__ == "__main__":
    main()
