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
    
    def analyze_text(self, text):
        """
        Analyze text for scam indicators
        Returns: (score, indicators_list)
        """
        score = 0
        indicators_list = []
        text_lower = text.lower()
        
        # Check 1: Urgency keywords
        urgency_score, urgency_indicators = self._check_keywords(
            text_lower, 
            self.indicators.URGENCY_KEYWORDS,
            'urgency',
            weight=8
        )
        score += urgency_score
        indicators_list.extend(urgency_indicators)
        
        # Check 2: Money keywords
        money_score, money_indicators = self._check_keywords(
            text_lower,
            self.indicators.MONEY_KEYWORDS,
            'money_offer',
            weight=10
        )
        score += money_score
        indicators_list.extend(money_indicators)
        
        # Check 3: Action keywords
        action_score, action_indicators = self._check_keywords(
            text_lower,
            self.indicators.ACTION_KEYWORDS,
            'action_request',
            weight=7
        )
        score += action_score
        indicators_list.extend(action_indicators)
        
        # Check 4: Threats
        threat_score, threat_indicators = self._check_keywords(
            text_lower,
            self.indicators.THREAT_KEYWORDS,
            'threats',
            weight=12
        )
        score += threat_score
        indicators_list.extend(threat_indicators)
        
        # Check 5: Personal info requests (CRITICAL)
        personal_score, personal_indicators = self._check_keywords(
            text_lower,
            self.indicators.PERSONAL_INFO_KEYWORDS,
            'personal_info_request',
            weight=15
        )
        score += personal_score
        indicators_list.extend(personal_indicators)
        
        # Check 6: Payment keywords
        payment_score, payment_indicators = self._check_keywords(
            text_lower,
            self.indicators.PAYMENT_KEYWORDS,
            'payment_request',
            weight=10
        )
        score += payment_score
        indicators_list.extend(payment_indicators)
        
        # Check 7: Impersonation
        imperson_score, imperson_indicators = self._check_impersonation(text_lower)
        score += imperson_score
        indicators_list.extend(imperson_indicators)
        
        # Check 8: Too good to be true
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
        
        return min(score, 60), indicators_list  # Cap at 60
    
    def _check_keywords(self, text, keyword_list, category, weight=10):
        """Check for presence of keywords from a list"""
        matches = [kw for kw in keyword_list if kw in text]
        
        if not matches:
            return 0, []
        
        score = min(len(matches) * weight, 25)  # Cap contribution
        
        # Determine severity
        if score > 20:
            severity = 'high'
        elif score > 10:
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
        
        # Check banks
        for bank in self.indicators.INDIAN_BANKS:
            if bank in text:
                score += 15
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'high',
                    'description': f'Mentions bank name: {bank.upper()}'
                })
                break
        
        # Check government
        for keyword in self.indicators.IMPERSONATION_KEYWORDS:
            if keyword in text:
                score += 20
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'critical',
                    'description': f'Impersonates government/authority: {keyword}'
                })
                break
        
        # Check e-commerce
        for platform in self.indicators.ECOMMERCE_PLATFORMS:
            if platform in text:
                score += 10
                indicators.append({
                    'type': 'impersonation',
                    'severity': 'medium',
                    'description': f'Mentions platform: {platform.upper()}'
                })
                break
        
        return min(score, 25), indicators
    
    def _check_unrealistic_offers(self, text):
        """Check for too-good-to-be-true offers"""
        score = 0
        indicators = []
        
        # Check for large money amounts
        money_pattern = r'₹\s*(\d+,?)+|rs\.?\s*(\d+,?)+|(\d+)\s*(lakh|crore)'
        money_matches = re.findall(money_pattern, text)
        
        if money_matches:
            score += 15
            indicators.append({
                'type': 'unrealistic_offer',
                'severity': 'high',
                'description': 'Mentions large sum of money'
            })
        
        # Check unrealistic claims
        matches = [kw for kw in self.indicators.UNREALISTIC_OFFERS if kw in text]
        if matches:
            score += 15
            indicators.append({
                'type': 'unrealistic_offer',
                'severity': 'high',
                'description': f'Unrealistic claims: {", ".join(matches[:2])}'
            })
        
        return min(score, 25), indicators
    
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