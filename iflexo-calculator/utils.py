{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import plotly.express as px\
import plotly.graph_objects as go\
from io import BytesIO\
\
def load_file(uploaded_file):\
    """Carga el archivo subido en un DataFrame de pandas."""\
    try:\
        if uploaded_file.name.endswith('.csv'):\
            return pd.read_csv(uploaded_file)\
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):\
            return pd.read_excel(uploaded_file)\
        else:\
            raise ValueError("Formato de archivo no soportado")\
    except Exception as e:\
        raise Exception(f"Error al cargar el archivo: \{str(e)\}")\
\
def generate_plot(df, plot_type, x_column, y_column):\
    """Genera diferentes tipos de gr\'e1ficos usando Plotly."""\
    if plot_type == "L\'edneas":\
        fig = px.line(df, x=x_column, y=y_column, \
                     title=f'Gr\'e1fico de l\'edneas: \{y_column\} vs \{x_column\}')\
    elif plot_type == "Barras":\
        fig = px.bar(df, x=x_column, y=y_column,\
                    title=f'Gr\'e1fico de barras: \{y_column\} vs \{x_column\}')\
    elif plot_type == "Dispersi\'f3n":\
        fig = px.scatter(df, x=x_column, y=y_column,\
                        title=f'Gr\'e1fico de dispersi\'f3n: \{y_column\} vs \{x_column\}')\
    elif plot_type == "\'c1rea":\
        fig = px.area(df, x=x_column, y=y_column,\
                     title=f'Gr\'e1fico de \'e1rea: \{y_column\} vs \{x_column\}')\
    else:\
        raise ValueError("Tipo de gr\'e1fico no soportado")\
    \
    fig.update_layout(\
        xaxis_title=x_column,\
        yaxis_title=y_column,\
        template="plotly_white"\
    )\
    return fig\
\
def export_dataframe(df, format_type):\
    """Exporta el DataFrame en diferentes formatos."""\
    if format_type == "CSV":\
        buffer = BytesIO()\
        df.to_csv(buffer, index=False, encoding='utf-8-sig')\
        return buffer.getvalue()\
    elif format_type == "Excel":\
        buffer = BytesIO()\
        df.to_excel(buffer, index=False)\
        return buffer.getvalue()\
    else:\
        raise ValueError("Formato de exportaci\'f3n no soportado")}