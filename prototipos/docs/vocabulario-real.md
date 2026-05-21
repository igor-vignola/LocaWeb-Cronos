# Vocabulário real do LWDATASET — input pros protótipos

> **Tudo aqui é extraído direto do `assets/Materal LocalWeb/LW-DATASET.xlsx`.** Zero invenção.
> Use estes nomes/valores nas telas do Cronos pra não soar inventado.

**Dataset:** 122,543 incidentes · 23 colunas · período 2023-01-02 a 2025-12-31

---

## 1. Distribuições estruturais

### Prioridade
| Prioridade | N | % |
|---|---|---|
| 4 - Baixa | 64,828 | 52.9% |
| 3 - Média | 41,732 | 34.1% |
| 2 - Alta | 15,649 | 12.8% |
| 5 - Muito Baixa | 333 | 0.3% |
| 1 - Crítica | 1 | 0.0% |

### Status
| Status | N | % |
|---|---|---|
| Sem Intervenção | 80,373 | 65.6% |
| Encerrado Automaticamente | 26,830 | 21.9% |
| Encerrado | 15,339 | 12.5% |
| Aguardando Problema | 1 | 0.0% |

### Origem (`Aberto por`)
| Origem | N | % |
|---|---|---|
| Monitoramento | 104,299 | 85.1% |
| Manual | 18,244 | 14.9% |

### Solução
| Tipo | N |
|---|---|
| (vazio — sem solução registrada) | 107,243 |
| Contorno | 9,407 |
| Definitiva | 5,893 |

### KPI
- **Entrou para KPI:** SIM: 25,600 · NAO: 96,943
- **KPI Violado** (entre os que entraram): SIM: 248 · NAO: 25,352
- Taxa de quebra de OLA: **0.97%** dos elegíveis ao KPI

---

## 2. Grupos designados (17 times reais)

| Grupo | N | % |
|---|---|---|
| Team14 | 92,775 | 75.7% |
| Team11 | 9,790 | 8.0% |
| Team05 | 9,276 | 7.6% |
| Team09 | 3,425 | 2.8% |
| Team12 | 2,173 | 1.8% |
| Team03 | 1,306 | 1.1% |
| Team10 | 1,172 | 1.0% |
| Team17 | 743 | 0.6% |
| Team02 | 579 | 0.5% |
| Team01 | 306 | 0.2% |
| Team16 | 279 | 0.2% |
| Team15 | 219 | 0.2% |
| Team07 | 197 | 0.2% |
| Team08 | 130 | 0.1% |
| Team04 | 122 | 0.1% |
| Team06 | 50 | 0.0% |
| Team13 | 1 | 0.0% |

> **Insight crítico:** o time **Team14** sozinho responde por **75.7%** do volume. Ranking de carga é fortemente assimétrico.

### Top 3 produtos por grupo (especialização real)
Útil pra mostrar 'roteamento automático' do Cronos respeitando essa especialização.

| Grupo | Produto | N |
|---|---|---|
| Team01 | lsin | 143 |
| Team01 | lhco | 18 |
| Team01 | lvps | 11 |
| Team02 | lsin | 302 |
| Team02 | lhco | 136 |
| Team02 | lrev | 26 |
| Team03 | lsin | 335 |
| Team03 | lclo | 247 |
| Team03 | lvps | 75 |
| Team04 | lsin | 64 |
| Team04 | lmse | 3 |
| Team04 | lsto | 3 |
| Team05 | lcem | 4,440 |
| Team05 | lrev | 775 |
| Team05 | lemg | 539 |
| Team06 | lcem | 41 |
| Team06 | lemg | 1 |
| Team06 | lrev | 1 |
| Team07 | lexc | 138 |
| Team07 | lcem | 44 |
| Team07 | lsin | 4 |
| Team08 | lsin | 44 |
| Team08 | lsd0 | 34 |
| Team08 | lhco | 20 |
| Team09 | lhco | 1,440 |
| Team09 | lsin | 775 |
| Team09 | lrev | 270 |
| Team10 | lsin | 220 |
| Team10 | lmse | 13 |
| Team10 | lclo | 4 |
| Team11 | lhco | 4,448 |
| Team11 | lcem | 1,268 |
| Team11 | lsin | 679 |
| Team12 | lsin | 605 |
| Team12 | lsto | 54 |
| Team12 | lvps | 53 |
| Team13 | lsin | 1 |
| Team14 | lhco | 6,472 |
| Team14 | lsin | 3,558 |
| Team14 | lhvp | 3,530 |
| Team15 | lsto | 56 |
| Team15 | lsin | 22 |
| Team15 | lost | 6 |
| Team16 | lsaa | 214 |
| Team16 | lsin | 41 |
| Team16 | lmse | 1 |
| Team17 | lhco | 243 |
| Team17 | lsin | 184 |
| Team17 | lrev | 152 |

