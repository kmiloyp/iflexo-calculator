import streamlit as st
import pandas as pd
from visualizations import (
    create_costos_comparison,
    create_tiempo_paradas_comparison,
    create_velocidad_comparison,
    create_tinta_comparison
)
from pdf_report import generate_pdf_report
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Eficiencia en Costos de Impresión",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos personalizados para mejorar la responsividad
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        white-space: pre-wrap;
        min-width: 100px;
        flex-grow: 1;
        padding: 10px 5px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 14px;
    }
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 12px;
            padding: 8px 4px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Logo y título
col1, col2 = st.columns([1, 3])
with col1:
    try:
        image = Image.open("attached_assets/iflexo6-sm-kit.jpg")
        st.image(image, width=200)
    except Exception as e:
        st.error(f"Error al cargar el logo: {str(e)}")

with col2:
    st.title("Calculadora de Eficiencia en Costos de Impresión")

st.markdown("""
Esta calculadora te ayuda a determinar los ahorros potenciales en tu proceso de impresión,
considerando diferentes factores como costos de planchas, velocidad de prensa y consumo de tintas.
""")

# Inicializar variables de estado si no existen
if 'ahorros' not in st.session_state:
    st.session_state.ahorros = {
        'planchas': 0.0,
        'velocidad_ajuste': 0.0,
        'velocidad_impresion': 0.0,
        'tinta_blanca': 0.0,
        'tintas': 0.0,
        'plancha_parada': 0.0
    }

# Crear las pestañas para cada sección
tabs = st.tabs([
    "Menú Principal",
    "Costo de Planchas",
    "Velocidad de Ajuste",
    "Velocidad en Impresión",
    "Relación Plancha-Parada",
    "Ahorro en Tinta Blanca",
    "Ahorro en Tintas"
])

# Pestaña: Menú Principal
with tabs[0]:
    st.header("Resumen de Costos")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Ahorro en Costo de Planchas", f"${st.session_state.ahorros['planchas']:,.1f} /año")
        st.metric("Ahorro en Velocidad de Ajuste", f"${st.session_state.ahorros['velocidad_ajuste']:,.1f} /año")
        st.metric("Ahorro en Velocidad de Impresión", f"${st.session_state.ahorros['velocidad_impresion']:,.1f} /año")

    with col2:
        st.metric("Ahorro en Tinta Blanca", f"${st.session_state.ahorros['tinta_blanca']:,.1f} /año")
        st.metric("Ahorro en Tintas", f"${st.session_state.ahorros['tintas']:,.1f} /año")
        st.metric("Ahorro por Relación Plancha-Parada", f"${st.session_state.ahorros['plancha_parada']:,.1f} /año")
        ahorro_total = sum(st.session_state.ahorros.values())
        st.metric("Ahorro Total Anual", f"${ahorro_total:,.1f} /año")

    # Agregar gráfico de comparación de ahorros
    st.plotly_chart(create_costos_comparison(st.session_state.ahorros))

    # Botón para generar reporte PDF
    if st.button("Generar Reporte PDF"):
        pdf_buffer = generate_pdf_report(st.session_state.ahorros, {})
        st.download_button(
            label="Descargar Reporte PDF",
            data=pdf_buffer,
            file_name="reporte_eficiencia_costos.pdf",
            mime="application/pdf"
        )

