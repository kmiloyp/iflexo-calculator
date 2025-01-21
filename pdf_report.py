from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from typing import Dict
import streamlit as st
import os

def create_custom_styles():
    """Crear estilos personalizados para el reporte."""
    styles = getSampleStyleSheet()

    # Estilo para el título principal
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a237e')
    ))

    # Estilo para subtítulos
    styles.add(ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=15,
        textColor=colors.HexColor('#283593')
    ))

    # Estilo para texto normal
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=10,
        leading=16
    ))

    return styles

def add_page_number(canvas, doc):
    """Agregar números de página al documento."""
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(
        letter[0] - 30,
        30,
        f"Página {doc.page}"
    )
    canvas.restoreState()

def generate_pdf_report(ahorros: Dict[str, float], datos_entrada: Dict) -> BytesIO:
    """Genera un reporte PDF con los resultados del análisis."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    story = []
    styles = create_custom_styles()

    # Logo y encabezado
    try:
        logo_path = "attached_assets/iflexo6-sm-kit.jpg"
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=200, height=100)
            story.append(logo)
            story.append(Spacer(1, 20))
    except Exception as e:
        st.warning(f"No se pudo cargar el logo en el PDF: {str(e)}")

    # Título del reporte
    story.append(Paragraph(
        "Reporte Ejecutivo de Eficiencia en Costos",
        styles['CustomTitle']
    ))
    story.append(Spacer(1, 20))

    # Resumen ejecutivo
    story.append(Paragraph("Resumen Ejecutivo", styles['CustomHeading2']))
    ahorro_total = sum(ahorros.values())
    resumen_text = f"""
    Este análisis detallado revela un potencial de ahorro anual de ${ahorro_total:,.1f} 
    a través de la implementación de la tecnología iFlexo. Los ahorros se distribuyen 
    en múltiples áreas operativas, maximizando la eficiencia y rentabilidad de su 
    proceso de impresión flexográfica.
    """
    story.append(Paragraph(resumen_text, styles['CustomBody']))
    story.append(Spacer(1, 10))

    # Tabla de desglose de ahorros
    story.append(Paragraph("Desglose Detallado de Ahorros", styles['CustomHeading2']))

    data = [
        ["Categoría", "Ahorro Anual"],
        ["Optimización de Planchas", f"${ahorros['planchas']:,.1f}"],
        ["Mejora en Velocidad de Ajuste", f"${ahorros['velocidad_ajuste']:,.1f}"],
        ["Incremento en Velocidad de Impresión", f"${ahorros['velocidad_impresion']:,.1f}"],
        ["Reducción en Consumo de Tinta Blanca", f"${ahorros['tinta_blanca']:,.1f}"],
        ["Optimización de Tintas", f"${ahorros['tintas']:,.1f}"],
        ["Eficiencia en Relación Plancha-Parada", f"${ahorros['plancha_parada']:,.1f}"],
        ["Total de Ahorros Anuales", f"${ahorro_total:,.1f}"]
    ]

    table = Table(data, colWidths=[4*inch, 2*inch])
    table.setStyle(TableStyle([
        # Estilo del encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Estilo del total
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8eaf6')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a237e')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        # Estilo general de la tabla
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#9fa8da')),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Nueva página para análisis detallado
    story.append(PageBreak())
    story.append(Paragraph("Análisis Detallado por Área", styles['CustomHeading2']))

    # Análisis por área
    areas = {
        'planchas': 'Optimización de Planchas',
        'velocidad_ajuste': 'Mejora en Velocidad de Ajuste',
        'velocidad_impresion': 'Velocidad de Impresión',
        'tinta_blanca': 'Consumo de Tinta Blanca',
        'tintas': 'Optimización de Tintas',
        'plancha_parada': 'Eficiencia Plancha-Parada'
    }

    for key, titulo in areas.items():
        story.append(Paragraph(titulo, styles['CustomHeading2']))
        analisis_text = f"""
        El análisis muestra un ahorro potencial de ${ahorros[key]:,.1f} anuales en el área de {titulo.lower()}.
        Esta optimización representa una mejora significativa en la eficiencia operativa y contribuye
        al ahorro total proyectado.
        """
        story.append(Paragraph(analisis_text, styles['CustomBody']))
        story.append(Spacer(1, 10))

    # Conclusiones y recomendaciones
    story.append(PageBreak())
    story.append(Paragraph("Conclusiones y Recomendaciones", styles['CustomHeading2']))

    conclusiones_text = f"""
    Basado en el análisis detallado, la implementación de la tecnología iFlexo presenta una 
    oportunidad significativa de optimización con un ahorro anual total proyectado de ${ahorro_total:,.1f}.

    Este ahorro no solo representa una mejora en la rentabilidad, sino también en la eficiencia 
    operativa global, posicionando su empresa para un crecimiento sostenible en el competitivo 
    mercado de la impresión flexográfica.

    Recomendamos proceder con la implementación, priorizando las áreas que muestran el mayor 
    potencial de ahorro para maximizar el retorno sobre la inversión en el menor tiempo posible.
    """
    story.append(Paragraph(conclusiones_text, styles['CustomBody']))

    # Construir el documento con números de página
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    return buffer
