"""
Test updated scoring
"""
from detector.analyzer import ScamAnalyzer
from detector.news_analyzer import FakeNewsAnalyzer

scam_analyzer = ScamAnalyzer()
news_analyzer = FakeNewsAnalyzer()

print("=" * 70)
print("TESTING UPDATED SCORING")
print("=" * 70)

# Test 1: Paytm Scam
print("\n1. PAYTM SCAM TEST:")
paytm_scam = """Congratulations from Paytm!
You won ₹25,000 cashback in our anniversary draw!
Claim here: paytm-prize.tk
Enter:
- Mobile number
- Paytm password
- UPI PIN"""

result = scam_analyzer.analyze(paytm_scam)
print(f"Risk Score: {result['risk_score']}/100")
print(f"Classification: {result['classification'].upper()}")
print(f"Score Breakdown: URL={result['score_breakdown']['url_score']}, Text={result['score_breakdown']['text_score']}")

# Test 2: Reuters News
print("\n2. REUTERS NEWS TEST:")
reuters_news = "According to a Reuters report dated January 15, 2026, the Reserve Bank of India announced changes to monetary policy, citing inflation concerns."

result = news_analyzer.analyze_news(reuters_news, "https://www.reuters.com/article/...")
print(f"Credibility Score: {result['credibility_score']}/100")
print(f"Classification: {result['classification'].upper()}")
print(f"Score Breakdown: Content={result['score_breakdown']['content_score']}, Source={result['score_breakdown']['source_score']}")

print("\n" + "=" * 70)