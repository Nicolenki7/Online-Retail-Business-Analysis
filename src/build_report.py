"""Construye docs/report.html de Online Retail a partir del RFM por cliente.

Uso: python src/build_report.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report import escribir, num

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "rfm_segmentation_final.csv")
d["banda"] = "M" + d["M_Score"].astype(str)

filas = []
for (b, s), g in d.groupby(["banda", "Segment"]):
    filas.append({"a": b, "g": "ingresos", "k": s, "v": round(float(g.Monetary.sum()), 2), "u": "$"})
    filas.append({"a": b, "g": "clientes", "k": s, "v": int(len(g)), "u": ""})

seg = d.groupby("Segment").agg(clientes=("Monetary", "size"), ingresos=("Monetary", "sum"))
seg["pct"] = seg.ingresos / seg.ingresos.sum() * 100
seg = seg.sort_values("ingresos", ascending=False)
tabla = [[s, num(r.clientes), num(r.ingresos), f"{num(r.pct, 1)} %",
          num(r.ingresos / r.clientes, 2)] for s, r in seg.iterrows()]

escribir(
    ROOT / "docs" / "report.html",
    eyebrow="Retail · segmentación RFM",
    titulo="Online Retail: ¿de quién depende la facturación?",
    pregunta=("Cada cliente tiene recencia, frecuencia y valor monetario. La pregunta no es "
              "cuántos clientes hay, sino cuántos hacen falta para sostener el negocio: si una "
              "minoría concentra los ingresos, el plan de retención no puede tratarlos a todos igual."),
    kpis=[("Clientes", num(len(d)), "con compras registradas"),
          ("Ingresos", f"{num(d.Monetary.sum())} $", "suma del valor por cliente"),
          ("Ticket medio por cliente", f"{num(d.Monetary.mean(), 2)} $", "media, no mediana"),
          ("Segmentos", num(d.Segment.nunique()), "reglas RFM")],
    filtros=["todos"] + sorted(d.banda.unique()),
    filtro_etiqueta="Banda de gasto",
    graficos=[
        {"id": "ing", "grupo": "ingresos", "titulo": "Ingresos por segmento",
         "subtitulo": "el filtro cambia la banda de gasto (M1 = menor, M4 = mayor)",
         "unidad": "$"},
        {"id": "cli", "grupo": "clientes", "titulo": "Clientes por segmento",
         "subtitulo": "cuánta gente hay detrás de cada barra de ingresos", "unidad": ""},
    ],
    filas=filas,
    tabla={"titulo": "Los segmentos, ordenados por ingresos",
           "subtitulo": "ticket medio = ingresos del segmento / clientes del segmento",
           "cabeceras": ["Segmento", "Clientes", "Ingresos ($)", "% ingresos", "Ticket medio ($)"],
           "filas": tabla},
    metodo=["Cada cliente viene ya puntuado en R, F y M (1-4) por el notebook; el informe no recalcula el modelo.",
            "Ingresos = suma de Monetary, que es el gasto histórico del cliente en el CSV.",
            "El filtro actúa sobre el cuartil de gasto (M_Score), no sobre el segmento.",
            "Ticket medio = ingresos del segmento / clientes del segmento, no el ticket de una compra."],
    limitaciones=["El CSV no trae las líneas de pedido, así que no hay margen, devoluciones ni antigüedad real.",
                  "Los segmentos son reglas sobre cuartiles, no clústeres: dos clientes del mismo segmento pueden ser muy distintos.",
                  "Recency está en días desde la última compra en el corte del dataset, no en fecha de calendario.",
                  "No hay coste de adquisición: retener se ve barato porque solo se mide lo que ya se vendió."],
    fuente="rfm_segmentation_final.csv",
    metodo_sub="El modelo RFM vive en el notebook; aquí solo se agregan sus resultados.",
    lim_sub="Los cortes que este informe no puede sostener.")
print("docs/report.html:", (ROOT / "docs" / "report.html").stat().st_size, "bytes")
