"""
Comprehensive Test Cases for AI Scam & Fake News Detector
Demonstrates detection across various scam types and news categories
"""

class TestCases:
    """Collection of test cases for demonstration"""
    
    # ====================================================================
    # SCAM DETECTION TEST CASES
    # ====================================================================
    
    SCAMS = {
        "lottery_prize": {
            "name": "KBC Lottery Scam",
            "input": "🎉 Congratulations! You have won ₹50,00,000 in KBC Bumper Lottery! Your lucky number is 7845. Click here to claim: http://kbc-winner.tk Enter your bank details, Aadhar number, and OTP to verify.",
            "expected_risk": 95,
            "expected_class": "scam",
            "category": "Lottery/Prize Scams"
        },
        
        "bank_phishing": {
            "name": "SBI Account Suspension",
            "input": "⚠️ URGENT! Your SBI account will be permanently blocked in 24 hours due to KYC non-compliance. Update immediately: sbi-kyc-update.ml Provide: Debit card number, CVV, OTP, and Aadhar. Failure to comply will result in account closure.",
            "expected_risk": 98,
            "expected_class": "scam",
            "category": "Banking Fraud"
        },
        
        "payment_scam": {
            "name": "Paytm Cashback Fraud",
            "input": "🎁 Congratulations from Paytm! You've won ₹25,000 cashback in our anniversary celebration! Claim here: paytm-rewards.tk Enter your: Mobile number, Paytm password, UPI PIN to receive instantly!",
            "expected_risk": 96,
            "expected_class": "scam",
            "category": "Payment Scams"
        },
        
        "job_scam": {
            "name": "Work From Home Scam",
            "input": "💼 Earn ₹50,000 per month working from home! No experience needed. Just pay ₹5,000 registration fee. Contact: jobs-easy-money.tk Limited slots! Join 10,000+ happy members. WhatsApp: +91-9999999999",
            "expected_risk": 92,
            "expected_class": "scam",
            "category": "Job Scams"
        },
        
        "government_impersonation": {
            "name": "Income Tax Refund Scam",
            "input": "🏛️ Income Tax Department Notice: You are eligible for ₹37,500 tax refund. Claim now: incometax-refund.ml Provide: PAN, Aadhar, Bank Account. Processing fee: ₹500. Expires in 48 hours!",
            "expected_risk": 94,
            "expected_class": "scam",
            "category": "Government Impersonation"
        },
        
        "ecommerce_fake": {
            "name": "Amazon Prize Scam",
            "input": "🎁 You've been selected as Amazon's lucky customer! Win iPhone 15 Pro + ₹1,00,000 shopping voucher! Click: amazon-lucky-winner.tk Enter delivery address and card details for verification. Hurry! Offer valid for 1 hour only!",
            "expected_risk": 93,
            "expected_class": "scam",
            "category": "E-commerce Fraud"
        },
        
        "aadhaar_fraud": {
            "name": "Aadhaar Update Scam",
            "input": "🆔 UIDAI Alert: Your Aadhaar card will be deactivated due to pending verification. Update now: uidai-update.ga Provide: Aadhaar number, OTP, Bank details. Mandatory update to avoid service disruption.",
            "expected_risk": 95,
            "expected_class": "scam",
            "category": "Government Impersonation"
        },
        
        "investment_scam": {
            "name": "Cryptocurrency Investment Fraud",
            "input": "💰 Turn ₹10,000 into ₹1,00,000 in 30 days! Guaranteed returns with our AI crypto trading bot. Join 5000+ investors earning daily. Register: crypto-profit.tk Deposit via UPI. Limited time 50% bonus!",
            "expected_risk": 91,
            "expected_class": "scam",
            "category": "Investment Fraud"
        }
    }
    
    LEGITIMATE = {
        "bank_genuine": {
            "name": "Legitimate Bank SMS",
            "input": "Dear Customer, your SBI account ending in 4567 has been debited with Rs.2,450.00 on 21-Mar-26. Available balance: Rs.45,678.90. For queries, call 1800-1234 or visit www.onlinesbi.sbi",
            "expected_risk": 25,
            "expected_class": "safe",
            "category": "Legitimate Banking"
        },
        
        "ecommerce_genuine": {
            "name": "Real Amazon Delivery",
            "input": "Your Amazon order #406-1234567-8901234 has been shipped via BlueDart (AWB: 12345678901). Expected delivery: March 22, 2026. Track your order at https://www.amazon.in/track",
            "expected_risk": 20,
            "expected_class": "safe",
            "category": "Legitimate E-commerce"
        },
        
        "otp_genuine": {
            "name": "Legitimate OTP",
            "input": "Your OTP for Paytm login is 482756. Valid for 10 minutes. Do not share with anyone. If you did not request this, please contact support immediately.",
            "expected_risk": 30,
            "expected_class": "suspicious",
            "category": "Legitimate OTP (cautious)"
        }
    }
    
    # ====================================================================
    # NEWS VERIFICATION TEST CASES
    # ====================================================================
    
    NEWS_VERIFIED = {
        "reuters_rbi": {
            "name": "Reuters - RBI Policy",
            "text": "According to a Reuters report dated January 15, 2026, the Reserve Bank of India announced changes to monetary policy, citing inflation concerns. The decision was made during the bi-monthly monetary policy committee meeting. RBI Governor stated that the repo rate will remain unchanged at 6.5%.",
            "url": "https://www.reuters.com/article/india-rbi-policy",
            "expected_credibility": 78,
            "expected_class": "verified",
            "category": "Credible News"
        },
        
        "bbc_elections": {
            "name": "BBC - Election Results",
            "text": "The BBC reports that voter turnout in Maharashtra state elections reached 68%, according to the Election Commission of India. Results are expected to be announced on March 23, 2026. Political analysts note this is a 5% increase from the previous election cycle.",
            "url": "https://www.bbc.com/news/world-asia-india",
            "expected_credibility": 76,
            "expected_class": "verified",
            "category": "Credible News"
        }
    }
    
    NEWS_FAKE = {
        "clickbait_health": {
            "name": "Clickbait Health Miracle",
            "text": "SHOCKING!!! Doctors HATE this one weird trick! 🔥🔥🔥 This common kitchen ingredient CURES cancer, diabetes, and heart disease OVERNIGHT! Number 5 will BLOW YOUR MIND! Scientists are trying to HIDE this from you! Click NOW before it's DELETED! 😱😱😱 VIRAL!!!",
            "url": "",
            "expected_credibility": 15,
            "expected_class": "false",
            "category": "Fake News / Clickbait"
        },
        
        "conspiracy_5g": {
            "name": "5G Conspiracy Theory",
            "text": "BREAKING: Secret government documents reveal 5G towers are actually mind control devices! They're controlling your thoughts and causing ALL diseases! Share this before they delete it! The government doesn't want you to know! Wake up people!!!",
            "url": "",
            "expected_credibility": 12,
            "expected_class": "false",
            "category": "Fake News / Conspiracy"
        },
        
        "unverified_celebrity": {
            "name": "Unverified Celebrity Gossip",
            "text": "Sources say that a famous Bollywood star has secretly married. The wedding allegedly took place in an undisclosed location. Friends close to the couple might have confirmed the news. Details are expected to emerge soon.",
            "url": "",
            "expected_credibility": 45,
            "expected_class": "unverified",
            "category": "Unverified Gossip"
        }
    }


