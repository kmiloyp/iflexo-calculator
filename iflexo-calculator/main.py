import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO, BytesIO
from visualizations import (
    create_costos_comparison,
    create_tiempo_paradas_comparison,
    create_velocidad_comparison,
    create_tinta_comparison
)
from pdf_report import generate_pdf_report
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Eficiencia en Costos de Impresión",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)
