"""
Main Scam Analyzer
Combines URL checking, text analysis, and risk scoring
"""
import hashlib
import time
from detector.url_checker import URLChecker
from detector.text_analyzer import TextAnalyzer

class ScamAnalyzer:
    """
    Main analyzer that combines all detection methods
    """
    
    def __init__(self):
        self.url_checker = URLChecker()
        self.text_analyzer = TextAnalyzer()
        
        # Risk thresholds
        self.SAFE_THRESHOLD = 30
        self.SUSPICIOUS_THRESHOLD = 60
    
    def analyze(self, input_text):
        """
        Main analysis function
        
        Args:
            input_text (str): Text or URL to analyze
        
        Returns:
            dict: Analysis results with risk score, classification, indicators, etc.
        """
        start_time = time.time()
        
        # Initialize result
        result = {
            'input': input_text[:200] + '...' if len(input_text) > 200 else input_text,
            'input_hash': self._generate_hash(input_text),
            'risk_score': 0,
            'classification': 'safe',
            'indicators': [],
            'recommendations': [],
            'urls_found': [],
            'analysis_time_ms': 0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Track scores from different components
        scores = {
            'url_score': 0,
            'text_score': 0,
            'total_score': 0
        }
        
        # Step 1: URL Analysis
        url_score, url_indicators, urls = self.url_checker.analyze_all_urls(input_text)
        scores['url_score'] = url_score
        result['indicators'].extend(url_indicators)
        result['urls_found'] = urls
        
        # Step 2: Text Analysis
        text_score, text_indicators = self.text_analyzer.analyze_text(input_text)
        scores['text_score'] = text_score
        result['indicators'].extend(text_indicators)
        
        # Step 3: Calculate total risk score
        # URL analysis: 40% weight, Text analysis: 60% weight
        total_score = min(url_score + text_score, 100)
        scores['total_score'] = total_score
        result['risk_score'] = total_score
        
        # Step 4: Classify based on score
        result['classification'] = self._classify(total_score)
        
        # Step 5: Generate recommendations
        result['recommendations'] = self._generate_recommendations(
            result['classification'],
            result['indicators']
        )
        
        # Step 6: Calculate analysis time
        analysis_time = int((time.time() - start_time) * 1000)
        result['analysis_time_ms'] = analysis_time
        
        # Add score breakdown (useful for debugging)
        result['score_breakdown'] = scores
        
        return result
    
    def _generate_hash(self, text):
        """Generate SHA-256 hash of input (for duplicate detection)"""
        hash_object = hashlib.sha256(text.encode())
        return hash_object.hexdigest()[:16]  # First 16 chars
    
    def _classify(self, score):
        """
        Classify risk level based on score
        
        0-30: Safe
        31-60: Suspicious
        61-100: Scam
        """
        if score <= self.SAFE_THRESHOLD:
            return 'safe'
        elif score <= self.SUSPICIOUS_THRESHOLD:
            return 'suspicious'
        else:
            return 'scam'
    
    def _generate_recommendations(self, classification, indicators):
        """Generate safety recommendations based on classification"""
        recommendations = []
        
        if classification == 'scam':
            recommendations.extend([
                '🚫 DO NOT click any links in this message',
                '🚫 DO NOT share personal information (OTP, PIN, password)',
                '🚫 DO NOT make any payments',
                '📱 Block the sender immediately',
                '👮 Report to cybercrime.gov.in if you lost money',
                '⚠️ Warn friends and family about this scam'
            ])
        elif classification == 'suspicious':
            recommendations.extend([
                '⚠️ Be very cautious - this message has suspicious elements',
                '🔍 Verify sender identity through official channels',
                '❌ Do not share sensitive information',
                '🔗 Do not click links - visit official website directly',
                '📞 Contact the company/bank using official phone numbers',
                '💭 If it seems too good to be true, it probably is'
            ])
        else:
            recommendations.extend([
                '✅ No immediate scam indicators detected',
                '💡 Always verify sender before sharing personal info',
                '🔒 Ensure websites use HTTPS before entering data',
                '📧 Be cautious with unsolicited messages'
            ])
        
        # Add specific recommendations based on indicators
        indicator_types = [ind['type'] for ind in indicators]
        
        if 'personal_info_request' in indicator_types:
            recommendations.insert(0, '🔴 CRITICAL: Never share OTP, PIN, or passwords via message/call')
        
        if 'impersonation' in indicator_types:
            recommendations.insert(0, '⚠️ Possible impersonation - verify through official channels only')
        
        if 'url_structure' in indicator_types or 'domain' in indicator_types:
            recommendations.insert(0, '🔗 Suspicious link detected - do not click')
        
        return recommendations