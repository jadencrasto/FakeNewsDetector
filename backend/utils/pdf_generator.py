"""
PDF Report Generator
Creates professional PDF reports for scan results
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import io

class PDFReportGenerator:
    """Generate PDF reports for scan results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=12
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=10
        ))
    
    def generate_scam_report(self, result: dict) -> bytes:
        """Generate PDF report for scam detection result"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Title
        title = Paragraph("🛡️ AI Scam Detection Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary Section
        classification = result.get('classification', 'unknown').upper()
        risk_score = result.get('risk_score', 0)
        
        # Color-code based on classification
        if classification == 'SCAM':
            color = colors.HexColor('#EF4444')
            status = 'DANGER - LIKELY SCAM'
        elif classification == 'SUSPICIOUS':
            color = colors.HexColor('#F59E0B')
            status = 'CAUTION - SUSPICIOUS'
        else:
            color = colors.HexColor('#10B981')
            status = 'SAFE - NO THREATS DETECTED'
        
        summary_data = [
            ['Risk Score:', f"{risk_score}/100"],
            ['Classification:', status],
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y at %H:%M:%S')],
            ['Analysis Time:', f"{result.get('analysis_time_ms', 0)}ms"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (1, 1), (1, 1), color),
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Analyzed Input
        story.append(Paragraph("📝 Analyzed Content", self.styles['SectionHeader']))
        input_text = result.get('input', 'N/A')[:400]
        if len(result.get('input', '')) > 400:
            input_text += '...'
        story.append(Paragraph(input_text, self.styles['BodyText']))
        story.append(Spacer(1, 0.3*inch))
        
        # URLs Found
        urls = result.get('urls_found', [])
        if urls:
            story.append(Paragraph(f"🔗 Suspicious URLs Detected ({len(urls)})", 
                                 self.styles['SectionHeader']))
            for url in urls[:5]:
                story.append(Paragraph(f"• {url}", self.styles['BodyText']))
            story.append(Spacer(1, 0.2*inch))
        
        # Indicators
        indicators = result.get('indicators', [])
        if indicators:
            story.append(Paragraph(f"⚠️ Risk Indicators ({len(indicators)} detected)", 
                                 self.styles['SectionHeader']))
            
            for i, indicator in enumerate(indicators[:12], 1):
                severity = indicator.get('severity', 'low').upper()
                severity_map = {
                    'CRITICAL': ('🔴', '#DC2626'),
                    'HIGH': ('🟠', '#F59E0B'),
                    'MEDIUM': ('🟡', '#FBBF24'),
                    'LOW': ('🔵', '#3B82F6'),
                    'POSITIVE': ('✅', '#10B981')
                }
                emoji, color_hex = severity_map.get(severity, ('⚪', '#000000'))
                
                desc = indicator.get('description', '')
                text = f"{emoji} <b>[{severity}]</b> {desc}"
                story.append(Paragraph(text, self.styles['BodyText']))
                story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        recommendations = result.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("💡 Safety Recommendations", self.styles['SectionHeader']))
            
            for i, rec in enumerate(recommendations[:10], 1):
                story.append(Paragraph(f"{i}. {rec}", self.styles['BodyText']))
                story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_text = """
        <para align=center>
        <font size=9 color='#6B7280'>
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br/>
        This report was generated by <b>AI Scam Detector</b><br/>
        For educational purposes only. Always verify with official sources.<br/>
        Report scams to: <b>cybercrime.gov.in</b><br/>
        Stay safe online! 🛡️
        </font>
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['BodyText']))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def generate_news_report(self, result: dict) -> bytes:
        """Generate PDF report for news verification"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Title
        title = Paragraph("📰 News Credibility Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        classification = result.get('classification', 'unknown').upper()
        credibility_score = result.get('credibility_score', result.get('risk_score', 0))
        
        if classification == 'VERIFIED':
            color = colors.HexColor('#10B981')
            status = 'VERIFIED - APPEARS CREDIBLE'
        elif classification == 'UNVERIFIED':
            color = colors.HexColor('#F59E0B')
            status = 'UNVERIFIED - CANNOT CONFIRM'
        else:
            color = colors.HexColor('#EF4444')
            status = 'FALSE - LIKELY MISLEADING'
        
        summary_data = [
            ['Credibility Score:', f"{credibility_score}/100"],
            ['Classification:', status],
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y at %H:%M:%S')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (1, 1), (1, 1), color),
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Content analyzed
        story.append(Paragraph("📝 Content Analyzed", self.styles['SectionHeader']))
        input_text = result.get('input', 'N/A')[:400]
        if len(result.get('input', '')) > 400:
            input_text += '...'
        story.append(Paragraph(input_text, self.styles['BodyText']))
        story.append(Spacer(1, 0.3*inch))
        
        # Indicators
        indicators = result.get('indicators', [])
        if indicators:
            story.append(Paragraph(f"🔍 Credibility Indicators ({len(indicators)})", 
                                 self.styles['SectionHeader']))
            
            for indicator in indicators[:12]:
                severity = indicator.get('severity', 'low').upper()
                severity_map = {
                    'CRITICAL': ('🔴', '#DC2626'),
                    'HIGH': ('🟠', '#F59E0B'),
                    'MEDIUM': ('🟡', '#FBBF24'),
                    'LOW': ('🔵', '#3B82F6'),
                    'POSITIVE': ('✅', '#10B981')
                }
                emoji, _ = severity_map.get(severity, ('⚪', '#000000'))
                
                desc = indicator.get('description', '')
                text = f"{emoji} <b>[{severity}]</b> {desc}"
                story.append(Paragraph(text, self.styles['BodyText']))
                story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        recommendations = result.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("💡 Recommendations", self.styles['SectionHeader']))
            
            for i, rec in enumerate(recommendations[:10], 1):
                story.append(Paragraph(f"{i}. {rec}", self.styles['BodyText']))
                story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_text = """
        <para align=center>
        <font size=9 color='#6B7280'>
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br/>
        This report was generated by <b>AI Scam & Fake News Detector</b><br/>
        Always cross-verify news with multiple credible sources<br/>
        Check fact-checking sites: AltNews, Boom, Vishvas News<br/>
        Stay informed! 📰
        </font>
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['BodyText']))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes