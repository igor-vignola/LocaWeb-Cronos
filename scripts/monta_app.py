# -*- coding: utf-8 -*-
"""Monta prototipos/telas/app.html — a aplicacao Cronos completa.

Cinco abas na mesma regua visual, navegacao sem recarregar, modal de aprofundamento em
incidente, ativo e produto, paleta de comando em Ctrl+K e o morning brief como porta de
entrada. Todo numero sai de parquet gerado por notebook.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'direcoes'))
from abas import ABAS, CALMO, HOJE_ACIMA10, HOJE_MAX, PIOR, TOPO
from componentes import barras_mes, ico
from dados import (ATIVOS, COMPONENTES, DIA_HOJE, EM_ABERTO, FILA_HOJE, FILA_TODA, HIST_ATIVO,
                   HOJE2, HOJE3, MEDIA_BASE, MES_LBL, N_FILA, ONTEM, ONTEM_TOTAL, ONTEM_VIOL,
                   TOP50_PEGA, VIOL_PERIODO, dm, mil, proj, pt, saude)
from estilo import CSS as CSS_BASE
from fundo import CSS_CAMPO, campo
from icones import CSS_ICO_CLARO

OUT = Path.cwd() / 'prototipos' / 'telas' / 'app.html'
OUT.parent.mkdir(parents=True, exist_ok=True)

# ── dados que o modal e a paleta consomem ──────────────────────────────────
MOD_INC = {r['incidente']: {
    'id': r['incidente'], 'risco': round(float(r['risco']), 1), 'pri': r['prioridade'],
    'produto': r['produto'], 'categoria': r['categoria'], 'subcategoria': r['subcategoria'],
    'equipe': r['equipe'], 'ativo': r['ativo'] if r['ativo'] != 'None' else 'sem ativo', 'dia': dm(r['dia']), 'hora': int(r['hora']),
    'pos': int(r['posicao']), 'av': int(r['ativo_violacoes']), 'ap': int(r['ativo_passagens']),
    'sinais': r['sinais'], 'cob': float(r['sinais_cobertura']),
    'em100': int(round(float(r['risco']))),
} for _, r in FILA_TODA.head(400).iterrows()}

MOD_ATIVO = {a: {'nome': a, 'pass': int(r['passagens']), 'viol': int(r['violacoes']),
                 'taxa': round(float(r['taxa']), 1),
                 'x': int(round(r['taxa'] / MEDIA_BASE)) if r['taxa'] else 0,
                 'hist': HIST_ATIVO.get(a, [])} for a, r in ATIVOS.iterrows()}

MOD_PROD = {p: {'nome': p, 'nota': pt(saude.loc[p, 'nota']), 'pos': int(saude.loc[p, 'posicao']),
                'quad': saude.loc[p, 'quadrante'], 'inc': mil(saude.loc[p, 'incidentes']),
                'viol': int(saude.loc[p, 'violacoes']),
                'comp': [{'rot': rot, 'v': pt(saude.loc[p, k] * mult, 2 if mult == 100 else 1),
                          'u': u, 'pos': round(float(saude.loc[p, 'pos_' + k]) * 100)}
                         for k, rot, u, mult in COMPONENTES]} for p in saude.index}

# a paleta de comando indexa tudo que da para abrir
PALETA = ([{'t': 'aba', 'k': k, 'r': nome, 's': 'ir para a aba'} for k, nome, _, _ in ABAS]
          + [{'t': 'inc', 'k': i, 'r': i, 's': f'{c["produto"]} · {c["equipe"]} · risco '
              f'{pt(c["risco"])}%'} for i, c in list(MOD_INC.items())[:120]]
          + [{'t': 'ativo', 'k': a, 'r': a, 's': f'{v["viol"]} de {v["pass"]} passagens '
              f'violaram'} for a, v in list(MOD_ATIVO.items())[:60]]
          + [{'t': 'prod', 'k': p, 'r': p, 's': f'nota {v["nota"]} · posição {v["pos"]} de 17'}
             for p, v in MOD_PROD.items()])

CSS_APP = r"""
/* navegacao entre abas */
.tl{animation:ent .5s var(--e) both}
.tl[hidden]{display:none}
@keyframes ent{from{opacity:0;transform:translateY(10px)}}
.lk{margin-left:auto;display:inline-flex;align-items:center;gap:5px;background:0;border:0;
 font:inherit;font-size:11.5px;font-weight:600;color:var(--ac);cursor:pointer;
 transition:gap .32s var(--e);flex-shrink:0}
.lk:hover{gap:9px}
/* faixa de 24h no card */
.fx24 svg{width:100%;height:auto;overflow:visible;display:block}
.h24{transform-origin:bottom;animation:hb .55s var(--e) both;
 animation-delay:calc(var(--i)*22ms);cursor:pointer;transition:filter .25s var(--e)}
