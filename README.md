# 🎬 CineMetrics 360: Segmentación de Películas mediante K-Means y Dashboard Interactivo

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-K--Means-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Proyecto Integrador de Minería de Datos**  
> Implementación del algoritmo de aprendizaje no supervisado **K-Means**, interpretación de patrones en la industria cinematográfica contemporánea (2024–2026) y desarrollo de un **Dashboard Interactivo** en Streamlit.

---

## 📌 1. Descripción del Proyecto y Planteamiento del Problema

La industria cinematográfica moderna (2024–2026) atraviesa un momento crucial de reconfiguración económica post-pandemia, caracterizado por presupuestos de producción de cientos de millones de dólares, ventanas de exhibición dinámicas y una audiencia cada vez más selectiva. Los estudios y distribuidores se enfrentan a un dilema permanente: ¿cómo maximizar el retorno sobre la inversión (ROI) y la aclamación crítica minimizando el riesgo de fracaso comercial?

Este proyecto aplica técnicas de **minería de datos y agrupamiento no supervisado (K-Means)** sobre un catálogo de más de 900 películas modernas para descubrir patrones intrínsecos de rendimiento financiero y calidad artística. Los resultados se condensan en arquetipos fílmicos claros y se presentan a través de un **dashboard interactivo** diseñado para facilitar el análisis estratégico y la toma de decisiones.

---

## 🎯 2. Objetivos

### Objetivo General
Desarrollar un proyecto integral de minería de datos mediante el algoritmo no supervisado K-Means para segmentar producciones cinematográficas modernas (2024–2026) en función de sus variables financieras y de recepción crítica, comunicando los hallazgos a través de un dashboard interactivo de dos páginas y documentación técnica formal.

### Objetivos Específicos
1. **Explorar, depurar y transformar** el dataset de más de 900 películas, corrigiendo inconsistencias, tratando valores atípicos y escalando variables cuantitativas con `StandardScaler`.
2. **Evaluar y seleccionar el número óptimo de clústeres ($K$)** evaluando al menos 5 valores distintos de $K$ mediante el Método del Codo y el Coeficiente de Silueta (*Silhouette Score*).
3. **Contrastar dos configuraciones del modelo** para validar el impacto de las variables predictoras en la cohesión y separación de los agrupamientos.
4. **Interpretar los centroides** y perfilar cada clúster asignándole un nombre descriptivo de negocio, identificando hallazgos clave y recomendaciones estratégicas.
5. **Construir un dashboard interactivo de dos páginas en Streamlit** con 4 KPIs relevantes, 3 filtros interactivos, gráficas de dispersión, distribución y comparativas.

---

## 📊 3. Descripción del Dataset

* **Nombre:** *Movies & Entertainment Dataset (2024–2026)*.
* **Fuente:** Kaggle (Metadatos cinematográficos contemporáneos y métricas de taquilla).
* **Volumen:** 916 registros iniciales / 914 registros limpios tras depuración de duplicados.
* **Dimensionalidad:** 20 atributos (financieros, temporales, descriptivos y de recepción).

### Variables Nucleares para el Agrupamiento:
* `budget_usd`: Presupuesto de producción en dólares estadounidenses ($).
* `box_office_usd`: Recaudación bruta en taquilla a nivel mundial ($).
* `rating_out_of_10`: Calificación otorgada por la crítica y audiencia (escala 0.0 a 10.0).
* *(Adicional para pruebas)* `vote_count`: Volumen de votos de usuarios.

---

## 🔬 4. Metodología e Implementación de K-Means

### 4.1 Preparación de Datos y Escalamiento
* Se eliminaron duplicados de títulos y se imputaron valores faltantes en campos descriptivos (`director`, `screenwriter`).
* Se crearon variables derivadas: **ROI %** (*Return on Investment*), **ganancia neta** (`net_profit_usd`) y **género principal** (`primary_genre`).
* Se aplicó `StandardScaler` de Scikit-learn para estandarizar las variables a media 0 y varianza unitaria.

### 4.2 Determinación de $K$ Óptimo
Se evaluaron valores de $K \in [2, 7]$:

| Valor K | Inercia (WCSS) | Silhouette Score | Decisión |
| :---: | :---: | :---: | :--- |
| 2 | 954.39 | 0.8748 | Agrupamiento trivial (Blockbusters vs Resto) |
| 3 | 285.40 | 0.5956 | Transición incompleta; colapsa grupos críticos |
| **4 (Óptimo)** | **159.92** | **0.5368** | **Punto de inflexión del Codo y alta interpretabilidad** |
| 5 | 118.09 | 0.4871 | Disminución de silueta; sobrefragmentación |
| 6 | 96.54 | 0.4639 | Ganancia marginal decreciente |
| 7 | 79.01 | 0.4628 | Clústeres redundantes |

### 4.3 Comparación de Dos Configuraciones
* **Configuración 1 (Seleccionada - 3 Variables, K=4):** Inercia = 159.92 | Silhouette = **0.5368**.
* **Configuración 2 (Alternativa - 4 Variables con `vote_count`, K=4):** Inercia = 781.14 | Silhouette = **0.3814**.
* **Conclusión comparativa:** La Configuración 1 es claramente superior; incluir `vote_count` añade ruido por popularidad en redes sociales y reduce drásticamente la cohesión de los grupos cualitativos y financieros.

---

## 🏆 5. Segmentos Identificados (Clústeres)

