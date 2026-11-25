"""
app.py
CineMetrics Intelligence Suite | Segmentación K-Means (2024–2026)
Diseñado con dirección de arte cinematográfica, micro-interacciones UX y visualizaciones de alta fidelidad.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y METADATOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CineMetrics Intelligence | K-Means Analytics",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. SISTEMA DE DISEÑO (IMPECCABLE & UX-MOTION)
# -----------------------------------------------------------------------------
# Tipografía de alta fidelidad: Plus Jakarta Sans + Space Grotesk + JetBrains Mono
# Materialidad oscura cinematográfica: Obsidian (#0B0F17) + Slate Glass + Glows sutiles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --bg-base: #090D16;
        --bg-surface: #111726;
        --bg-surface-elevated: #161F33;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-highlight: rgba(255, 255, 255, 0.16);
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-crimson: #FF4D6D;
        --accent-emerald: #10B981;
        --accent-sky: #38BDF8;
        --accent-violet: #A78BFA;
        --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Reset global y tipografía */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-base);
        color: var(--text-primary);
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }

    /* Superficie principal de Streamlit */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #151D30 0%, #090D16 70%);
    }

    /* Selección de texto temática */
    ::selection {
        background: rgba(56, 189, 248, 0.25);
        color: #FFFFFF;
    }

    /* Barra de desplazamiento refinada */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-base);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.25);
    }

    /* Animaciones UX Motion (Principios 3, 5 y 8) */
    @keyframes heroEntrance {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes cardStagger {
        from {
            opacity: 0;
            transform: translateY(12px) scale(0.99);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Títulos editoriales */
    .editorial-header {
        animation: heroEntrance 400ms var(--ease-out) forwards;
        margin-bottom: 2rem;
    }
    .editorial-tag {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--accent-sky);
        display: inline-block;
        padding: 4px 10px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 6px;
        margin-bottom: 0.75rem;
    }
    .editorial-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #FFFFFF;
        line-height: 1.15;
        margin: 0 0 0.5rem 0;
    }
    .editorial-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        max-width: 800px;
        line-height: 1.5;
        margin: 0;
    }

    /* Tarjetas KPI de precisión (Sin templates genéricos de IA) */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        position: relative;
        overflow: hidden;
        transition: transform 200ms var(--ease-out), border-color 200ms var(--ease-out), box-shadow 200ms var(--ease-out);
        animation: cardStagger 350ms var(--ease-out) forwards;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: var(--border-highlight);
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.5);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        font-variant-numeric: tabular-nums;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.75rem;
        color: var(--accent-sky);
        margin-top: 0.4rem;
        font-weight: 500;
    }

    /* Tarjetas de Clúster (Diseño Editorial Cinematográfico) */
    .archetype-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.25rem;
        margin-top: 1rem;
    }
    .archetype-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.5rem;
        position: relative;
        transition: all 250ms var(--ease-out);
    }
    .archetype-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.22);
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6);
    }
    .archetype-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .archetype-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }
    .archetype-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    .archetype-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        padding: 0.85rem;
        background: rgba(0, 0, 0, 0.25);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    .metric-item-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-item-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.92rem;
        font-weight: 600;
        color: #F8FAFC;
        font-variant-numeric: tabular-nums;
        margin-top: 2px;
    }

    /* Sidebar Tematizado */
    [data-testid="stSidebar"] {
        background-color: #070A12 !important;
        border-right: 1px solid var(--border-subtle);
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
    }

    /* Respeto a accesibilidad y movimiento reducido */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. CARGA DE DATOS Y DEFINICIÓN DE PALETA CROMÁTICA
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Carga y valida el dataset de películas agrupadas."""
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'movies_clustered_2024_2026.csv')
    if not os.path.exists(filepath):
        filepath = os.path.join('data', 'processed', 'movies_clustered_2024_2026.csv')
    return pd.read_csv(filepath)


df_data = load_data()

