"""
Extrai métricas reais do LWDATASET para alimentar os protótipos.
Saída: prototipos/data/metricas-telas.json
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "assets" / "Materal LocalWeb" / "LW-DATASET.xlsx"
OUT  = ROOT / "prototipos" / "data" / "metricas-telas.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(XLSX)

# normaliza nomes (espaços, acentos)
df.columns = [c.strip() for c in df.columns]

# Identifica colunas-chave (vocabulario-real.md confirma essas)
COL_OPEN = "Aberto"
COL_PAI  = "Incidente Pai"
COL_KPI_ENT = "Entrou para KPI?"
COL_KPI_VIO = "KPI Violado?"

df[COL_OPEN] = pd.to_datetime(df[COL_OPEN], errors="coerce")
df = df.dropna(subset=[COL_OPEN]).copy()
df["date"] = df[COL_OPEN].dt.date
df["weekday"] = df[COL_OPEN].dt.weekday  # 0=Mon
df["hour"] = df[COL_OPEN].dt.hour
df["ym"] = df[COL_OPEN].dt.to_period("M").astype(str)

# Filtros KPI: só pai e KPI elegível
def yes(v): return str(v).strip().upper() in {"SIM", "S", "YES", "TRUE", "1"}

is_pai = df[COL_PAI].isna() | (df[COL_PAI].astype(str).str.strip() == "")
kpi_eleg = df[COL_KPI_ENT].apply(yes)
kpi_vio  = df[COL_KPI_VIO].apply(yes)

df_kpi   = df[is_pai & kpi_eleg].copy()
df_viol  = df[is_pai & kpi_eleg & kpi_vio].copy()

# ────────────────────────────────────────────────────────────
# 1) Volume diário — últimos 30 dias do dataset (foco dez/2025)
# ────────────────────────────────────────────────────────────
last_date = df["date"].max()
first_30  = pd.Timestamp(last_date) - pd.Timedelta(days=29)
dia30 = (
    df[df["date"] >= first_30.date()]
    .groupby("date")
    .size()
    .reindex(pd.date_range(first_30, last_date).date, fill_value=0)
)
trend_30d = [
    {"d": d.isoformat(), "vol": int(v)}
    for d, v in dia30.items()
]

# Mesma janela: OLAs quebrados por dia
viol_30d = (
    df_viol[df_viol["date"] >= first_30.date()]
    .groupby("date")
    .size()
    .reindex(pd.date_range(first_30, last_date).date, fill_value=0)
)
ola_30d = [
    {"d": d.isoformat(), "ola": int(v)}
    for d, v in viol_30d.items()
]

# ────────────────────────────────────────────────────────────
# 2) Heatmap 7×24 — média semanal recente (últimos 90 dias)
#    Duas dimensões pro quadrado diagonal: volume + OLA quebrado
# ────────────────────────────────────────────────────────────
recent_cut = pd.Timestamp(last_date) - pd.Timedelta(days=89)
df_recent = df[df["date"] >= recent_cut.date()]
vio_recent = df_viol[df_viol["date"] >= recent_cut.date()]

# volume médio por hora/weekday — normaliza dividindo por nº de semanas presentes
weeks_present = (pd.Timestamp(last_date) - recent_cut).days / 7
vol_pivot = (
    df_recent.groupby(["weekday", "hour"])
    .size()
    .unstack(fill_value=0)
    .reindex(index=range(7), columns=range(24), fill_value=0)
    / weeks_present
).round(1)
ola_pivot = (
    vio_recent.groupby(["weekday", "hour"])
    .size()
    .unstack(fill_value=0)
    .reindex(index=range(7), columns=range(24), fill_value=0)
    / weeks_present
).round(2)

heatmap = {
    "weeks_window": round(weeks_present, 1),
    "vol_max": float(vol_pivot.values.max()),
    "ola_max": float(ola_pivot.values.max()),
    "vol": vol_pivot.values.tolist(),   # 7 linhas × 24 colunas
    "ola": ola_pivot.values.tolist(),
}

# ────────────────────────────────────────────────────────────
# 3) Volume mensal completo (pro contexto da lateral)
# ────────────────────────────────────────────────────────────
monthly = df.groupby("ym").size().to_dict()

# ────────────────────────────────────────────────────────────
# 4) Saúde produto — por janela (24h / 7d / 30d)
#    Score simplificado pra mockup: 100 - (incid/baseline * 30)
#    aterrissamos em volume real por produto na janela
# ────────────────────────────────────────────────────────────
def janela(dias):
    cut = pd.Timestamp(last_date) - pd.Timedelta(days=dias - 1)
    return df_kpi[df_kpi["date"] >= cut.date()]

def top_prod(dfj, n=10):
    return (
        dfj.assign(p=dfj["Produto"].fillna("(sem produto)"))
        .groupby("p")
        .agg(inc=("p", "size"))
        .sort_values("inc", ascending=False)
        .head(n)
    )

windows = {}
for label, dias in [("24h", 1), ("7d", 7), ("30d", 30)]:
    dfj = janela(dias)
    tp = top_prod(dfj, 12)
    windows[label] = {
        "total_incidentes": int(dfj.shape[0]),
        "total_ola_quebrado": int(dfj[kpi_vio.reindex(dfj.index, fill_value=False)].shape[0]) if dias > 0 else 0,
        "produtos": [{"prod": p, "inc": int(v)} for p, v in tp["inc"].items()],
    }

# OLA violado por janela (precisa recalcular pq kpi_vio é mask global)
for label, dias in [("24h", 1), ("7d", 7), ("30d", 30)]:
    cut = pd.Timestamp(last_date) - pd.Timedelta(days=dias - 1)
    sub = df_viol[df_viol["date"] >= cut.date()]
    windows[label]["total_ola_quebrado"] = int(sub.shape[0])
    by_prod = (
        sub.assign(p=sub["Produto"].fillna("(sem produto)"))
        .groupby("p").size().sort_values(ascending=False).head(8)
    )
    windows[label]["ola_por_produto"] = [{"prod": p, "ola": int(v)} for p, v in by_prod.items()]

# ────────────────────────────────────────────────────────────
# 5) Top cascatas (incidente pai com mais filhos)
# ────────────────────────────────────────────────────────────
filhos = (
    df[~(df[COL_PAI].isna() | (df[COL_PAI].astype(str).str.strip() == ""))]
    .groupby(COL_PAI).size().sort_values(ascending=False).head(10)
)
top_cascatas = [{"pai": p, "filhos": int(v)} for p, v in filhos.items()]

# ────────────────────────────────────────────────────────────
# 6) Resumo geral
# ────────────────────────────────────────────────────────────
resumo = {
    "total_incidentes": int(df.shape[0]),
    "total_pai": int(df_kpi.shape[0]),
    "total_ola_violado": int(df_viol.shape[0]),
    "data_min": str(df["date"].min()),
    "data_max": str(df["date"].max()),
    "team_top": "Team14",
    "team_top_share": 0.757,
}

payload = {
    "resumo": resumo,
    "monthly": monthly,
    "trend_30d_volume": trend_30d,
    "trend_30d_ola": ola_30d,
    "heatmap_7x24": heatmap,
    "saude_windows": windows,
    "top_cascatas": top_cascatas,
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK — escrito {OUT.relative_to(ROOT)}  ({OUT.stat().st_size/1024:.1f} KB)")
print(f"resumo: {resumo}")
print(f"trend_30d primeiros 5: {trend_30d[:5]}")
print(f"ola_30d ultimos 5: {ola_30d[-5:]}")
print(f"heatmap vol[2] (qua): {heatmap['vol'][2]}")
print(f"saude 7d: {windows['7d']['total_incidentes']} inc / {windows['7d']['total_ola_quebrado']} OLA")