@keyframes hb{from{opacity:0;transform:scaleY(.15)}}
.h24:hover{filter:brightness(.86)}
.h24.t-ok{fill:#BCD1FA}.h24.t-wn{fill:#F2C486}.h24.t-no{fill:#EE7C74}
.h24-ag{stroke:var(--ink);stroke-width:1.4;stroke-dasharray:3 3;opacity:0;
 animation:fd .5s ease .9s forwards;--o:.5}
.h24-n{fill:var(--ink);opacity:0;animation:pn .4s var(--e2) 1s forwards}
.h24-al{fill:var(--ink);font-size:9.5px;font-weight:700;letter-spacing:.09em;
 text-transform:uppercase;font-family:'Outfit',sans-serif;opacity:0;
 animation:fd .5s ease 1.1s forwards;--o:1}
.h24-x{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.h24-l{display:flex;gap:14px;margin-top:8px;flex-wrap:wrap;align-items:center}
.h24-l span{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--tx2)}
.h24-l i{width:9px;height:9px;border-radius:3px}
.h24-l i.t-ok{background:#BCD1FA}.h24-l i.t-wn{background:#F2C486}.h24-l i.t-no{background:#EE7C74}
.h24-l .dica{margin-left:auto;color:var(--tx3)}
/* heroi */
.hc{width:380px;flex-shrink:0}
.hc svg{width:100%;height:auto;overflow:visible;display:block}
.hl-l{fill:none;stroke:var(--ac);stroke-width:4.4;stroke-linecap:round;stroke-linejoin:round;
 stroke-dasharray:1000;stroke-dashoffset:1000;animation:dw 1.9s var(--e) .3s forwards}
.hl-f{fill:none;stroke:var(--ac);stroke-width:3;stroke-linecap:round;stroke-dasharray:7 7;
 opacity:0;animation:fd .9s ease 1.7s forwards;--o:.55}
.hl-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.8s forwards;--o:.11}
.hl-n{fill:var(--ac);opacity:0;animation:pn .5s var(--e2) 1.6s forwards}
.hl-o1{fill:none;stroke:var(--ac);stroke-width:2;opacity:0;animation:fd .5s ease 1.8s forwards;--o:.4}
.hl-o2,.hl-o3{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center}
.hl-o2{animation:on 3.4s ease-out 2s infinite}
.hl-o3{animation:on 3.4s ease-out 2.6s infinite}
@keyframes on{0%{opacity:.2;transform:scale(.45)}70%,100%{opacity:0;transform:scale(1.5)}}
.hl-x{fill:var(--tx3);font-size:10px;font-weight:600;letter-spacing:.08em;
 text-transform:uppercase;font-family:'Outfit',sans-serif}
.hl-x.ag{fill:var(--ac);font-weight:700}
.hc-v{display:flex;align-items:center;gap:15px;justify-content:center;margin-top:4px}
.hc-v b{font-size:62px;font-weight:700;letter-spacing:-.055em;line-height:.9}
.hc-vt{text-align:left}
.hc-z{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;padding:4px 11px;border-radius:8px}
.hc-z.z-ok{background:var(--okl);color:var(--ok)}
.hc-z.z-ac{background:var(--acl);color:var(--ac)}
.hc-z.z-no{background:var(--nol);color:var(--no)}
.hc-vt em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:6px;
 line-height:1.5;max-width:24ch}
/* tabela */
.tbw{overflow-x:auto;margin:0 -4px;padding:0 4px}
.tb{width:100%;border-collapse:collapse;font-size:13px}
.tb th{font-size:9.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx3);text-align:right;padding:0 10px 10px;white-space:nowrap}
.tb th:nth-child(1),.tb th:nth-child(2){text-align:left}
.tb td{padding:9px 10px;border-top:1px solid var(--ln);text-align:right;white-space:nowrap}
.tb td:nth-child(1),.tb td:nth-child(2){text-align:left}
.tb tbody tr{transition:background .25s var(--e)}
.tb tbody tr[data-mod]{cursor:pointer}
.tb tbody tr[data-mod]:hover{background:var(--pg)}
.tb .o{color:var(--tx3);font-size:11.5px;width:34px;font-variant-numeric:tabular-nums}
.tb .dm{color:var(--tx2)}
.tb .no{color:var(--no);font-weight:600}
.tb .rc{display:flex;align-items:center;gap:9px;justify-content:flex-end;font-weight:650;
 font-variant-numeric:tabular-nums}
.tb .rc small{font-size:.76em;color:var(--tx2);margin-left:-5px}
.rb{width:52px;height:6px;border-radius:3px;background:#EDEFF3;overflow:hidden;flex-shrink:0}
.rb i{display:block;height:100%;border-radius:3px;width:0;background:var(--c);
 animation:gw .9s var(--e) both;animation-delay:calc(300ms + var(--i,0)*22ms)}
.tb.sm{font-size:12.5px}
.tb.sm td{padding:8px 9px}
.tag{font-size:9.5px;font-weight:700;letter-spacing:.06em;padding:3px 8px;border-radius:6px;
 text-transform:uppercase;white-space:nowrap}
.tag.ok{background:var(--okl);color:var(--ok)}.tag.no{background:var(--nol);color:var(--no)}
.tag.wn{background:var(--wnl);color:var(--wn)}.tag.az{background:var(--acl);color:var(--ac)}
/* resumo por faixa */
.fxs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}
.fx{background:var(--c);border:1px solid var(--ln);border-radius:16px;padding:14px 16px;
 cursor:pointer;font:inherit;text-align:left;box-shadow:var(--s1);
 transition:all .34s var(--e)}
.fx:hover{transform:translateY(-2px);box-shadow:var(--s2)}
.fx.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink),var(--s1)}
.fx em{font-size:9.5px;font-style:normal;font-weight:700;letter-spacing:.11em;
 text-transform:uppercase;display:block}
