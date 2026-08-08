"""
Test analytics endpoint
"""
import requests
import json

API_URL = 'http://localhost:5000/api/analytics'

print("=" * 70)
print("TESTING ANALYTICS ENDPOINT")
print("=" * 70)

try:
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n✅ SUCCESS!")
        print("\n📊 OVERVIEW:")
        overview = data['overview']
        print(f"   Total Scans: {overview['total_scans']}")
        print(f"   Scams Detected: {overview['scams_detected']}")
        print(f"   Detection Rate: {overview['detection_rate']}%")
        print(f"   Avg Risk Score: {overview['avg_risk_score']}")
        
        print("\n📈 CLASSIFICATION BREAKDOWN:")
        breakdown = data['classification_breakdown']
        for i, label in enumerate(breakdown['labels']):
            print(f"   {label}: {breakdown['data'][i]}")
        
        print("\n📅 SCANS TIMELINE (Last 7 Days):")
        timeline = data['scans_timeline']
        for i, date in enumerate(timeline['labels']):
            print(f"   {date}: {timeline['data'][i]} scans")
        
        print("\n🎯 TOP SCAM TYPES:")
        for scam_type in data['top_scam_types']:
            print(f"   {scam_type['type']}: {scam_type['count']} reports")
        
        print("\n" + "=" * 70)
        print("✅ Analytics data ready for frontend!")
        print("=" * 70)
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"❌ Request failed: {e}")
    print("\nMake sure:")
    print("1. Backend is running (python app.py)")
    print("2. Database has some scan data")