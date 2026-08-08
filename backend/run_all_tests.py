"""
Automated Test Runner
Runs all test cases and generates accuracy report
"""
from detector.analyzer import ScamAnalyzer
from detector.news_analyzer import FakeNewsAnalyzer
from test_cases import TestCases

analyzer = ScamAnalyzer()
news_analyzer = FakeNewsAnalyzer()

def test_scam_detection():
    """Test all scam detection cases"""
    print("\n" + "=" * 70)
    print("🚨 TESTING SCAM DETECTION")
    print("=" * 70)
    
    results = []
    
    # Test scams
    print("\n📍 Testing Known Scams:")
    for key, case in TestCases.SCAMS.items():
        result = analyzer.analyze(case['input'])
        risk = result['risk_score']
        classification = result['classification']
        
        # Check if detection was accurate
        correct = classification == case['expected_class']
        
        status = "✅ PASS" if correct else "❌ FAIL"
        print(f"\n{status} {case['name']}")
        print(f"   Risk Score: {risk}/100 (Expected: ~{case['expected_risk']})")
        print(f"   Classification: {classification.upper()} (Expected: {case['expected_class'].upper()})")
        
        results.append({
            'name': case['name'],
            'correct': correct,
            'risk': risk,
            'expected_risk': case['expected_risk']
        })
    
    # Test legitimate messages
    print("\n📍 Testing Legitimate Messages:")
    for key, case in TestCases.LEGITIMATE.items():
        result = analyzer.analyze(case['input'])
        risk = result['risk_score']
        classification = result['classification']
        
        correct = classification == case['expected_class']
        
        status = "✅ PASS" if correct else "❌ FAIL"
        print(f"\n{status} {case['name']}")
        print(f"   Risk Score: {risk}/100 (Expected: ~{case['expected_risk']})")
        print(f"   Classification: {classification.upper()} (Expected: {case['expected_class'].upper()})")
        
        results.append({
            'name': case['name'],
            'correct': correct,
            'risk': risk,
            'expected_risk': case['expected_risk']
        })
    
    # Calculate accuracy
    total = len(results)
    correct = sum(1 for r in results if r['correct'])
    accuracy = (correct / total * 100) if total > 0 else 0
    
    print("\n" + "=" * 70)
    print(f"📊 SCAM DETECTION ACCURACY: {correct}/{total} ({accuracy:.1f}%)")
    print("=" * 70)
    
    return accuracy


def test_news_verification():
    """Test all news verification cases"""
    print("\n" + "=" * 70)
    print("📰 TESTING NEWS VERIFICATION")
    print("=" * 70)
    
    results = []
    
    # Test verified news
    print("\n📍 Testing Credible News:")
    for key, case in TestCases.NEWS_VERIFIED.items():
        result = news_analyzer.analyze_news(case['text'], case['url'])
        credibility = result['credibility_score']
        classification = result['classification']
        
        correct = classification == case['expected_class']
        
        status = "✅ PASS" if correct else "❌ FAIL"
        print(f"\n{status} {case['name']}")
        print(f"   Credibility: {credibility}/100 (Expected: ~{case['expected_credibility']})")
        print(f"   Classification: {classification.upper()} (Expected: {case['expected_class'].upper()})")
        
        results.append({
            'name': case['name'],
            'correct': correct,
            'credibility': credibility
        })
    
    # Test fake news
    print("\n📍 Testing Fake/Unverified News:")
    for key, case in TestCases.NEWS_FAKE.items():
        result = news_analyzer.analyze_news(case['text'], case['url'])
        credibility = result['credibility_score']
        classification = result['classification']
        
        correct = classification == case['expected_class']
        
        status = "✅ PASS" if correct else "❌ FAIL"
        print(f"\n{status} {case['name']}")
        print(f"   Credibility: {credibility}/100 (Expected: ~{case['expected_credibility']})")
        print(f"   Classification: {classification.upper()} (Expected: {case['expected_class'].upper()})")
        
        results.append({
            'name': case['name'],
            'correct': correct,
            'credibility': credibility
        })
    
    # Calculate accuracy
    total = len(results)
    correct = sum(1 for r in results if r['correct'])
    accuracy = (correct / total * 100) if total > 0 else 0
    
    print("\n" + "=" * 70)
    print(f"📊 NEWS VERIFICATION ACCURACY: {correct}/{total} ({accuracy:.1f}%)")
    print("=" * 70)
    
    return accuracy


if __name__ == "__main__":
    print("\n🚀 RUNNING COMPREHENSIVE TEST SUITE")
    
    scam_accuracy = test_scam_detection()
    news_accuracy = test_news_verification()
    
    overall = (scam_accuracy + news_accuracy) / 2
    
    print("\n" + "=" * 70)
    print("🎯 FINAL RESULTS")
    print("=" * 70)
    print(f"   Scam Detection Accuracy: {scam_accuracy:.1f}%")
    print(f"   News Verification Accuracy: {news_accuracy:.1f}%")
    print(f"   Overall System Accuracy: {overall:.1f}%")
    print("=" * 70)