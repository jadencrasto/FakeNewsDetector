"""
Text Analysis Module
Analyzes message text for scam indicators using pattern matching
"""
import re
from detector.indicators import ScamIndicators

class TextAnalyzer:
    """Analyze text content for scam patterns"""
    
    def __init__(self):
        self.indicators = ScamIndicators()
    
    def _check_legitimate_patterns(self, text):
        """
        Check if message matches legitimate patterns
        Returns: (is_legitimate, confidence, patterns)
        """
        text_lower = text.lower()
        
        # Legitimate patterns
        legitimate_indicators = []
        
        # Pattern 1: Transaction notifications (debited/credited with specific amounts)
        if any(word in text_lower for word in ['debited', 'credited', 'withdrawn', 'deposited']):
            if 'rs.' in text_lower or '₹' in text or 'available balance' in text_lower:
                legitimate_indicators.append('transaction_notification')
        
        # Pattern 2: Official customer care numbers
        if '1800' in text or 'toll free' in text_lower or 'toll-free' in text_lower:
            legitimate_indicators.append('official_helpline')
        
        # Pattern 3: Order/shipment tracking with specific IDs
        order_patterns = ['order #', 'order number', 'awb:', 'tracking', 'shipment']
        if any(pattern in text_lower for pattern in order_patterns):
            official_domains = ['amazon.in', 'flipkart.com', 'bluedart', 'delhivery', 'dtdc']
            if any(domain in text_lower for domain in official_domains):
                legitimate_indicators.append('shipment_tracking')
        
        # Pattern 4: OTP with "do not share" warning
        if 'otp' in text_lower:
            if 'do not share' in text_lower or 'never share' in text_lower:
                legitimate_indicators.append('secure_otp')
        
        # Pattern 5: Official domain in message
        official_domains = [
            'onlinesbi.sbi', 'sbi.co.in', 'hdfcbank.com', 'icicibank.com',
            'amazon.in', 'flipkart.com', 'paytm.com', 'www.amazon', 'www.flipkart'
        ]
        if any(domain in text_lower for domain in official_domains):
            legitimate_indicators.append('official_domain')
        
        # Pattern 6: Specific account/order reference numbers
        if re.search(r'ending in \d{4}', text_lower) or re.search(r'#\d{3}-\d{7}-\d{7}', text):
            legitimate_indicators.append('specific_reference')
        
        is_legitimate = len(legitimate_indicators) >= 2  # Need 2+ legitimate indicators
        confidence = min(len(legitimate_indicators) * 15, 50)  # Max 40 point reduction
        
        return is_legitimate, confidence, legitimate_indicators

    def analyze_text(self, text):
        """
        Analyze text for scam indicators
        Returns: (score, indicators_list)
        """
        # Check for legitimate patterns FIRST
        is_legitimate, legit_confidence, legit_patterns = self._check_legitimate_patterns(text)
        
        score = 0
        indicators_list = []
        text_lower = text.lower()
        
        # If highly legitimate, add positive indicators
        if is_legitimate:
            for pattern in legit_patterns:
                indicators_list.append({
                    'type': 'legitimate_pattern',
                    'severity': 'positive',
                    'description': f'Legitimate pattern: {pattern.replace("_", " ")}'
                })
        
        # Check 1: Urgency keywords (increased from 8 to 15)
        urgency_score, urgency_indicators = self._check_keywords(
            text_lower, 
            self.indicators.URGENCY_KEYWORDS,
            'urgency',
            weight=15
        )
        score += urgency_score
        indicators_list.extend(urgency_indicators)
        
        # Check 2: Money keywords (increased from 10 to 25)
        money_score, money_indicators = self._check_keywords(
            text_lower,
            self.indicators.MONEY_KEYWORDS,
            'money_offer',
            weight=25
        )
        score += money_score
        indicators_list.extend(money_indicators)
        
        # Check 3: Action keywords (increased from 7 to 12)
        action_score, action_indicators = self._check_keywords(
            text_lower,
            self.indicators.ACTION_KEYWORDS,
            'action_request',
            weight=12
        )
        score += action_score
        indicators_list.extend(action_indicators)
        
        # Check 4: Threats (increased from 12 to 20)
        threat_score, threat_indicators = self._check_keywords(
            text_lower,
            self.indicators.THREAT_KEYWORDS,
            'threats',
            weight=20
        )
        score += threat_score
        indicators_list.extend(threat_indicators)
        
        # Check 5: Personal info requests - CRITICAL (increased from 15 to 30)
        personal_score, personal_indicators = self._check_keywords(
            text_lower,
            self.indicators.PERSONAL_INFO_KEYWORDS,
            'personal_info_request',
            weight=30
        )
        score += personal_score
        indicators_list.extend(personal_indicators)
        
        # Check 6: Payment keywords (kept at 10)
        payment_score, payment_indicators = self._check_keywords(
            text_lower,
            self.indicators.PAYMENT_KEYWORDS,
            'payment_request',
            weight=10
        )
        score += payment_score
        indicators_list.extend(payment_indicators)
        
        # Check 7: Impersonation (increased from weight in function)
        imperson_score, imperson_indicators = self._check_impersonation(text_lower)
        score += imperson_score
        indicators_list.extend(imperson_indicators)
        
        # Check 8: Too good to be true (increased scoring)
        tgtbt_score, tgtbt_indicators = self._check_unrealistic_offers(text_lower)
        score += tgtbt_score
        indicators_list.extend(tgtbt_indicators)
        
        # Check 9: Formatting (excessive caps, punctuation)
        format_score, format_indicators = self._check_formatting(text)
        score += format_score
        indicators_list.extend(format_indicators)
        
        # Check 10: Phone numbers (suspicious in unsolicited messages)
        phone_score, phone_indicators = self._check_phone_numbers(text)
        score += phone_score
        indicators_list.extend(phone_indicators)
        
        # Apply legitimate pattern reduction AFTER calculating suspicious score
        if is_legitimate:
            score = max(score - legit_confidence, 0)  # Reduce score, but don't go below 0
        
        return min(score, 60), indicators_list  # Cap at 60
    
    def _check_keywords(self, text, keyword_list, category, weight=10):
        """Check for presence of keywords from a list"""
        matches = [kw for kw in keyword_list if kw in text]
        
        if not matches:
            return 0, []
        
        # Increased cap from 25 to 35 for critical categories
        score = min(len(matches) * weight, 35)
        
        # Determine severity based on score
        if score >= 25:
            severity = 'critical'
        elif score > 15:
            severity = 'high'
        elif score > 8:
            severity = 'medium'
        else:
            severity = 'low'
        
        indicator = {
            'type': category,
            'severity': severity,
            'description': f'Contains {category.replace("_", " ")} keywords: {", ".join(matches[:3])}'
        }
        
        return score, [indicator]
    
    def _check_impersonation(self, text):
        """Check for brand/institution impersonation"""
        score = 0
        indicators = []
        
        # Check banks (increased from 15 to 20)
        for bank in self.indicators.INDIAN_BANKS:
            if bank in text:
                score += 20
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'high',
                    'description': f'Mentions bank name: {bank.upper()}'
                })
                break
        
        # Check government (increased from 20 to 30)
        for keyword in self.indicators.IMPERSONATION_KEYWORDS:
            if keyword in text:
                score += 30
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'critical',
                    'description': f'Impersonates government/authority: {keyword}'
                })
                break
        
        # Check e-commerce (increased from 10 to 15)
        for platform in self.indicators.ECOMMERCE_PLATFORMS:
            if platform in text:
                score += 15
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'medium',
                    'description': f'Mentions platform: {platform.upper()}'
                })
                break
        
        return min(score, 30), indicators
    
    def _check_unrealistic_offers(self, text):
        """Check for too-good-to-be-true offers"""
        score = 0
        indicators = []
        
        # Check for large money amounts (increased from 15 to 20)
        money_pattern = r'₹\s*(\d+,?)+|rs\.?\s*(\d+,?)+|(\d+)\s*(lakh|crore)'
        money_matches = re.findall(money_pattern, text)
        
        if money_matches:
            score += 20
            indicators.append({
                'type': 'unrealistic_offer',
                'severity': 'high',
                'description': 'Mentions large sum of money'
            })
        
        # Check unrealistic claims (increased from 15 to 18)
        matches = [kw for kw in self.indicators.UNREALISTIC_OFFERS if kw in text]
        if matches:
            score += 18
            indicators.append({
                'type': 'unrealistic_offer',
                'severity': 'high',
                'description': f'Unrealistic claims: {", ".join(matches[:2])}'
            })
        
        return min(score, 30), indicators
    
    def _check_formatting(self, text):
        """Check for suspicious formatting"""
        score = 0
        indicators = []
        
        # Excessive exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            score += 8
            indicators.append({
                'type': 'formatting',
                'severity': 'low',
                'description': f'Excessive exclamation marks ({exclamation_count})'
            })
        
        # All caps (aggressive tone)
        if text.isupper() and len(text) > 20:
            score += 10
            indicators.append({
                'type': 'formatting',
                'severity': 'medium',
                'description': 'Message in ALL CAPS (aggressive tone)'
            })
        
        # Excessive emojis
        emoji_pattern = r'[\U0001F300-\U0001F9FF]'
        emoji_count = len(re.findall(emoji_pattern, text))
        if emoji_count > 5:
            score += 5
            indicators.append({
                'type': 'formatting',
                'severity': 'low',
                'description': f'Excessive emojis ({emoji_count})'
            })
        
        return min(score, 15), indicators
    
    def _check_phone_numbers(self, text):
        """Check for phone numbers"""
        score = 0
        indicators = []
        
        # Indian phone number pattern
        phone_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'
        matches = re.findall(phone_pattern, text)
        
        if matches:
            score += 8
            indicators.append({
                'type': 'contact_info',
                'severity': 'low',
                'description': f'Contains phone number(s): {len(matches)} found'
            })
        
        return score, indicators