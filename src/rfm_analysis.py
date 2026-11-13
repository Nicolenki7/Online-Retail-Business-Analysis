"""Segmentación RFM: quién sostiene la facturación y cuánto está en riesgo.

Datos: rfm_segmentation_final.csv (4.338 clientes de Online Retail, ya
puntuados por recencia, frecuencia y valor monetario en cuartiles).

Uso: python src/rfm_analysis.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_chart import AZUL, ROJO, barras

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "rfm_segmentation_final.csv"
IMG, OUT = ROOT / "docs" / "img", ROOT / "outputs"
IMG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

d = pd.read_csv(RAW)
total = d["Monetary"].sum()
print(f"1. cargado: {len(d):,} clientes · facturación {total:,.0f}")

g = d.groupby("Segment").agg(
    clientes=("CustomerID", "size"),
    ingresos=("Monetary", "sum"),
    recencia=("Recency", "mean"),
    frecuencia=("Frequency", "mean"),
    ticket=("Monetary", "mean"))
g["pct_clientes"] = g.clientes / len(d) * 100
g["pct_ingresos"] = g.ingresos / total * 100
g = g.sort_values("pct_ingresos", ascending=False)
print("\n2. segmentos ordenados por facturación:")
print(g.round(1).to_string())
g.to_csv(OUT / "segment_summary.csv")

# Etiquetas cortas solo para los gráficos: los nombres completos no caben
# en 51 px de ancho de barra y se pisarían entre ellos.
CORTO = {"Clientes Leales": "Leales", "Clientes en Riesgo": "En riesgo",
         "Potencial Leal": "Potencial", "Otros": "Otros",
         "No se pueden perder": "No perder", "Durmiendo": "Durmiendo",
         "Nuevos Clientes": "Nuevos"}

barras(
    [(CORTO.get(s, s), v, ROJO if v > 50 else AZUL) for s, v in g["pct_ingresos"].items()],
    "Un segmento sostiene la caja",
    IMG / "rfm-ingresos.svg",
    subtitulo="% de la facturación total por segmento RFM",
    formato="{:.1f}", sufijo="%")

orden_clientes = g["pct_clientes"].reindex(g.index)
barras(
    [(CORTO.get(s, s), v, AZUL) for s, v in orden_clientes.items()],
    "Y no es el segmento más numeroso",
    IMG / "rfm-clientes.svg",
    subtitulo="% de los clientes por segmento (mismo orden que el gráfico anterior)",
    formato="{:.1f}", sufijo="%")

# ---------- concentración: Pareto ----------
ordenado = d["Monetary"].sort_values(ascending=False).reset_index(drop=True)
acumulado = ordenado.cumsum() / total * 100


def cuota(pct):
    k = max(1, int(len(ordenado) * pct / 100))
    return acumulado.iloc[k - 1]


cortes = [1, 5, 10, 20, 50]
pareto = {f"top {c}%": cuota(c) for c in cortes}
print("\n3. concentración de la facturación:")
print({k: round(v, 1) for k, v in pareto.items()})

barras(
    [(k, v, ROJO if c in (1, 10) else AZUL) for (k, v), c in zip(pareto.items(), cortes)],
    f"El 10 % de los clientes paga el {pareto['top 10%']:.0f} % de la factura",
    IMG / "rfm-pareto.svg",
    subtitulo="% acumulado de la facturación que aporta cada grupo de clientes",
    formato="{:.1f}", sufijo="%")

# ---------- riesgo ----------
riesgo = d[d.Segment.isin(["Clientes en Riesgo", "No se pueden perder"])]
print(f"\n4. en riesgo: {len(riesgo)} clientes ({len(riesgo)/len(d):.1%}) · "
      f"{riesgo.Monetary.sum():,.0f} ({riesgo.Monetary.sum()/total:.1%} de la facturación)")
print("   recencia media:", round(riesgo.Recency.mean(), 1),
      "vs resto:", round(d[~d.Segment.isin(['Clientes en Riesgo', 'No se pueden perder'])].Recency.mean(), 1))
