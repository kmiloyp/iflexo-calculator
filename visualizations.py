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

    # Crear gráfico de barras con mejoras visuales
    fig = go.Figure(data=[
        go.Bar(
            x=list(categorias.values()),
            y=[ahorros[k] for k in categorias.keys()],
            text=[f"${v:,.1f}" for v in [ahorros[k] for k in categorias.keys()]],
            textposition='auto',
            marker_color='rgb(55, 83, 109)',
            hovertemplate='<b>%{x}</b><br>' +
                         'Ahorro: $%{y:,.1f}<br>' +
                         '<extra></extra>'
        )
    ])

    fig.update_layout(
        title={
            'text': "Comparación de Ahorros por Categoría",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Categoría",
        yaxis_title="Ahorro ($)",
        template="plotly_white",
        showlegend=False,
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=100, l=70, r=40, b=80)
    )

    return fig

def create_costos_pie(ahorros: Dict[str, float]) -> go.Figure:
    """Crear gráfico circular para mostrar la distribución de ahorros."""
    categorias = {
        'planchas': 'Planchas',
        'velocidad_ajuste': 'Velocidad de Ajuste',
        'velocidad_impresion': 'Velocidad en Impresión',
        'tinta_blanca': 'Tinta Blanca',
        'tintas': 'Tintas',
        'plancha_parada': 'Plancha-Parada'
    }

    valores = [ahorros[k] for k in categorias.keys()]
    nombres = list(categorias.values())

    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=valores,
        hole=.3,
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>" +
                     "Ahorro: $%{value:,.1f}<br>" +
                     "Porcentaje: %{percent}<br>" +
                     "<extra></extra>"
    )])

    fig.update_layout(
        title={
            'text': "Distribución de Ahorros",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def create_tiempo_paradas_comparison(tiempo_actual: float, tiempo_iflexo: float) -> go.Figure:
    """Crear gráfico para comparar tiempos de parada con visualización mejorada."""
    fig = go.Figure()

    # Agregar barras con gradiente de color
    fig.add_trace(go.Bar(
        x=['Actual', 'Con iFlexo'],
        y=[tiempo_actual, tiempo_iflexo],
        text=[f"{v:,.1f} hrs" for v in [tiempo_actual, tiempo_iflexo]],
        textposition='auto',
        marker=dict(
            color=['rgba(255, 75, 75, 0.8)', 'rgba(75, 192, 192, 0.8)']
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "Tiempo: %{y:,.1f} hrs<br>" +
                     "<extra></extra>"
    ))

    # Agregar línea de conexión
    fig.add_trace(go.Scatter(
        x=['Actual', 'Con iFlexo'],
        y=[tiempo_actual, tiempo_iflexo],
        mode='lines',
        line=dict(color='rgba(0,0,0,0.3)', dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        title={
            'text': "Comparación de Tiempo en Paradas de Prensa",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Escenario",
        yaxis_title="Tiempo (horas/año)",
        template="plotly_white",
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=100, l=70, r=40, b=80)
    )

    return fig

def create_velocidad_radar(velocidad_actual: float, velocidad_iflexo: float, 
                         tiempo_ajuste_actual: float, tiempo_ajuste_iflexo: float,
                         consumo_tinta_actual: float, consumo_tinta_iflexo: float) -> go.Figure:
    """Crear gráfico de radar para comparación multidimensional de mejoras."""

    categorias = ['Velocidad', 'Tiempo de Ajuste', 'Consumo de Tinta']

    # Calcular porcentajes de mejora (normalizado a escala 0-100)
    actual_values = [
        100,  # Velocidad actual como base
        100,  # Tiempo ajuste actual como base
        100   # Consumo tinta actual como base
    ]

    # Calcular valores relativos para iFlexo
    iflexo_values = [
        (velocidad_iflexo/velocidad_actual) * 100,
        (tiempo_ajuste_iflexo/tiempo_ajuste_actual) * 100,
        (consumo_tinta_iflexo/consumo_tinta_actual) * 100
    ]

    fig = go.Figure()

    # Agregar datos actuales
    fig.add_trace(go.Scatterpolar(
        r=actual_values,
        theta=categorias,
        fill='toself',
        name='Actual',
        line_color='rgb(255, 75, 75)'
    ))

    # Agregar datos con iFlexo
    fig.add_trace(go.Scatterpolar(
        r=iflexo_values,
        theta=categorias,
        fill='toself',
        name='Con iFlexo',
        line_color='rgb(75, 192, 192)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title={
            'text': "Análisis Comparativo Multidimensional",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    return fig

def create_waterfall_chart(ahorros: Dict[str, float]) -> go.Figure:
    """Crear gráfico de cascada para mostrar el impacto acumulativo de los ahorros."""
    categorias = {
        'planchas': 'Planchas',
        'velocidad_ajuste': 'Velocidad de Ajuste',
        'velocidad_impresion': 'Velocidad en Impresión',
        'tinta_blanca': 'Tinta Blanca',
        'tintas': 'Tintas',
        'plancha_parada': 'Plancha-Parada'
    }

    # Preparar datos para el waterfall
    x = list(categorias.values()) + ['Total']
    y = [ahorros[k] for k in categorias.keys()] + [sum(ahorros.values())]

    # Configurar los colores y el modo de medida
    measure = ['relative'] * len(categorias) + ['total']

    fig = go.Figure(go.Waterfall(
        name="Análisis de Ahorros",
        orientation="v",
        measure=measure,
        x=x,
        textposition="outside",
        text=[f"${val:,.1f}" for val in y],
        y=y,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "rgb(255, 75, 75)"}},
        increasing={"marker": {"color": "rgb(75, 192, 192)"}},
        totals={"marker": {"color": "rgb(55, 83, 109)"}},
        hovertemplate="<b>%{x}</b><br>" +
                     "Ahorro: $%{y:,.1f}<br>" +
                     "<extra></extra>"
    ))

    fig.update_layout(
        title={
            'text': "Análisis de Impacto Acumulativo de Ahorros",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        xaxis_title="Categoría",
        yaxis_title="Ahorro ($)",
        waterfallgap=0.2,
        template="plotly_white",
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=100, l=70, r=40, b=80)
    )

    return fig

def create_tinta_comparison(consumo_actual: float, ahorro: float, tipo: str = "blanca") -> go.Figure:
    """Crear gráfico mejorado para comparar consumo de tinta."""
    consumo_iflexo = consumo_actual - ahorro

    fig = go.Figure()

    # Agregar barras con diseño mejorado
    fig.add_trace(go.Bar(
        x=['Actual', 'Con iFlexo'],
        y=[consumo_actual, consumo_iflexo],
        text=[f"{v:,.1f} kg" for v in [consumo_actual, consumo_iflexo]],
        textposition='auto',
        marker_color=['rgba(255, 75, 75, 0.8)', 'rgba(75, 192, 192, 0.8)'],
        hovertemplate="<b>%{x}</b><br>" +
                     "Consumo: %{y:,.1f} kg<br>" +
                     "<extra></extra>"
    ))

    # Agregar línea de tendencia
    fig.add_trace(go.Scatter(
        x=['Actual', 'Con iFlexo'],
        y=[consumo_actual, consumo_iflexo],
        mode='lines',
        line=dict(color='rgba(0,0,0,0.3)', dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        title={
            'text': f"Comparación de Consumo de Tinta {tipo.title()}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Escenario",
        yaxis_title="Consumo (kg/año)",
        template="plotly_white",
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=100, l=70, r=40, b=80)
    )

    return fig
