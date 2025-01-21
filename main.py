import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image
import os

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Calculadora de Eficiencia en Costos de Impresión",
        page_icon="💰",
        layout="wide"
    )

    # Cargar y mostrar el logo
    try:
        logo_path = "attached_assets/iflexo6-sm-kit.jpg"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, width=200)
    except Exception as e:
        st.warning("Logo no encontrado")

    st.title("Calculadora de Eficiencia en Costos de Impresión")

    # Inicializar variables de estado en session_state
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
        "Costo de Planchas"
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

if __name__ == "__main__":
    main()
