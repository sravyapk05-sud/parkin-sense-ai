from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def create_medical_report(output_filename, data):
    """
    Create a medical diagnosis report PDF

    Args:
        output_filename (str): Path where the PDF will be saved
        data (dict): Dictionary containing report data with keys:
            - date: Report date
            - doctor: Doctor's name
            - patient: Patient's name
            - mri: MRI prediction (0 or 1)
            - voice: Voice prediction (0 or 1)
            - final: Final fused prediction (0 or 1)
    """
    try:
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Get styles
        styles = getSampleStyleSheet()

        # Create custom styles
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a4d8c'),
            spaceAfter=20,
            alignment=1,
            fontName='Helvetica-Bold'
        ))

        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2E5090'),
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))

        styles.add(ParagraphStyle(
            name='Label',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica-Bold'
        ))

        styles.add(ParagraphStyle(
            name='Value',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        ))

        styles.add(ParagraphStyle(
            name='ResultNormal',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27ae60'),
            fontName='Helvetica-Bold',
            alignment=1
        ))

        styles.add(ParagraphStyle(
            name='ResultAbnormal',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold',
            alignment=1
        ))

        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        ))

        # Build the story
        story = []

        # Header with hospital/clinic name
        story.append(Paragraph(
            "<b>CITY NEURO CENTER</b>",
            ParagraphStyle(
                name='HospitalName',
                fontSize=20,
                textColor=colors.HexColor('#1a4d8c'),
                alignment=1,
                fontName='Helvetica-Bold'
            )
        ))
        story.append(Paragraph(
            "Advanced Neurology & Diagnostics",
            ParagraphStyle(
                name='HospitalSub',
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                alignment=1
            )
        ))
        story.append(Spacer(1, 20))

        # Title
        story.append(Paragraph("MEDICAL DIAGNOSIS REPORT", styles['ReportTitle']))
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=colors.HexColor('#1a4d8c'),
            spaceBefore=5,
            spaceAfter=20
        ))

        # Report Information Section
        story.append(Paragraph("Report Information", styles['SectionHeading']))

        # Create info table
        info_data = [
            ['Date:', data['date'], 'Doctor:', data['doctor']],
            ['Patient:', data['patient'], '', ''],
        ]

        info_table = Table(info_data, colWidths=[80, 180, 80, 180])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#666666')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(info_table)
        story.append(Spacer(1, 20))

        # Diagnostic Results Section
        story.append(Paragraph("Diagnostic Results", styles['SectionHeading']))

        # Results table
        results_data = [
            ['Test Type', 'Result', 'Interpretation'],
            ['MRI Analysis', self._format_result(data['mri']), self._get_interpretation(data['mri'])],
            ['Voice Analysis', self._format_result(data['voice']), self._get_interpretation(data['voice'])],
        ]

        results_table = Table(results_data, colWidths=[120, 100, 200])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d8c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
        ]))

        story.append(results_table)
        story.append(Spacer(1, 20))

        # Final Fused Prediction
        story.append(Paragraph("Final Diagnosis", styles['SectionHeading']))

        final_result = data['final']
        result_text = "NORMAL" if final_result == 0 else "ABNORMAL DETECTED"
        result_color = colors.HexColor('#27ae60') if final_result == 0 else colors.HexColor('#e74c3c')

        # Create a highlighted box for final result
        final_data = [[
            Paragraph(
                f"<para alignment='center'><b>FINAL FUSED PREDICTION: {result_text}</b></para>",
                ParagraphStyle(
                    name='FinalResult',
                    fontSize=16,
                    textColor=result_color,
                    alignment=1,
                    fontName='Helvetica-Bold'
                )
            )
        ]]

        final_table = Table(final_data, colWidths=[400])
        final_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1),
             colors.HexColor('#f0f7f0') if final_result == 0 else colors.HexColor('#fef5f5')),
            ('BOX', (0, 0), (-1, -1), 2, result_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))

        story.append(final_table)
        story.append(Spacer(1, 30))

        # Clinical Recommendations based on results
        story.append(Paragraph("Clinical Recommendations", styles['SectionHeading']))

        if final_result == 0:
            recommendations = [
                "• Regular follow-up as scheduled",
                "• Maintain healthy lifestyle habits",
                "• Report any new symptoms immediately",
                "• Continue current medications as prescribed"
            ]
        else:
            recommendations = [
                "• Immediate consultation with specialist recommended",
                "• Further diagnostic tests may be required",
                "• Consider starting appropriate treatment protocol",
                "• Schedule follow-up within 2 weeks"
            ]

        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 5))

        story.append(Spacer(1, 30))

        # Doctor's signature section
        signature_data = [
            ['', '', f"Dr. {data['doctor']}", ''],
            ['', '', 'Consultant Neurologist', ''],
            ['', '', datetime.now().strftime("%Y-%m-%d"), ''],
        ]

        signature_table = Table(signature_data, colWidths=[200, 50, 150, 50])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
            ('FONTNAME', (2, 1), (2, 1), 'Helvetica'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('TEXTCOLOR', (2, 1), (2, 1), colors.grey),
        ]))

        story.append(signature_table)
        story.append(Spacer(1, 10))

        # Add a line for signature
        story.append(HRFlowable(
            width="30%",
            thickness=1,
            color=colors.grey,
            hAlign='RIGHT',
            spaceBefore=5,
            spaceAfter=5
        ))

        story.append(Paragraph(
            "(Doctor's Signature)",
            ParagraphStyle(
                name='SignatureLabel',
                fontSize=8,
                textColor=colors.grey,
                alignment=2
            )
        ))

        story.append(Spacer(1, 20))

        # Footer
        story.append(HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.grey,
            spaceBefore=10,
            spaceAfter=5
        ))

        footer_text = "This is a computer-generated report based on AI analysis. "
        footer_text += "Please consult with your doctor for complete medical advice."
        story.append(Paragraph(footer_text, styles['Footer']))

        # Generate PDF
        doc.build(story)

        return True

    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        return False


