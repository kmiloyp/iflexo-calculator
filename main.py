{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import datetime\
from io import StringIO, BytesIO\
from visualizations import (\
    create_costos_comparison,\
    create_tiempo_paradas_comparison,\
    create_velocidad_comparison,\
    create_tinta_comparison\
)\
from pdf_report import generate_pdf_report\
import os\
from PIL import Image\
\
# Configuraci\'f3n de la p\'e1gina\
st.set_page_config(\
    page_title="Calculadora de Eficiencia en Costos de Impresi\'f3n",\
    page_icon="\uc0\u55357 \u56496 ",\
    layout="wide",\
    initial_sidebar_state="collapsed"\
)\
\
[... resto del c\'f3digo del archivo main.py ...]}