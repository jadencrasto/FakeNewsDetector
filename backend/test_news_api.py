"""
Test News Verification API
"""
import requests
import json

API_URL = 'http://localhost:5000/api/verify-news'

test_cases = [
    {
        'name': 'Clickbait Headline',
        'text': 'SHOCKING! You won\'t believe what this celebrity did! Number 5 will blow your mind! VIRAL!!!',
        'url': None
    },
    {
        'name': 'Credible News with Source',
        'text': 'According to a report by The Hindu, the Indian government announced new education reforms on March 10, 2026, citing officials from the Ministry of Education.',
        'url': 'https://www.thehindu.com/news/education/...'
    },
    {
        'name': 'Unverified Claim',
        'text': 'Breaking: Major earthquake predicted for next week. Panic spreads across the city.',
        'url': None
    },
    {
        'name': 'Satire Source',
        'text': 'Scientists discover that eating pizza cures all diseases',
        'url': 'http://fakingnews.com/pizza-cure'
    }
]

print("=" * 70)
print("🔍 TESTING NEWS VERIFICATION API")
print("=" * 70)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. {test['name']}")
    print("-" * 70)
    print(f"Text: {test['text'][:60]}...")
    
    try:
        response = requests.post(API_URL, json={
            'text': test['text'],
            'url': test['url']
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n🎯 Credibility Score: {result['credibility_score']}/100")
            print(f"📊 Classification: {result['classification'].upper()}")
            
            if result.get('score_breakdown'):
                breakdown = result['score_breakdown']
                print(f"\n📈 Score Breakdown:")
                print(f"   Content: {breakdown.get('content_score', 0)}")
                print(f"   Source: {breakdown.get('source_score', 0)}")
                print(f"   Verification: {breakdown.get('verification_score', 0)}")
            
            if result.get('indicators'):
                print(f"\n⚠️  Indicators ({len(result['indicators'])}):")
                for ind in result['indicators'][:3]:
                    emoji = {
                        'positive': '✅',
                        'low': '🔵',
                        'medium': '🟡',
                        'high': '🟠',
                        'critical': '🔴'
                    }.get(ind['severity'], '⚪')
                    print(f"   {emoji} [{ind['severity'].upper()}] {ind['description'][:60]}...")
            
            if result.get('recommendations'):
                print(f"\n💡 Recommendations:")
                for rec in result['recommendations'][:2]:
                    print(f"   {rec}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 70)

print("\n✅ All tests completed!")