def _format_result(value):
    """Format the result value"""
    if value == 0:
        return "Normal"
    elif value == 1:
        return "Abnormal"
    else:
        return "Unknown"


def _get_interpretation(value):
    """Get interpretation text for the result"""
    if value == 0:
        return "No significant abnormalities detected"
    elif value == 1:
        return "Abnormal findings detected - further evaluation recommended"
    else:
        return "Inconclusive"


# Main function to generate report with given data
def generate_patient_report():
    """
    Generate a medical report with the provided data
    """
    # Input data
    report_data = {
        'date': '2026-03-11',
        'doctor': 'Sudheer',
        'patient': 'Ramesh',
        'mri': 0,
        'voice': 1,
        'final': 0
    }

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Medical_Report_{report_data['patient']}_{timestamp}.pdf"

    # Create the report
    success = create_medical_report(filename, report_data)

    if success:
        print(f"✅ Report generated successfully: {filename}")
        print("\nReport Summary:")
        print(f"  Patient: {report_data['patient']}")
        print(f"  Doctor: {report_data['doctor']}")
        print(f"  Date: {report_data['date']}")
        print(f"  MRI Result: {'Normal' if report_data['mri'] == 0 else 'Abnormal'}")
        print(f"  Voice Result: {'Normal' if report_data['voice'] == 0 else 'Abnormal'}")
        print(f"  Final Diagnosis: {'Normal' if report_data['final'] == 0 else 'Abnormal'}")
    else:
        print("❌ Failed to generate report")

    return filename


