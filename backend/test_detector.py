"""
Test the Scam Detector
"""
import requests
import json

API_URL = 'http://localhost:5000/api/analyze'

# Test cases
test_cases = [
    {
        'name': 'UPI Scam',
        'input': 'Congratulations! You won ₹50,000 in KBC lottery. Click here immediately to claim: http://kbc-lottery.tk. Enter your UPI PIN to verify.'
    },
    {
        'name': 'Fake Job Scam',
        'input': 'Selected for Data Entry job. Salary Rs 25,000/month. Pay Rs 5,000 registration fee. No experience needed. Contact: 9876543210'
    },
    {
        'name': 'Bank Phishing',
        'input': 'ALERT: Your SBI account is blocked due to suspicious activity. Verify within 24 hours: http://sbi-verify-india.com. Enter password and OTP.'
    },
    {
        'name': 'Legitimate Message',
        'input': 'Your Amazon order #123-456-789 has been shipped and will arrive by Feb 20. Track: https://amazon.in/track/123'
    },
    {
        'name': 'Simple Test',
        'input': 'You won 50000 rupees! Click here to claim'
    }
]

print("=" * 70)
print("🔍 TESTING AI SCAM DETECTOR")
print("=" * 70)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. TEST: {test['name']}")
    print("-" * 70)
    print(f"Input: {test['input'][:70]}...")
    
    try:
        response = requests.post(API_URL, json={'input': test['input']})
        result = response.json()
        
        # Check if error
        if 'error' in result:
            print(f"❌ ERROR: {result['error']}")
            print(f"   Message: {result.get('message', 'Unknown error')}")
            continue
        
        # Display results
        print(f"\n🎯 Risk Score: {result['risk_score']}/100")
        print(f"📊 Classification: {result['classification'].upper()}")
        print(f"⏱️  Analysis Time: {result.get('analysis_time_ms', 'N/A')}ms")
        
        # Show score breakdown
        if 'score_breakdown' in result:
            breakdown = result['score_breakdown']
            print(f"\n📈 Score Breakdown:")
            print(f"   URL Score: {breakdown.get('url_score', 0)}")
            print(f"   Text Score: {breakdown.get('text_score', 0)}")
            print(f"   Total: {breakdown.get('total_score', 0)}")
        
        # Show indicators
        if result.get('indicators'):
            print(f"\n⚠️  Indicators Found: {len(result['indicators'])}")
            for ind in result['indicators'][:5]:  # Show first 5
                severity_emoji = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🔵'
                }.get(ind['severity'], '⚪')
                print(f"   {severity_emoji} [{ind['severity'].upper()}] {ind['description'][:60]}...")
        
        # Show URLs found
        if result.get('urls_found'):
            print(f"\n🔗 URLs Found: {len(result['urls_found'])}")
            for url in result['urls_found'][:3]:
                print(f"   - {url}")
        
        # Show recommendations
        if result.get('recommendations'):
            print(f"\n💡 Recommendations:")
            for rec in result['recommendations'][:3]:
                print(f"   {rec}")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API. Is the server running?")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 70)

print("\n✅ All tests completed!")