"""
Test what analytics API actually returns
"""
import requests
import json

response = requests.get('http://localhost:5000/api/analytics')

print("=" * 70)
print("ANALYTICS API RESPONSE")
print("=" * 70)

if response.status_code == 200:
    data = response.json()
    print("\n📊 RAW JSON:")
    print(json.dumps(data, indent=2))
    
    print("\n" + "=" * 70)
    print("OVERVIEW DATA:")
    print("=" * 70)
    if 'overview' in data:
        for key, value in data['overview'].items():
            print(f"  {key}: {value}")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)