.f-no{color:var(--no)}.f-wn{color:var(--wn)}.f-ok{color:var(--ok)}.f-ac{color:var(--ac)}
.fx b{font-size:27px;font-weight:650;letter-spacing:-.04em;display:block;margin-top:5px;
 line-height:1}
.fx span{font-size:11px;color:var(--tx2);display:block;margin-top:3px}
/* regua de risco */
.reg{display:flex;flex-direction:column;gap:2px}
.rg-l{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--ln)}
.rg-l:last-child{border:0}
.rg-b{width:10px;height:32px;border-radius:4px;flex-shrink:0}
.rg-b.f-no{background:var(--no)}.rg-b.f-wn{background:var(--wn)}.rg-b.f-ok{background:var(--ok)}
.rg-l div{flex:1}
.rg-l b{font-size:13px;font-weight:600;display:block}
.rg-l span{font-size:11px;color:var(--tx2)}
.rg-l em{font-size:12px;font-style:normal;color:var(--tx2);font-weight:600;
 font-variant-numeric:tabular-nums}
/* componentes da nota */
.cps{display:flex;flex-direction:column;gap:2px}
.cp{padding:10px 0;border-bottom:1px solid var(--ln)}
.cp:last-child{border:0}
.cp b{font-size:13px;font-weight:600;display:block}
.cp span{font-size:11.5px;color:var(--tx2);line-height:1.5}
/* recorrentes */
.rcs{display:flex;flex-direction:column;gap:2px}
.rc2{padding:10px 0;border-bottom:1px solid var(--ln);animation:sl .5s var(--e) both;
 animation-delay:calc(120ms + var(--i)*55ms)}
.rc2:last-child{border:0}
.rc2-t{font-size:12.5px;font-weight:500;display:block;color:var(--hd)}
.rc2-m{font-size:11px;color:var(--tx2);display:block;margin-top:3px}
.rc2-m b{color:var(--hd);font-weight:650}.rc2-m b.no{color:var(--no)}.rc2-m b.ok{color:var(--ok)}
/* achados no card escuro */
.ach{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ac2{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);border-radius:16px;
 padding:16px 18px}
