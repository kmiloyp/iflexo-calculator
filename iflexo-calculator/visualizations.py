{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import plotly.graph_objects as go\
import plotly.express as px\
from typing import Dict, List\
\
def create_costos_comparison(ahorros: Dict[str, float]) -> go.Figure:\
    """Crear gr\'e1fico de barras para comparar los diferentes tipos de ahorro."""\
    categorias = \{\
        'planchas': 'Planchas',\
        'velocidad_ajuste': 'Velocidad de Ajuste',\
        'velocidad_impresion': 'Velocidad en Impresi\'f3n',\
        'tinta_blanca': 'Tinta Blanca',\
        'tintas': 'Tintas',\
        'plancha_parada': 'Plancha-Parada'\
    \}\
    \
    fig = go.Figure(data=[\
        go.Bar(\
            x=list(categorias.values()),\
            y=[ahorros[k] for k in categorias.keys()],\
            text=[f"$\{v:,.1f\}" for v in [ahorros[k] for k in categorias.keys()]],\
            textposition='auto',\
        )\
    ])\
    \
    fig.update_layout(\
        title="Comparaci\'f3n de Ahorros por Categor\'eda",\
        xaxis_title="Categor\'eda",\
        yaxis_title="Ahorro ($)",\
        template="plotly_white"\
    )\
    \
    return fig\
\
def create_tiempo_paradas_comparison(tiempo_actual: float, tiempo_iflexo: float) -> go.Figure:\
    """Crear gr\'e1fico para comparar tiempos de parada."""\
    fig = go.Figure(data=[\
        go.Bar(\
            x=['Actual', 'Con iFlexo'],\
            y=[tiempo_actual, tiempo_iflexo],\
            text=[f"\{v:,.1f\} hrs" for v in [tiempo_actual, tiempo_iflexo]],\
            textposition='auto',\
        )\
    ])\
    \
    fig.update_layout(\
        title="Comparaci\'f3n de Tiempo en Paradas de Prensa",\
        xaxis_title="Escenario",\
        yaxis_title="Tiempo (horas/a\'f1o)",\
        template="plotly_white"\
    )\
    \
    return fig\
\
def create_velocidad_comparison(velocidad_actual: float, velocidad_iflexo: float) -> go.Figure:\
    """Crear gr\'e1fico para comparar velocidades."""\
    fig = go.Figure(data=[\
        go.Bar(\
            x=['Actual', 'Con iFlexo'],\
            y=[velocidad_actual, velocidad_iflexo],\
            text=[f"\{v:,.1f\} m/min" for v in [velocidad_actual, velocidad_iflexo]],\
            textposition='auto',\
        )\
    ])\
    \
    fig.update_layout(\
        title="Comparaci\'f3n de Velocidades",\
        xaxis_title="Escenario",\
        yaxis_title="Velocidad (m/min)",\
        template="plotly_white"\
    )\
    \
    return fig\
\
def create_tinta_comparison(consumo_actual: float, ahorro: float, tipo: str = "blanca") -> go.Figure:\
    """Crear gr\'e1fico para comparar consumo de tinta."""\
    consumo_iflexo = consumo_actual - ahorro\
    \
    fig = go.Figure(data=[\
        go.Bar(\
            x=['Actual', 'Con iFlexo'],\
            y=[consumo_actual, consumo_iflexo],\
            text=[f"\{v:,.1f\} kg" for v in [consumo_actual, consumo_iflexo]],\
            textposition='auto',\
        )\
    ])\
    \
    fig.update_layout(\
        title=f"Comparaci\'f3n de Consumo de Tinta \{tipo.title()\}",\
        xaxis_title="Escenario",\
        yaxis_title="Consumo (kg/a\'f1o)",\
        template="plotly_white"\
    )\
    \
    return fig}