"""
data_processing.py
Módulo de carga, exploración, limpieza y preparación de datos
para el proyecto integrador de segmentación cinematográfica (2024-2026).
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_dataset(filepath: str) -> pd.DataFrame:
    """Importa el dataset original utilizando read_csv."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo en {filepath}")
    df = pd.read_csv(filepath)
    return df


def explore_dataset(df: pd.DataFrame) -> dict:
    """
    Obtiene dimensiones, tipos de datos, valores nulos,
    duplicados y estadísticas descriptivas.
    """
    summary = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isna().sum().to_dict(),
        "total_duplicates": int(df.duplicated().sum()),
        "duplicate_titles": int(df.duplicated(subset=['title']).sum()),
        "descriptive_stats": df.describe().round(2)
    }
    return summary


def clean_and_prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Realiza limpieza de inconsistencias, tratamiento de nulos,
    ingeniería de características y escalamiento numérico.
    
    Retorna:
    - df_clean: DataFrame limpio con nuevas características (ROI, primary_genre).
    - df_scaled: DataFrame con las variables numéricas escaladas con StandardScaler.
    - scaler: Objeto StandardScaler ajustado.
    """
    df_clean = df.copy()

    # 1. Tratamiento de duplicados en títulos
    if df_clean.duplicated(subset=['title']).sum() > 0:
        df_clean = df_clean.drop_duplicates(subset=['title'], keep='first').reset_index(drop=True)

    # 2. Imputación controlada de valores nulos en columnas descriptivas
    df_clean['director'] = df_clean['director'].fillna('Desconocido')
    df_clean['screenwriter'] = df_clean['screenwriter'].fillna('No especificado')
    df_clean['release_day'] = df_clean['release_day'].fillna(1).astype(int)

    # 3. Ingeniería de características (Feature Engineering)
    # ROI: Retorno de inversión en porcentaje
    df_clean['roi_pct'] = ((df_clean['box_office_usd'] - df_clean['budget_usd']) / df_clean['budget_usd'] * 100).round(2)
    # Ganancia bruta en USD
    df_clean['net_profit_usd'] = df_clean['box_office_usd'] - df_clean['budget_usd']
    # Primer género (para filtrados y agregaciones)
    df_clean['primary_genre'] = df_clean['genres'].apply(lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Other')

    # 4. Selección de variables cuantitativas para el clustering
    # Variables principales: budget_usd, box_office_usd, rating_out_of_10, vote_count
    cluster_features = ['budget_usd', 'box_office_usd', 'rating_out_of_10', 'vote_count']
    
    # 5. Escalamiento con StandardScaler
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(df_clean[cluster_features])
    df_scaled = pd.DataFrame(
        scaled_values, 
        columns=[f"{col}_scaled" for col in cluster_features]
    )

    return df_clean, df_scaled, scaler


if __name__ == '__main__':
    raw_path = os.path.join('data', 'raw', 'recent_movies_2024_2026.csv')
    df = load_dataset(raw_path)
    info = explore_dataset(df)
    print("=== EXPLORACIÓN INICIAL ===")
    print(f"Dimensiones: {info['shape']}")
    print(f"Duplicados totales: {info['total_duplicates']}")
    print(f"Duplicados por título: {info['duplicate_titles']}")
    print(f"Nulos por columna:\n{pd.Series(info['null_counts'])[lambda x: x > 0]}")

    df_clean, df_scaled, scaler = clean_and_prepare_data(df)
    print("\n=== LIMPIEZA Y PREPARACIÓN COMPLETADA ===")
    print(f"Dimensiones tras limpieza: {df_clean.shape}")
    print(f"Variables escaladas: {list(df_scaled.columns)}")