---

## 3. Produtos reais (51 valores únicos)

_~36% dos incidentes têm produto preenchido (44,608 de 122,543)._

| # | Produto | Incidentes | % do total | % dos preenchidos |
|---|---|---|---|---|
| 1 | `lhco` | 12,835 | 10.5% | 28.8% |
| 2 | `lsin` | 7,342 | 6.0% | 16.5% |
| 3 | `lcem` | 5,878 | 4.8% | 13.2% |
| 4 | `lhvp` | 4,454 | 3.6% | 10.0% |
| 5 | `lrev` | 3,784 | 3.1% | 8.5% |
| 6 | `lcho` | 1,368 | 1.1% | 3.1% |
| 7 | `lcsi` | 1,085 | 0.9% | 2.4% |
| 8 | `lsaa` | 919 | 0.7% | 2.1% |
| 9 | `lrel` | 905 | 0.7% | 2.0% |
| 10 | `lvps` | 703 | 0.6% | 1.6% |
| 11 | `lemg` | 643 | 0.5% | 1.4% |
| 12 | `lemn` | 639 | 0.5% | 1.4% |
| 13 | `lrdo` | 573 | 0.5% | 1.3% |
| 14 | `lssl` | 512 | 0.4% | 1.1% |
| 15 | `lgoa` | 404 | 0.3% | 0.9% |
| 16 | `lsmt` | 335 | 0.3% | 0.8% |
| 17 | `lcsp` | 326 | 0.3% | 0.7% |
| 18 | `lsg2` | 282 | 0.2% | 0.6% |
| 19 | `lclo` | 272 | 0.2% | 0.6% |
| 20 | `lwpl` | 204 | 0.2% | 0.5% |
| 21 | `lexc` | 196 | 0.2% | 0.4% |
| 22 | `lsd0` | 166 | 0.1% | 0.4% |
| 23 | `lvpk` | 165 | 0.1% | 0.4% |
| 24 | `khvp` | 126 | 0.1% | 0.3% |
| 25 | `lsto` | 125 | 0.1% | 0.3% |
| … | _(26 produtos restantes)_ | | | |

---

## 4. Categorias (141 reais) — Top 25

| # | Categoria | N |
|---|---|---|
| 1 | `cat71` | 7,335 |
| 2 | `cat77` | 4,425 |
| 3 | `cat85` | 4,319 |
| 4 | `cat76` | 4,304 |
| 5 | `cat73` | 3,388 |
| 6 | `cat31` | 2,483 |
| 7 | `cat137` | 1,716 |
| 8 | `cat91` | 1,246 |
| 9 | `cat36` | 1,086 |
| 10 | `cat141` | 933 |
| 11 | `cat18` | 932 |
| 12 | `cat103` | 699 |
| 13 | `cat29` | 650 |
| 14 | `cat96` | 575 |
| 15 | `cat97` | 556 |
| 16 | `cat138` | 543 |
| 17 | `cat41` | 535 |
| 18 | `cat45` | 533 |
| 19 | `cat123` | 476 |
| 20 | `cat102` | 436 |
| 21 | `cat24` | 433 |
| 22 | `cat74` | 403 |
| 23 | `cat35` | 364 |
| 24 | `cat40` | 348 |
| 25 | `cat94` | 347 |

## 5. Subcategorias (447 reais) — Top 25

| # | Subcategoria | N |
|---|---|---|
| 1 | `sub7` | 4,668 |
| 2 | `sub336` | 4,297 |
| 3 | `sub36` | 2,741 |
| 4 | `sub387` | 2,494 |
| 5 | `sub427` | 2,192 |
| 6 | `sub225` | 1,638 |
| 7 | `sub392` | 1,625 |
| 8 | `sub127` | 1,470 |
| 9 | `sub438` | 1,116 |
| 10 | `sub95` | 1,070 |
| 11 | `sub446` | 933 |
| 12 | `sub307` | 889 |
| 13 | `sub285` | 885 |
| 14 | `sub84` | 851 |
| 15 | `sub12` | 820 |
| 16 | `sub79` | 647 |
| 17 | `sub59` | 630 |
| 18 | `sub30` | 499 |
| 19 | `sub288` | 446 |
| 20 | `sub65` | 379 |
| 21 | `sub426` | 352 |
| 22 | `sub6` | 349 |
| 23 | `sub362` | 345 |
| 24 | `sub212` | 336 |
| 25 | `sub220` | 334 |

