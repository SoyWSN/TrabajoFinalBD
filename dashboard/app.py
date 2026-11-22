"""
app.py
Dashboard Interactivo para la Segmentación de Películas (2024-2026) mediante K-Means.
Desarrollado en Streamlit con visualizaciones interactivas en Plotly.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(
    page_title="CineMetrics | Segmentación K-Means (2024-2026)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .cluster-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carga el dataset procesado con los clústeres asignados."""
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'movies_clustered_2024_2026.csv')
    if not os.path.exists(filepath):
        # Fallback a ruta local
        filepath = os.path.join('data', 'processed', 'movies_clustered_2024_2026.csv')
    df = pd.read_csv(filepath)
    return df


df_data = load_data()

# Paleta de colores consistente por Clúster
CLUSTER_COLORS = {
    'Mega Blockbusters Taquilleros': '#E63946',
    'Joyas Aclamadas por la Crítica': '#2A9D8F',
    'Producciones Comerciales Estándar': '#457B9D',
    'Bajo Desempeño Crítico': '#9B5DE5'
}

# ==========================================
# BARRA LATERAL (SIDEBAR): FILTROS Y NAVEGACIÓN
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60", use_container_width=True)
st.sidebar.title("🎬 CineMetrics 360")
st.sidebar.markdown("**Minería de Datos & Agrupamiento Fílmico**")
st.sidebar.markdown("---")