# Pestaña: Costo de Planchas
with tabs[1]:
    st.header("Cálculo de Costo de Planchas")

    consumo_planchas = st.number_input(
        "Consumo de planchas (unidades/año)",
        min_value=0,
        format="%d",
        key="consumo_planchas"
    )

    costo_actual = st.number_input(
        "Actual costo de plancha (/cm²)",
        min_value=0.0,
        format="%.1f",
        key="costo_actual_plancha"
    )

    costo_iflexo = st.number_input(
        "Costo de plancha iFlexo (/cm²)",
        min_value=0.0,
        format="%.1f",
        key="costo_iflexo_plancha"
    )

    if all([consumo_planchas, costo_actual, costo_iflexo]):
        diferencia = ((costo_actual - costo_iflexo) / costo_actual) * 100
        gasto_actual = consumo_planchas * costo_actual
        gasto_iflexo = consumo_planchas * costo_iflexo
        diferencia_gasto = gasto_actual - gasto_iflexo

        st.metric("Diferencia en costo con iFlexo", f"{diferencia:.1f}%")
        st.metric("Actual gasto en planchas", f"${gasto_actual:,.1f} /año")
        st.metric("Gasto en planchas con iFlexo", f"${gasto_iflexo:,.1f} /año")
        st.metric("Diferencia en gasto de planchas con iFlexo", f"${diferencia_gasto:,.1f} /año")
        st.session_state.ahorros['planchas'] = diferencia_gasto

# Pestaña: Velocidad de Ajuste
with tabs[2]:
    st.header("Cálculo de Velocidad de Ajuste")

    num_trabajos = st.number_input(
        "Número de trabajos (trabajos/año)",
        min_value=0,
        format="%d",
        key="num_trabajos_ajuste"
    )

    valor_hora_prensa = st.number_input(
        "Valor de hora en prensa (/hora)",
        min_value=0.0,
        format="%.1f",
        key="valor_hora_ajuste"
    )

    tiempo_ajuste_actual = st.number_input(
        "Tiempo actual de ajuste (minutos)",
        min_value=0,
        format="%d",
        key="tiempo_ajuste_actual"
    )

    diferencia_tiempo_ajuste = st.number_input(
        "Diferencia de tiempo de ajuste de prensa con iFlexo (minutos)",
        min_value=0,
        format="%d",
        key="diferencia_tiempo_ajuste"
    )

    metros_material_actual = st.number_input(
        "Metros actuales de material en ajuste de prensa (m)",
        min_value=0.0,
        format="%.1f",
        key="metros_material_actual"
    )

    costo_material = st.number_input(
        "Costo de material (/m)",
        min_value=0.0,
        format="%.1f",
        key="costo_material"
    )

    diferencia_material = st.number_input(
        "Diferencia con iFlexo (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.1f",
        key="diferencia_material"
    )

    if all([num_trabajos, valor_hora_prensa, tiempo_ajuste_actual, diferencia_tiempo_ajuste,
            metros_material_actual, costo_material, diferencia_material]):
        # Cálculos de tiempo
        tiempo_ajuste_iflexo = tiempo_ajuste_actual - diferencia_tiempo_ajuste
        tiempo_ahorrado = diferencia_tiempo_ajuste * num_trabajos
        tiempo_ahorrado_horas = tiempo_ahorrado / 60  # Convertir a horas
        ahorro_tiempo = (tiempo_ahorrado / 60) * valor_hora_prensa

        # Cálculos de material
        metros_material_iflexo = metros_material_actual * (1 - diferencia_material/100)
        ahorro_material_metros = (metros_material_actual - metros_material_iflexo) * num_trabajos  # metros/año
        ahorro_material = ahorro_material_metros * costo_material

        # Métricas
        st.metric("Tiempo promedio de ajuste de prensa con iFlexo", f"{tiempo_ajuste_iflexo:,.1f} minutos")
        st.metric("Tiempo ahorrado con iFlexo", f"{tiempo_ahorrado_horas:,.1f} horas/año")
        st.metric("Metros de material en ajuste de prensa con iFlexo", f"{metros_material_iflexo:,.1f} m")
        st.metric("Ahorro en desperdicio de material con iFlexo", f"{ahorro_material_metros:,.1f} metros/año")
        st.metric("Ahorro en costos con iFlexo", f"${(ahorro_tiempo + ahorro_material):,.1f} /año")

        st.session_state.ahorros['velocidad_ajuste'] = ahorro_tiempo + ahorro_material
        st.plotly_chart(create_tiempo_paradas_comparison(tiempo_ajuste_actual, tiempo_ajuste_iflexo))