### Top 20 pares Produto × Categoria
| Produto | Categoria | N |
|---|---|---|
| `lhco` | `cat71` | 5,907 |
| `lsin` | `cat77` | 4,388 |
| `lcem` | `cat76` | 4,287 |
| `lhvp` | `cat73` | 3,388 |
| `lhco` | `cat85` | 3,148 |
| `lhco` | `cat31` | 1,518 |
| `lhco` | `cat137` | 1,295 |
| `lcem` | `cat91` | 1,246 |
| `lrev` | `cat36` | 1,086 |
| `lcho` | `cat71` | 1,026 |
| `lsin` | `cat141` | 933 |
| `lhco` | `cat18` | 895 |
| `lsin` | `cat29` | 650 |
| `lrev` | `cat96` | 575 |
| `lrev` | `cat97` | 556 |
| `lhvp` | `cat138` | 543 |
| `lcsi` | `cat41` | 535 |
| `lemn` | `cat45` | 532 |
| `lrel` | `cat123` | 476 |
| `lssl` | `cat102` | 436 |

---

## 6. Itens de Configuração (9,171 ICs únicos)

_120,763 incidentes têm IC preenchido (98.5%)._

### Top 20 ICs por volume
| # | IC | Incidentes |
|---|---|---|
| 1 | `IC00014` | 6,069 |
| 2 | `IC00019` | 4,435 |
| 3 | `IC00008` | 4,196 |
| 4 | `IC00349` | 3,271 |
| 5 | `IC00002` | 3,119 |
| 6 | `IC00325` | 1,600 |
| 7 | `IC00004` | 1,149 |
| 8 | `IC00604` | 1,079 |
| 9 | `IC00725` | 988 |
| 10 | `IC02447` | 978 |
| 11 | `IC02448` | 978 |
| 12 | `IC02761` | 968 |
| 13 | `IC00367` | 935 |
| 14 | `IC00324` | 927 |
| 15 | `IC00511` | 902 |
| 16 | `IC00024` | 882 |
| 17 | `IC04860` | 857 |
| 18 | `IC00032` | 824 |
| 19 | `IC01285` | 796 |
| 20 | `IC00100` | 699 |

---

## 7. Códigos de fechamento (17 reais)

| # | Código | N |
|---|---|---|
| 1 | Falha de Aplicação | 20,612 |
| 2 | Falha de Sistema Operacional | 5,009 |
| 3 | Outro | 3,490 |
| 4 | Falha causada pelo cliente | 1,796 |
| 5 | Sem retorno do solicitante | 1,527 |
| 6 | Falha não reproduzida | 1,401 |
| 7 | Incidente causado por Change | 1,353 |
| 8 | Falha de Cloud | 1,202 |
| 9 | Falha de Segurança | 1,068 |
| 10 | Falha de Hardware | 743 |
| 11 | Falso Positivo | 715 |
| 12 | Falha de Monitoração | 641 |
| 13 | Falha de Storage | 605 |
| 14 | Falha de Banco de Dados | 455 |
| 15 | Falha de Redes | 161 |
| 16 | Gerado para auditoria de Segurança | 23 |
| 17 | Carta de Risco | 3 |

---

## 8. Descrições recorrentes (Top 30) — USAR NOS MOCKUPS

Estes são textos REAIS que aparecem em alertas. Use-os literalmente nos cards de incidente em vez de inventar.

