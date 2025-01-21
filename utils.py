import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

def load_file(uploaded_file):
    """Carga el archivo subido en un DataFrame de pandas."""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(uploaded_file)
        else:
            raise ValueError("Formato de archivo no soportado")
    except Exception as e:
        raise Exception(f"Error al cargar el archivo: {str(e)}")

def generate_plot(df, plot_type, x_column, y_column):
    """Genera diferentes tipos de gráficos usando Plotly."""
    if plot_type == "Líneas":
        fig = px.line(df, x=x_column, y=y_column, 
                     title=f'Gráfico de líneas: {y_column} vs {x_column}')
    elif plot_type == "Barras":
        fig = px.bar(df, x=x_column, y=y_column,
                    title=f'Gráfico de barras: {y_column} vs {x_column}')
    elif plot_type == "Dispersión":
        fig = px.scatter(df, x=x_column, y=y_column,
                        title=f'Gráfico de dispersión: {y_column} vs {x_column}')
    elif plot_type == "Área":
        fig = px.area(df, x=x_column, y=y_column,
                     title=f'Gráfico de área: {y_column} vs {x_column}')
    else:
        raise ValueError("Tipo de gráfico no soportado")
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        template="plotly_white"
    )
    return fig

def export_dataframe(df, format_type):
    """Exporta el DataFrame en diferentes formatos."""
    if format_type == "CSV":
        buffer = BytesIO()
        df.to_csv(buffer, index=False, encoding='utf-8-sig')
        return buffer.getvalue()
    elif format_type == "Excel":
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        return buffer.getvalue()
    else:
        raise ValueError("Formato de exportación no soportado")