.ac2 b{font-size:14px;font-weight:650;display:block;color:#fff}
.ac2 span{font-size:12px;color:#98A2B3;line-height:1.55;display:block;margin-top:6px}
/* barras por dia da semana */
.sms{display:flex;align-items:flex-end;gap:9px;height:120px;margin-top:8px}
.sm{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;
 justify-content:flex-end}
.sm i{width:62%;height:var(--h);border-radius:8px 8px 3px 3px;background:#DFE4EC;
 transform:scaleY(0);transform-origin:bottom;animation:gu .8s var(--e) both;
 animation-delay:calc(300ms + var(--i)*55ms)}
@keyframes gu{to{transform:scaleY(1)}}
.sm span{font-size:10.5px;color:var(--tx2)}
.sm em{font-size:11px;font-style:normal;color:var(--tx3);font-variant-numeric:tabular-nums}
.sm.ag i{background:var(--ac)}.sm.ag span{color:var(--ac);font-weight:650}
.sm.ag em{color:var(--ac)}
/* estado vazio */
.vz{display:flex;flex-direction:column;align-items:center;text-align:center;padding:34px 20px;
 gap:4px}
.vz .chp{margin-bottom:8px}
.vz b{font-size:14.5px;font-weight:650}
.vz span{font-size:12.5px;color:var(--tx2);max-width:44ch;line-height:1.55}
.mr.cl{cursor:pointer;width:100%;font:inherit;color:inherit;text-align:left;
 transition:all .3s var(--e)}
.mr.cl:hover{background:var(--c);border-color:var(--ln2);box-shadow:var(--s1);
 transform:translateX(3px)}
.mr .sq{color:var(--tx3);transition:transform .3s var(--e),color .3s var(--e)}
.mr.cl:hover .sq{color:var(--ac);transform:translateX(3px)}
.mh{width:100%;height:auto}
.mh-p{fill:#E4E8EE}.mh-v{fill:var(--no)}
.mh-l{fill:var(--tx3);font-size:9.5px;font-family:'Outfit',sans-serif}
/* paleta de comando */
.pl{position:fixed;inset:0;z-index:120;display:grid;place-items:start center;padding:12vh 20px;
 background:rgba(12,16,23,.4);backdrop-filter:blur(8px);animation:fd .22s ease both;--o:1}
.pl[hidden]{display:none}
.pl-c{width:min(560px,100%);background:var(--c);border-radius:20px;overflow:hidden;
 box-shadow:0 36px 80px -24px rgba(12,16,23,.42);animation:mu .38s var(--e) both}
.pl-i{display:flex;align-items:center;gap:11px;padding:16px 18px;border-bottom:1px solid var(--ln)}
.pl-i .ic{color:var(--tx3)}
.pl-i input{flex:1;border:0;outline:0;font:inherit;font-size:15.5px;background:0;color:var(--hd)}
.pl-i input::placeholder{color:var(--tx3)}
.pl-k{font-size:10px;font-weight:700;color:var(--tx3);background:var(--pg);
 border:1px solid var(--ln);border-radius:6px;padding:3px 7px}
.pl-r{max-height:46vh;overflow:auto;padding:7px}
.pl-o{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:11px;
 cursor:pointer;width:100%;background:0;border:0;font:inherit;text-align:left;color:inherit}
.pl-o.on{background:var(--pg)}
.pl-o .tp2{font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ac);background:var(--acl);border-radius:5px;padding:3px 7px;flex-shrink:0;width:52px;
 text-align:center}
.pl-o b{font-size:13.5px;font-weight:600}
.pl-o span{font-size:11.5px;color:var(--tx2);display:block}
.pl-vz{padding:26px;text-align:center;font-size:13px;color:var(--tx2)}
/* morning brief */
.br-ov{position:fixed;inset:0;z-index:110;display:grid;place-items:center;padding:28px;
 background:rgba(12,16,23,.38);backdrop-filter:blur(10px);animation:fd .35s ease both;--o:1}
.br-ov[hidden]{display:none}
.brf{width:min(660px,100%);max-height:88dvh;overflow:auto;background:var(--c);border-radius:26px;
 padding:30px 32px;box-shadow:0 44px 96px -26px rgba(12,16,23,.42);
 animation:mu .5s var(--e) both;position:relative}
.brf-t{display:flex;align-items:center;gap:12px}
.brf-s{font-size:11.5px;font-weight:600;color:var(--tx2);letter-spacing:.02em}
.brf-t .ct{margin-left:auto;background:var(--pg);border:1px solid var(--ln);padding:4px 10px;
 border-radius:6px;font-size:10.5px;color:var(--tx2)}
.brf h2{font-size:30px;font-weight:650;letter-spacing:-.038em;margin-top:16px;line-height:1.16}
.brf h2 .mu{color:var(--tx3);font-weight:400}
.brf-b{margin-top:16px}
.brf-b p{font-size:14.5px;line-height:1.68;color:var(--tx);margin-bottom:12px}
.brf-b b{color:var(--hd);font-weight:650}
.brf-b em{font-style:normal;font-weight:700;color:var(--hd)}
.brf-a{margin-top:18px;display:flex;flex-direction:column;gap:8px}
.ax{display:flex;align-items:center;gap:11px;font:inherit;font-size:13.5px;color:var(--tx);
 background:var(--pg);border:1px solid var(--ln);border-radius:14px;padding:13px 15px;
 cursor:pointer;text-align:left;width:100%;transition:all .32s var(--e)}
.ax:hover{background:var(--c);border-color:rgba(37,99,235,.24);color:var(--hd);
 box-shadow:var(--s1);transform:translateX(3px)}
.ax-d{font-size:9.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ac);background:var(--acl);border-radius:5px;padding:3px 8px;flex-shrink:0}
.ax .ic{margin-left:auto;color:var(--tx3)}
.brf-f{display:flex;align-items:center;gap:16px;margin-top:22px;padding-top:16px;
 border-top:1px solid var(--ln)}
.brf-f .ct{font-size:11px;color:var(--tx3);max-width:36ch;line-height:1.5}
.brf-f .bt{margin-left:auto}
.bl{position:relative;background:var(--c);border:1px solid var(--ln);border-radius:11px;
 width:36px;height:36px;display:grid;place-items:center;cursor:pointer;color:var(--tx);
 box-shadow:var(--s1);transition:all .3s var(--e)}
.bl:hover{color:var(--ac);transform:translateY(-1px);box-shadow:var(--s2)}
.bl b{position:absolute;top:-4px;right:-4px;min-width:16px;height:16px;border-radius:8px;
 background:var(--no);color:#fff;font-size:9.5px;font-weight:700;display:grid;place-items:center;
 box-shadow:0 0 0 2px var(--pg)}

/* ── ajustes da aplicacao Django: a navegacao virou <a> ─────────────────── */
.pil a,.da,.ax,.lk{text-decoration:none;color:inherit}
.pil a{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:500;
 color:var(--tx2);padding:8px 14px;border-radius:9px;transition:all .34s var(--e);
 white-space:nowrap}
.pil a:hover{color:var(--hd)}
.pil a.on{background:var(--ink);color:#fff}
a.da{display:block}
.lk{color:var(--ac)}
.rod{display:flex;gap:20px;flex-wrap:wrap;margin-top:56px;padding-top:20px;
 border-top:1px solid var(--ln);font-size:11px;color:var(--tx3);line-height:1.6}
.rod span:last-child{margin-left:auto}
/* faixa antes do numero: a previsao e um intervalo */
.fxv{display:flex;align-items:baseline;justify-content:center;gap:9px;margin-top:6px;
 flex-wrap:wrap}
.fxv b{font-size:52px;font-weight:700;letter-spacing:-.055em;line-height:.9}
.fxv-r,.fxv-e{font-size:13px;color:var(--tx2);font-weight:500}
.fxv-b{text-align:center;margin-top:8px}
.fxv-c{font-size:11px;color:var(--tx3)}
.fxv-c b{font-size:12px;color:var(--tx);font-weight:650}
/* previsto contra realizado ao longo do dia */
.acp svg{width:100%;height:auto;overflow:visible;display:block}
.ac-g{stroke:var(--ln);stroke-width:1}
.ac-gy{fill:var(--tx3);font-size:9.5px;font-family:'Outfit',sans-serif}
.ac-bd{fill:var(--ac);opacity:0;animation:fd .9s ease .5s forwards;--o:.1}
.ac-es{fill:none;stroke:var(--ac);stroke-width:2;stroke-dasharray:6 5;opacity:0;
 animation:fd .8s ease .7s forwards;--o:.65}
.ac-re{fill:none;stroke:var(--ink);stroke-width:3;stroke-linecap:round;stroke-dasharray:900;
 stroke-dashoffset:900;animation:dw 1.4s var(--e) .4s forwards}
.ac-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 4}
.ac-pe{fill:var(--c);stroke:var(--ac);stroke-width:2;opacity:0;
 animation:fd .4s ease 1.5s forwards;--o:1}
.ac-pr{fill:var(--ink);opacity:0;animation:pn .5s var(--e2) 1.6s forwards}
.ac-x{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.acp-l{display:flex;gap:16px;margin-top:10px;flex-wrap:wrap}
.acp-l span{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--tx2)}
.acp-l i{width:14px;height:3px;border-radius:2px;flex-shrink:0}
.acp-l .l-re{background:var(--ink)}
.acp-l .l-es{background:var(--ac);opacity:.65}
.acp-l .l-bd{background:var(--ac);opacity:.2;height:10px;border-radius:3px}
/* carga e erro do modal */
.md-carga{padding:44px 20px;text-align:center;font-size:13px;color:var(--tx2)}
.md-carga.erro{color:var(--no)}
/* paginacao */
.pag{display:flex;align-items:center;gap:10px;margin-top:16px;padding-top:14px;
 border-top:1px solid var(--ln);font-size:12px;color:var(--tx2)}
.pag a{display:inline-flex;align-items:center;gap:6px;text-decoration:none;color:var(--ac);
 font-weight:600;padding:7px 13px;border:1px solid var(--ln);border-radius:10px;
 background:var(--c);transition:all .3s var(--e)}
.pag a:hover{border-color:var(--ln2);box-shadow:var(--s1)}
.pag .cnt{margin-left:auto}
/* busca dentro da tabela */
.bsc{display:flex;align-items:center;gap:9px;background:var(--pg);border:1px solid var(--ln);
 border-radius:11px;padding:8px 12px;flex-shrink:0}
.bsc input{border:0;outline:0;background:0;font:inherit;font-size:12.5px;width:170px;
 color:var(--hd)}
.bsc .ic{color:var(--tx3)}
@media (max-width:1100px){.hc{width:100%;max-width:380px}.fxs,.ach{grid-template-columns:1fr 1fr}}
@media (max-width:680px){.fxs,.ach{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){
 .h24,.sm i,.rc2{opacity:1!important;transform:none!important}
 .hl-l{stroke-dashoffset:0!important}
 .hl-f,.hl-bd,.hl-n,.hl-o1,.h24-ag,.h24-n,.h24-al{opacity:1!important}
 .hl-bd{opacity:.11!important}.hl-o2,.hl-o3{opacity:0!important}
 .rb i{width:var(--w)!important}.tl{opacity:1!important;transform:none!important}}
"""

nav = ''.join(
    f'<button class="{"on" if k == "hoje" else ""}" data-ir="{k}">{ico(i, 15)}{nome}</button>'
    for k, nome, i, _ in ABAS)
telas = ''.join(f'<section class="tl" id="s-{k}"{"" if k == "hoje" else " hidden"}>{fn()}</section>'
                for k, _, _, fn in ABAS)

brief = f'''<div class="br-ov" id="brov"><div class="brf" role="dialog" aria-label="Resumo do dia">
  <button class="md-x" id="brx" aria-label="fechar">{ico('fechar', 16)}</button>
  <div class="brf-t"><span class="brf-s">{DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year} · 07h00</span>
    <span class="ct">redação automática</span></div>
  <h2>Situação da operação<br><span class="mu">em três pontos</span></h2>
  <div class="brf-b">
    <p><em>Ontem</em> entraram <b>{ONTEM_TOTAL}</b> incidentes elegíveis e
      <b>{ONTEM_VIOL}</b> violaram o prazo. São <b>{mil(EM_ABERTO)}</b> em atendimento agora.</p>
    <p><em>Hoje</em> a previsão é de <b>{pt(HOJE3['valor'], 0)}</b> no P3 e
      <b>{pt(HOJE2['valor'], 0)}</b> no P2. {'Nenhum dos casos abertos hoje passa de 10% de risco: o maior está em <b>' + pt(HOJE_MAX) + '%</b>.' if CALMO else '<b>' + str(HOJE_ACIMA10) + ' casos</b> passam de 10% de risco.'}</p>
    <p><em>Atenção</em> ao P3: a projeção de fechamento está em
      <b>{pt(proj.loc['P3', 'projeção'])}</b> contra meta de
      <b>{int(proj.loc['P3', 'meta máxima'])}</b>. A faixa vai de
      <b>{pt(proj.loc['P3', 'faixa baixa'], 0)}</b> a <b>{pt(proj.loc['P3', 'faixa alta'], 0)}</b>,
      então fechar dentro ainda cabe.</p>
  </div>
  <div class="brf-a">
    <button class="ax" data-ir="fila"><span class="ax-d">fila de risco</span>
      Cinco dos seis casos mais arriscados estão no ativo {TOPO['ativo']}{ico('seta', 15)}</button>
    <button class="ax" data-ir="saude"><span class="ax-d">saúde</span>
      Produto {PIOR} na última posição do ranking{ico('seta', 15)}</button>
  </div>
  <div class="brf-f"><span class="ct">Sem interação por conversa. O texto é escrito sobre a
    saída dos modelos.</span>
    <button class="bt pr" id="brf-ok">Abrir o painel{ico('seta', 15)}</button></div>
</div></div>'''

HTML = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · inteligência preditiva de incidentes</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS_BASE}{CSS_ICO_CLARO}{CSS_CAMPO}{CSS_APP}</style></head><body>
{campo('#2563EB', .13)}
<div class="sh">
  <div class="tp">
    <div class="br"><div class="br-m"><svg viewBox="0 0 28 28" width="18" height="18" fill="none">
      <path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.6" stroke-linecap="round"
        stroke-linejoin="round"/><circle cx="22" cy="8" r="3" stroke="#6EA0FF" stroke-width="1.9"/>
      <circle cx="22" cy="8" r="1.3" fill="#6EA0FF"/></svg></div>
      <div><b>Cronos</b><em>VEJA ANTES · AJA ANTES</em></div></div>
    <div class="pil">{nav}</div>
    <div class="tp-r">
      <button class="stl" id="abrepl" title="buscar (Ctrl+K)">{ico('lupa', 14)}buscar
        <span class="pl-k">Ctrl K</span></button>
      <span class="stl"><i></i>carga de {dm(ONTEM['dia'])} · 23h59</span>
      <button class="bl" id="sino" title="reabrir o resumo do dia">{ico('sino', 17)}<b>1</b></button>
    </div>
  </div>
  {telas}
</div>

{brief}

<div class="ov" id="ov" hidden><div class="md" role="dialog" aria-modal="true">
  <button class="md-x" id="mx" aria-label="fechar">{ico('fechar', 16)}</button>
  <div id="mc"></div></div></div>

<div class="pl" id="pl" hidden><div class="pl-c">
  <div class="pl-i">{ico('lupa', 18)}
    <input id="plq" placeholder="Buscar incidente, ativo, produto ou aba…" autocomplete="off">
    <span class="pl-k">Esc</span></div>
  <div class="pl-r" id="plr"></div></div></div>

<script>
const INC={json.dumps(MOD_INC, ensure_ascii=False)},
      ATIVO={json.dumps(MOD_ATIVO, ensure_ascii=False)},
      PROD={json.dumps(MOD_PROD, ensure_ascii=False)},
      PAL={json.dumps(PALETA, ensure_ascii=False)},
      MES={json.dumps(MES_LBL, ensure_ascii=False)},
      MEDIA={MEDIA_BASE};
const q=s=>document.getElementById(s), nb=v=>String(v).replace('.',',');
const IC={{bal:'{ico("balanca",18)}',alvo:'{ico("alvo",18)}',fila:'{ico("fila",15)}',
  sino:'{ico("sino",15)}',pes:'{ico("pessoas",15)}',res:'{ico("resolvido",15)}',
  lupa:'{ico("lupa",15)}',prev:'{ico("previsao",15)}',ativo:'{ico("ativo",18)}'}};
['.ch','.mr','.dc','.it','.h24','.sm','.rc2','.rb i','.tb tbody tr'].forEach(s=>
  document.querySelectorAll(s).forEach((e,i)=>e.style.setProperty('--i',Math.min(i,30))));

/* ── navegação entre abas ─────────────────────────────────────────────── */
function vai(k){{
  document.querySelectorAll('.pil button').forEach(b=>
    b.classList.toggle('on',b.dataset.ir===k));
  document.querySelectorAll('.tl').forEach(s=>s.hidden=s.id!=='s-'+k);
  const t=document.querySelector('.pil button.on');
  document.title='Cronos · '+(t?t.textContent.trim():'');
  scrollTo({{top:0,behavior:'smooth'}});
}}
document.addEventListener('click',e=>{{
  const b=e.target.closest('[data-ir]');
  if(b){{fechaTudo();vai(b.dataset.ir);}}
}});

/* ── morning brief como porta de entrada ──────────────────────────────── */
const brov=q('brov');
const fechaBrief=()=>brov.hidden=true;
q('brx').onclick=fechaBrief;q('brf-ok').onclick=fechaBrief;
brov.onclick=e=>{{if(e.target===brov)fechaBrief()}};
q('sino').onclick=()=>brov.hidden=false;

/* ── modal de aprofundamento ──────────────────────────────────────────── */
const ov=q('ov'),mc=q('mc');
const fechaModal=()=>ov.hidden=true;
q('mx').onclick=fechaModal;
ov.onclick=e=>{{if(e.target===ov)fechaModal()}};
function barras(h){{
  if(!h||!h.length)return '<p class="sub">Sem passagens registradas no período.</p>';
  const mx=Math.max(...h.map(m=>m.passagens))||1,W=560,H=92,lar=W/h.length;
  return `<svg class="mh" viewBox="0 0 ${{W}} ${{H}}">`+h.map((m,i)=>
    `<g><rect x="${{(i*lar+3).toFixed(1)}}" y="${{(H-16-m.passagens/mx*(H-20)).toFixed(1)}}"
      width="${{(lar-6).toFixed(1)}}" height="${{(m.passagens/mx*(H-20)).toFixed(1)}}" rx="3" class="mh-p"/>
    <rect x="${{(i*lar+3).toFixed(1)}}" y="${{(H-16-m.violacoes/mx*(H-20)).toFixed(1)}}"
      width="${{(lar-6).toFixed(1)}}" height="${{(m.violacoes/mx*(H-20)).toFixed(1)}}" rx="3" class="mh-v"/></g>
    <text class="mh-l" x="${{(i*lar+lar/2).toFixed(1)}}" y="${{H-2}}" text-anchor="middle">${{MES[m.mes-1]}}</text>`
  ).join('')+'</svg>';
}}
function abre(tipo,k){{
  let h='';
  if(tipo==='inc'){{const c=INC[k];if(!c)return;
    const tom=c.risco>=10?'no':c.risco>=3?'wn':'ok';
    h=`<span class="md-k">incidente · posição ${{c.pos}} na fila</span>
      <h3 class="id">${{c.id}}</h3>
      <p class="sub">${{c.produto}} · ${{c.categoria}} · equipe ${{c.equipe}} · ativo
        <span class="id">${{c.ativo}}</span> · aberto em ${{c.dia}} às
        ${{String(c.hora).padStart(2,'0')}}h</p>
      <div class="md-g">
        <div class="md-s ${{tom}}"><em>risco</em><b>${{nb(c.risco)}}%</b></div>
        <div class="md-s"><em>vs média</em><b>${{Math.round(c.risco/MEDIA)}}x</b></div>
        <div class="md-s"><em>prioridade</em><b>${{c.pri}}</b></div></div>
      <div class="cx"><span class="chp t-ac">${{IC.alvo}}</span>
        <p>Em <b>100 casos parecidos com este</b>, o modelo espera que
        <b>${{c.em100}} estourem o prazo</b>. No incidente comum da base seriam
        ${{nb(MEDIA)}} em 100.</p></div>
      <div class="md-h">o que pesa neste caso</div>
      ${{c.sinais.map(s=>`<div class="sg"><span class="sg-t">${{s.sinal}}</span>
        <span class="sg-b"><i style="width:${{Math.min(s.peso*2,100)}}%"></i></span>
        <span class="sg-v">${{nb(s.peso)}}%</span></div>`).join('')}}
      <p class="sub" style="margin-top:10px">Os sinais acima explicam
        <b>${{Math.round(c.cob)}}%</b> do empurrão para cima. O resto vem de dezenas de
        contribuições pequenas demais para listar.</p>
      <div class="md-h">histórico do ativo ${{c.ativo}}</div>
      ${{barras((ATIVO[c.ativo]||{{}}).hist)}}
      <p class="sub" style="margin-top:8px">${{c.av}} de ${{c.ap}} passagens por este ativo
        violaram o prazo. <b>Este histórico não entra no modelo</b> — é contexto para quem
        decide.</p>
      <div class="md-f"><button class="bt pr">${{IC.pes}}Escalar para ${{c.equipe}}</button>
        <button class="bt sc">${{IC.sino}}Avisar se passar de 60%</button>
        <button class="bt sc">${{IC.res}}Marcar como tratado</button></div>`;}}
  if(tipo==='ativo'){{const a=ATIVO[k];if(!a)return;
    const tom=a.taxa>=10?'no':a.taxa>=1?'wn':'ok';
    h=`<span class="md-k">ativo de configuração</span><h3 class="id">${{a.nome}}</h3>
      <p class="sub">${{a.pass}} incidentes elegíveis passaram por este ativo em 2025 até o
        corte.</p>
      <div class="md-g"><div class="md-s"><em>passagens</em><b>${{a.pass}}</b></div>
        <div class="md-s ${{tom}}"><em>violaram</em><b>${{a.viol}}</b></div>
        <div class="md-s ${{tom}}"><em>taxa</em><b>${{nb(a.taxa)}}%</b></div></div>
      <div class="md-h">histórico mês a mês</div>${{barras(a.hist)}}
      <p class="sub" style="margin-top:10px">A barra clara é o volume do mês. A parte vermelha
        embaixo é a fração que violou o prazo.</p>
      <div class="cx"><span class="chp t-ac">${{IC.bal}}</span>
        <p>Este ativo viola <b>${{a.x}} vezes mais</b> que a média da base, que é
        ${{nb(MEDIA)}}%. <b>O modelo não usa essa taxa</b>: ele usa a identidade do ativo, e só
        quando ela aparece o bastante para virar coluna própria.</p></div>
      <div class="md-f"><button class="bt pr">${{IC.fila}}Ver incidentes deste ativo</button>
        <button class="bt sc">${{IC.sino}}Avisar quando abrir outro</button></div>`;}}
  if(tipo==='prod'){{const p=PROD[k];if(!p)return;
    h=`<span class="md-k">produto · posição ${{p.pos}} de 17</span><h3 class="id">${{p.nome}}</h3>
      <p class="sub">${{p.quad}} · ${{p.inc}} incidentes elegíveis, ${{p.viol}} violaram o prazo.</p>
      <div class="md-g">
        <div class="md-s ${{parseFloat(p.nota)<40?'no':'wn'}}"><em>nota</em><b>${{p.nota}}</b></div>
        <div class="md-s"><em>posição</em><b>${{p.pos}}º</b></div>
        <div class="md-s"><em>incidentes</em><b>${{p.inc}}</b></div></div>
      <div class="md-h">os cinco componentes da nota</div>
      ${{p.comp.map(c=>`<div class="sg"><span class="sg-t">${{c.rot}}
        <span style="color:#A3ABBA"> ${{c.v}}${{c.u}}</span></span>
        <span class="sg-b"><i style="width:${{c.pos}}%;background:${{c.pos>66?'#DC2626':c.pos>33?'#B45309':'#059669'}}"></i></span>
        <span class="sg-v">${{c.pos}}</span></div>`).join('')}}
      <p class="sub" style="margin-top:8px">A barra mostra a posição relativa entre os dezessete
        produtos: quanto mais cheia, pior comparado aos outros. A nota é a média dessas posições.</p>
      <div class="md-f"><button class="bt pr">${{IC.lupa}}Ver causas deste produto</button>
        <button class="bt sc">${{IC.prev}}Comparar com outro</button></div>`;}}
  mc.innerHTML=h;ov.hidden=false;ov.querySelector('.md').scrollTop=0;
}}
document.addEventListener('click',e=>{{
  const b=e.target.closest('[data-mod]');
  if(b)abre(b.dataset.mod,b.dataset.k);
}});

/* ── filtros ──────────────────────────────────────────────────────────── */
document.querySelectorAll('.fb').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll(`.fb[data-g="${{b.dataset.g}}"]`).forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  if(b.dataset.g==='pri'){{
    let n=0;
    document.querySelectorAll('#tb-fila tr').forEach(t=>{{
      const ok=b.dataset.v==='t'||t.dataset.p===b.dataset.v;
      t.hidden=!ok;if(ok)n++;}});
    q('tb-vazio').hidden=n>0;
  }}
  if(b.dataset.g==='quad'){{
    let n=0;
    document.querySelectorAll('#tb-saude tr').forEach(t=>{{
      const ok=b.dataset.v==='t'||t.dataset.q===b.dataset.v;
      t.hidden=!ok;if(ok)n++;}});
    q('tb-vazio-s').hidden=n>0;
  }}
}});
document.querySelectorAll('.fx').forEach(b=>b.onclick=()=>{{
  const lig=!b.classList.contains('on');
  document.querySelectorAll('.fx').forEach(x=>x.classList.remove('on'));
  if(lig)b.classList.add('on');
  const lo=parseFloat(b.dataset.v);
  let n=0;
  document.querySelectorAll('#tb-fila tr').forEach(t=>{{
    const r=parseFloat(t.dataset.r);
    const faixa=lo>=10?r>=10:lo>=5?(r>=5&&r<10):lo>=1?(r>=1&&r<5):r<1;
    const ok=!lig||faixa;t.hidden=!ok;if(ok)n++;}});
  q('tb-vazio').hidden=n>0;
}});

/* ── paleta de comando ────────────────────────────────────────────────── */
const pl=q('pl'),plq=q('plq'),plr=q('plr');
let sel=0,vis=[];
const ROT={{aba:'aba',inc:'caso',ativo:'ativo',prod:'produto'}};
function pinta(){{
  const t=plq.value.trim().toLowerCase();
  vis=(t?PAL.filter(o=>(o.r+' '+o.s).toLowerCase().includes(t)):PAL.slice(0,9)).slice(0,40);
  sel=0;
  plr.innerHTML=vis.length?vis.map((o,i)=>
    `<button class="pl-o${{i===0?' on':''}}" data-i="${{i}}"><span class="tp2">${{ROT[o.t]}}</span>
      <span><b class="id">${{o.r}}</b><span>${{o.s}}</span></span></button>`).join('')
    :'<div class="pl-vz">Nada encontrado. Tente o número do incidente, o código do ativo ou o nome do produto.</div>';
}}
function escolhe(o){{
  pl.hidden=true;
  if(o.t==='aba')vai(o.k);else abre(o.t,o.k);
}}
q('abrepl').onclick=()=>{{pl.hidden=false;plq.value='';pinta();plq.focus();}};
plq.oninput=pinta;
plr.onclick=e=>{{const b=e.target.closest('.pl-o');if(b)escolhe(vis[+b.dataset.i]);}};
addEventListener('keydown',e=>{{
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){{
    e.preventDefault();pl.hidden=false;plq.value='';pinta();plq.focus();return;}}
  if(e.key==='Escape'){{fechaTudo();return;}}
  if(pl.hidden)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){{
    e.preventDefault();
    sel=(sel+(e.key==='ArrowDown'?1:-1)+vis.length)%vis.length;
    plr.querySelectorAll('.pl-o').forEach((x,i)=>x.classList.toggle('on',i===sel));
    plr.querySelectorAll('.pl-o')[sel]?.scrollIntoView({{block:'nearest'}});}}
  if(e.key==='Enter'&&vis[sel])escolhe(vis[sel]);
}});
function fechaTudo(){{pl.hidden=true;ov.hidden=true;brov.hidden=true;}}

/* ── luz que acompanha o cursor ───────────────────────────────────────── */
addEventListener('pointermove',e=>{{const c=e.target.closest?.('.cd');if(!c)return;
  const b=c.getBoundingClientRect();
  c.style.setProperty('--mx',(e.clientX-b.left)+'px');
  c.style.setProperty('--my',(e.clientY-b.top)+'px');}},{{passive:true}});
</script></body></html>'''

OUT.write_text(HTML, encoding='utf-8')
kb = len(HTML) / 1024
print(f'app: {OUT}  ({kb:.0f} kB)')
print(f'  {len(ABAS)} abas | {len(MOD_INC)} incidentes, {len(MOD_ATIVO)} ativos e '
      f'{len(MOD_PROD)} produtos no modal | {len(PALETA)} itens na paleta')