| Clúster | Nombre Descriptivo | N° Películas | Presupuesto Prom. | Taquilla Prom. | Rating Prom. | ROI Prom. |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **0** | **Mega Blockbusters Taquilleros** | 20 (2.2%) | $164.9M USD | $492.6M USD | 7.61 / 10 | **198.7%** |
| **1** | **Joyas Aclamadas por la Crítica** | 301 (32.9%) | $21.3M USD | $31.1M USD | **8.69 / 10** | 58.6% |
| **2** | **Producciones Comerciales Estándar** | 287 (31.4%) | $21.2M USD | $31.3M USD | 7.60 / 10 | 60.3% |
| **3** | **Bajo Desempeño Crítico** | 306 (33.5%) | $21.6M USD | $30.7M USD | 6.50 / 10 | 51.8% |

---

## 🖥️ 6. Dashboard Interactivo (Streamlit)

El dashboard cuenta con dos páginas de análisis:

1. **Página 1: Análisis General:**
   * 4 Tarjetas de KPIs (Total de películas, Taquilla total, Presupuesto promedio, Calificación promedio).
   * Gráfica de dispersión interactiva (Presupuesto vs Taquilla por Género y Calificación).
   * Gráfica de barras horizontal con el Top de Géneros más taquilleros.
   * Histograma de distribución de calificaciones.
   * Explorador de registros filtrados.
2. **Página 2: Segmentación mediante K-Means:**
   * 4 KPIs del algoritmo (K=4, Silueta = 0.537, ROI Máximo, Algoritmo utilizado).
   * Gráfica de distribución de títulos por clúster.
   * Gráfica de dispersión interactiva de agrupamientos con Centroides.
   * Dos gráficas comparativas adicionales (Boxplots de Calificación y ROI por grupo).
   * Tabla interactiva de estadísticas descriptivas de los clústeres.
   * Fichas descriptivas de los 4 segmentos.
   * Sección formal de hallazgos y recomendaciones.

---

## 📂 7. Estructura del Repositorio

```text
TrabajoFinalBD/
│
├── data/
│   ├── raw/
│   │   └── recent_movies_2024_2026.csv          # Dataset original de Kaggle
│   └── processed/
│       └── movies_clustered_2024_2026.csv       # Dataset procesado con clústeres asignados
│
├── dashboard/
│   └── app.py                                   # Aplicación interactiva en Streamlit
│
├── docs/
│   └── documentacion_proyecto.pdf               # Documento PDF oficial (8 apartados)
│
├── figures/                                     # Gráficas generadas en alta resolución (300 DPI)
│   ├── exploratoria_1_distribucion_taquilla.png
│   ├── exploratoria_2_presupuesto_vs_taquilla.png
│   ├── exploratoria_3_calificaciones_histograma.png
│   ├── kmeans_metodo_codo_silueta.png
│   ├── kmeans_comparativa_configuraciones.png
│   ├── kmeans_clusters_dispersion.png
│   ├── kmeans_distribucion_clusters.png
│   ├── kmeans_comparativa_metricas.png
│   ├── dashboard_pagina1_analisis_general.png
│   └── dashboard_pagina2_segmentacion_kmeans.png
│
├── notebooks/
│   └── analisis_kmeans_peliculas.ipynb          # Jupyter Notebook completamente documentado
│
├── src/
│   ├── data_processing.py                       # Módulo de carga, limpieza y escalamiento
│   └── clustering.py                            # Módulo de entrenamiento, evaluación y gráficos
│
├── capture_dashboard.py                         # Script para capturas automatizadas del dashboard
├── generate_notebook.py                         # Generador del notebook
├── generate_pdf_report.py                       # Generador del PDF oficial (ReportLab)
├── requirements.txt                             # Dependencias del proyecto
└── README.md                                    # Documentación principal del repositorio
```

---

## 🚀 8. Instrucciones de Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/oskar/TrabajoFinalBD.git
cd TrabajoFinalBD
```

### 2. Crear y activar un entorno virtual (recomendado)
```bash
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el pipeline de procesamiento y clustering
```bash
python src/data_processing.py
python src/clustering.py
```

### 5. Iniciar el Dashboard Interactivo
```bash
streamlit run dashboard/app.py
```
El navegador se abrirá automáticamente en `http://localhost:8501`.

### 6. Explorar el Notebook
```bash
jupyter notebook notebooks/analisis_kmeans_peliculas.ipynb
```

---

## 💡 9. Hallazgos y Recomendaciones

* **Hallazgo 1 (Concentración Exponencial):** Solo el 2.2% de los títulos son Mega Blockbusters, pero concentran un ROI cercano al 200%, constituyendo la principal fuente de retorno masivo del mercado.
* **Hallazgo 2 (Independencia Presupuesto-Calidad):** La correlación entre presupuesto y calificación es nula (-0.002). El segmento de *Joyas Críticas* logra una calificación media de 8.69 con un presupuesto contenido ($21.3M USD).
* **Hallazgo 3 (Zona de Riesgo):** Un tercio de las producciones cae en *Bajo Desempeño Crítico*, consumiendo el mismo presupuesto que filmes exitosos pero con un retorno deficiente (51.8%).

### Recomendaciones:
1. **Estrategia Bi-Modal:** Financiar franquicias selectas de alto presupuesto respaldadas por marcas globales, combinadas con un portafolio de costo moderado enfocado en guiones de autor.
2. **Control de Calidad Temprano:** Implementar filtros de preproducción rigurosos para proyectos en el rango de $20M a $25M USD.
3. **Distribución Segmentada:** Priorizar festivales y streaming exclusivo para títulos con alta aclamación crítica.

---

## 👥 Autores y Créditos
* **Proyecto:** Minería de Datos y Segmentación K-Means.
* **Dataset:** Movies & Entertainment Dataset (2024–2026), Kaggle.
* **Licencia:** MIT.