| # | Descrição resumida | Ocorrências |
|---|---|---|
| 1 | `Problem: Check Application Monitoring` | 28,728 |
| 2 | `Problem: Free disk space is less than 10% on volume /` | 4,770 |
| 3 | `Problem: Check Application Monitoring VIP` | 4,281 |
| 4 | `Problem: Unavailable by ICMP ping` | 4,133 |
| 5 | `Problem: Apache Busy Workers` | 3,925 |
| 6 | `Problem: Lack of free swap space 40m <5%` | 3,255 |
| 7 | `Problem: Processor load is too high P3` | 2,174 |
| 8 | `Problem: High bandwidth >60% at least 15m` | 1,874 |
| 9 | `Problem: Error Backup Full Bacula` | 1,689 |
| 10 | `Problem: Alarm Application Monitoring feeds Message: HTTPSConnectionPool(host='IC00004IC04172locawebIC04172comIC04172br', port=443): Read…` | 1,465 |
| 11 | `Problem: IOwait grown up CPU queue` | 1,438 |
| 12 | `Problem: Error Backup Inc Bacula` | 1,367 |
| 13 | `Problem: Check PostgreSQL Replication Slave` | 1,341 |
| 14 | `Problem: /: Free disk space is less than 5` | 977 |
| 15 | `Problem: Check PMTA IC00622 Queue` | 852 |
| 16 | `Problem: Hank Instalation Recipes::Domains::Domain::IC04228::Activate Created_dmarc_entry` | 722 |
| 17 | `Problem: Check: HTTP Type: tcp on Port: 80 Not Running` | 702 |
| 18 | `Problem: Check: Nginx Type: tcp on Port: 80 Not Running` | 688 |
| 19 | `Problem: Check: Nginx Type: tcp on Port: 443 Not Running` | 683 |
| 20 | `Problem: Check: HTTPS Type: tcp on Port: 443 Not Running` | 666 |
| 21 | `Problem: CPU Used in %` | 665 |
| 22 | `Problem: Perf Teste Asp - Web Test Fail` | 655 |
| 23 | `Problem: Gurnicorn is down` | 542 |
| 24 | `Problem: Check PostgreSQL Replication Master` | 509 |
| 25 | `Problem: Check Service Nginx isn´t Running` | 493 |
| 26 | `Problem: CPU Idle is less than 5%` | 439 |
| 27 | `Problem: Hank Instalation Recipes::Domains::Domain::IC04228::Activate Domain_reserved` | 437 |
| 28 | `Problem: Processor load is too high > 20%` | 401 |
| 29 | `Problem: Free Disk Space is less than 10% on volume /home/storage` | 400 |
| 30 | `Problem: Disk I/O is overloaded on IC00069` | 396 |

---

## 9. Incidentes-pai mais 'famosos' (candidatos a estudo de cascata)

_15,127 incidentes têm pai. Os números abaixo são quantos FILHOS cada pai tem._

| Pai (Número) | Nº de filhos |
|---|---|
| `INC8542250` | 630 |
| `INC8591143` | 510 |
| `INC8570109` | 296 |
| `INC8522386` | 238 |
| `INC8445074` | 227 |
| `INC8558823` | 213 |
| `INC8578958` | 147 |
| `INC8525293` | 146 |
| `INC8618742` | 146 |
| `INC8563438` | 144 |
| `INC8602660` | 140 |
| `INC8643147` | 135 |
| `INC8544781` | 131 |
| `INC8256155` | 127 |
| `INC8607139` | 125 |

---

## 10. Quem mais quebra OLA (KPI Violado=SIM, só pais)

_Filtro: `Incidente Pai` vazio + `KPI Violado?` = SIM → 248 casos._

### Por prioridade
| Prioridade | Violações |
|---|---|
| 3 - Média | 206 |
| 2 - Alta | 42 |

### Top 15 produtos com mais quebras
| # | Produto | Quebras |
|---|---|---|
| 1 | `lsin` | 63 |
| 2 | `lhco` | 55 |
| 3 | `lcem` | 25 |
| 4 | `lexc` | 14 |
| 5 | `lhvp` | 14 |
| 6 | `lvps` | 10 |
| 7 | `lrev` | 9 |
| 8 | `lssl` | 9 |
| 9 | `lrdo` | 8 |
| 10 | `lsaa` | 8 |
| 11 | `lgoa` | 7 |
| 12 | `lrel` | 5 |
| 13 | `lemg` | 4 |
| 14 | `lcho` | 3 |
| 15 | `lemn` | 3 |

### Top 15 categorias com mais quebras
| # | Categoria | Quebras |
|---|---|---|
| 1 | `cat31` | 46 |
| 2 | `cat85` | 33 |
| 3 | `cat71` | 26 |
| 4 | `cat103` | 11 |
| 5 | `cat77` | 11 |
| 6 | `cat91` | 11 |
| 7 | `cat48` | 9 |
| 8 | `cat102` | 8 |
| 9 | `cat24` | 8 |
| 10 | `cat73` | 8 |
| 11 | `cat88` | 7 |
| 12 | `cat76` | 7 |
| 13 | `cat74` | 5 |
| 14 | `cat112` | 4 |
| 15 | `cat35` | 4 |

### Grupos com mais quebras
| # | Grupo | Quebras |
|---|---|---|
| 1 | Team11 | 114 |
| 2 | Team09 | 56 |
| 3 | Team07 | 16 |
| 4 | Team05 | 13 |
| 5 | Team03 | 12 |
| 6 | Team14 | 10 |
| 7 | Team12 | 8 |
| 8 | Team02 | 4 |
| 9 | Team17 | 4 |
| 10 | Team06 | 4 |
| 11 | Team08 | 3 |
| 12 | Team16 | 2 |
| 13 | Team01 | 1 |
| 14 | Team10 | 1 |

