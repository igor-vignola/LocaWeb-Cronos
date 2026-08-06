# -*- coding: utf-8 -*-
"""Folha de estilo da aplicacao Cronos, direcao B.

Clara e editorial, com o campo de linhas ao fundo. Extraida de dir_b.py para as cinco
abas compartilharem a mesma regua: cabecalho que diz o que o card e, filtro em pilula,
modal de aprofundamento, linha de metrica com icone tingido."""

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--pg:#F6F7F9;--c:#FFF;--ink:#0C1017;--ln:rgba(12,16,23,.08);--ln2:rgba(12,16,23,.16);
 --tx:#4E586B;--tx2:#7B8598;--tx3:#A3ABBA;--hd:#0C1017;
 --ac:#2563EB;--acl:#EFF4FF;--no:#DC2626;--nol:#FEF2F2;--wn:#B45309;--wnl:#FFFAEC;
 --ok:#059669;--okl:#ECFDF5;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 10px 26px -14px rgba(12,16,23,.14);
 --s2:0 2px 6px rgba(12,16,23,.06),0 28px 54px -20px rgba(12,16,23,.22)}
html{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}
body{background:var(--pg);color:var(--hd);min-height:100dvh;overflow-x:hidden;
 font-family:'Outfit',system-ui,sans-serif;font-size:15px;letter-spacing:-.011em}
.id{font-weight:600;letter-spacing:.05em;font-variant-numeric:tabular-nums lining-nums}
.nb{font-variant-numeric:tabular-nums lining-nums}
.sh{position:relative;z-index:1;max-width:1420px;margin:0 auto;padding:0 32px 80px}
/* topo */
.tp{display:flex;align-items:center;gap:14px;padding:16px 0;margin-bottom:6px;
 position:sticky;top:0;z-index:30;
 background:linear-gradient(180deg,rgba(246,247,249,.97) 58%,transparent);backdrop-filter:blur(8px)}
.br{display:flex;align-items:center;gap:11px}
.br-m{width:34px;height:34px;border-radius:11px;background:var(--ink);display:grid;
 place-items:center;box-shadow:var(--s1)}
.br b{font-size:17px;font-weight:700;letter-spacing:-.04em;display:block;line-height:1}
.br em{font-size:8.5px;letter-spacing:.16em;color:var(--tx3);font-style:normal;font-weight:600}
.pil{display:flex;gap:2px;background:var(--c);border:1px solid var(--ln);border-radius:13px;
 padding:4px;box-shadow:var(--s1)}
.pil button{display:inline-flex;align-items:center;gap:7px;background:0;border:0;font:inherit;
 font-size:13px;font-weight:500;color:var(--tx2);padding:8px 14px;border-radius:9px;
 cursor:pointer;transition:all .34s var(--e);white-space:nowrap}
