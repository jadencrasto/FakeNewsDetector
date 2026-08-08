"""
Test PDF generation
"""
from utils.pdf_generator import PDFReportGenerator

generator = PDFReportGenerator()

# Test scam report
scam_result = {
    'scan_id': 1,
    'input': 'Congratulations! You won ₹50,000 in KBC lottery. Click here: http://kbc-lottery.tk',
    'risk_score': 95,
    'classification': 'scam',
    'analysis_time_ms': 12,
    'urls_found': ['http://kbc-lottery.tk'],
    'indicators': [
        {'severity': 'critical', 'description': 'Suspicious domain extension: .tk'},
        {'severity': 'high', 'description': 'Contains money offer keywords: won, lottery'},
        {'severity': 'critical', 'description': 'Requests personal information'}
    ],
    'recommendations': [
        '🚫 DO NOT click any links',
        '🚫 DO NOT share personal information',
        '📱 Block the sender'
    ]
}

print("Generating scam report PDF...")
pdf_bytes = generator.generate_scam_report(scam_result)

# Save to file
with open('test_scam_report.pdf', 'wb') as f:
    f.write(pdf_bytes)

print(f"✓ PDF generated: test_scam_report.pdf ({len(pdf_bytes)} bytes)")
print("\nOpen the PDF to verify it looks good!")