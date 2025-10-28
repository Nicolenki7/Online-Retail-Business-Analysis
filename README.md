# 🛍️ Análisis de Segmentación de Clientes RFM - Retail Online

## 🎯 Objetivo del Proyecto

Este proyecto aplica el modelo **RFM (Recency, Frequency, Monetary)** para segmentar la base de clientes de un minorista en línea y definir estrategias de marketing específicas para maximizar el valor de vida del cliente (CLV) y la retención.

## 💡 Metodología (RFM)

El análisis RFM asigna una puntuación a cada cliente basada en tres métricas clave:

* **R (Recencia):** Hace cuánto tiempo el cliente hizo su última compra. (*Puntuación alta = Compró recientemente*).
* **F (Frecuencia):** Con qué frecuencia el cliente realiza compras. (*Puntuación alta = Compra a menudo*).
* **M (Valor Monetario):** Cuánto dinero ha gastado el cliente. (*Puntuación alta = Alto gasto*).

Utilizando Python (Pandas) y la distribución de cuartiles, se creó una puntuación RFM combinada para clasificar a los clientes en segmentos accionables.

## 📊 Hallazgos Clave y Conclusiones Ejecutivas

El análisis reveló una fuerte dependencia del ingreso en una gran fracción de la base de clientes (47.55%) que genera la inmensa mayoría de los ingresos, lo cual es crucial para la asignación de recursos (Ley de Pareto).

| Hallazgo | Base de Clientes (Gráfico Circular) | Ingresos Totales (Gráfico de Barras) |
| :--- | :--- | :--- |
| **Foco Estratégico (Leales + Potencial Leal)** | **47.55%** | **78.91%** |
| **Clientes Leales (Individual)** | 24.20% | 71.80% |

### 🔑 Conclusiones

* **Sólido Rendimiento del Valor:** El **47.55%** de la base de clientes (principalmente los segmentos 'Leales' y 'Potencial Leal') es responsable de generar un impresionante **78.91%** de los ingresos.
* **Prioridad Absoluta:** El segmento **'Clientes Leales'** es el motor del negocio, aportando casi las tres cuartas partes (71.80%) de los ingresos. La estrategia de retención y recompensa (ej. Programas VIP) debe ser su prioridad.
* **Oportunidad de Reactivación:** El gran tamaño del segmento **'Durmiendo'** (23.4%) indica una gran cantidad de clientes con alto riesgo de abandono que requieren una campaña de *win-back* urgente y segmentada.

## 📋 Estrategia de Intervención por Segmento

| Segmento | % de Ingresos | Estrategia de Intervención Recomendada |
| :--- | :--- | :--- |
| **Clientes Leales** | 71.80% | **Programa VIP y Exclusivo.** Recompensa por lealtad para maximizar la retención y el *upselling*. |
| **Potencial Leal** | 7.11% | **Incentivo de Frecuencia.** Campañas de segunda/tercera compra con descuentos por volumen. |
| **Clientes en Riesgo** | 11.27% | **Campaña *Win-Back* Inmediata.** Descuentos de reactivación y ofertas personalizadas. |
| **Durmiendo** | 0.8% (Aprox.) | **Email Masivo de Última Oportunidad.** Baja prioridad, enfocar recursos en segmentos más rentables. |

## 🔗 Dashboard Interactivo (Looker Studio)

El informe completo, interactivo y con la segmentación RFM por colores, está disponible en el siguiente enlace:

[**Acceder al Dashboard de Segmentación RFM**](https://lookerstudio.google.com/s/l3I-jf7mSGs)
