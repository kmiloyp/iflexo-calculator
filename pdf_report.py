from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from typing import Dict
import streamlit as st

def generate_pdf_report(ahorros: Dict[str, float], datos_entrada: Dict) -> BytesIO:
    """Genera un reporte PDF con los resultados del análisis."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Logo
    logo = Image("attached_assets/iflexo6-sm-kit.jpg", width=200, height=100)
    story.append(logo)
    story.append(Spacer(1, 12))

    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Reporte de Análisis de Eficiencia en Costos", title_style))
    story.append(Spacer(1, 12))

    # Resumen de Ahorros
    story.append(Paragraph("Resumen de Ahorros", styles['Heading2']))

    data = [
        ["Categoría", "Ahorro Anual"],
        ["Costo de Planchas", f"${ahorros['planchas']:,.1f}"],
        ["Velocidad de Ajuste", f"${ahorros['velocidad_ajuste']:,.1f}"],
        ["Velocidad en Impresión", f"${ahorros['velocidad_impresion']:,.1f}"],
        ["Tinta Blanca", f"${ahorros['tinta_blanca']:,.1f}"],
        ["Tintas", f"${ahorros['tintas']:,.1f}"],
        ["Relación Plancha-Parada", f"${ahorros['plancha_parada']:,.1f}"],
        ["Total", f"${sum(ahorros.values()):,.1f}"]
    ]

    table = Table(data, colWidths=[4*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Descripción de iFlexo
    story.append(Paragraph("Solución iFlexo", styles['Heading2']))
    iflexo_text = """
    Estos resultados han sido calculados considerando la implementación integral de la tecnología 
    y servicios de iFlexo Visión Gráfica. Nuestro enfoque no solo incluye tecnología de planchas 
    de última generación, sino también un acompañamiento experto durante todo el proceso de 
    implementación en prensa, asegurando que cada una de estas mejoras se materialice de 
    manera efectiva en su operación.
    """
    story.append(Paragraph(iflexo_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Conclusión persuasiva
    story.append(Paragraph("Proyección de Inversión", styles['Heading2']))
    ahorro_total = sum(ahorros.values())
    conclusion_text = f"""
    Con un ahorro anual proyectado de ${ahorro_total:,.1f}, imagine cómo esta 
    optimización podría transformar su negocio. Estos ahorros representan una 
    oportunidad única para reinvertir en su empresa - por ejemplo, podrían cubrir 
    un porcentaje significativo del costo de una nueva impresora Flexo, 
    impulsando aún más su capacidad productiva y competitividad en el mercado.

    La decisión de implementar iFlexo no solo es una mejora operativa, es una 
    inversión estratégica en el futuro de su empresa, que se paga por sí misma 
    a través de los ahorros generados.
    """
    story.append(Paragraph(conclusion_text, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
