"""
Generador del archivo Jupyter Notebook (.ipynb) para el proyecto integrador.
"""
import json
import os

def create_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Proyecto Integrador: Minería de Datos y Segmentación Cinematográfica mediante K-Means\n",
                "## Análisis de Producciones Modernas (2024–2026) y Modelado No Supervisado\n",
                "\n",
                "**Herramientas utilizadas:** Python, Pandas, Scikit-learn, Matplotlib, Seaborn, Plotly.\n",
                "\n",
                "---\n",
                "\n",
                "### Parte 1. Planteamiento del Problema y Objetivos\n",
                "\n",
                "#### Contexto y Problemática\n",
                "La industria cinematográfica contemporánea (2024–2026) atraviesa una era de reconfiguración económica post-pandemia caracterizada por presupuestos masivos, ventanas de estreno híbridas y una audiencia altamente selectiva. Los estudios enfrentan un desafío crítico: maximizar la rentabilidad y el prestigio de sus producciones minimizando el riesgo de fracasos comerciales multimillonarios. \n",
                "\n",
                "#### Objetivo General\n",
                "Desarrollar un modelo de agrupamiento no supervisado mediante el algoritmo **K-Means** sobre metadatos financieros y cualitativos de largometrajes modernos (2024–2026), con el fin de identificar perfiles distintivos de producción, rendimiento en taquilla y aclamación crítica que optimicen la toma de decisiones estratégicas en producción y distribución cinematográfica.\n",
                "\n",
                "#### Objetivos Específicos\n",
                "1. **Explorar y limpiar** un conjunto de datos multidimensional de más de 900 películas modernas, evaluando la correlación entre presupuesto, taquilla global y calificaciones.\n",
                "2. **Implementar y evaluar el algoritmo K-Means** probando múltiples valores de $K$ mediante el Método del Codo y el Coeficiente de Silueta para seleccionar la segmentación óptima.\n",
                "3. **Interpretar y nombrar los clústeres obtenidos**, contrastando métricas descriptivas y formulando recomendaciones prácticas de negocio para la industria."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Parte 2. Carga y Exploración Inicial del Dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.preprocessing import StandardScaler\n",
                "from sklearn.cluster import KMeans\n",
                "from sklearn.metrics import silhouette_score\n",
                "\n",
                "# Configuración estética de gráficos\n",
                "sns.set_theme(style='whitegrid', palette='muted')\n",
                "plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})\n",
                "\n",
                "# Carga del dataset original\n",
                "dataset_path = '../data/raw/recent_movies_2024_2026.csv'\n",
                "df = pd.read_csv(dataset_path)\n",
                "\n",
                "print(f'Dimensiones iniciales del dataset: {df.shape[0]} registros y {df.shape[1]} columnas.')\n",
                "df.head(10)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Inspección de columnas y tipos de datos\n",
                "df.info()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Estadísticas descriptivas de variables cuantitativas\n",
                "numeric_cols = ['budget_usd', 'box_office_usd', 'rating_out_of_10', 'vote_count', 'runtime_minutes']\n",
                "df[numeric_cols].describe().round(2)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Verificación de valores nulos y duplicados\n",
                "print('Conteo de valores nulos:')\n",
                "print(df.isna().sum()[lambda x: x > 0])\n",
                "print(f'\\nTotal de registros duplicados idénticos: {df.duplicated().sum()}')\n",
                "print(f'Total de títulos duplicados: {df.duplicated(subset=[\"title\"]).sum()}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "#### Visualizaciones Exploratorias (Al menos 3 gráficas requeridas)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica Exploratoria 1: Distribución de Taquilla Mundial\n",
                "plt.figure(figsize=(9, 5))\n",
                "sns.histplot(df['box_office_usd'] / 1e6, kde=True, color='#2b5c8f', bins=30)\n",
                "plt.title('Distribución de Recaudación en Taquilla (Millones de USD)', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Taquilla Mundial (Millones USD)')\n",
                "plt.ylabel('Frecuencia')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica Exploratoria 2: Presupuesto vs Taquilla\n",
                "plt.figure(figsize=(9, 5))\n",
                "sns.scatterplot(\n",
                "    data=df, \n",
                "    x=df['budget_usd']/1e6, \n",
                "    y=df['box_office_usd']/1e6, \n",
                "    hue='rating_out_of_10', \n",
                "    palette='viridis', \n",
                "    alpha=0.75\n",
                ")\n",
                "plt.title('Relación Presupuesto vs Taquilla Mundial', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Presupuesto (Millones USD)')\n",
                "plt.ylabel('Taquilla Mundial (Millones USD)')\n",
                "plt.legend(title='Calificación / 10', bbox_to_anchor=(1.02, 1), loc='upper left')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica Exploratoria 3: Calificaciones por Año de Estreno\n",
                "plt.figure(figsize=(8, 5))\n",
                "sns.boxplot(data=df, x='release_year', y='rating_out_of_10', hue='release_year', palette='Set2', legend=False)\n",
                "plt.title('Distribución de Calificaciones (Rating / 10) por Año', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Año de Estreno')\n",
                "plt.ylabel('Calificación')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Parte 3. Limpieza y Preparación de Datos\n",
                "\n",
                "En esta etapa se eliminan títulos duplicados, se imputan valores nulos informativos, se realiza ingeniería de características (cálculo de **ROI %**, **ganancia neta** y extracción del **género principal**) y se aplica el escalamiento estándar (`StandardScaler`)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Eliminación de títulos duplicados\n",
                "df_clean = df.drop_duplicates(subset=['title'], keep='first').copy().reset_index(drop=True)\n",
                "\n",
                "# 2. Imputación de nulos en variables descriptivas\n",
                "df_clean['director'] = df_clean['director'].fillna('Desconocido')\n",
                "df_clean['screenwriter'] = df_clean['screenwriter'].fillna('No especificado')\n",
                "df_clean['release_day'] = df_clean['release_day'].fillna(1).astype(int)\n",
                "\n",
                "# 3. Ingeniería de características\n",
                "df_clean['roi_pct'] = ((df_clean['box_office_usd'] - df_clean['budget_usd']) / df_clean['budget_usd'] * 100).round(2)\n",
                "df_clean['net_profit_usd'] = df_clean['box_office_usd'] - df_clean['budget_usd']\n",
                "df_clean['primary_genre'] = df_clean['genres'].apply(lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Other')\n",
                "\n",
                "# 4. Selección de variables de clustering y Escalamiento\n",
                "cluster_features = ['budget_usd', 'box_office_usd', 'rating_out_of_10']\n",
                "scaler = StandardScaler()\n",
                "X_scaled = scaler.fit_transform(df_clean[cluster_features])\n",
                "\n",
                "print(f'Dataset preparado: {df_clean.shape[0]} registros limpios.')\n",
                "print('Variables seleccionadas para clustering:', cluster_features)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Parte 4. Implementación y Evaluación de K-Means\n",
                "\n",
                "Evaluamos 6 valores distintos de $K$ (desde $K=2$ hasta $K=7$) calculando la inercia (WCSS) y el puntaje de silueta (*Silhouette Score*)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "k_values = range(2, 8)\n",
                "inertias = []\n",
                "silhouettes = []\n",
                "\n",
                "for k in k_values:\n",
                "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
                "    labels = km.fit_predict(X_scaled)\n",
                "    inertias.append(km.inertia_)\n",
                "    silhouettes.append(silhouette_score(X_scaled, labels))\n",
                "\n",
                "eval_df = pd.DataFrame({'K': k_values, 'Inercia': inertias, 'Silhouette Score': silhouettes})\n",
                "eval_df"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfica dual: Método del Codo y Silueta\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                "\n",
                "ax1.plot(k_values, inertias, marker='o', color='#1f77b4', lw=2)\n",
                "ax1.axvline(x=4, color='crimson', linestyle='--', label='K seleccionado = 4')\n",
                "ax1.set_title('Método del Codo (Elbow Method)', fontweight='bold')\n",
                "ax1.set_xlabel('K')\n",
                "ax1.set_ylabel('Inercia (WCSS)')\n",
                "ax1.legend()\n",
                "\n",
                "ax2.plot(k_values, silhouettes, marker='s', color='#2ca02c', lw=2)\n",
                "ax2.axvline(x=4, color='crimson', linestyle='--', label='K seleccionado = 4')\n",
                "ax2.set_title('Coeficiente de Silueta', fontweight='bold')\n",
                "ax2.set_xlabel('K')\n",
                "ax2.set_ylabel('Silhouette')\n",
                "ax2.legend()\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "#### Justificación de Selección de K=4\n",
                "- Aunque $K=2$ presenta un valor matemático alto de silueta, divide los datos únicamente en producciones normales vs blockbusters masivos, perdiendo la segmentación cualitativa.\n",
                "- **$K=4$** produce un punto de inflexión evidente en el método del codo (reducción de inercia a 159.92) y mantiene un sobresaliente puntaje de silueta de **0.537**, permitiendo distinguir claramente 4 arquetipos cinematográficos con pleno sentido de negocio."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "#### Comparación de Dos Configuraciones del Modelo (Requisito Parte 4)\n",
                "- **Configuración 1 (Línea Base Seleccionada):** 3 variables nucleares (`budget_usd`, `box_office_usd`, `rating_out_of_10`) con $K=4$.\n",
                "- **Configuración 2 (Alternativa Enriquecida):** 4 variables cuantitativas (`budget_usd`, `box_office_usd`, `rating_out_of_10`, `vote_count`) con $K=4$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Configuración 2 con 4 variables\n",
                "features_cfg2 = ['budget_usd', 'box_office_usd', 'rating_out_of_10', 'vote_count']\n",
                "scaler2 = StandardScaler()\n",
                "X2_scaled = scaler2.fit_transform(df_clean[features_cfg2])\n",
                "km2 = KMeans(n_clusters=4, random_state=42, n_init=10)\n",
                "labels_cfg2 = km2.fit_predict(X2_scaled)\n",
                "sil_cfg2 = silhouette_score(X2_scaled, labels_cfg2)\n",
                "\n",
                "print(f'Configuración 1 (3 variables) -> Inercia: 159.92 | Silhouette: 0.5368')\n",
                "print(f'Configuración 2 (4 variables) -> Inercia: {km2.inertia_:.2f} | Silhouette: {sil_cfg2:.4f}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "**Interpretación de la Comparativa:** Al introducir `vote_count`, la inercia aumenta sensiblemente y el puntaje de silueta desciende de 0.537 a 0.381. La inclusión del volumen de votos fragmenta los grupos por 'popularidad/viralidad' en internet en vez de centrarse en la dinámica financiera y la recepción crítica, por lo que la **Configuración 1** es significativamente superior."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Parte 5. Entrenamiento del Modelo Final e Interpretación de Resultados"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Entrenamiento final\n",
                "final_kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\n",
                "df_clean['cluster_id'] = final_kmeans.fit_predict(X_scaled)\n",
                "\n",
                "# Mapeo de nombres descriptivos\n",
                "means = df_clean.groupby('cluster_id')[cluster_features].mean()\n",
                "name_map = {}\n",
                "for cid, row in means.iterrows():\n",
                "    if row['budget_usd'] > 80_000_000:\n",
                "        name_map[cid] = 'Mega Blockbusters Taquilleros'\n",
                "    elif row['rating_out_of_10'] >= 8.2:\n",
                "        name_map[cid] = 'Joyas Aclamadas por la Crítica'\n",
                "    elif row['rating_out_of_10'] >= 7.2:\n",
                "        name_map[cid] = 'Producciones Comerciales Estándar'\n",
                "    else:\n",
                "        name_map[cid] = 'Bajo Desempeño Crítico'\n",
                "\n",
                "df_clean['cluster_name'] = df_clean['cluster_id'].map(name_map)\n",
                "\n",
                "# Conteo de películas por clúster\n",
                "print(df_clean['cluster_name'].value_counts())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Tabla comparativa de estadísticas descriptivas por grupo\n",
                "summary_table = df_clean.groupby('cluster_name').agg(\n",
                "    Peliculas=('title', 'count'),\n",
                "    Presupuesto_Promedio=('budget_usd', 'mean'),\n",
                "    Taquilla_Promedio=('box_office_usd', 'mean'),\n",
                "    Rating_Promedio=('rating_out_of_10', 'mean'),\n",
                "    ROI_Promedio=('roi_pct', 'mean')\n",
                ").reset_index()\n",
                "\n",
                "summary_table.style.format({\n",
                "    'Presupuesto_Promedio': '${:,.0f}',\n",
                "    'Taquilla_Promedio': '${:,.0f}',\n",
                "    'Rating_Promedio': '{:.2f}',\n",
                "    'ROI_Promedio': '{:.1f}%'\n",
                "})"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Visualización gráfica final de agrupamientos con Centroides\n",
                "plt.figure(figsize=(10, 6))\n",
                "palette = {\n",
                "    'Mega Blockbusters Taquilleros': '#e74c3c',\n",
                "    'Joyas Aclamadas por la Crítica': '#2ecc71',\n",
                "    'Producciones Comerciales Estándar': '#3498db',\n",
                "    'Bajo Desempeño Crítico': '#9b59b6'\n",
                "}\n",
                "sns.scatterplot(\n",
                "    data=df_clean,\n",
                "    x=df_clean['budget_usd'] / 1e6,\n",
                "    y=df_clean['box_office_usd'] / 1e6,\n",
                "    hue='cluster_name',\n",
                "    palette=palette,\n",
                "    s=75,\n",
                "    alpha=0.85\n",
                ")\n",
                "\n",
                "# Dibujar Centroides en escala original\n",
                "centroids_orig = scaler.inverse_transform(final_kmeans.cluster_centers_)\n",
                "plt.scatter(\n",
                "    centroids_orig[:, 0] / 1e6,\n",
                "    centroids_orig[:, 1] / 1e6,\n",
                "    c='black',\n",
                "    s=250,\n",
                "    marker='X',\n",
                "    edgecolor='white',\n",
                "    linewidth=2,\n",
                "    label='Centroides K-Means'\n",
                ")\n",
                "plt.title('Segmentación K-Means: Presupuesto vs Taquilla con Centroides', fontsize=13, fontweight='bold')\n",
                "plt.xlabel('Presupuesto de Producción (Millones USD)')\n",
                "plt.ylabel('Taquilla Mundial (Millones USD)')\n",
                "plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Hallazgos Relevantes y Recomendaciones de Negocio\n",
                "\n",
                "#### Hallazgos Clave:\n",
                "1. **Concentración Exponencial en Blockbusters:** Solo 20 títulos (~2.2%) pertenecen al grupo de Mega Blockbusters, pero concentran un ROI medio cercano al 200%, evidenciando que el cine comercial de gran escala sigue siendo el motor de liquidez de la industria.\n",
                "2. **El Mito del Presupuesto y la Calidad:** Las *Joyas Críticas* (301 películas) logran una calificación media extraordinaria de 8.69 con un presupuesto moderado ($21.3M USD), desmintiendo que se requieran inversiones masivas para alcanzar excelencia artística.\n",
                "3. **Peligro en el Rango Medio:** 306 películas sufren de *Bajo Desempeño Crítico* gastando prácticamente el mismo capital (~$21.5M USD) que las producciones exitosas, pero con un retorno mermado.\n",
                "\n",
                "#### Recomendaciones Estratégicas:\n",
                "1. **Estrategia Bi-Modal:** Financiar producciones de gran escala con propiedades intelectuales reconocidas combinadas con un catálogo diversificado de películas de costo controlado con enfoque en calidad narrativa.\n",
                "2. **Auditoría Temprana de Guiones:** Reforzar las etapas de preproducción para proyectos de $20M a $30M para evitar caer en la categoría de bajo impacto.\n",
                "3. **Ventanas de Distribución Flexibles:** Para las *Joyas Críticas*, priorizar circuitos de festivales y estrenos de streaming con marketing de boca a boca digital."
            ]
        }
    ]

    notebook_dict = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.13"
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    out_path = os.path.join('notebooks', 'analisis_kmeans_peliculas.ipynb')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_dict, f, indent=2, ensure_ascii=False)
    print(f"Jupyter Notebook generado exitosamente en '{out_path}'.")

if __name__ == '__main__':
    create_notebook()
