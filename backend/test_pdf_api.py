"""
Test PDF export API endpoint
"""
import requests
import json

API_URL = 'http://localhost:5000/api/export-pdf'

# Test data
scam_result = {
    'scan_id': 1,
    'input': 'Congratulations! You won ₹50,000 in KBC lottery. Click here: http://kbc-lottery.tk. Enter your UPI PIN to verify.',
    'risk_score': 95,
    'classification': 'scam',
    'analysis_time_ms': 12,
    'urls_found': ['http://kbc-lottery.tk'],
    'indicators': [
        {'type': 'domain', 'severity': 'critical', 'description': 'Suspicious domain extension: .tk'},
        {'type': 'money_offer', 'severity': 'high', 'description': 'Contains money offer keywords: won, lottery'},
        {'type': 'personal_info_request', 'severity': 'critical', 'description': 'Requests personal information: UPI PIN'}
    ],
    'recommendations': [
        '🚫 DO NOT click any links',
        '🚫 DO NOT share personal information',
        '📱 Block the sender',
        '👮 Report to cybercrime.gov.in'
    ]
}

print("Testing PDF export API...")
print(f"POST {API_URL}")

try:
    response = requests.post(API_URL, json={'result': scam_result})
    
    if response.status_code == 200:
        # Save PDF
        with open('api_test_report.pdf', 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Success! PDF downloaded ({len(response.content)} bytes)")
        print("📄 Saved as: api_test_report.pdf")
        print("\nOpen the file to verify!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"❌ Request failed: {e}")
    print("\nMake sure the backend is running!")
    print("Start it with: python app.py")