# Pestaña: Velocidad en Impresión
with tabs[3]:
    st.header("Cálculo de Velocidad en Impresión")

    tiempo_prensa = st.number_input(
        "Tiempo en prensa disponible (horas/año)",
        min_value=0.0,
        format="%.1f",
        key="tiempo_prensa_impresion"
    )

    valor_hora = st.number_input(
        "Valor de hora en prensa (/hora)",
        min_value=0.0,
        format="%.1f",
        key="valor_hora_impresion"
    )

    velocidad_actual = st.number_input(
        "Velocidad actual (m/min)",
        min_value=0.0,
        format="%.1f",
        key="velocidad_actual"
    )

    velocidad_iflexo = st.number_input(
        "Velocidad con iFlexo (m/min)",
        min_value=0.0,
        format="%.1f",
        key="velocidad_iflexo"
    )

    if all([tiempo_prensa, valor_hora, velocidad_actual, velocidad_iflexo]):
        mejora_velocidad = ((velocidad_iflexo - velocidad_actual) / velocidad_actual) * 100
        ahorro_velocidad = tiempo_prensa * valor_hora * (mejora_velocidad / 100)
        capacidad_adicional = (velocidad_iflexo - velocidad_actual) * tiempo_prensa * 60  # en metros
        ahorro_tiempo = tiempo_prensa * (mejora_velocidad / 100)  # en horas

        st.metric("Mejora en velocidad", f"{mejora_velocidad:.1f}%")
        st.metric("Capacidad adicional con iFlexo", f"{capacidad_adicional:,.1f} m/año")
        st.metric("Ahorro en tiempo con iFlexo", f"{ahorro_tiempo:,.1f} horas/año")
        st.metric("Ahorro estimado", f"${ahorro_velocidad:,.1f} /año")

        st.session_state.ahorros['velocidad_impresion'] = ahorro_velocidad
        st.plotly_chart(create_velocidad_comparison(velocidad_actual, velocidad_iflexo))

# Pestaña: Relación Plancha-Parada
with tabs[4]:
    st.header("Relación Plancha-Parada")

    num_trabajos_parada = st.number_input(
        "Número de trabajos (trabajos/año)",
        min_value=0,
        format="%d",
        key="num_trabajos_parada"
    )

    valor_hora_parada = st.number_input(
        "Valor de hora en prensa (/hora)",
        min_value=0.0,
        format="%.1f",
        key="valor_hora_parada"
    )

    tiempo_parada = st.number_input(
        "Tiempo promedio por cada parada de prensa (minutos)",
        min_value=0,
        format="%d",
        key="tiempo_parada"
    )

    paradas_actual = st.number_input(
        "Número de paradas promedio por trabajo actual",
        min_value=0.0,
        format="%.1f",
        key="paradas_actual"
    )

    paradas_iflexo = st.number_input(
        "Número de paradas promedio por trabajo con iFlexo",
        min_value=0.0,
        format="%.1f",
        key="paradas_iflexo"
    )

    if all([num_trabajos_parada, valor_hora_parada, tiempo_parada, paradas_actual, paradas_iflexo]):
        tiempo_actual = tiempo_parada * paradas_actual * num_trabajos_parada
        tiempo_iflexo = tiempo_parada * paradas_iflexo * num_trabajos_parada
        diferencia_tiempo = tiempo_actual - tiempo_iflexo
        diferencia_porcentual = ((paradas_actual - paradas_iflexo) / paradas_actual) * 100
        ahorro_costos = (diferencia_tiempo / 60) * valor_hora_parada

        # Convertir tiempos a horas para mostrar
        tiempo_actual_horas = tiempo_actual / 60
        tiempo_iflexo_horas = tiempo_iflexo / 60
        diferencia_tiempo_horas = diferencia_tiempo / 60

        st.metric("Diferencia de tiempo de ajuste de prensa con iFlexo", f"{diferencia_tiempo_horas:,.1f} horas/año")
        st.metric("Tiempo en paradas de prensa actuales", f"{tiempo_actual_horas:,.1f} horas/año")
        st.metric("Tiempo en paradas de prensa con iFlexo", f"{tiempo_iflexo_horas:,.1f} horas/año")
        st.metric("Diferencia con iFlexo", f"{diferencia_porcentual:.1f}%")
        st.metric("Ahorro en costos con iFlexo", f"${ahorro_costos:,.1f} /año")

        st.session_state.ahorros['plancha_parada'] = ahorro_costos
        st.plotly_chart(create_tiempo_paradas_comparison(tiempo_actual_horas, tiempo_iflexo_horas))