# Alternative: More detailed report with additional sections
def create_detailed_medical_report(output_filename, data):
    """
    Create a more detailed medical report with additional sections
    """
    try:
        # Create the PDF document
        doc = SimpleDocTemplate(
            r"C:\Users\isasu\Music\project\web\D_daignosis\media\\"+output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Get styles
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            name='CustomTitle',
            fontSize=24,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=1,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            name='CustomHeading',
            fontSize=16,
            textColor=colors.HexColor('#2E5090'),
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )

        normal_style = ParagraphStyle(
            name='CustomNormal',
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            fontName='Helvetica'
        )

        # Build story
        story = []

        # Header
        story.append(Paragraph("CITY NEURO CENTER", title_style))
        story.append(Paragraph("Medical Diagnosis Report",
                               ParagraphStyle(name='SubTitle', fontSize=14, alignment=1, textColor=colors.grey)))
        story.append(Spacer(1, 20))

        # Patient Information Card
        story.append(Paragraph("PATIENT INFORMATION", heading_style))

        patient_data = [
            ["Patient Name:", data['patient'], "Date:", data['date']],
            ["Doctor:", data['doctor'], "Report ID:", f"RPT-{datetime.now().strftime('%Y%m%d%H%M')}"],
        ]

        patient_table = Table(patient_data, colWidths=[100, 150, 80, 150])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(patient_table)
        story.append(Spacer(1, 20))

        # Test Results
        story.append(Paragraph("DIAGNOSTIC TEST RESULTS", heading_style))

        # Test results with visual indicators
        tests = [
            ("MRI Analysis", data['mri'], "Based on MRI 0" if data['mri'] == 0 else "Based on MRI 1"),
            ("Voice Analysis", data['voice'], "Based on voice 1" if data['voice'] == 1 else "Based on voice 0"),
        ]

        for test_name, value, description in tests:
            # Test name and result
            result_text = "✓ NORMAL" if value == 0 else "⚠ ABNORMAL"
            result_color = colors.HexColor('#27ae60') if value == 0 else colors.HexColor('#e74c3c')

            test_data = [
                [Paragraph(f"<b>{test_name}</b>", normal_style),
                 Paragraph(f"<font color='{'#27ae60' if value == 0 else '#e74c3c'}'><b>{result_text}</b></font>",
                           normal_style)],
                [Paragraph(f"<font size='10'>{description}</font>", normal_style), ""],
            ]

            test_table = Table(test_data, colWidths=[300, 200])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('SPAN', (0, 1), (1, 1)),
            ]))

            story.append(test_table)
            story.append(Spacer(1, 10))

        story.append(Spacer(1, 10))

        # Final Fused Prediction
        story.append(Paragraph("FINAL FUSED PREDICTION", heading_style))

        final_result = data['final']
        if final_result == 0:
            result_box = [
                [Paragraph("<b><font size='14' color='#27ae60'>NORMAL</font></b>", normal_style)],
                ["Based on fusion of MRI and Voice analysis: No abnormalities detected"]
            ]
            bg_color = colors.HexColor('#e8f5e9')
            border_color = colors.HexColor('#27ae60')
        else:
            result_box = [
                [Paragraph("<b><font size='14' color='#e74c3c'>ABNORMAL DETECTED</font></b>", normal_style)],
                ["Based on fusion of MRI and Voice analysis: Further evaluation recommended"]
            ]
            bg_color = colors.HexColor('#ffebee')
            border_color = colors.HexColor('#e74c3c')

        final_table = Table(result_box, colWidths=[480])
        final_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), 2, border_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 15),
        ]))

        story.append(final_table)
        story.append(Spacer(1, 20))

        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", heading_style))

        if data['final'] == 0:
            recs = [
                "• Continue regular monitoring",
                "• Maintain healthy lifestyle",
                "• Follow-up in 6 months",
                "• Report any new symptoms immediately"
            ]
        else:
            recs = [
                "• Schedule consultation with specialist",
                "• Additional diagnostic tests may be required",
                "• Consider treatment options",
                "• Follow-up in 2 weeks"
            ]

        for rec in recs:
            story.append(Paragraph(rec, normal_style))

        story.append(Spacer(1, 30))

        # Footer with signatures
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Spacer(1, 10))

        footer_data = [
            [f"Dr. {data['doctor']}", "", datetime.now().strftime("%Y-%m-%d %H:%M")],
            ["Consultant Neurologist", "", "Generated by AI System"]
        ]

        footer_table = Table(footer_data, colWidths=[200, 100, 200])
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ]))

        story.append(footer_table)

        # Build PDF
        doc.build(story)
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# # Run the report generation
# if __name__ == "__main__":
#     # Generate simple report
#
#     if success:
#         print(f"\n✅ Detailed report generated: {detailed_filename}")