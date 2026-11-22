"""
clustering.py
Módulo de entrenamiento, evaluación, comparación de configuraciones y generación
de gráficos para K-Means en el dataset de películas 2024-2026.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from data_processing import load_dataset, clean_and_prepare_data

# Configuración visual para matplotlib y seaborn
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})


def generate_exploratory_plots(df: pd.DataFrame, output_dir: str = 'figures'):
    """Genera al menos tres gráficas exploratorias requeridas por la Parte 2."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Distribución de Taquilla Mundial (Box Office)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['box_office_usd'] / 1e6, kde=True, color='#2b5c8f', ax=ax, bins=30)
    ax.set_title('Distribución de Recaudación Mundial en Taquilla (2024-2026)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Recaudación Mundial (Millones de USD)', fontsize=11)
    ax.set_ylabel('Frecuencia (Películas)', fontsize=11)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'exploratoria_1_distribucion_taquilla.png'), dpi=300)
    plt.close()

    # 2. Relación Presupuesto vs Taquilla (Scatter Plot)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df, 
        x=df['budget_usd'] / 1e6, 
        y=df['box_office_usd'] / 1e6, 
        hue='rating_out_of_10', 
        palette='viridis', 
        size='vote_count',
        sizes=(30, 200),
        alpha=0.7, 
        ax=ax
    )
    ax.set_title('Relación entre Presupuesto de Producción y Taquilla Mundial', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Presupuesto (Millones de USD)', fontsize=11)
    ax.set_ylabel('Taquilla Mundial (Millones de USD)', fontsize=11)
    ax.legend(title='Calificación / Votos', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'exploratoria_2_presupuesto_vs_taquilla.png'), dpi=300)
    plt.close()

    # 3. Distribución de Calificaciones de la Audiencia / Crítica
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x='release_year', y='rating_out_of_10', palette='Set2', ax=ax)
    ax.set_title('Distribución de Calificaciones (Rating / 10) por Año de Estreno', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Año de Estreno', fontsize=11)
    ax.set_ylabel('Calificación (0 - 10)', fontsize=11)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'exploratoria_3_calificaciones_histograma.png'), dpi=300)
    plt.close()
    print("Gráficas exploratorias generadas exitosamente en 'figures/'.")


def evaluate_k_values(X_scaled: np.ndarray, k_range=range(2, 8)) -> pd.DataFrame:
    """Evalúa múltiples valores de K calculando Inercia y Silhouette Score."""
    metrics = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        inertia = kmeans.inertia_
        sil = silhouette_score(X_scaled, labels)
        metrics.append({"K": k, "Inertia": inertia, "Silhouette": sil})
    return pd.DataFrame(metrics)