# Pestaña: Ahorro en Tinta Blanca
with tabs[5]:
    st.header("Ahorro en Tinta Blanca")

    consumo_tinta_blanca = st.number_input(
        "Actual consumo de tinta blanca (kg/año)",
        min_value=0.0,
        format="%.1f",
        key="consumo_tinta_blanca"
    )

    costo_tinta_blanca = st.number_input(
        "Costo de tinta blanca (/kg)",
        min_value=0.0,
        format="%.1f",
        key="costo_tinta_blanca"
    )

    reduccion_consumo_blanca = st.number_input(
        "Reducción de consumo (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.1f",
        key="reduccion_consumo_blanca"
    )

    if all([consumo_tinta_blanca, costo_tinta_blanca, reduccion_consumo_blanca]):
        gasto_actual = consumo_tinta_blanca * costo_tinta_blanca
        ahorro_tinta_blanca = gasto_actual * (reduccion_consumo_blanca / 100)
        ahorro_kg_blanca = consumo_tinta_blanca * (reduccion_consumo_blanca / 100)

        st.metric("Gasto actual en tinta blanca", f"${gasto_actual:,.1f} /año")
        st.metric("Ahorro en tinta blanca con iFlexo", f"${ahorro_tinta_blanca:,.1f} /año")
        st.metric("Ahorro en tinta blanca con iFlexo", f"{ahorro_kg_blanca:,.1f} kg/año")
        st.session_state.ahorros['tinta_blanca'] = ahorro_tinta_blanca
        st.plotly_chart(create_tinta_comparison(consumo_tinta_blanca, ahorro_kg_blanca, "blanca"))

# Pestaña: Ahorro en Tintas
with tabs[6]:
    st.header("Ahorro en Tintas")

    consumo_tinta = st.number_input(
        "Actual consumo de tinta no blanca (kg/año)",
        min_value=0.0,
        format="%.1f",
        key="consumo_tinta"
    )

    costo_tinta = st.number_input(
        "Promedio costo de tinta (/kg)",
        min_value=0.0,
        format="%.1f",
        key="costo_tinta"
    )

    reduccion_consumo = st.number_input(
        "Reducción de consumo (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.1f",
        key="reduccion_consumo"
    )

    if all([consumo_tinta, costo_tinta, reduccion_consumo]):
        gasto_actual = consumo_tinta * costo_tinta
        ahorro_tintas = gasto_actual * (reduccion_consumo / 100)
        ahorro_kg_tintas = consumo_tinta * (reduccion_consumo / 100)

        st.metric("Gasto actual en tintas", f"${gasto_actual:,.1f} /año")
        st.metric("Ahorro en tintas con iFlexo", f"${ahorro_tintas:,.1f} /año")
        st.metric("Ahorro en tinta no blanca con iFlexo", f"{ahorro_kg_tintas:,.1f} kg/año")
        st.session_state.ahorros['tintas'] = ahorro_tintas
        st.plotly_chart(create_tinta_comparison(consumo_tinta, ahorro_kg_tintas, "no blanca"))