.pil button:hover:not(:disabled){color:var(--hd)}
.pil button.on{background:var(--ink);color:#fff}
.pil button:disabled{opacity:.35;cursor:default}
.tp-r{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.stl{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;color:var(--tx);
 background:var(--c);border:1px solid var(--ln);padding:7px 12px;border-radius:999px;
 box-shadow:var(--s1)}
.stl .ic{color:var(--tx3)}
.stl i{width:6px;height:6px;border-radius:50%;background:var(--ok);
 box-shadow:0 0 0 3px rgba(5,150,105,.16);animation:pu 2.6s ease-in-out infinite}
@keyframes pu{50%{opacity:.35}}
/* abas de dia, do app de clima */
.dias{display:flex;gap:6px;margin:18px 0 22px}
.da{background:var(--c);border:1px solid var(--ln);border-radius:15px;padding:11px 17px;
 cursor:pointer;font:inherit;text-align:left;transition:all .36s var(--e);box-shadow:var(--s1)}
.da em{display:block;font-size:9.5px;font-style:normal;letter-spacing:.12em;text-transform:uppercase;
 color:var(--tx3);font-weight:700}
.da b{display:block;font-size:17px;font-weight:650;letter-spacing:-.03em;margin-top:3px}
.da span{font-size:10.5px;color:var(--tx2)}
.da:hover{transform:translateY(-2px);box-shadow:var(--s2)}
.da.on{background:var(--ink);border-color:var(--ink)}
.da.on em{color:rgba(255,255,255,.5)}.da.on b{color:#fff}.da.on span{color:rgba(255,255,255,.62)}
/* hero editorial */
.hr{display:grid;grid-template-columns:1fr auto;gap:44px;align-items:center;margin-bottom:34px}
.hr .kk{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ac);display:inline-flex;align-items:center;gap:8px}
.hr h1{font-size:47px;font-weight:600;line-height:1.09;letter-spacing:-.042em;margin-top:14px;
 max-width:20ch}
.hr h1 .mu{color:var(--tx3)}
.hr .lead{font-size:17px;color:var(--tx);line-height:1.62;margin-top:18px;max-width:60ch}
.hr .lead b{color:var(--hd);font-weight:650}
.hr .lead .cr{color:var(--no);font-weight:650}
/* chips de metrica */
.chips{display:flex;gap:9px;margin-top:22px;flex-wrap:wrap}
.ch{display:inline-flex;align-items:center;gap:10px;background:var(--c);border:1px solid var(--ln);
 border-radius:14px;padding:9px 14px 9px 10px;box-shadow:var(--s1);
 animation:sl .55s var(--e) both;animation-delay:calc(var(--i,0)*70ms)}
@keyframes sl{from{opacity:0;transform:translateY(9px)}}
.ch .chp{width:30px;height:30px;border-radius:9px}
.ch div em{display:block;font-size:9.5px;font-style:normal;letter-spacing:.09em;
 text-transform:uppercase;color:var(--tx3);font-weight:700}
.ch div b{display:block;font-size:15px;font-weight:650;letter-spacing:-.03em;margin-top:1px;
 font-variant-numeric:tabular-nums}
.ch div b u{font-size:10.5px;font-weight:500;color:var(--tx2);text-decoration:none;margin-left:2px}
/* relogio */
.rl{position:relative;width:340px;flex-shrink:0}
.rl svg{width:100%;height:auto;overflow:visible}
.rl-g{fill:none;stroke:var(--ln);stroke-width:1}
.rl-b{cursor:pointer;transform-origin:center;animation:rb .6s var(--e) both;
 animation-delay:calc(var(--i)*26ms);transition:filter .25s var(--e)}
@keyframes rb{from{opacity:0;transform:scale(.86)}to{opacity:1;transform:scale(1)}}
.rl-b.t-ok{fill:#BFD3FA}.rl-b.t-wn{fill:#F3C98A}.rl-b.t-no{fill:#EF8078}
.rl-b:hover{filter:brightness(.9)}
.rl-m{fill:none;stroke:var(--no);stroke-width:2.6;stroke-linecap:round;opacity:0;
 animation:fd .7s ease 1.1s forwards;--o:.85}
.rl-h{fill:var(--tx3);font-size:11px;font-weight:600;text-anchor:middle;
 font-family:'Outfit',sans-serif}
.rl-p{stroke:var(--ink);stroke-width:2;stroke-linecap:round;transform-origin:center;
 animation:gi 1.2s var(--e) .5s both}
@keyframes gi{from{transform:rotate(-120deg)}to{transform:rotate(0)}}
.rl-c{fill:var(--ink)}
.rl-ag{fill:var(--ink);font-size:10px;font-weight:700;text-anchor:middle;
 letter-spacing:.08em;text-transform:uppercase;font-family:'Outfit',sans-serif}
.rl-in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
 justify-content:center;pointer-events:none;text-align:center}
.rl-in b{font-size:46px;font-weight:650;letter-spacing:-.05em;line-height:1}
.rl-in span{font-size:11px;color:var(--tx2);margin-top:3px}
.rl-in em{font-size:10px;color:var(--tx3);font-style:normal;margin-top:2px}
/* atos */
.ato{display:flex;align-items:flex-start;gap:15px;margin:42px 0 16px}
.ato-n{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--ac);background:var(--acl);
 border:1px solid rgba(37,99,235,.18);border-radius:9px;padding:5px 10px;flex-shrink:0;margin-top:3px}
.ato h2{font-size:22px;font-weight:650;letter-spacing:-.033em}
.ato p{font-size:13.5px;color:var(--tx2);margin-top:2px}
/* cards */
.gr{display:grid;gap:16px;align-items:stretch}
.g2{grid-template-columns:1.5fr 1fr}
.g3{grid-template-columns:1fr 1fr 1fr}
.cd{display:flex;flex-direction:column;background:var(--c);border:1px solid var(--ln);
 border-radius:22px;padding:20px 22px;box-shadow:var(--s1);position:relative;overflow:hidden;
 transition:box-shadow .5s var(--e),transform .5s var(--e)}
.cd:hover{box-shadow:var(--s2);transform:translateY(-2px)}
.cd>.nt{margin-top:auto}
/* o card escuro no meio dos claros, de plataforma-card-escuro-meta */
.cd.dk{background:var(--ink);border-color:var(--ink);color:#E8ECF3}
.cd.dk .hdr h3{color:#fff}.cd.dk .hdr p{color:#8D97A8}.cd.dk .hdr .ic{color:#6EA0FF}
.cd.dk .nt{color:#8D97A8;border-color:rgba(255,255,255,.1)}.cd.dk .nt b{color:#fff}
.hdr{display:flex;align-items:flex-start;gap:13px;margin-bottom:15px}
.hdr-t{display:flex;gap:10px;flex:1;min-width:0}
.hdr-t .ic{color:var(--ac);margin-top:2px;flex-shrink:0}
.hdr h3{font-size:14.5px;font-weight:650;letter-spacing:-.022em}
.hdr p{font-size:11.5px;color:var(--tx2);margin-top:2px;line-height:1.45}
.fg{display:flex;gap:2px;background:var(--pg);border:1px solid var(--ln);border-radius:10px;
 padding:3px;flex-shrink:0}
.fb{background:0;border:0;font:inherit;font-size:11px;font-weight:600;color:var(--tx2);
 padding:5px 10px;border-radius:7px;cursor:pointer;transition:all .3s var(--e);white-space:nowrap}
.fb:hover{color:var(--hd)}.fb.on{background:var(--c);color:var(--hd);box-shadow:var(--s1)}
.vr{font-size:10.5px;font-weight:700;padding:3px 7px;border-radius:6px;margin-left:6px}
.vr.ok{background:var(--okl);color:var(--ok)}.vr.no{background:var(--nol);color:var(--no)}
/* trilho */
.tr{position:relative;margin-top:8px}
.tr svg{width:100%;height:150px;display:block;overflow:visible}
.t-l{fill:none;stroke:var(--ac);stroke-width:2.4;stroke-linecap:round;stroke-dasharray:1600;
 stroke-dashoffset:1600;animation:dw 1.8s var(--e) .3s forwards}
.t-f{fill:none;stroke:var(--ac);stroke-width:2;stroke-dasharray:5 5;opacity:0;
 animation:fd .8s ease 1.6s forwards;--o:.8}
.t-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.7s forwards;--o:.12}
.t-a{opacity:0;animation:fd 1s ease 1.2s forwards;--o:1}
.t-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 4;opacity:0;
 animation:fd .5s ease 1.5s forwards;--o:1}
.t-n{fill:var(--ac);opacity:0;animation:pn .5s var(--e2) 1.4s forwards}
.t-h{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center;
 animation:hl 3s ease-out 2.1s infinite}
@keyframes hl{0%{opacity:.28;transform:scale(.3)}70%,100%{opacity:0;transform:scale(1.7)}}
@keyframes dw{to{stroke-dashoffset:0}}
@keyframes fd{to{opacity:var(--o,1)}}
@keyframes pn{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.anp{position:absolute;transform:translateX(-50%);background:var(--acl);
 border:1px solid rgba(37,99,235,.22);color:var(--ac);padding:4px 9px;border-radius:8px;
 font-size:11px;font-weight:650;white-space:nowrap;opacity:0;
 animation:fd .6s ease 2s forwards}
.tr-x{display:flex;justify-content:space-between;font-size:9.5px;color:var(--tx3);
 letter-spacing:.09em;text-transform:uppercase;position:relative;margin-top:2px}
.tr-x .ag{position:absolute;transform:translateX(-50%);color:var(--ac);font-weight:700}
/* linha de metrica */
.ml{display:flex;flex-direction:column;gap:8px}
.mr{display:flex;align-items:center;gap:12px;background:var(--pg);border:1px solid var(--ln);
 border-radius:14px;padding:11px 13px;animation:sl .5s var(--e) both;
 animation-delay:calc(120ms + var(--i,0)*60ms)}
.mr-t{flex:1;min-width:0}
.mr-t b{font-size:13px;font-weight:500;display:block}
.mr-t span{font-size:11px;color:var(--tx2);display:block;margin-top:1px}
.mr-v{font-size:20px;font-weight:650;letter-spacing:-.035em;flex-shrink:0;
 font-variant-numeric:tabular-nums;display:inline-flex;align-items:baseline}
.mr-v u{font-size:11.5px;font-weight:500;color:var(--tx2);text-decoration:none;margin-left:3px}
.mr-v.no{color:var(--no)}.mr-v.ok{color:var(--ok)}
/* circulos por dia */
.dcs{display:flex;gap:6px}
.dc{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px}
.dc i{width:100%;aspect-ratio:1;max-width:38px;border-radius:50%;border:1.5px solid var(--ln2);
 display:grid;place-items:center;font-style:normal;font-size:12px;font-weight:650;
 color:var(--tx3);animation:pn .4s var(--e2) both;animation-delay:calc(var(--i,0)*45ms)}
.dc.vi i{background:var(--nol);border-color:rgba(220,38,38,.42);color:var(--no)}
.dc span{font-size:9.5px;color:var(--tx2)}
.dc em{font-size:9.5px;font-style:normal;color:var(--tx3);font-variant-numeric:tabular-nums}
/* fila */
.fl{display:flex;flex-direction:column;gap:8px}
.it{display:flex;align-items:center;gap:12px;background:var(--pg);border:1px solid var(--ln);
 border-radius:15px;padding:11px 13px;cursor:pointer;transition:all .34s var(--e);width:100%;
 font:inherit;color:inherit;text-align:left;animation:sl .5s var(--e) both;
 animation-delay:calc(140ms + var(--i)*58ms)}
.it:hover{background:var(--c);border-color:var(--ln2);box-shadow:var(--s1);transform:translateX(4px)}
.it-r{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;flex-shrink:0;
 font-size:13.5px;font-weight:700;letter-spacing:-.03em}
.it-r.crit{background:var(--nol);color:var(--no)}.it-r.alta{background:var(--wnl);color:var(--wn)}
.it-t{flex:1;min-width:0}
.it-t b{font-size:13.5px;display:block}
.it-t span{font-size:11.5px;color:var(--tx2);margin-top:2px;display:flex;gap:4px;flex-wrap:wrap;
 align-items:center}
.it-t span .ic{width:12px;height:12px;opacity:.5}
.it-t span u{text-decoration:none;margin-right:7px;display:inline-flex;align-items:center;gap:4px}
.it-b{flex-shrink:0;text-align:right}
.it-b em{font-size:9.5px;font-style:normal;color:var(--tx3);letter-spacing:.07em;
 text-transform:uppercase;display:block}
.it-b b{font-size:12.5px;color:var(--tx);font-weight:600}
.it .sq{color:var(--tx3);transition:transform .3s var(--e),color .3s var(--e)}
.it:hover .sq{color:var(--ac);transform:translateX(3px)}
/* meta no card escuro */
.mt{margin-top:16px}
.mt-h{display:flex;align-items:baseline;gap:9px}
.mt-p{font-size:10.5px;font-weight:700;letter-spacing:.1em;color:#8D97A8}
.mt-v{font-size:29px;font-weight:650;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.mt-v.ok{color:#37D39B}.mt-v.no{color:#FF7D74}
.mt-l{font-size:12px;color:#8D97A8}
.tg{font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;
 border-radius:6px;margin-left:auto}
.tg.ok{background:rgba(55,211,155,.16);color:#37D39B}
.tg.no{background:rgba(255,125,116,.16);color:#FF7D74}
.mt-b{height:13px;border-radius:7px;background:rgba(255,255,255,.09);position:relative;
 margin-top:11px}
.mt-b s{position:absolute;top:0;bottom:0;border-radius:7px;text-decoration:none;
 transform:scaleX(0);transform-origin:left;animation:ab 1s var(--e) .6s forwards}
.mt-b s.ok{background:linear-gradient(90deg,rgba(55,211,155,.4),rgba(55,211,155,.75))}
.mt-b s.no{background:linear-gradient(90deg,rgba(255,125,116,.4),rgba(255,125,116,.75))}
.mt-b i{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:2px;opacity:0;
 animation:fd .5s ease 1.4s forwards}
.mt-b i.ok{background:#37D39B}.mt-b i.no{background:#FF7D74}
.mt-b u{position:absolute;top:-5px;bottom:-5px;width:2px;background:#fff;opacity:0;
 animation:fd .5s ease 1.2s forwards;--o:.85}
@keyframes ab{to{transform:scaleX(1)}}
.mt-f{font-size:10.5px;color:#8D97A8;margin-top:7px}
/* ranking */
.rw{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--ln);
 cursor:pointer;background:0;border-left:0;border-right:0;border-top:0;width:100%;font:inherit;
 color:inherit;text-align:left;transition:padding .3s var(--e)}
.rw:hover{padding-left:5px}.rw:last-of-type{border-bottom:0}
.rw-p{width:46px;font-weight:650;font-size:12.5px}
.rw-b{flex:1;height:6px;border-radius:3px;background:#EDEFF3;overflow:hidden}
.rw-b i{display:block;height:100%;border-radius:3px;width:0;background:var(--c2);
 animation:gw 1s var(--e) both;animation-delay:calc(400ms + var(--i)*70ms)}
@keyframes gw{to{width:var(--w)}}
.rw-v{width:36px;text-align:right;font-size:13px;font-weight:650;
 font-variant-numeric:tabular-nums}
.rw-q{width:88px;font-size:10px;color:var(--tx3);text-align:right}
.nt{font-size:11.5px;color:var(--tx2);line-height:1.62;margin-top:14px;padding-top:12px;
 border-top:1px solid var(--ln)}
.nt b{color:var(--hd);font-weight:650}
.anr .anr-t{fill:none;stroke:#EDEFF3;stroke-width:4}
.anr .anr-v{fill:none;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);
 transform-origin:center;animation:ar 1.1s var(--e) .5s forwards}
.anr.t-no .anr-v{stroke:var(--no)}.anr.t-wn .anr-v{stroke:var(--wn)}
.anr text{fill:var(--hd);font-size:15px;font-weight:650;font-family:'Outfit',sans-serif}
@keyframes ar{to{stroke-dashoffset:var(--f)}}
/* modal */
.ov{position:fixed;inset:0;z-index:90;display:grid;place-items:center;padding:28px;
 background:rgba(12,16,23,.42);backdrop-filter:blur(8px);animation:fd .3s ease both;--o:1}
.ov[hidden]{display:none}
.md{width:min(620px,100%);max-height:86dvh;overflow:auto;position:relative;background:var(--c);
 border-radius:26px;padding:26px 28px;box-shadow:0 40px 90px -26px rgba(12,16,23,.4);
 animation:mu .5s var(--e) both}
@keyframes mu{from{opacity:0;transform:translateY(18px) scale(.976)}}
.md-x{position:absolute;top:18px;right:18px;width:32px;height:32px;border-radius:10px;
 background:var(--pg);border:1px solid var(--ln);color:var(--tx);cursor:pointer;display:grid;
 place-items:center;transition:all .3s var(--e)}
.md-x:hover{background:#E9ECF1;color:var(--hd)}
.md-k{font-size:9.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ac)}
.md h3{font-size:26px;font-weight:650;letter-spacing:-.035em;margin-top:7px}
.md .sub{font-size:13px;color:var(--tx);margin-top:5px}
.md-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px}
.md-s{background:var(--pg);border:1px solid var(--ln);border-radius:14px;padding:13px 14px}
.md-s em{font-size:9.5px;font-style:normal;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx3);display:block;font-weight:700}
.md-s b{font-size:23px;font-weight:650;letter-spacing:-.04em;display:block;margin-top:5px;
 line-height:1}
.md-s.no b{color:var(--no)}.md-s.ok b{color:var(--ok)}.md-s.wn b{color:var(--wn)}
.md-h{font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--tx3);
 margin:22px 0 11px;display:flex;align-items:center;gap:8px}
.md-h::after{content:'';flex:1;height:1px;background:var(--ln)}
.hb{display:flex;align-items:flex-end;gap:5px;height:74px}
.hb-c{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px;height:100%;
 justify-content:flex-end}
.hb-c i{width:100%;border-radius:5px 5px 2px 2px;background:#E4E8EE;position:relative;
 height:var(--h)}
.hb-c i u{position:absolute;inset:auto 0 0 0;height:var(--v);border-radius:0 0 2px 2px;
 background:var(--no);text-decoration:none}
.hb-c span{font-size:9.5px;color:var(--tx3)}
.sg{display:flex;align-items:center;gap:11px;padding:8px 0}
.sg-t{flex:1;font-size:12.5px}
.sg-b{width:130px;height:6px;border-radius:3px;background:#EDEFF3;overflow:hidden}
.sg-b i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,#7DA8FF,#2563EB)}
.sg-v{width:34px;text-align:right;font-size:12.5px;font-weight:650;
 font-variant-numeric:tabular-nums}
.cx{background:var(--acl);border:1px solid rgba(37,99,235,.16);border-radius:15px;padding:14px 16px;
 margin-top:18px;display:flex;gap:12px}
.cx p{font-size:12.5px;color:var(--tx);line-height:1.6}.cx p b{color:var(--hd);font-weight:650}
.md-f{margin-top:20px;padding-top:15px;border-top:1px solid var(--ln);display:flex;gap:9px;
 flex-wrap:wrap}
.bt{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12.5px;font-weight:600;
 padding:10px 15px;border-radius:11px;cursor:pointer;transition:all .3s var(--e)}
.bt.pr{background:var(--ink);border:1px solid var(--ink);color:#fff}
.bt.pr:hover{transform:translateY(-1px);box-shadow:var(--s2)}
.bt.sc{background:var(--c);border:1px solid var(--ln);color:var(--tx)}
.bt.sc:hover{background:var(--pg);color:var(--hd)}
.bt:active{transform:scale(.98)}

/* B1 · a marca virada heroi */
.hl{position:relative;width:360px;flex-shrink:0}
.hl svg{width:100%;height:auto;overflow:visible}
.hl-l{fill:none;stroke:var(--ac);stroke-width:4.2;stroke-linecap:round;stroke-linejoin:round;
 stroke-dasharray:900;stroke-dashoffset:900;animation:dw 1.9s var(--e) .3s forwards}
.hl-f{fill:none;stroke:var(--ac);stroke-width:3;stroke-linecap:round;stroke-dasharray:7 7;
 opacity:0;animation:fd .9s ease 1.7s forwards;--o:.55}
.hl-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.8s forwards;--o:.11}
.hl-n{fill:var(--ac);opacity:0;animation:pn .5s var(--e2) 1.6s forwards}
.hl-o1{fill:none;stroke:var(--ac);stroke-width:2;opacity:0;
 animation:fd .5s ease 1.8s forwards;--o:.45}
.hl-o2,.hl-o3{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center}
.hl-o2{animation:on 3.2s ease-out 2s infinite}
.hl-o3{animation:on 3.2s ease-out 2.5s infinite}
@keyframes on{0%{opacity:.22;transform:scale(.45)}70%,100%{opacity:0;transform:scale(1.5)}}
.hl-x{fill:var(--tx3);font-size:10px;font-weight:600;letter-spacing:.08em;
 text-transform:uppercase;font-family:'Outfit',sans-serif}
.hl-x.ag{fill:var(--ac);font-weight:700}
.hl-v{text-align:center;margin-top:-4px}
.hl-v b{font-size:54px;font-weight:700;letter-spacing:-.05em;line-height:1;display:block}
.hl-v span{font-size:11.5px;color:var(--tx2);display:block;margin-top:6px}
/* B2 · o dia esticado */
.hf{width:360px;flex-shrink:0}
.hf svg{width:100%;height:auto;overflow:visible}
.hf-b{transform-origin:bottom;animation:hb .55s var(--e) both;
 animation-delay:calc(var(--i)*24ms);cursor:pointer;transition:filter .25s var(--e)}
@keyframes hb{from{opacity:0;transform:scaleY(.2)}}
.hf-b:hover{filter:brightness(.88)}
.hf-b.t-ok{fill:#B9CFFA}.hf-b.t-wn{fill:#F2C486}.hf-b.t-no{fill:#EE7C74}
.hf-ag{stroke:var(--ink);stroke-width:1.4;stroke-dasharray:3 3;opacity:0;
 animation:fd .5s ease .9s forwards;--o:.5}
.hf-n{fill:var(--ink);opacity:0;animation:pn .4s var(--e2) 1s forwards}
.hf-al{fill:var(--ink);font-size:9.5px;font-weight:700;letter-spacing:.09em;
 text-transform:uppercase;font-family:'Outfit',sans-serif;opacity:0;
 animation:fd .5s ease 1.1s forwards;--o:1}
.hf-x{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.hf-l{display:flex;gap:13px;justify-content:center;margin-top:4px;flex-wrap:wrap}
.hf-l span{display:inline-flex;align-items:center;gap:5px;font-size:10px;color:var(--tx2)}
.hf-l i{width:9px;height:9px;border-radius:3px}
.hf-l i.t-ok{background:#B9CFFA}.hf-l i.t-wn{background:#F2C486}.hf-l i.t-no{background:#EE7C74}
.hf-v{text-align:center;margin-top:14px}
.hf-v b{font-size:48px;font-weight:700;letter-spacing:-.05em;line-height:1;display:block}
.hf-v span{font-size:11.5px;color:var(--tx2);display:block;margin-top:5px}
/* B3 · o veredito */
.mdd{position:relative;width:340px;flex-shrink:0}
.mdd svg{width:100%;height:auto;overflow:visible}
.md-z{fill:none;stroke-width:16;stroke-linecap:butt;opacity:.22}
.md-z.z-ok{stroke:var(--ok)}.md-z.z-ac{stroke:var(--ac)}.md-z.z-no{stroke:var(--no)}
.md-fx{fill:none;stroke:var(--ac);stroke-width:16;stroke-linecap:round;opacity:0;
 animation:fd .9s ease .7s forwards;--o:.8}
.md-p{stroke:var(--ink);stroke-width:3.2;stroke-linecap:round;transform-origin:center;
 animation:gi 1.3s var(--e) .4s both}
@keyframes gi{from{transform:rotate(-42deg)}to{transform:rotate(0)}}
.md-c{fill:var(--ink);opacity:0;animation:pn .5s var(--e2) 1.3s forwards}
.md-md{stroke:var(--tx3);stroke-width:1.4;stroke-dasharray:2 2}
.md-ml{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.mdd-in{text-align:center;margin-top:-62px}
.mdd-in b{font-size:58px;font-weight:700;letter-spacing:-.055em;line-height:1;display:block}
.mdd-z{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;padding:4px 12px;border-radius:8px;margin-top:10px}
.mdd-z.z-ok{background:var(--okl);color:var(--ok)}
.mdd-z.z-ac{background:var(--acl);color:var(--ac)}
.mdd-z.z-no{background:var(--nol);color:var(--no)}
.mdd-in em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:9px;
 max-width:32ch;margin-inline:auto;line-height:1.55}
@media (max-width:1100px){.hl,.hf,.mdd{width:100%;max-width:360px}}
@media (prefers-reduced-motion:reduce){
 .hl-l{stroke-dashoffset:0!important}
 .hl-f,.hl-bd,.hl-n,.hl-o1,.hf-ag,.hf-n,.hf-al,.md-fx,.md-c{opacity:1!important}
 .hl-bd{opacity:.11!important}.hl-o2,.hl-o3{opacity:0!important}
 .hf-b{opacity:1!important;transform:none!important}.md-p{transform:none!important}}

/* B1 completa · tres escalas de tempo empilhadas */
.hc{width:380px;flex-shrink:0}
.hc svg{width:100%;height:auto;overflow:visible;display:block}
.hc-v{display:flex;align-items:center;gap:14px;justify-content:center;margin-top:2px}
.hc-v b{font-size:58px;font-weight:700;letter-spacing:-.055em;line-height:.9}
.hc-vt{text-align:left}
.hc-z{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;padding:4px 11px;border-radius:8px}
.hc-z.z-ok{background:var(--okl);color:var(--ok)}
.hc-z.z-ac{background:var(--acl);color:var(--ac)}
.hc-z.z-no{background:var(--nol);color:var(--no)}
.hc-vt em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:5px;
 line-height:1.45;max-width:22ch}
.hc-f{margin-top:14px;padding-top:13px;border-top:1px solid var(--ln);position:relative}
.hc-fl{position:absolute;top:-7px;left:50%;transform:translateX(-50%);background:var(--pg);
 padding:0 9px;font-size:9px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
 color:var(--tx3)}
.hc-b{transform-origin:bottom;animation:hb .5s var(--e) both;
 animation-delay:calc(1.9s + var(--i)*20ms);cursor:pointer;transition:filter .25s var(--e)}
@keyframes hb{from{opacity:0;transform:scaleY(.15)}}
.hc-b:hover{filter:brightness(.86)}
.hc-b.t-ok{fill:#BCD1FA}.hc-b.t-wn{fill:#F2C486}.hc-b.t-no{fill:#EE7C74}
.hc-ag{stroke:var(--ink);stroke-width:1.3;stroke-dasharray:2 3;opacity:0;
 animation:fd .5s ease 2.3s forwards;--o:.5}
.hc-n{fill:var(--ink);opacity:0;animation:pn .4s var(--e2) 2.4s forwards}
.hc-x{fill:var(--tx3);font-size:9px;font-weight:600;font-family:'Outfit',sans-serif}
@media (max-width:1100px){.hc{width:100%;max-width:380px}}
@media (prefers-reduced-motion:reduce){
 .hc-b{opacity:1!important;transform:none!important}.hc-ag,.hc-n{opacity:1!important}}
@media (max-width:1100px){.hr,.g2,.g3{grid-template-columns:1fr}.rl{width:100%;max-width:340px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}
 .t-l{stroke-dashoffset:0!important}
 .t-f,.t-bd,.t-a,.t-ag,.t-n,.anp,.rl-m{opacity:1!important}.t-bd{opacity:.12!important}
 .t-h{opacity:0!important}.rw-b i{width:var(--w)!important}
 .it,.mr,.dc i,.ch,.rl-b{opacity:1!important;transform:none!important}
 .mt-b s{transform:none!important}.mt-b i,.mt-b u{opacity:1!important}
 .anr .anr-v{stroke-dashoffset:var(--f)!important}}
"""