# Paleta cromática coordinada (Estándar de Contraste WCAG 2.2 AA)
CLUSTER_PALETTE = {
    'Mega Blockbusters Taquilleros': '#FF4D6D',       # Coral Neón
    'Joyas Aclamadas por la Crítica': '#10B981',      # Esmeralda Intenso
    'Producciones Comerciales Estándar': '#38BDF8',  # Cian Cielo
    'Bajo Desempeño Crítico': '#A78BFA'              # Lavanda Editorial
}

# Template de diseño para gráficos Plotly sincronizado con el tema
PLOTLY_THEME = {
    'layout': go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(17, 23, 38, 0.45)',
        font=dict(family='Plus Jakarta Sans, sans-serif', color='#94A3B8', size=11),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.12)',
            tickfont=dict(size=10, family='JetBrains Mono, monospace')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.12)',
            tickfont=dict(size=10, family='JetBrains Mono, monospace')
        ),
        margin=dict(l=45, r=25, t=40, b=45)
    )
}


# -----------------------------------------------------------------------------
# 4. BARRA LATERAL (FILTROS Y CONTROL DE NAVEGACIÓN)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 0.5rem 0 1rem 0;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em;">
                CINEMETRICS 360
            </div>
            <div style="font-size: 0.75rem; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase;">
                Intelligence & Clustering Suite
            </div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        label="Navegación del Proyecto",
        options=["Página 1: Análisis General", "Página 2: Segmentación K-Means"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 1.2rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.08em; margin-bottom: 0.8rem;'>Filtros de Exploración</div>", unsafe_allow_html=True)

    # Filtro 1: Año
    available_years = sorted(df_data['release_year'].unique())
    selected_years = st.multiselect(
        "Año de Estreno",
        options=available_years,
        default=available_years
    )

    # Filtro 2: Género Principal
    available_genres = sorted(df_data['primary_genre'].unique())
    selected_genres = st.multiselect(
        "Género Cinematográfico",
        options=available_genres,
        default=available_genres[:8] if len(available_genres) > 8 else available_genres
    )

    # Filtro 3: Segmento de Clustering
    available_clusters = sorted(df_data['cluster_name'].unique())
    selected_clusters = st.multiselect(
        "Segmento Fílmico (K-Means)",
        options=available_clusters,
        default=available_clusters
    )

    # Aplicación reactiva de filtros
    df_filtered = df_data[
        (df_data['release_year'].isin(selected_years)) &
        (df_data['primary_genre'].isin(selected_genres)) &
        (df_data['cluster_name'].isin(selected_clusters))
    ]

    st.markdown("<hr style='margin: 1.2rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #94A3B8;">
            Muestra activa: <span style="color: #38BDF8; font-weight: 600;">{len(df_filtered):,}</span> / {len(df_data):,} títulos
        </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. PÁGINA 1: ANÁLISIS GENERAL Y EXPLORACIÓN
# -----------------------------------------------------------------------------
if page == "Página 1: Análisis General":
    st.markdown("""
        <div class="editorial-header">
            <span class="editorial-tag">Sección 01 · Exploración de Datos</span>
            <h1 class="editorial-title">Panorama Macroeconómico de la Industria (2024–2026)</h1>
            <p class="editorial-subtitle">Auditoría multidimensional de capital de producción, rendimiento en taquilla global y dinámicas de recepción crítica en el cine contemporáneo.</p>
        </div>
    """, unsafe_allow_html=True)

    # Cuatro Indicadores KPI Principales
    total_films = len(df_filtered)
    total_box = df_filtered['box_office_usd'].sum()
    avg_budget = df_filtered['budget_usd'].mean() if total_films > 0 else 0
    avg_rating = df_filtered['rating_out_of_10'].mean() if total_films > 0 else 0

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-label">Volumen de Títulos</div>
                <div class="kpi-value">{total_films:,}</div>
                <div class="kpi-subtext">Largometrajes analizados</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Taquilla Acumulada</div>
                <div class="kpi-value">${total_box / 1e9:.2f}B</div>
                <div class="kpi-subtext">Ingresos brutos globales</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Presupuesto Promedio</div>
                <div class="kpi-value">${avg_budget / 1e6:.1f}M</div>
                <div class="kpi-subtext">Costo de producción / título</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Calificación Global</div>
                <div class="kpi-value">{avg_rating:.2f}<span style="font-size: 1rem; color: #64748B;"> / 10</span></div>
                <div class="kpi-subtext">Recepción media ponderada</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Gráficas Exploratorias Principales
    col_g1, col_g2 = st.columns([6, 4])

    with col_g1:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>Dispersión Financiera: Inversión vs Recaudación Mundial</div>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_filtered,
            x='budget_usd',
            y='box_office_usd',
            color='primary_genre',
            size='rating_out_of_10',
            hover_name='title',
            hover_data={
                'budget_usd': ':$,.0f',
                'box_office_usd': ':$,.0f',
                'rating_out_of_10': ':.1f',
                'roi_pct': ':.1f%',
                'director': True
            },
            labels={
                'budget_usd': 'Presupuesto de Producción ($ USD)',
                'box_office_usd': 'Taquilla Mundial ($ USD)',
                'primary_genre': 'Género'
            },
            template='plotly_dark',
            height=440
        )
        fig_scatter.update_layout(PLOTLY_THEME['layout'])
        fig_scatter.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5, font=dict(size=10))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_g2:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>Top Géneros por Volumen de Taquilla</div>", unsafe_allow_html=True)
        genre_summary = df_filtered.groupby('primary_genre')['box_office_usd'].sum().reset_index()
        genre_summary = genre_summary.sort_values(by='box_office_usd', ascending=True).tail(8)
        fig_genre = px.bar(
            genre_summary,
            x='box_office_usd',
            y='primary_genre',
            orientation='h',
            labels={'box_office_usd': 'Taquilla Total ($)', 'primary_genre': ''},
            color='box_office_usd',
            color_continuous_scale='Blues',
            template='plotly_dark',
            height=440
        )
        fig_genre.update_layout(PLOTLY_THEME['layout'])
        fig_genre.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_genre, use_container_width=True)

    # Fila de Distribución de Calificaciones y Explorador Tabular
    col_d1, col_d2 = st.columns([5, 5])
    with col_d1:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>Curva de Densidad de Calificaciones (Audiencia / Crítica)</div>", unsafe_allow_html=True)
        fig_dist_rating = px.histogram(
            df_filtered,
            x='rating_out_of_10',
            nbins=22,
            marginal='box',
            color_discrete_sequence=['#38BDF8'],
            labels={'rating_out_of_10': 'Calificación (0 - 10)'},
            template='plotly_dark',
            height=370
        )
        fig_dist_rating.update_layout(PLOTLY_THEME['layout'])
        st.plotly_chart(fig_dist_rating, use_container_width=True)

    with col_d2:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>Muestra de Registros Auditorados</div>", unsafe_allow_html=True)
        view_cols = ['title', 'release_year', 'primary_genre', 'rating_out_of_10', 'budget_usd', 'box_office_usd', 'roi_pct']
        st.dataframe(
            df_filtered[view_cols].head(8).style.format({
                'budget_usd': '${:,.0f}',
                'box_office_usd': '${:,.0f}',
                'rating_out_of_10': '{:.1f}',
                'roi_pct': '{:.1f}%'
            }),
            use_container_width=True,
            height=370
        )