def plot_elbow_and_silhouette(metrics_df: pd.DataFrame, output_dir: str = 'figures'):
    """Genera la gráfica dual del Método del Codo y Coeficiente de Silueta."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Inercia (Método del Codo)
    ax1.plot(metrics_df['K'], metrics_df['Inertia'], marker='o', color='#1f77b4', linewidth=2, markersize=8)
    ax1.axvline(x=4, color='crimson', linestyle='--', label='K seleccionado = 4')
    ax1.set_title('Método del Codo (Elbow Method)', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Número de Clústeres (K)', fontsize=11)
    ax1.set_ylabel('Inercia (WCSS)', fontsize=11)
    ax1.legend()

    # Silhouette Score
    ax2.plot(metrics_df['K'], metrics_df['Silhouette'], marker='s', color='#2ca02c', linewidth=2, markersize=8)
    ax2.axvline(x=4, color='crimson', linestyle='--', label='K seleccionado = 4')
    ax2.set_title('Coeficiente de Silueta por Valor de K', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Número de Clústeres (K)', fontsize=11)
    ax2.set_ylabel('Puntaje de Silueta', fontsize=11)
    ax2.legend()

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'kmeans_metodo_codo_silueta.png'), dpi=300)
    plt.close()
    print("Gráfica de Codo y Silueta guardada en 'figures/kmeans_metodo_codo_silueta.png'.")


def compare_model_configurations(df_clean: pd.DataFrame, output_dir: str = 'figures') -> dict:
    """
    Compara dos configuraciones del modelo K-Means:
    - Configuración 1 (Óptima): 3 variables clave (Presupuesto, Taquilla, Calificación) con K=4.
    - Configuración 2 (Alternativa): 4 variables (Presupuesto, Taquilla, Calificación, Votos) con K=4.
    """
    # Configuración 1
    features_cfg1 = ['budget_usd', 'box_office_usd', 'rating_out_of_10']
    scaler1 = StandardScaler()
    X1_scaled = scaler1.fit_transform(df_clean[features_cfg1])
    km1 = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels1 = km1.fit_predict(X1_scaled)
    sil1 = silhouette_score(X1_scaled, labels1)

    # Configuración 2
    features_cfg2 = ['budget_usd', 'box_office_usd', 'rating_out_of_10', 'vote_count']
    scaler2 = StandardScaler()
    X2_scaled = scaler2.fit_transform(df_clean[features_cfg2])
    km2 = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels2 = km2.fit_predict(X2_scaled)
    sil2 = silhouette_score(X2_scaled, labels2)

    # Gráfica comparativa
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    scatter1 = ax1.scatter(
        df_clean['budget_usd'] / 1e6, 
        df_clean['box_office_usd'] / 1e6, 
        c=labels1, 
        cmap='tab10', 
        alpha=0.75, 
        edgecolors='none'
    )
    ax1.set_title(f'Configuración 1: 3 Variables (K=4)\nSilhouette Score: {sil1:.4f}', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Presupuesto (Millones USD)', fontsize=10)
    ax1.set_ylabel('Taquilla (Millones USD)', fontsize=10)

    scatter2 = ax2.scatter(
        df_clean['budget_usd'] / 1e6, 
        df_clean['box_office_usd'] / 1e6, 
        c=labels2, 
        cmap='Set1', 
        alpha=0.75, 
        edgecolors='none'
    )
    ax2.set_title(f'Configuración 2: 4 Variables (+Vote Count, K=4)\nSilhouette Score: {sil2:.4f}', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Presupuesto (Millones USD)', fontsize=10)
    ax2.set_ylabel('Taquilla (Millones USD)', fontsize=10)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'kmeans_comparativa_configuraciones.png'), dpi=300)
    plt.close()

    return {
        "cfg1": {"features": features_cfg1, "K": 4, "inertia": km1.inertia_, "silhouette": sil1},
        "cfg2": {"features": features_cfg2, "K": 4, "inertia": km2.inertia_, "silhouette": sil2}
    }


def train_and_label_final_model(df_clean: pd.DataFrame, output_dir: str = 'figures') -> pd.DataFrame:
    """
    Entrena el modelo final con K=4 y las 3 variables nucleares,
    asigna etiquetas descriptivas a cada clúster y exporta gráficos descriptivos.
    """
    features = ['budget_usd', 'box_office_usd', 'rating_out_of_10']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[features])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    df_result = df_clean.copy()
    df_result['cluster_id'] = cluster_labels

    # Asignación de nombres descriptivos basados en el perfil de centroides
    cluster_means = df_result.groupby('cluster_id')[features].mean()
    
    # Mapeo descriptivo según métricas reales observadas:
    # Cluster con presupuesto masivo (> 100M) -> Mega Blockbusters
    # Cluster con rating alto (> 8.2) -> Joyas Aclamadas de Presupuesto Moderado
    # Cluster con rating medio (7.2 - 8.0) -> Producciones Comerciales Estándar
    # Cluster con rating bajo (< 7.0) -> Producciones de Bajo Desempeño Crítico
    name_map = {}
    for cid, row in cluster_means.iterrows():
        if row['budget_usd'] > 80_000_000:
            name_map[cid] = 'Mega Blockbusters Taquilleros'
        elif row['rating_out_of_10'] >= 8.2:
            name_map[cid] = 'Joyas Aclamadas por la Crítica'
        elif row['rating_out_of_10'] >= 7.2:
            name_map[cid] = 'Producciones Comerciales Estándar'
        else:
            name_map[cid] = 'Bajo Desempeño Crítico'

    df_result['cluster_name'] = df_result['cluster_id'].map(name_map)

    # Gráfica 1: Dispersión Presupuesto vs Taquilla coloreado por Clúster
    fig, ax = plt.subplots(figsize=(10, 6))
    palette = {'Mega Blockbusters Taquilleros': '#e74c3c',
               'Joyas Aclamadas por la Crítica': '#2ecc71',
               'Producciones Comerciales Estándar': '#3498db',
               'Bajo Desempeño Crítico': '#9b59b6'}
    sns.scatterplot(
        data=df_result,
        x=df_result['budget_usd'] / 1e6,
        y=df_result['box_office_usd'] / 1e6,
        hue='cluster_name',
        palette=palette,
        style='cluster_name',
        s=80,
        alpha=0.85,
        ax=ax
    )
    # Centroides en escala original
    centroids_orig = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(
        centroids_orig[:, 0] / 1e6,
        centroids_orig[:, 1] / 1e6,
        c='black',
        s=250,
        marker='X',
        edgecolor='white',
        linewidth=2,
        label='Centroides (KMeans)'
    )
    ax.set_title('Segmentación K-Means: Presupuesto vs Taquilla Mundial (K=4)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Presupuesto de Producción (Millones USD)', fontsize=11)
    ax.set_ylabel('Taquilla Mundial (Millones USD)', fontsize=11)
    ax.legend(title='Segmento Fílmico', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'kmeans_clusters_dispersion.png'), dpi=300)
    plt.close()

    # Gráfica 2: Distribución de Películas por Clúster
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df_result['cluster_name'].value_counts()
    sns.barplot(x=counts.values, y=counts.index, palette=palette, ax=ax)
    for i, v in enumerate(counts.values):
        ax.text(v + 5, i, f"{v} ({v/len(df_result)*100:.1f}%)", va='center', fontweight='bold', fontsize=10)
    ax.set_title('Distribución de Películas por Segmento Identificado', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Cantidad de Películas', fontsize=11)
    ax.set_xlim(0, counts.values.max() * 1.18)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'kmeans_distribucion_clusters.png'), dpi=300)
    plt.close()

    # Gráfica 3: Comparativa de Métricas Promedio por Clúster (Boxplots de Rating y ROI)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=df_result, x='cluster_name', y='rating_out_of_10', palette=palette, ax=ax1)
    ax1.set_title('Comparativa de Calificación por Clúster', fontsize=12, fontweight='bold')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=25, ha='right')
    ax1.set_xlabel('')
    ax1.set_ylabel('Calificación (0 a 10)')

    sns.boxplot(data=df_result, x='cluster_name', y='roi_pct', palette=palette, ax=ax2)
    ax2.set_title('Comparativa de Retorno de Inversión (ROI %) por Clúster', fontsize=12, fontweight='bold')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=25, ha='right')
    ax2.set_xlabel('')
    ax2.set_ylabel('ROI Estimado (%)')
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, 'kmeans_comparativa_metricas.png'), dpi=300)
    plt.close()

    # Guardar dataset procesado con clústeres asignados
    output_csv = os.path.join('data', 'processed', 'movies_clustered_2024_2026.csv')
    df_result.to_csv(output_csv, index=False)
    print(f"Dataset procesado y etiquetado guardado en '{output_csv}'.")

    return df_result


if __name__ == '__main__':
    raw_csv = os.path.join('data', 'raw', 'recent_movies_2024_2026.csv')
    df = load_dataset(raw_csv)
    df_clean, df_scaled, scaler = clean_and_prepare_data(df)

    print("--- 1. Generando Gráficas Exploratorias ---")
    generate_exploratory_plots(df_clean)

    print("--- 2. Evaluando Valores de K ---")
    features_core = ['budget_usd', 'box_office_usd', 'rating_out_of_10']
    scaler_core = StandardScaler()
    X_core_scaled = scaler_core.fit_transform(df_clean[features_core])
    metrics_df = evaluate_k_values(X_core_scaled)
    print(metrics_df.to_string(index=False))
    plot_elbow_and_silhouette(metrics_df)

    print("--- 3. Comparando Configuraciones del Modelo ---")
    cmp_results = compare_model_configurations(df_clean)
    print(f"Configuración 1 (3 variables, K=4): Inercia={cmp_results['cfg1']['inertia']:.2f}, Silhouette={cmp_results['cfg1']['silhouette']:.4f}")
    print(f"Configuración 2 (4 variables, K=4): Inercia={cmp_results['cfg2']['inertia']:.2f}, Silhouette={cmp_results['cfg2']['silhouette']:.4f}")

    print("--- 4. Entrenando Modelo Final y Exportando Resultados ---")
    df_final = train_and_label_final_model(df_clean)
    print("Resumen por clúster:")
    print(df_final.groupby('cluster_name')[['budget_usd', 'box_office_usd', 'rating_out_of_10', 'roi_pct']].agg(['count', 'mean']).round(2))