---

## 11. Padrões temporais

> 🚨 **Achado importante:** a "anomalia de setembro/2025" que a Locaweb mencionou na mentoria é uma **ALTA**, não uma queda — set/25 saltou de ~4k pra **21,6k** (5x). Out-nov estabilizaram em patamar alto e dez bateu 27,3k. 2023 e 2024 inteiros têm volume desprezível (~750 incidentes nos dois anos somados). **Hipótese mais provável: expansão/mudança do sistema de monitoramento em set/2025.**

### Volume mensal
| Mês | Volume |
|---|---|
| 2023-01 | 12 |
| 2023-02 | 7 |
| 2023-03 | 8 |
| 2023-04 | 6 |
| 2023-05 | 7 |
| 2023-06 | 2 |
| 2023-07 | 6 |
| 2023-08 | 6 |
| 2023-09 | 14 |
| 2023-10 | 21 |
| 2023-11 | 13 |
| 2023-12 | 8 |
| 2024-01 | 7 |
| 2024-02 | 12 |
| 2024-03 | 32 |
| 2024-04 | 26 |
| 2024-05 | 16 |
| 2024-06 | 16 |
| 2024-07 | 44 |
| 2024-08 | 39 |
| 2024-09 | 34 |
| 2024-10 | 50 |
| 2024-11 | 75 |
| 2024-12 | 271 |
| 2025-01 | 3,714 |
| 2025-02 | 3,553 |
| 2025-03 | 3,588 |
| 2025-04 | 3,202 |
| 2025-05 | 3,329 |
| 2025-06 | 3,558 |
| 2025-07 | 3,448 |
| 2025-08 | 3,996 |
| 2025-09 | 21,561 |
| 2025-10 | 23,017 |
| 2025-11 | 21,524 |
| 2025-12 | 27,321 |

### Hora do dia
| Hora | Volume |
|---|---|
| 00h | 5,609 |
| 01h | 4,613 |
| 02h | 3,876 |
| 03h | 5,132 |
| 04h | 4,574 |
| 05h | 3,977 |
| 06h | 4,886 |
| 07h | 4,153 |
| 08h | 4,996 |
| 09h | 6,428 |
| 10h | 6,356 |
| 11h | 6,294 |
| 12h | 5,617 |
| 13h | 5,188 |
| 14h | 5,624 |
| 15h | 6,124 |
| 16h | 5,465 |
| 17h | 5,399 |
| 18h | 5,019 |
| 19h | 4,247 |
| 20h | 4,512 |
| 21h | 4,932 |
| 22h | 4,581 |
| 23h | 4,941 |

### Dia da semana
| Dia | Volume |
|---|---|
| Segunda | 19,070 |
| Terça | 19,482 |
| Quarta | 19,964 |
| Quinta | 18,806 |
| Sexta | 18,170 |
| Sábado | 14,432 |
| Domingo | 12,619 |

---

## 12. Duração dos incidentes

| Métrica | Segundos | Tradução |
|---|---|---|
| mean | 248,547 | 2.9d |
| std | 2,480,123 | 28.7d |
| min | 1 | 1s |
| 25% | 263 | 4min |
| 50% | 978 | 16min |
| 75% | 4,240 | 1.2h |
| max | 88,280,481 | 1021.8d |

> ⚠️ Distribuição **extremamente assimétrica** — usar **mediana** (não média) em KPIs visíveis. Outliers monstruosos (ver max).

---

## 13. Frases reais prontas pra colar nos mockups

Combinações de números/nomes reais que dão peso de produto:

- **Volume total:** "122,543 incidentes nos últimos 3 anos"
- **Produto top:** `lhco` liderou com 12,835 ocorrências
- **Carga concentrada:** "Team14 responde por 75.7% dos atendimentos"
- **Origem automatizada:** "85.1% vêm do monitoramento"
- **Auto-resolução:** "65.6% são encerrados sem intervenção humana"
- **OLA:** "248 violações em 25,600 incidentes elegíveis (0.97%)"
- **Alerta mais comum:** `Problem: Check Application Monitoring` (28,728 ocorrências)
- **IC mais instável:** `IC00014` com 6,069 ocorrências
- **Maior cascata histórica:** `INC8542250` gerou 630 incidentes-filhos
- **Tempo típico de resolução:** 16min (mediana)

---

*Gerado automaticamente pelo script `prototipos/_gera_vocabulario.py` em 21/05/2026.*