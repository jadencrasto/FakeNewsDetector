"""
Fake News & Misinformation Detection Module
Analyzes news articles and claims for credibility
"""
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

class FakeNewsAnalyzer:
    """
    Analyzes news content for credibility and misinformation
    """
    
    # Credible news sources (Indian & International)
    CREDIBLE_SOURCES = {
        # Indian Sources
        'thehindu.com', 'indianexpress.com', 'ndtv.com', 'thequint.com',
        'scroll.in', 'livemint.com', 'business-standard.com', 'moneycontrol.com',
        'pib.gov.in',  # Press Information Bureau (Government)
        
        # International Sources
        'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk',
        'aljazeera.com', 'theguardian.com', 'nytimes.com',
        'washingtonpost.com', 'economist.com'
    }
    
    # Known fake news / unreliable sources
    UNRELIABLE_SOURCES = {
        'fakingnews.com', 'newsthump.com', 'theonion.com',
        'worldnewsdailyreport.com', 'huzlers.com', 'empirenews.net',
        'nationalreport.net', 'newsnerd.com', 'react365.com'
    }
    
    # Fact-checking websites
    FACT_CHECKING_SITES = {
        'factcheck.org', 'snopes.com', 'politifact.com',
        'fullfact.org', 'factcheck.afp.com', 'boomlive.in',
        'altnews.in', 'thequint.com/news/webqoof', 'vishvasnews.com'
    }
    
    # Sensationalized/clickbait keywords
    SENSATIONAL_KEYWORDS = [
        'shocking', 'unbelievable', 'you won\'t believe', 'mind-blowing',
        'jaw-dropping', 'incredible', 'miraculous', 'explosive',
        'bombshell', 'devastating', 'breaking news', 'just in',
        'alert', 'warning', 'urgent', 'must read', 'must see',
        'viral', 'trending now', 'going viral', 'everyone is talking',
        # Hindi transliterations
        'khabar', 'breaking', 'viral', 'shocking news'
    ]
    
    # Emotional manipulation indicators
    EMOTIONAL_TRIGGERS = [
        'outrage', 'fury', 'anger', 'fear', 'panic', 'terror',
        'horror', 'disgust', 'hate', 'love', 'heartwarming',
        'tearjerker', 'emotional', 'touching', 'inspiring'
    ]
    
    # Clickbait patterns (regex)
    CLICKBAIT_PATTERNS = [
        r'\d+\s+(things|ways|reasons|facts|secrets)',  # "10 things you..."
        r'(what|why|how)\s+.+\s+(will|might|should)',  # "What you should know"
        r'number\s+\d+\s+will\s+(shock|surprise|amaze)',  # "Number 5 will shock you"
        r'(doctors|scientists|experts)\s+hate\s+this',  # "Doctors hate this"
        r'this\s+one\s+(trick|tip|secret|hack)',  # "This one trick"
    ]
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def analyze_news(self, text: str, url: str = None) -> dict:
        """
        Main analysis function for news verification
        
        Args:
            text: News headline or article text
            url: Source URL (optional)
        
        Returns:
            dict: Credibility score, classification, evidence
        """
        result = {
            'input': text[:200] + '...' if len(text) > 200 else text,
            'credibility_score': 0,
            'classification': 'unverified',
            'indicators': [],
            'sources_checked': [],
            'recommendations': []
        }
        
        scores = {
            'content_score': 0,
            'source_score': 0,
            'verification_score': 0
        }
        
        # Step 1: Content Analysis
        content_score, content_indicators = self._analyze_content(text)
        scores['content_score'] = content_score
        result['indicators'].extend(content_indicators)
        
        # Step 2: Source Credibility (if URL provided)
        if url:
            source_score, source_indicators = self._analyze_source(url)
            scores['source_score'] = source_score
            result['indicators'].extend(source_indicators)
        
        # Step 3: Web Verification (search for the claim)
        verification_score, sources = self._verify_claim(text)
        scores['verification_score'] = verification_score
        result['sources_checked'] = sources
        
        # Calculate final credibility score
        # Higher score = More credible
        # Content: 30%, Source: 30%, Verification: 40%
        final_score = (
            content_score * 0.3 +
            (source_score * 0.3 if url else 0) +
            verification_score * 0.4
        )
        
        result['credibility_score'] = int(final_score)
        result['classification'] = self._classify_credibility(final_score)
        result['recommendations'] = self._generate_recommendations(
            result['classification'],
            result['indicators']
        )
        result['score_breakdown'] = scores
        result['risk_score'] = result['credibility_score']
        return result
    
    def _analyze_content(self, text: str) -> tuple:
        """Analyze content for sensationalism, clickbait, emotional manipulation"""
        score = 50  # Start at neutral
        indicators = []
        text_lower = text.lower()
        
        # Check for sensational language (reduces credibility)
        sensational_matches = [kw for kw in self.SENSATIONAL_KEYWORDS if kw in text_lower]
        if sensational_matches:
            penalty = min(len(sensational_matches) * 5, 20)
            score -= penalty
            indicators.append({
                'type': 'sensationalism',
                'severity': 'medium',
                'description': f'Contains sensational language: {", ".join(sensational_matches[:3])}'
            })
        
        # Check for emotional manipulation
        emotional_matches = [kw for kw in self.EMOTIONAL_TRIGGERS if kw in text_lower]
        if len(emotional_matches) > 2:
            score -= 15
            indicators.append({
                'type': 'emotional_manipulation',
                'severity': 'medium',
                'description': f'Uses emotional triggers: {", ".join(emotional_matches[:3])}'
            })
        
        # Check for clickbait patterns
        clickbait_found = []
        for pattern in self.CLICKBAIT_PATTERNS:
            if re.search(pattern, text_lower):
                clickbait_found.append(pattern)
        
        if clickbait_found:
            score -= 20
            indicators.append({
                'type': 'clickbait',
                'severity': 'high',
                'description': 'Uses clickbait patterns (e.g., "You won\'t believe...", "Number X will shock you")'
            })
        
        # Check for ALL CAPS (aggressive/sensational)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3 and len(text) > 20:
            score -= 10
            indicators.append({
                'type': 'formatting',
                'severity': 'low',
                'description': 'Excessive use of CAPS (aggressive tone)'
            })
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            score -= 5
            indicators.append({
                'type': 'formatting',
                'severity': 'low',
                'description': f'Excessive exclamation marks ({exclamation_count})'
            })
        
        # Positive indicators (increase credibility)
        # Check for specific dates, numbers, quotes (factual indicators)
        if re.search(r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}', text):
            score += 10
            indicators.append({
                'type': 'factual',
                'severity': 'positive',
                'description': 'Contains specific dates (factual indicator)'
            })
        
        # Check for attributions ("according to", "says", "reported by")
        attribution_patterns = ['according to', 'says', 'reported by', 'source:', 'citing']
        if any(pattern in text_lower for pattern in attribution_patterns):
            score += 20
            indicators.append({
                'type': 'attribution',
                'severity': 'positive',
                'description': 'Properly attributes information to sources'
            })
        
        return max(0, min(score, 100)), indicators
    
    def _analyze_source(self, url: str) -> tuple:
        """Analyze source credibility based on domain"""
        score = 50
        indicators = []
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower().replace('www.', '')
            
            # Check if it's a credible source
            if any(credible in domain for credible in self.CREDIBLE_SOURCES):
                score = 95
                indicators.append({
                    'type': 'source_credibility',
                    'severity': 'positive',
                    'description': f'Credible news source: {domain}'
                })
            
            # Check if it's a known unreliable source
            elif any(unreliable in domain for unreliable in self.UNRELIABLE_SOURCES):
                score = 10
                indicators.append({
                    'type': 'source_credibility',
                    'severity': 'critical',
                    'description': f'Known unreliable/satire source: {domain}'
                })
            
            # Check for HTTPS
            if parsed.scheme != 'https':
                score -= 10
                indicators.append({
                    'type': 'security',
                    'severity': 'low',
                    'description': 'Website does not use HTTPS'
                })
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                score -= 30
                indicators.append({
                    'type': 'domain',
                    'severity': 'high',
                    'description': f'Suspicious domain extension: {domain.split(".")[-1]}'
                })
            
        except Exception as e:
            indicators.append({
                'type': 'error',
                'severity': 'low',
                'description': f'Could not analyze source URL: {str(e)}'
            })
        
        return max(0, min(score, 100)), indicators
    
    def _verify_claim(self, text: str) -> tuple:
        """
        Search web to verify the claim
        Returns: (verification_score, list_of_sources)
        """
        score = 50
        sources = []
        
        try:
            # Extract main claim (first 100 chars as search query)
            search_query = text[:100].strip()
            
            # Search Google News (simplified - in production use proper API)
            # For now, we'll do basic credibility heuristics
            
            # Check if claim contains specific verifiable elements
            has_specific_details = any([
                re.search(r'\d+', text),  # Numbers
                re.search(r'\d{4}', text),  # Years
                re.search(r'[A-Z][a-z]+ \d+', text),  # "January 15"
            ])
            
            if has_specific_details:
                score += 20
                sources.append({
                    'type': 'analysis',
                    'note': 'Contains specific, verifiable details'
                })
            
            # In a real implementation, you would:
            # 1. Use Google Custom Search API or News API
            # 2. Search fact-checking sites
            # 3. Compare multiple sources
            # 4. Use NLP to check if sources support or contradict the claim
            
        except Exception as e:
            print(f"Verification error: {e}")
        
        return max(0, min(score, 100)), sources
    
    def _classify_credibility(self, score: int) -> str:
        """Classify credibility based on score"""
        if score >= 70:
            return 'verified'  # Likely true/credible
        elif score >= 40:
            return 'unverified'  # Cannot confirm
        else:
            return 'false'  # Likely false/misleading
    
    def _generate_recommendations(self, classification: str, indicators: list) -> list:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if classification == 'false':
            recommendations.extend([
                '🚫 Likely FALSE or MISLEADING information',
                '⚠️ Do NOT share this without verification',
                '🔍 Cross-check with credible news sources',
                '📰 Look for coverage from Reuters, AP, BBC, The Hindu',
                '✅ Check fact-checking sites: AltNews, Boom, Vishvas News'
            ])
        elif classification == 'unverified':
            recommendations.extend([
                '⚠️ Cannot verify - treat with caution',
                '🔍 Search for this news on credible sources',
                '📰 Check if mainstream media has covered this',
                '✅ Look for official statements or press releases',
                '💭 Consider waiting for more information before sharing'
            ])
        else:
            recommendations.extend([
                '✅ Appears credible based on analysis',
                '💡 Still verify through multiple sources',
                '📰 Check the original source and publication date',
                '🔗 Ensure URL matches the official news site'
            ])
        
        # Add specific recommendations based on indicators
        indicator_types = [ind['type'] for ind in indicators]
        
        if 'clickbait' in indicator_types or 'sensationalism' in indicator_types:
            recommendations.insert(0, '⚠️ WARNING: Content uses sensational/clickbait language')
        
        if 'source_credibility' in indicator_types:
            if any(ind['severity'] == 'critical' for ind in indicators if ind['type'] == 'source_credibility'):
                recommendations.insert(0, '🚫 SOURCE IS KNOWN FOR SATIRE/FAKE NEWS')
        
        return recommendations