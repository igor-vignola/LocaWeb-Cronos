---
data: 2026-07-20
tipo: conhecimento
status: ativo
relacionados: [prototipo-reflete-arquitetura]
---

# Setup do ambiente de modelagem (Windows) — Prophet, tslearn, SHAP

## Contexto

Início da Sprint 3 (MVP Preliminar). Ao montar o `.venv` e instalar a stack de
modelagem no **Windows 11 + Python 3.13.2**, batemos em dois problemas de instalação
que abortavam o setup. Ambos resolvidos. Este arquivo existe pra ninguém (Ana, Hygor,
sessão futura) redescobrir do zero.

## O que ficou definido

**Ambiente:** `.venv` na raiz do projeto (já no `.gitignore`). Instalar com
`.venv/Scripts/python -m pip install -r requirements.txt`. Versões fixadas no
`requirements.txt` são as que **de fato rodam** — não atualizar por atualizar.

**Rodar notebooks:** headless via `nbconvert`/`nbclient` + `ipykernel`. **NÃO usamos
JupyterLab.**

### Problema 1 — Long Path aborta o install inteiro
Instalar `jupyter`/`jupyterlab`/`notebook`/`ipywidgets` traz "labextensions" com nomes
de arquivo enormes (ex: `vendors-node_modules_d3-color_src...js`) que estouram o limite
de **260 caracteres** de caminho do Windows. O pip faz o install numa transação só, então
esse `OSError` **desfaz a instalação toda** (nem pandas sobra).
- **Fix:** não instalar esses pacotes. Rodar notebook via nbconvert/nbclient (não precisam do Lab).

### Problema 2 — Prophet quebra no backend Stan (Windows PT-BR)
`Prophet().fit()` estourava `AttributeError: 'Prophet' object has no attribute
'stan_backend'`. Causa real (mascarada em 2 camadas): o **cmdstanpy** roda
`where.exe tbb.dll` pra localizar uma DLL da Intel; no **Windows em português** a saída
de "não encontrado" vem em **cp850** (onde `Ç` = byte 0x80), mas o cmdstanpy lê como
**UTF-8** → `UnicodeDecodeError` → o fallback que adicionaria a DLL ao PATH nunca roda.
- **Fix:** pôr a pasta do `tbb` no PATH **antes** de importar/usar o Prophet:
  ```python
  import os, glob
  base = os.path.join(".venv","Lib","site-packages","prophet","stan_model")
  tbb = [p for p in glob.glob(os.path.join(base,"**","tbb"), recursive=True) if os.path.isdir(p)]
  if tbb:
      os.environ["PATH"] = os.path.abspath(tbb[0]) + os.pathsep + os.environ["PATH"]
  ```
  Com o `tbb.dll` no PATH, `where.exe` retorna um caminho ASCII limpo e o cmdstanpy segue.
  Esse fix vai embutido no helper de modelagem (topo dos notebooks 02/03).

## Por quê

Sem isso, a stack central da nossa arquitetura (Prophet + XGBoost + tslearn/DTW + SHAP)
não roda — e sem modelos rodando não existe MVP. A banca da Sprint 3/4 avalia MVP em
funcionamento. Resolver o ambiente é pré-requisito de tudo.

## Como aplicar

- **Clonou o repo?** Cria o `.venv`, instala o `requirements.txt`, pronto.
- **Vai usar Prophet num script/notebook novo?** Aplica o fix do PATH no topo (ou importa o helper).
- **Instalação abortou com erro de path longo?** Confirma que não tem jupyterlab/ipywidgets na lista.

## Smoke test

Todos validados em 20/07/2026 (Python 3.13.2): Prophet fit+predict OK, TimeSeriesKMeans
com `metric='dtw'` OK, XGBoost+SHAP TreeExplainer OK, holidays.Brazil OK.

## Conexões

- Stack e regras técnicas: `../decisoes-tecnicas.md`
- Tudo que declaramos precisa rodar no MVP: `../preferencias/prototipo-reflete-arquitetura.md`

---

*Última atualização: 2026-07-20*