# Navegación entre las dos páginas requeridas
page = st.sidebar.radio(
    "Selecciona la Sección:",
    ["📄 Página 1: Análisis General", "🎯 Página 2: Segmentación K-Means"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros Interactivos")

# Filtro 1: Año de estreno
available_years = sorted(df_data['release_year'].unique())
selected_years = st.sidebar.multiselect(
    "1. Año de Estreno:",
    options=available_years,
    default=available_years
)

# Filtro 2: Género Principal
available_genres = sorted(df_data['primary_genre'].unique())
selected_genres = st.sidebar.multiselect(
    "2. Género Principal:",
    options=available_genres,
    default=available_genres[:8] if len(available_genres) > 8 else available_genres
)

# Filtro 3: Segmento K-Means
available_clusters = sorted(df_data['cluster_name'].unique())
selected_clusters = st.sidebar.multiselect(
    "3. Segmento (Clúster):",
    options=available_clusters,
    default=available_clusters
)

# Aplicación de filtros
df_filtered = df_data[
    (df_data['release_year'].isin(selected_years)) &
    (df_data['primary_genre'].isin(selected_genres)) &
    (df_data['cluster_name'].isin(selected_clusters))
]

st.sidebar.caption(f"Mostrando **{len(df_filtered)}** de **{len(df_data)}** producciones.")

# ==========================================
# PÁGINA 1: ANÁLISIS GENERAL
# ==========================================
if page == "📄 Página 1: Análisis General":
    st.markdown('<div class="main-title">Panorama General de la Industria Fílmica (2024–2026)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Exploración estadística, desempeño financiero y métricas de recepción crítica en la era contemporánea.</div>', unsafe_allow_html=True)

    # 4 Indicadores KPI Relevantes
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="Total de Producciones",
            value=f"{len(df_filtered):,}",
            delta=f"{len(df_filtered) - len(df_data)}" if len(df_filtered) != len(df_data) else None
        )
    with kpi2:
        total_box_office = df_filtered['box_office_usd'].sum()
        st.metric(
            label="Taquilla Global Acumulada",
            value=f"${total_box_office / 1e9:.2f} B USD"
        )
    with kpi3:
        avg_budget = df_filtered['budget_usd'].mean()
        st.metric(
            label="Presupuesto Promedio",
            value=f"${avg_budget / 1e6:.1f} M USD"
        )
    with kpi4:
        avg_rating = df_filtered['rating_out_of_10'].mean()
        st.metric(
            label="Calificación Promedio",
            value=f"{avg_rating:.2f} / 10"
        )

    st.markdown("---")

    # Fila de Gráficas Exploratorias
    col_g1, col_g2 = st.columns([6, 4])

    with col_g1:
        st.subheader("Relación entre Presupuesto y Taquilla Mundial")
        fig_scatter = px.scatter(
            df_filtered,
            x='budget_usd',
            y='box_office_usd',
            color='primary_genre',
            size='rating_out_of_10',
            hover_name='title',
            hover_data=['release_year', 'director', 'rating_out_of_10', 'roi_pct'],
            labels={
                'budget_usd': 'Presupuesto de Producción ($ USD)',
                'box_office_usd': 'Recaudación Mundial ($ USD)',
                'primary_genre': 'Género Principal',
                'rating_out_of_10': 'Calificación'
            },
            template='plotly_white',
            height=460
        )
        fig_scatter.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_g2:
        st.subheader("Top 8 Géneros por Taquilla Acumulada")
        genre_box = df_filtered.groupby('primary_genre')['box_office_usd'].sum().reset_index()
        genre_box = genre_box.sort_values(by='box_office_usd', ascending=True).tail(8)
        fig_bar_genre = px.bar(
            genre_box,
            x='box_office_usd',
            y='primary_genre',
            orientation='h',
            labels={'box_office_usd': 'Taquilla Total ($ USD)', 'primary_genre': 'Género'},
            color='box_office_usd',
            color_continuous_scale='Blues',
            template='plotly_white',
            height=460
        )
        fig_bar_genre.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar_genre, use_container_width=True)

    # Segunda fila exploratoria: Distribución de Calificaciones y Tabla Resumen
    col_d1, col_d2 = st.columns([5, 5])
    with col_d1:
        st.subheader("Distribución de Calificaciones de la Audiencia")
        fig_hist = px.histogram(
            df_filtered,
            x='rating_out_of_10',
            nbins=20,
            marginal='box',
            color_discrete_sequence=['#2B6CB0'],
            labels={'rating_out_of_10': 'Calificación (0 - 10)'},
            template='plotly_white',
            height=380
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_d2:
        st.subheader("Muestra de Registros Explorados")
        cols_show = ['title', 'release_year', 'primary_genre', 'rating_out_of_10', 'budget_usd', 'box_office_usd', 'roi_pct']
        st.dataframe(
            df_filtered[cols_show].head(10).style.format({
                'budget_usd': '${:,.0f}',
                'box_office_usd': '${:,.0f}',
                'rating_out_of_10': '{:.1f}',
                'roi_pct': '{:.1f}%'
            }),
            use_container_width=True,
            height=380
        )

# ==========================================
# PÁGINA 2: SEGMENTACIÓN MEDIANTE K-MEANS
# ==========================================
elif page == "🎯 Página 2: Segmentación K-Means":
    st.markdown('<div class="main-title">Segmentación de Películas mediante K-Means</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Descubrimiento de patrones no supervisados a partir de Presupuesto, Taquilla Mundial y Calificación Crítica.</div>', unsafe_allow_html=True)

    # Cuatro Indicadores KPI del Agrupamiento
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="Número de Clústeres (K)", value="4")
    with kpi2:
        st.metric(label="Coeficiente de Silueta", value="0.537", delta="Estructura Coherente")
    with kpi3:
        roi_top = df_filtered.groupby('cluster_name')['roi_pct'].mean().max()
        st.metric(label="ROI Promedio Máximo", value=f"{roi_top:.1f}%")
    with kpi4:
        st.metric(label="Algoritmo / Escalador", value="K-Means / Standard")

    st.markdown("---")

    # Visualizaciones Principales Requeridas:
    # 1. Distribución de registros por clúster
    # 2. Gráfica de dispersión de agrupamientos
    c_left, c_right = st.columns([5, 5])

    with c_left:
        st.subheader("1. Distribución de Producciones por Clúster")
        cluster_counts = df_filtered['cluster_name'].value_counts().reset_index()
        cluster_counts.columns = ['cluster_name', 'count']
        fig_dist = px.bar(
            cluster_counts,
            x='count',
            y='cluster_name',
            orientation='h',
            color='cluster_name',
            color_discrete_map=CLUSTER_COLORS,
            text='count',
            labels={'count': 'Número de Películas', 'cluster_name': 'Segmento'},
            template='plotly_white',
            height=420
        )
        fig_dist.update_traces(textposition='outside')
        fig_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    with c_right:
        st.subheader("2. Gráfica de Dispersión de Agrupamientos (K-Means)")
        fig_clusters = px.scatter(
            df_filtered,
            x='budget_usd',
            y='box_office_usd',
            color='cluster_name',
            color_discrete_map=CLUSTER_COLORS,
            hover_name='title',
            hover_data=['release_year', 'rating_out_of_10', 'director', 'roi_pct'],
            labels={
                'budget_usd': 'Presupuesto ($ USD)',
                'box_office_usd': 'Taquilla Mundial ($ USD)',
                'cluster_name': 'Clúster'
            },
            template='plotly_white',
            height=420
        )
        fig_clusters.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
        st.plotly_chart(fig_clusters, use_container_width=True)

    # Dos Gráficas Adicionales para Comparar Características de los Grupos
    st.markdown("---")
    st.subheader("3. Comparativa de Características entre Clústeres")
    g_add1, g_add2 = st.columns(2)

    with g_add1:
        st.markdown("**Comparativa de Calificación (Rating / 10)**")
        fig_box_rating = px.box(
            df_filtered,
            x='cluster_name',
            y='rating_out_of_10',
            color='cluster_name',
            color_discrete_map=CLUSTER_COLORS,
            labels={'rating_out_of_10': 'Calificación', 'cluster_name': ''},
            template='plotly_white',
            height=380
        )
        fig_box_rating.update_layout(showlegend=False, xaxis_tickangle=-15)
        st.plotly_chart(fig_box_rating, use_container_width=True)

    with g_add2:
        st.markdown("**Comparativa de Retorno de Inversión (ROI %)**")
        fig_box_roi = px.box(
            df_filtered,
            x='cluster_name',
            y='roi_pct',
            color='cluster_name',
            color_discrete_map=CLUSTER_COLORS,
            labels={'roi_pct': 'ROI Estimado (%)', 'cluster_name': ''},
            template='plotly_white',
            height=380
        )
        fig_box_roi.update_layout(showlegend=False, xaxis_tickangle=-15)
        st.plotly_chart(fig_box_roi, use_container_width=True)

    # Tabla con Estadísticas Descriptivas de los Clústeres
    st.markdown("---")
    st.subheader("4. Tabla de Estadísticas Descriptivas por Clúster")
    cluster_summary = df_filtered.groupby('cluster_name').agg(
        Total_Peliculas=('title', 'count'),
        Presupuesto_Promedio=('budget_usd', 'mean'),
        Taquilla_Promedio=('box_office_usd', 'mean'),
        Rating_Promedio=('rating_out_of_10', 'mean'),
        Votos_Promedio=('vote_count', 'mean'),
        ROI_Promedio=('roi_pct', 'mean')
    ).reset_index()

    st.dataframe(
        cluster_summary.style.format({
            'Total_Peliculas': '{:,.0f}',
            'Presupuesto_Promedio': '${:,.0f}',
            'Taquilla_Promedio': '${:,.0f}',
            'Rating_Promedio': '{:.2f}',
            'Votos_Promedio': '{:,.0f}',
            'ROI_Promedio': '{:.1f}%'
        }),
        use_container_width=True
    )

    # Sección con la Descripción de los Grupos Identificados
    st.markdown("---")
    st.subheader("5. Descripción y Perfilamiento de los Segmentos")

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        <div class="cluster-card" style="border-left: 5px solid #E63946;">
            <h4 style="color: #E63946; margin:0;">🌟 Mega Blockbusters Taquilleros</h4>
            <p><strong>Perfil:</strong> Grandes producciones de franquicias mundiales (ej. <em>Dune: Part Two</em>, <em>Inside Out 2</em>, <em>Deadpool & Wolverine</em>).</p>
            <ul>
                <li><strong>Presupuesto:</strong> Masivo (~$165M USD promedio).</li>
                <li><strong>Taquilla:</strong> Extraordinaria (~$493M USD promedio).</li>
                <li><strong>ROI:</strong> ~198.7% de retorno sobre la inversión.</li>
                <li><strong>Recepción:</strong> Sólida aceptación crítica y masiva movilización de audiencia.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cluster-card" style="border-left: 5px solid #457B9D;">
            <h4 style="color: #457B9D; margin:0;">🎬 Producciones Comerciales Estándar</h4>
            <p><strong>Perfil:</strong> Cine comercial tradicional y películas de catálogo con desempeño balanceado.</p>
            <ul>
                <li><strong>Presupuesto:</strong> Moderado (~$21.2M USD).</li>
                <li><strong>Taquilla:</strong> Estable (~$31.3M USD).</li>
                <li><strong>ROI:</strong> ~60.3% promedio.</li>
                <li><strong>Recepción:</strong> Calificación promedio de 7.6 / 10.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="cluster-card" style="border-left: 5px solid #2A9D8F;">
            <h4 style="color: #2A9D8F; margin:0;">🏆 Joyas Aclamadas por la Crítica</h4>
            <p><strong>Perfil:</strong> Cine de autor, prestigio e historias aclamadas con presupuestos muy contenidos.</p>
            <ul>
                <li><strong>Presupuesto:</strong> Muy eficiente (~$21.3M USD).</li>
                <li><strong>Taquilla:</strong> Sólida (~$31.1M USD).</li>
                <li><strong>ROI:</strong> ~58.6% promedio.</li>
                <li><strong>Recepción:</strong> Sobresaliente calificación promedio de <strong>8.69 / 10</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cluster-card" style="border-left: 5px solid #9B5DE5;">
            <h4 style="color: #9B5DE5; margin:0;">📉 Producciones de Bajo Desempeño Crítico</h4>
            <p><strong>Perfil:</strong> Películas con presupuestos convencionales pero fría recepción de crítica y público.</p>
            <ul>
                <li><strong>Presupuesto:</strong> Estándar (~$21.6M USD).</li>
                <li><strong>Taquilla:</strong> Limitada (~$30.7M USD).</li>
                <li><strong>ROI:</strong> Menor retorno (~51.8% promedio).</li>
                <li><strong>Recepción:</strong> Calificación modesta (~6.50 / 10).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Sección con los Principales Hallazgos y Recomendaciones
    st.markdown("---")
    st.subheader("6. Principales Hallazgos y Recomendaciones Estratégicas")

    h_col, r_col = st.columns(2)
    with h_col:
        st.markdown("### 📌 Hallazgos Clave")
        st.markdown("""
        1. **Polarización del Negocio:** Un grupo exclusivo (~2.2% de los títulos) acapara presupuestos y recaudaciones exorbitantes (Blockbusters), con un ROI casi cuatro veces superior a las producciones promedio.
        2. **Independencia entre Presupuesto y Calidad:** La correlación entre presupuesto y calificación es prácticamente nula (-0.002). El segmento de *Joyas Críticas* alcanza calificaciones superiores a 8.5 con presupuestos moderados (~$21M USD).
        3. **Sensibilidad del Desempeño Crítico:** Las películas en el segmento de *Bajo Desempeño* absorben un capital similar (~$21.5M USD) pero obtienen el menor retorno económico y recepción insatisfactoria.
        """)

    with r_col:
        st.markdown("### 💡 Recomendaciones de Negocio")
        st.markdown("""
        1. **Estrategia de Portafolio Diversificado:** Balancear las inversiones de alto riesgo (Blockbusters de >$100M USD) con proyectos medianos de alta rentabilidad y aclamación crítica.
        2. **Control de Calidad en Etapa Temprana:** Implementar filtros rigurosos de guion y proyecciones de prueba para producciones de $20M-$25M USD, evitando caer en la zona de bajo desempeño.
        3. **Potenciación del Prestigio en Distribución:** Aprovechar los estrenos de películas con alta calificación crítica para campañas de festivales, premios y ventanas exclusivas en streaming.
        """)

    st.markdown("---")
    st.caption("Proyecto Integrador de Minería de Datos | Segmentación K-Means | Dashboard Interactivo Desarrollado con Streamlit y Plotly")
