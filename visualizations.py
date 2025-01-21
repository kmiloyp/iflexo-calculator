import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List

def create_costos_comparison(ahorros: Dict[str, float]) -> go.Figure:
    """Crear gráfico de barras para comparar los diferentes tipos de ahorro."""
    categorias = {
        'planchas': 'Planchas',
        'velocidad_ajuste': 'Velocidad de Ajuste',
        'velocidad_impresion': 'Velocidad en Impresión',
        'tinta_blanca': 'Tinta Blanca',
        'tintas': 'Tintas',
        'plancha_parada': 'Plancha-Parada'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(categorias.values()),
            y=[ahorros[k] for k in categorias.keys()],
            text=[f"${v:,.1f}" for v in [ahorros[k] for k in categorias.keys()]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Comparación de Ahorros por Categoría",
        xaxis_title="Categoría",
        yaxis_title="Ahorro ($)",
        template="plotly_white"
    )
    
    return fig

def create_tiempo_paradas_comparison(tiempo_actual: float, tiempo_iflexo: float) -> go.Figure:
    """Crear gráfico para comparar tiempos de parada."""
    fig = go.Figure(data=[
        go.Bar(
            x=['Actual', 'Con iFlexo'],
            y=[tiempo_actual, tiempo_iflexo],
            text=[f"{v:,.1f} hrs" for v in [tiempo_actual, tiempo_iflexo]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Comparación de Tiempo en Paradas de Prensa",
        xaxis_title="Escenario",
        yaxis_title="Tiempo (horas/año)",
        template="plotly_white"
    )
    
    return fig

def create_velocidad_comparison(velocidad_actual: float, velocidad_iflexo: float) -> go.Figure:
    """Crear gráfico para comparar velocidades."""
    fig = go.Figure(data=[
        go.Bar(
            x=['Actual', 'Con iFlexo'],
            y=[velocidad_actual, velocidad_iflexo],
            text=[f"{v:,.1f} m/min" for v in [velocidad_actual, velocidad_iflexo]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Comparación de Velocidades",
        xaxis_title="Escenario",
        yaxis_title="Velocidad (m/min)",
        template="plotly_white"
    )
    
    return fig

def create_tinta_comparison(consumo_actual: float, ahorro: float, tipo: str = "blanca") -> go.Figure:
    """Crear gráfico para comparar consumo de tinta."""
    consumo_iflexo = consumo_actual - ahorro
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Actual', 'Con iFlexo'],
            y=[consumo_actual, consumo_iflexo],
            text=[f"{v:,.1f} kg" for v in [consumo_actual, consumo_iflexo]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f"Comparación de Consumo de Tinta {tipo.title()}",
        xaxis_title="Escenario",
        yaxis_title="Consumo (kg/año)",
        template="plotly_white"
    )
    
    return fig
