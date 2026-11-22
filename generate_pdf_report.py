"""
generate_pdf_report.py
Generador del Documento PDF oficial de Documentación del Proyecto Integrador
cumpliendo estrictamente con la estructura de 8 apartados requerida por la rúbrica.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado para agregar pie de página con numeración y encabezado."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))
            # Encabezado
            self.drawString(54, 755, "Proyecto Integrador: Minería de Datos | Segmentación Cinematográfica K-Means")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)
            
            # Pie de página
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(558, 36, page_text)
            self.drawString(54, 36, "Repositorio GitHub: TrabajoFinalBD | Dashboard Interactivo")
            self.line(54, 46, 558, 46)
            self.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos tipográficos
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A365D'),
        alignment=1, # Centrado
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#2D3748')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # 1. PORTADA
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROYECTO INTEGRADOR", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#2B6CB0'), alignment=1, spaceAfter=10)))
    story.append(Paragraph("Segmentación de Datos Mediante K-Means y Desarrollo de un Dashboard Interactivo", title_style))
    story.append(Paragraph("Minería de Datos Aplicada a la Industria Cinematográfica Contemporánea (2024–2026)", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#2B6CB0'), spaceBefore=10, spaceAfter=30))

    story.append(Spacer(1, 40))

    meta_table_data = [
        [Paragraph("<b>Asignatura:</b>", table_cell), Paragraph("Bases de Datos Avanzadas / Minería de Datos", table_cell)],
        [Paragraph("<b>Tema del Proyecto:</b>", table_cell), Paragraph("Segmentación Fílmica No Supervisada con Algoritmo K-Means", table_cell)],
        [Paragraph("<b>Herramientas:</b>", table_cell), Paragraph("Python 3.13, Pandas, Scikit-learn, Matplotlib, Seaborn, Streamlit, Plotly", table_cell)],
        [Paragraph("<b>Modalidad:</b>", table_cell), Paragraph("Equipo de Proyecto", table_cell)],
        [Paragraph("<b>Integrantes:</b>", table_cell), Paragraph("Equipo Investigador de Minería de Datos", table_cell)],
        [Paragraph("<b>Grupo / Período:</b>", table_cell), Paragraph("Grupo Académico 2026", table_cell)],
        [Paragraph("<b>Fecha de Entrega:</b>", table_cell), Paragraph("Noviembre 2026", table_cell)],
        [Paragraph("<b>Repositorio GitHub:</b>", table_cell), Paragraph("https://github.com/oskar/TrabajoFinalBD (Público)", table_cell)]
    ]
    t_meta = Table(meta_table_data, colWidths=[130, 320])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)

    story.append(Spacer(1, 60))
    story.append(Paragraph("<i>Documento Técnico Formal y Reporte de Resultados</i>", ParagraphStyle('CoverFooter', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#718096'), alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # 2. INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA
    # =========================================================================
    story.append(Paragraph("2. Introducción y Planteamiento del Problema", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>Descripción de la Temática:</b> La industria del entretenimiento y el cine contemporáneo (2024–2026) se encuentra inmersa en una fase de profunda reestructuración económica y operativa tras la estabilización de los modelos de exhibición en salas y la madurez de las plataformas de streaming. A diferencia de las décadas pasadas, donde los comportamientos de taquilla seguían patrones de estacionalidad convencionales, la era actual combina presupuestos de producción multimillonarios con una recepción del público altamente fragmentada y exigente.", body_style))

    story.append(Paragraph("<b>Planteamiento del Problema:</b> Los estudios cinematográficos, distribuidores e inversionistas se enfrentan a una asimetría crítica: destinar presupuestos que superan los cientos de millones de dólares a producciones sin contar con un entendimiento cuantitativo de cómo interactúan la inversión de capital, el retorno en taquilla y la aclamación crítica. Existen proyectos de costo moderado que generan altísimos márgenes y prestigio artístico sobresaliente, mientras que producciones de alto presupuesto fracasan estrepitosamente en taquilla. La problemática radica en la carencia de modelos analíticos no supervisados que permitan clasificar la oferta de largometrajes en arquetipos operacionales homogéneos para gestionar eficientemente el riesgo de inversión.", body_style))

    story.append(Paragraph("<b>Justificación del Proyecto:</b> El análisis de agrupamiento (clustering) mediante minería de datos proporciona un marco riguroso para categorizar el comportamiento fílmico sin imponer etiquetas predeterminadas. Al aplicar el algoritmo K-Means sobre las variables de presupuesto, recaudación mundial y calificaciones de la crítica/audiencia, este proyecto identifica perfiles objetivos de desempeño. Esto posibilita a los directores de producción y analistas de negocios optimizar la asignación presupuestaria, planificar ventanas de distribución diferenciadas y mitigar pérdidas financieras.", body_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # 3. OBJETIVOS
    # =========================================================================
    story.append(Paragraph("3. Objetivos", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>Objetivo General:</b>", body_bold))
    story.append(Paragraph("Desarrollar e implementar un proyecto integral de minería de datos mediante el algoritmo de aprendizaje no supervisado K-Means para segmentar largometrajes producidos entre 2024 y 2026 en función de su presupuesto, taquilla global y recepción crítica, presentando los hallazgos en un dashboard interactivo de dos páginas que facilite la interpretación y la toma de decisiones estratégicas.", body_style))

    story.append(Paragraph("<b>Objetivos Específicos:</b>", body_bold))
    story.append(Paragraph("1. <b>Explorar, depurar y normalizar</b> un dataset de más de 900 producciones cinematográficas modernas, resolviendo duplicidades, imputando nulos y aplicando técnicas de escalamiento estadístico (StandardScaler).", body_style))
    story.append(Paragraph("2. <b>Determinar y validar el número óptimo de clústeres ($K$)</b> mediante la evaluación empírica de múltiples configuraciones con el Método del Codo (Elbow Method) y el Coeficiente de Silueta (Silhouette Score).", body_style))
    story.append(Paragraph("3. <b>Caracterizar, interpretar y perfilar</b> cada uno de los agrupamientos resultantes, contrastando métricas de retorno de inversión (ROI) y formulando recomendaciones prácticas y limitaciones del modelo.", body_style))
    story.append(Paragraph("4. <b>Diseñar y construir un Dashboard Interactivo funcional</b> estructurado en dos páginas (Análisis General y Segmentación K-Means) con filtros dinámicos, KPIs clave y visualizaciones multidimensionales.", body_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # 4. DESCRIPCIÓN DEL DATASET
    # =========================================================================
    story.append(Paragraph("4. Descripción del Dataset", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>Fuente y Recolección:</b> El conjunto de datos proviene del catálogo especializado <i>'Movies & Entertainment Dataset (2024–2026)'</i> alojado en Kaggle. Captura metadatos contemporáneos de estrenos cinematográficos mundiales incluyendo títulos icónicos (ej. <i>Dune: Part Two</i>, <i>Inside Out 2</i>, <i>Deadpool & Wolverine</i>) y un amplio espectro de cine independiente y comercial.", body_style))

    story.append(Paragraph("<b>Dimensiones:</b> El conjunto de datos original cuenta con <b>916 registros (largometrajes)</b> y <b>20 variables</b> que abarcan dimensiones temporales, financieras, cualitativas y descriptivas.", body_style))

    # Tabla de variables
    var_table_data = [
        [Paragraph("Variable", table_header), Paragraph("Tipo", table_header), Paragraph("Descripción", table_header), Paragraph("Rol en el Proyecto", table_header)],
        [Paragraph("title", table_cell), Paragraph("String", table_cell), Paragraph("Título canónico del largometraje", table_cell), Paragraph("Identificador descriptivo", table_cell)],
        [Paragraph("release_year", table_cell), Paragraph("Integer", table_cell), Paragraph("Año de estreno oficial (2024 - 2026)", table_cell), Paragraph("Filtro y análisis temporal", table_cell)],
        [Paragraph("genres", table_cell), Paragraph("String", table_cell), Paragraph("Géneros cinematográficos separados por coma", table_cell), Paragraph("Ingeniería de primary_genre", table_cell)],
        [Paragraph("rating_out_of_10", table_cell), Paragraph("Float", table_cell), Paragraph("Calificación crítica y audiencia (0.0 a 10.0)", table_cell), Paragraph("<b>Variable Nuclear de Clustering</b>", table_cell)],
        [Paragraph("box_office_usd", table_cell), Paragraph("Float/Int", table_cell), Paragraph("Recaudación mundial bruta en dólares USD", table_cell), Paragraph("<b>Variable Nuclear de Clustering</b>", table_cell)],
        [Paragraph("budget_usd", table_cell), Paragraph("Float/Int", table_cell), Paragraph("Presupuesto de producción en dólares USD", table_cell), Paragraph("<b>Variable Nuclear de Clustering</b>", table_cell)],
        [Paragraph("vote_count", table_cell), Paragraph("Integer", table_cell), Paragraph("Volumen de votos emitidos por usuarios", table_cell), Paragraph("Evaluación de Configuración 2", table_cell)],
        [Paragraph("runtime_minutes", table_cell), Paragraph("Integer", table_cell), Paragraph("Duración del largometraje en minutos", table_cell), Paragraph("Variable de control exploratoria", table_cell)],
        [Paragraph("director / cast", table_cell), Paragraph("String", table_cell), Paragraph("Director(es) y elenco protagónico", table_cell), Paragraph("Metadatos para el Dashboard", table_cell)],
    ]
    t_vars = Table(var_table_data, colWidths=[90, 55, 205, 150])
    t_vars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_vars)

    story.append(PageBreak())

    # =========================================================================
    # 5. DESARROLLO DEL PROYECTO
    # =========================================================================
    story.append(Paragraph("5. Desarrollo del Proyecto", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>5.1 Limpieza y Preparación de Datos:</b>", h2_style))
    story.append(Paragraph("El preprocesamiento de los datos se llevó a cabo siguiendo las mejores prácticas de la minería de datos:", body_style))
    story.append(Paragraph("• <b>Tratamiento de Duplicados:</b> Se identificaron y eliminaron 2 registros duplicados por título, preservando una muestra final de <b>914 registros únicos</b>.", body_style))
    story.append(Paragraph("• <b>Tratamiento de Nulos:</b> Las columnas descriptivas `director` (305 nulos) y `screenwriter` (22 nulos) fueron imputadas con los valores 'Desconocido' y 'No especificado' respectivamente, garantizando integridad referencial sin descartar registros financieros válidos.", body_style))
    story.append(Paragraph("• <b>Ingeniería de Características:</b> Se calculó el <b>ROI %</b> (<i>Return on Investment</i>) mediante la fórmula $((\\text{box\\_office} - \\text{budget}) / \\text{budget}) \\times 100$, la <b>ganancia neta</b> en USD y la extracción del género principal (`primary_genre`).", body_style))
    story.append(Paragraph("• <b>Escalamiento Estadístico:</b> Dado que las variables numéricas poseen escalas intrínsecamente dispares (presupuestos en decenas de millones vs calificaciones de 0 a 10), se implementó <b>StandardScaler</b> de Scikit-learn para transformar los datos a media $\\mu = 0$ y desviación estándar $\\sigma = 1$, evitando que las variables con órdenes de magnitud superiores sesguen la distancia euclidiana.", body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>5.2 Exploración Visual Inicial:</b>", h2_style))
    story.append(Paragraph("Se construyeron visualizaciones exploratorias para entender el comportamiento de las variables antes de entrenar el algoritmo:", body_style))

    fig2_path = os.path.join('figures', 'exploratoria_2_presupuesto_vs_taquilla.png')
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=6.2*inch, height=2.8*inch))
        story.append(Paragraph("<i>Figura 1: Gráfica exploratoria de dispersión - Relación entre Presupuesto y Taquilla Mundial clasificada por Calificación.</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    story.append(Paragraph("<b>5.3 Implementación de K-Means y Selección de K:</b>", h2_style))
    story.append(Paragraph("Se evaluaron 6 valores de $K$ (de 2 a 7) registrando la inercia (suma de distancias al cuadrado a los centroides) y el Coeficiente de Silueta:", body_style))

    k_eval_data = [
        [Paragraph("Valor K", table_header), Paragraph("Inercia (WCSS)", table_header), Paragraph("Silhouette Score", table_header), Paragraph("Interpretación", table_header)],
        [Paragraph("2", table_cell), Paragraph("954.39", table_cell), Paragraph("0.8748", table_cell), Paragraph("División binaria trivial (Blockbusters vs Resto)", table_cell)],
        [Paragraph("3", table_cell), Paragraph("285.40", table_cell), Paragraph("0.5956", table_cell), Paragraph("Fuerte caída de inercia; colapsa grupos críticos", table_cell)],
        [Paragraph("<b>4 (Óptimo)</b>", table_cell), Paragraph("<b>159.92</b>", table_cell), Paragraph("<b>0.5368</b>", table_cell), Paragraph("<b>Punto de inflexión del codo y alta coherencia temática</b>", table_cell)],
        [Paragraph("5", table_cell), Paragraph("118.09", table_cell), Paragraph("0.4871", table_cell), Paragraph("Disminuye la silueta; sobrefragmentación", table_cell)],
        [Paragraph("6", table_cell), Paragraph("96.54", table_cell), Paragraph("0.4639", table_cell), Paragraph("Baja ganancia explicativa", table_cell)],
        [Paragraph("7", table_cell), Paragraph("79.01", table_cell), Paragraph("0.4628", table_cell), Paragraph("Clústeres redundantes con tamaños ínfimos", table_cell)],
    ]
    t_keval = Table(k_eval_data, colWidths=[65, 100, 110, 225])
    t_keval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#EBF8FF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_keval)

    story.append(PageBreak())

    # Gráfica del codo y silueta
    fig_elbow_path = os.path.join('figures', 'kmeans_metodo_codo_silueta.png')
    if os.path.exists(fig_elbow_path):
        story.append(Image(fig_elbow_path, width=6.5*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figura 2: Evaluación formal de K-Means mediante Método del Codo e Índice de Silueta (K=4 seleccionado).</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    story.append(Paragraph("<b>5.4 Comparación de Dos Configuraciones del Modelo (Requisito Parte 4):</b>", h2_style))
    story.append(Paragraph("Para dar estricto cumplimiento al lineamiento de contrastar dos configuraciones del modelo, se entrenaron dos variantes con K=4:", body_style))
    story.append(Paragraph("• <b>Configuración 1 (Seleccionada):</b> 3 variables nucleares (`budget_usd`, `box_office_usd`, `rating_out_of_10`). Obtiene una Inercia de <b>159.92</b> y un <b>Silhouette Score de 0.5368</b>.", body_style))
    story.append(Paragraph("• <b>Configuración 2 (Alternativa):</b> 4 variables (`budget_usd`, `box_office_usd`, `rating_out_of_10`, `vote_count`). Obtiene una Inercia de <b>781.14</b> y un <b>Silhouette Score de 0.3814</b>.", body_style))
    story.append(Paragraph("<b>Explicación de las Diferencias:</b> La Configuración 1 separa con nitidez la excelencia crítica y el rendimiento comercial. La inclusión de `vote_count` en la Configuración 2 penaliza severamente el coeficiente de silueta (-28.9%) debido a que el volumen de votos añade una dispersión artificial por 'viralidad' en redes sociales que distorsiona la cohesión de los grupos financieros y artísticos.", body_style))

    fig_cmp_path = os.path.join('figures', 'kmeans_comparativa_configuraciones.png')
    if os.path.exists(fig_cmp_path):
        story.append(Image(fig_cmp_path, width=6.5*inch, height=2.5*inch))
        story.append(Paragraph("<i>Figura 3: Comparación lado a lado de las dos configuraciones evaluadas (Configuración 1 óptima vs Configuración 2).</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    # =========================================================================
    # 6. RESULTADOS Y ANÁLISIS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Resultados y Análisis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>6.1 Asignación y Denominación de Clústeres:</b>", h2_style))
    story.append(Paragraph("A partir del modelo final ($K=4$, 3 variables escaladas), se asignó cada película a su clúster mediante `fit_predict()` y se calcularon los centroides tanto en escala estandarizada como en unidades originales del dominio:", body_style))

    res_table_data = [
        [Paragraph("Nombre Descriptivo del Clúster", table_header), Paragraph("Registros", table_header), Paragraph("Presupuesto Prom.", table_header), Paragraph("Taquilla Prom.", table_header), Paragraph("Rating Prom.", table_header), Paragraph("ROI Prom.", table_header)],
        [Paragraph("<b>Mega Blockbusters Taquilleros</b>", table_cell), Paragraph("20 (2.2%)", table_cell), Paragraph("$164,899,024", table_cell), Paragraph("$492,566,177", table_cell), Paragraph("7.61", table_cell), Paragraph("<b>198.7%</b>", table_cell)],
        [Paragraph("<b>Joyas Aclamadas por la Crítica</b>", table_cell), Paragraph("301 (32.9%)", table_cell), Paragraph("$21,312,214", table_cell), Paragraph("$31,142,144", table_cell), Paragraph("<b>8.69</b>", table_cell), Paragraph("58.6%", table_cell)],
        [Paragraph("<b>Producciones Comerciales Estándar</b>", table_cell), Paragraph("287 (31.4%)", table_cell), Paragraph("$21,233,024", table_cell), Paragraph("$31,313,811", table_cell), Paragraph("7.60", table_cell), Paragraph("60.3%", table_cell)],
        [Paragraph("<b>Bajo Desempeño Crítico</b>", table_cell), Paragraph("306 (33.5%)", table_cell), Paragraph("$21,557,914", table_cell), Paragraph("$30,700,681", table_cell), Paragraph("6.50", table_cell), Paragraph("51.8%", table_cell)],
    ]
    t_res = Table(res_table_data, colWidths=[150, 60, 85, 85, 60, 60])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_res)

    story.append(Spacer(1, 6))

    fig_disp_path = os.path.join('figures', 'kmeans_clusters_dispersion.png')
    if os.path.exists(fig_disp_path):
        story.append(Image(fig_disp_path, width=6.2*inch, height=3.1*inch))
        story.append(Paragraph("<i>Figura 4: Agrupamientos generados por K-Means (Presupuesto vs Taquilla) con centroides señalados en 'X'.</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    fig_box_path = os.path.join('figures', 'kmeans_comparativa_metricas.png')
    if os.path.exists(fig_box_path):
        story.append(Image(fig_box_path, width=6.2*inch, height=2.4*inch))
        story.append(Paragraph("<i>Figura 5: Comparación de distribuciones de Calificación y ROI (%) entre los cuatro segmentos identificados.</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    # =========================================================================
    # 7. DASHBOARD INTERACTIVO
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Dashboard Interactivo", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>Descripción General de la Herramienta:</b> Se desarrolló un Dashboard interactivo de alto impacto utilizando el framework <b>Streamlit</b> y la librería de gráficos dinámicos <b>Plotly</b>. La aplicación se organiza en una arquitectura de dos páginas completamente integradas:", body_style))

    story.append(Paragraph("<b>Página 1: Análisis General:</b> Proporciona una perspectiva exploratoria macroeconómica del dataset con 4 indicadores KPI (Total de películas, Taquilla acumulada en billones USD, Presupuesto promedio y Calificación promedio), histogramas de distribución, gráficos de dispersión con hover interactivo y un explorador tabular de registros.", body_style))

    dash1_path = os.path.join('figures', 'dashboard_pagina1_analisis_general.png')
    if os.path.exists(dash1_path):
        story.append(Image(dash1_path, width=6.2*inch, height=3.2*inch))
        story.append(Paragraph("<i>Figura 6: Captura de pantalla de la Página 1 del Dashboard: Análisis General y Exploratorio.</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=10)))

    story.append(Paragraph("<b>Página 2: Segmentación mediante K-Means:</b> Presenta los resultados del modelo de aprendizaje no supervisado. Incluye métricas del algoritmo (K=4, Silueta = 0.537), la distribución de títulos por clúster, el gráfico de dispersión interactivo con centroides, boxplots comparativos de Calificación y ROI, la tabla de estadísticas descriptivas y fichas descriptivas de cada arquetipo fílmico.", body_style))

    dash2_path = os.path.join('figures', 'dashboard_pagina2_segmentacion_kmeans.png')
    if os.path.exists(dash2_path):
        story.append(Image(dash2_path, width=6.2*inch, height=3.2*inch))
        story.append(Paragraph("<i>Figura 7: Captura de pantalla de la Página 2 del Dashboard: Segmentación no supervisada mediante K-Means.</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#718096'), alignment=1, spaceAfter=8)))

    # =========================================================================
    # 8. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("8. Conclusiones y Recomendaciones", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("<b>8.1 Principales Hallazgos:</b>", h2_style))
    story.append(Paragraph("1. <b>El Efecto 'Blockbuster' y la Concentración Financiera:</b> Solo el 2.2% de los largometrajes analizados constituyen la categoría de Mega Blockbusters. No obstante, este reducido grupo promedia más de $492M USD en taquilla con un ROI cercano al 200%, confirmando que las producciones de gran espectáculo siguen siendo el pilar de liquidez de la industria.", body_style))
    story.append(Paragraph("2. <b>Independencia entre Inversión Monetaria y Calidad Artística:</b> La correlación entre presupuesto y calificación es nula (-0.002). El clúster de <i>Joyas Aclamadas por la Crítica</i> (301 películas) alcanza una nota promedio sobresaliente de 8.69 con un presupuesto medio contenido ($21.3M USD), evidenciando que el talento narrativo no depende linealmente de presupuestos astronómicos.", body_style))
    story.append(Paragraph("3. <b>La Zona Crítica de Ineficiencia:</b> Un tercio del mercado (306 producciones) cae en el grupo de <i>Bajo Desempeño Crítico</i> (rating promedio 6.50). Estas películas consumen un capital similar (~$21.5M USD) al de las producciones exitosas, pero obtienen el menor retorno financiero (51.8%) y una débil resonancia en el público.", body_style))

    story.append(Paragraph("<b>8.2 Recomendaciones Derivadas del Análisis:</b>", h2_style))
    story.append(Paragraph("1. <b>Estrategia de Portafolio Bi-Modal:</b> Las casas productoras deben equilibrar sus inversiones financiando un número acotado de franquicias de alto presupuesto respaldadas por marcas establecidas, combinado con un catálogo diversificado de películas de presupuesto medio-bajo enfocado en guiones de alta calidad.", body_style))
    story.append(Paragraph("2. <b>Mecanismos de Control Temprano de Calidad:</b> Para las películas en el rango de los $20M a $25M USD, se recomienda establecer filtros rigurosos de preproducción y proyecciones de prueba para evitar que proyectos con fallas estructurales entren a la zona de bajo desempeño crítico.", body_style))
    story.append(Paragraph("3. <b>Ventanas de Exhibición Personalizadas:</b> Los títulos clasificados como <i>Joyas Críticas</i> deben capitalizar el marketing de boca a boca mediante circuitos de festivales y ventanas de exclusividad en streaming, donde la aclamación de la audiencia genera retención de suscriptores sin el costo de campañas masivas de publicidad en salas.", body_style))

    story.append(Paragraph("<b>8.3 Limitaciones del Modelo:</b>", h2_style))
    story.append(Paragraph("• <b>Naturaleza Esférica de K-Means:</b> K-Means asume clústeres globulares y homogéneos de varianza similar. En la industria cinematográfica, la presencia de valores atípicos multimillonarios (super blockbusters) puede distorsionar levemente la posición de los centroides.", body_style))
    story.append(Paragraph("• <b>Ausencia de Gastos de Mercadotecnia (P&A):</b> Los presupuestos reportados reflejan exclusivamente el costo de producción, sin incluir los gastos de publicidad y promoción que suelen representar un 50% a 100% adicional del costo del filme.", body_style))
    story.append(Paragraph("• <b>Sensibilidad a la Inicialización:</b> Aunque se mitigó utilizando `n_init=10` y semilla aleatoria controlada (`random_state=42`), K-Means requiere validar su estabilidad ante nuevas distribuciones de datos.", body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E0'), spaceBefore=5, spaceAfter=15))
    story.append(Paragraph("<b>Fin del Reporte Oficial de Documentación</b> | Código, notebooks y datasets disponibles en el repositorio público de GitHub.", ParagraphStyle('FinalNote', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#2B6CB0'), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documento PDF generado exitosamente en '{filename}'.")


if __name__ == '__main__':
    pdf_output = os.path.join('docs', 'documentacion_proyecto.pdf')
    build_pdf(pdf_output)
