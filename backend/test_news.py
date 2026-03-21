"""
Test Fake News Analyzer
"""
from detector.news_analyzer import FakeNewsAnalyzer

analyzer = FakeNewsAnalyzer()

# Test cases
test_cases = [
    {
        'name': 'Clickbait Fake News',
        'text': 'SHOCKING! Scientists HATE this one trick! You won\'t believe what happens next! VIRAL!!',
        'url': None
    },
    {
        'name': 'Credible News',
        'text': 'According to Reuters, the Reserve Bank of India announced new monetary policy on January 15, 2026.',
        'url': 'https://www.reuters.com/article/...'
    },
    {
        'name': 'Satire Site',
        'text': 'Breaking: Moon made of cheese, says new study',
        'url': 'http://fakingnews.com/moon-cheese'
    },
    {
        'name': 'Sensational but Unverified',
        'text': 'BREAKING NEWS: Shocking revelations about celebrity! Everyone is talking about this explosive story!',
        'url': None
    }
]

print("=" * 80)
print("TESTING FAKE NEWS ANALYZER")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. {test['name']}")
    print("-" * 80)
    print(f"Input: {test['text'][:70]}...")
    if test['url']:
        print(f"URL: {test['url']}")
    
    result = analyzer.analyze_news(test['text'], test['url'])
    
    print(f"\n🎯 Credibility Score: {result['credibility_score']}/100")
    print(f"📊 Classification: {result['classification'].upper()}")
    
    if result['indicators']:
        print(f"\n⚠️  Indicators ({len(result['indicators'])}):")
        for ind in result['indicators'][:3]:
            emoji = '✅' if ind['severity'] == 'positive' else '⚠️' if ind['severity'] in ['low', 'medium'] else '🔴'
            print(f"   {emoji} [{ind['severity'].upper()}] {ind['description']}")
    
    if result['recommendations']:
        print(f"\n💡 Top Recommendation:")
        print(f"   {result['recommendations'][0]}")
    
    print("\n" + "=" * 80)

print("\n✅ All tests completed!")