# -----------------------------------------------------------------------------
# 6. PÁGINA 2: SEGMENTACIÓN MEDIANTE K-MEANS
# -----------------------------------------------------------------------------
elif page == "Página 2: Segmentación K-Means":
    st.markdown("""
        <div class="editorial-header">
            <span class="editorial-tag">Sección 02 · Aprendizaje No Supervisado</span>
            <h1 class="editorial-title">Segmentación Multidimensional con K-Means</h1>
            <p class="editorial-subtitle">Descubrimiento de arquetipos cinematográficos estructurados en el espacio vectorial euclidiano estandarizado (StandardScaler).</p>
        </div>
    """, unsafe_allow_html=True)

    # 4 KPIs del Algoritmo
    roi_max = df_filtered.groupby('cluster_name')['roi_pct'].mean().max() if len(df_filtered) > 0 else 0
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-label">Número de Clústeres (K)</div>
                <div class="kpi-value">4</div>
                <div class="kpi-subtext">Optimizado mediante Método del Codo</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Coeficiente de Silueta</div>
                <div class="kpi-value">0.537</div>
                <div class="kpi-subtext">Estructura coherente y bien separada</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">ROI Máximo por Segmento</div>
                <div class="kpi-value">{roi_max:.1f}%</div>
                <div class="kpi-subtext">Liderado por Mega Blockbusters</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Preprocesamiento Vectorial</div>
                <div class="kpi-value" style="font-size: 1.45rem;">StandardScaler</div>
                <div class="kpi-subtext">Normalización a media 0 y varianza 1</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Visualizaciones Principales del Clustering:
    # 1. Distribución de Títulos por Clúster
    # 2. Scatter Plot con Centroides
    col_c1, col_c2 = st.columns([5, 5])

    with col_c1:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>1. Composición Cuantitativa por Segmento</div>", unsafe_allow_html=True)
        counts = df_filtered['cluster_name'].value_counts().reset_index()
        counts.columns = ['cluster_name', 'total']
        fig_counts = px.bar(
            counts,
            x='total',
            y='cluster_name',
            orientation='h',
            color='cluster_name',
            color_discrete_map=CLUSTER_PALETTE,
            text='total',
            labels={'total': 'Cantidad de Títulos', 'cluster_name': ''},
            template='plotly_dark',
            height=420
        )
        fig_counts.update_layout(PLOTLY_THEME['layout'])
        fig_counts.update_traces(textposition='outside', cliponaxis=False)
        fig_counts.update_layout(showlegend=False)
        st.plotly_chart(fig_counts, use_container_width=True)

    with col_c2:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #FFFFFF; margin-bottom: 0.5rem;'>2. Espacio de Agrupamiento: Presupuesto vs Taquilla</div>", unsafe_allow_html=True)
        fig_scatter_clusters = px.scatter(
            df_filtered,
            x='budget_usd',
            y='box_office_usd',
            color='cluster_name',
            color_discrete_map=CLUSTER_PALETTE,
            hover_name='title',
            hover_data={
                'budget_usd': ':$,.0f',
                'box_office_usd': ':$,.0f',
                'rating_out_of_10': ':.2f',
                'roi_pct': ':.1f%'
            },
            labels={
                'budget_usd': 'Presupuesto ($ USD)',
                'box_office_usd': 'Taquilla Mundial ($ USD)',
                'cluster_name': 'Segmento'
            },
            template='plotly_dark',
            height=420
        )
        fig_scatter_clusters.update_layout(PLOTLY_THEME['layout'])
        fig_scatter_clusters.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.38, xanchor="center", x=0.5, font=dict(size=9.5))
        )
        st.plotly_chart(fig_scatter_clusters, use_container_width=True)

    # Dos Gráficas Adicionales para Comparación entre Grupos
    st.markdown("<div style='margin-top: 1.5rem; font-size: 0.95rem; font-weight: 700; color: #FFFFFF;'>3. Comparación Paramétrica entre Segmentos Fílmicos</div>", unsafe_allow_html=True)
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.markdown("<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.3rem;'>Distribución de Calificación Artística (Rating / 10)</div>", unsafe_allow_html=True)
        fig_box_rating = px.box(
            df_filtered,
            x='cluster_name',
            y='rating_out_of_10',
            color='cluster_name',
            color_discrete_map=CLUSTER_PALETTE,
            labels={'rating_out_of_10': 'Calificación', 'cluster_name': ''},
            template='plotly_dark',
            height=370
        )
        fig_box_rating.update_layout(PLOTLY_THEME['layout'])
        fig_box_rating.update_layout(showlegend=False, xaxis=dict(tickangle=-12))
        st.plotly_chart(fig_box_rating, use_container_width=True)

    with g_col2:
        st.markdown("<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.3rem;'>Eficiencia Financiera: Retorno de Inversión (ROI %)</div>", unsafe_allow_html=True)
        fig_box_roi = px.box(
            df_filtered,
            x='cluster_name',
            y='roi_pct',
            color='cluster_name',
            color_discrete_map=CLUSTER_PALETTE,
            labels={'roi_pct': 'ROI Estimado (%)', 'cluster_name': ''},
            template='plotly_dark',
            height=370
        )
        fig_box_roi.update_layout(PLOTLY_THEME['layout'])
        fig_box_roi.update_layout(showlegend=False, xaxis=dict(tickangle=-12))
        st.plotly_chart(fig_box_roi, use_container_width=True)

    # Tabla de Estadísticas Descriptivas de los Clústeres
    st.markdown("<div style='margin-top: 1.5rem; font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.5rem;'>4. Tabla de Centroides y Estadísticas por Grupo</div>", unsafe_allow_html=True)
    cluster_stats = df_filtered.groupby('cluster_name').agg(
        Peliculas=('title', 'count'),
        Presupuesto_Medio=('budget_usd', 'mean'),
        Taquilla_Media=('box_office_usd', 'mean'),
        Rating_Medio=('rating_out_of_10', 'mean'),
        ROI_Medio=('roi_pct', 'mean')
    ).reset_index()

    st.dataframe(
        cluster_stats.style.format({
            'Peliculas': '{:,.0f}',
            'Presupuesto_Medio': '${:,.0f}',
            'Taquilla_Media': '${:,.0f}',
            'Rating_Medio': '{:.2f}',
            'ROI_Medio': '{:.1f}%'
        }),
        use_container_width=True
    )

    # Sección 5: Perfilamiento de los 4 Arquetipos Identificados
    st.markdown("<div style='margin-top: 2rem; font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.8rem;'>5. Caracterización de los Arquetipos de la Industria</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="archetype-grid">
            <div class="archetype-card">
                <div class="archetype-header">
                    <h3 class="archetype-title">Mega Blockbusters Taquilleros</h3>
                    <span class="archetype-badge" style="background: rgba(255, 77, 109, 0.15); color: #FF4D6D; border: 1px solid rgba(255, 77, 109, 0.3);">SEGMENTO 01</span>
                </div>
                <p class="archetype-desc">Producciones de escala épica y franquicias de propiedad intelectual global (ej. <em>Dune: Part Two</em>, <em>Deadpool & Wolverine</em>). Concentran la máxima liquidez de la industria.</p>
                <div class="metrics-row">
                    <div>
                        <div class="metric-item-label">Presupuesto</div>
                        <div class="metric-item-val">$164.9M</div>
                    </div>
                    <div>
                        <div class="metric-item-label">Taquilla</div>
                        <div class="metric-item-val">$492.6M</div>
                    </div>
                    <div>
                        <div class="metric-item-label">ROI Medio</div>
                        <div class="metric-item-val" style="color: #FF4D6D;">+198.7%</div>
                    </div>
                </div>
            </div>

            <div class="archetype-card">
                <div class="archetype-header">
                    <h3 class="archetype-title">Joyas Aclamadas por la Crítica</h3>
                    <span class="archetype-badge" style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3);">SEGMENTO 02</span>
                </div>
                <p class="archetype-desc">Cine de autor, prestigio narrativo y festivales. Logran excelencia artística con presupuestos altamente controlados y sólida rentabilidad porcentual.</p>
                <div class="metrics-row">
                    <div>
                        <div class="metric-item-label">Presupuesto</div>
                        <div class="metric-item-val">$21.3M</div>
                    </div>
                    <div>
                        <div class="metric-item-label">Calificación</div>
                        <div class="metric-item-val" style="color: #10B981;">8.69 / 10</div>
                    </div>
                    <div>
                        <div class="metric-item-label">ROI Medio</div>
                        <div class="metric-item-val">+58.6%</div>
                    </div>
                </div>
            </div>

            <div class="archetype-card">
                <div class="archetype-header">
                    <h3 class="archetype-title">Producciones Comerciales Estándar</h3>
                    <span class="archetype-badge" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3);">SEGMENTO 03</span>
                </div>
                <p class="archetype-desc">Películas de catálogo destinadas a consumo masivo, géneros consolidados y comedia. Mantienen un retorno estable y calificaciones satisfactorias.</p>
                <div class="metrics-row">
                    <div>
                        <div class="metric-item-label">Presupuesto</div>
                        <div class="metric-item-val">$21.2M</div>
                    </div>
                    <div>
                        <div class="metric-item-label">Calificación</div>
                        <div class="metric-item-val">7.60 / 10</div>
                    </div>
                    <div>
                        <div class="metric-item-label">ROI Medio</div>
                        <div class="metric-item-val">+60.3%</div>
                    </div>
                </div>
            </div>

            <div class="archetype-card">
                <div class="archetype-header">
                    <h3 class="archetype-title">Bajo Desempeño Crítico</h3>
                    <span class="archetype-badge" style="background: rgba(167, 139, 250, 0.15); color: #A78BFA; border: 1px solid rgba(167, 139, 250, 0.3);">SEGMENTO 04</span>
                </div>
                <p class="archetype-desc">Zona de riesgo operacional. Proyectos que absorbieron el mismo presupuesto promedio pero sufrieron de recepción crítica deficiente y retornos mermados.</p>
                <div class="metrics-row">
                    <div>
                        <div class="metric-item-label">Presupuesto</div>
                        <div class="metric-item-val">$21.6M</div>
                    </div>
                    <div>
                        <div class="metric-item-label">Calificación</div>
                        <div class="metric-item-val" style="color: #A78BFA;">6.50 / 10</div>
                    </div>
                    <div>
                        <div class="metric-item-label">ROI Medio</div>
                        <div class="metric-item-val">+51.8%</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sección 6: Hallazgos y Recomendaciones Estratégicas
    st.markdown("<div style='margin-top: 2rem; font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.8rem;'>6. Hallazgos Analíticos y Recomendaciones Ejecutivas</div>", unsafe_allow_html=True)
    c_h, c_r = st.columns(2)

    with c_h:
        st.markdown("""
            <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.4rem;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.75rem;">
                    Hallazgos Clave de Minería de Datos
                </div>
                <ul style="font-size: 0.88rem; color: #94A3B8; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong style="color: #F8FAFC;">Concentración Asimétrica:</strong> Una élite de solo 20 títulos (2.2% del mercado) genera un ROI promedio cercano al 200%, confirmando que los eventos globales siguen dictando la solvencia de la industria.</li>
                    <li><strong style="color: #F8FAFC;">Independencia Presupuesto-Calidad:</strong> La correlación entre costo de producción y calificación artística es nula (-0.002). El segmento aclamado alcanza 8.69/10 con solo $21.3M USD.</li>
                    <li><strong style="color: #F8FAFC;">Fuga de Capital en Rango Medio:</strong> El 33.5% de los filmes caen en la zona de bajo desempeño consumiendo el mismo presupuesto ($21.5M USD) sin retorno reputacional ni económico acorde.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with c_r:
        st.markdown("""
            <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.4rem;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.75rem;">
                    Recomendaciones de Negocio para Producción
                </div>
                <ul style="font-size: 0.88rem; color: #94A3B8; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong style="color: #F8FAFC;">Portafolio Bi-Modal:</strong> Financiar un número acotado de franquicias globales de alto presupuesto respaldado por un catálogo diversificado de películas de presupuesto medio-bajo.</li>
                    <li><strong style="color: #F8FAFC;">Auditorías de Guion Tempranas:</strong> Implementar filtros de control de calidad estrictos en la fase de desarrollo para proyectos de $20M a $25M USD, reduciendo la entrada a la zona de bajo impacto.</li>
                    <li><strong style="color: #F8FAFC;">Ventanas Híbridas para Cine Aclamado:</strong> Capitalizar el boca a boca de las 'Joyas Críticas' en festivales antes de estrenos exclusivos en streaming para maximizar retención sin sobrecostos de marketing.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 3rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06); font-family: \"JetBrains Mono\", monospace; font-size: 0.72rem; color: #64748B; text-align: center;'>CineMetrics Intelligence Suite · Proyecto Integrador de Minería de Datos · K-Means Clustering</div>", unsafe_allow_html=True)