def print_test_case_summary():
    """Print summary of all test cases"""
    print("=" * 70)
    print("📋 TEST CASE SUMMARY")
    print("=" * 70)
    
    print("\n🚨 SCAM DETECTION TEST CASES:")
    print(f"   Total Scams: {len(TestCases.SCAMS)}")
    for key, case in TestCases.SCAMS.items():
        print(f"   ✓ {case['name']} ({case['category']})")
    
    print(f"\n   Total Legitimate: {len(TestCases.LEGITIMATE)}")
    for key, case in TestCases.LEGITIMATE.items():
        print(f"   ✓ {case['name']} ({case['category']})")
    
    print("\n📰 NEWS VERIFICATION TEST CASES:")
    print(f"   Total Verified: {len(TestCases.NEWS_VERIFIED)}")
    for key, case in TestCases.NEWS_VERIFIED.items():
        print(f"   ✓ {case['name']}")
    
    print(f"\n   Total Fake/Unverified: {len(TestCases.NEWS_FAKE)}")
    for key, case in TestCases.NEWS_FAKE.items():
        print(f"   ✓ {case['name']}")
    
    total = (len(TestCases.SCAMS) + len(TestCases.LEGITIMATE) + 
             len(TestCases.NEWS_VERIFIED) + len(TestCases.NEWS_FAKE))
    
    print(f"\n📊 TOTAL TEST CASES: {total}")
    print("=" * 70)


if __name__ == "__main__":
    print_test_case_summary()