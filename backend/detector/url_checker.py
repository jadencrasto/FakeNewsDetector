"""
URL Analysis Module
Checks URLs for suspicious patterns and malicious indicators
"""
import re
import validators
import tldextract
from urllib.parse import urlparse

class URLChecker:
    """Analyze URLs for scam indicators"""
    
    # Suspicious TLDs (top-level domains)
    SUSPICIOUS_TLDS = [
        'tk', 'ml', 'ga', 'cf', 'gq',  # Free domains
        'xyz', 'top', 'work', 'click', 'link',
        'download', 'loan', 'win', 'racing'
    ]
    
    # URL shorteners
    URL_SHORTENERS = [
        'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
        'is.gd', 'buff.ly', 'adf.ly', 'cutt.ly', 'rb.gy'
    ]
    
    # Common typosquatting targets
    LEGITIMATE_DOMAINS = {
        'amazon': ['amazon.in', 'amazon.com'],
        'google': ['google.com', 'google.co.in'],
        'facebook': ['facebook.com'],
        'flipkart': ['flipkart.com'],
        'paytm': ['paytm.com'],
        'sbi': ['onlinesbi.sbi', 'sbi.co.in'],
        'hdfc': ['hdfcbank.com'],
        'icici': ['icicibank.com'],
    }
    
    def __init__(self):
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
    
    def extract_urls(self, text):
        """Extract all URLs from text"""
        urls = self.url_pattern.findall(text)
        return urls
    
    def analyze_url(self, url):
        """
        Analyze a single URL for suspicious indicators
        Returns: (score, indicators)
        """
        score = 0
        indicators = []
        
        if not validators.url(url):
            return 0, []
        
        # Parse URL
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        # Check 1: HTTP vs HTTPS
        if parsed.scheme == 'http':
            score += 15
            indicators.append({
                'type': 'security',
                'severity': 'medium',
                'description': f'URL not using HTTPS (insecure): {url[:50]}...'
            })
        
        # Check 2: IP address instead of domain
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.search(ip_pattern, parsed.netloc):
            score += 30
            indicators.append({
                'type': 'url_structure',
                'severity': 'critical',
                'description': 'URL uses IP address instead of domain name'
            })
        
        # Check 3: Suspicious TLD
        if extracted.suffix in self.SUSPICIOUS_TLDS:
            score += 20
            indicators.append({
                'type': 'domain',
                'severity': 'high',
                'description': f'Suspicious domain extension: .{extracted.suffix}'
            })
        
        # Check 4: URL shortener
        if any(shortener in url.lower() for shortener in self.URL_SHORTENERS):
            score += 15
            indicators.append({
                'type': 'url_structure',
                'severity': 'medium',
                'description': 'URL is shortened (destination unknown)'
            })
        
        # Check 5: Long domain name
        if len(extracted.domain) > 25:
            score += 10
            indicators.append({
                'type': 'url_structure',
                'severity': 'medium',
                'description': f'Unusually long domain name: {extracted.domain}'
            })
        
        # Check 6: Multiple subdomains (suspicious)
        if extracted.subdomain and extracted.subdomain.count('.') >= 2:
            score += 10
            indicators.append({
                'type': 'url_structure',
                'severity': 'low',
                'description': f'Multiple subdomains: {extracted.subdomain}'
            })
        
        # Check 7: Typosquatting detection
        typosquat_score, typosquat_indicators = self._check_typosquatting(extracted.domain)
        score += typosquat_score
        indicators.extend(typosquat_indicators)
        
        # Check 8: Suspicious keywords in URL
        suspicious_url_keywords = ['verify', 'secure', 'account', 'update', 'login', 'banking', 'confirm']
        for keyword in suspicious_url_keywords:
            if keyword in url.lower():
                score += 5
                indicators.append({
                    'type': 'url_content',
                    'severity': 'low',
                    'description': f'Suspicious keyword in URL: {keyword}'
                })
                break
        
        return min(score, 40), indicators  # Cap at 40 points
    
    def _check_typosquatting(self, domain):
        """Check if domain is typosquatting a legitimate brand"""
        score = 0
        indicators = []
        domain_lower = domain.lower()
        
        for brand, legitimate_domains in self.LEGITIMATE_DOMAINS.items():
            # Check if brand name is in domain but it's not the legitimate domain
            if brand in domain_lower:
                is_legitimate = any(legit in domain_lower for legit in legitimate_domains)
                if not is_legitimate:
                    score += 35
                    indicators.append({
                        'type': 'impersonation',
                        'severity': 'critical',
                        'description': f'Possible {brand.upper()} impersonation: {domain}'
                    })
                    break
        
        # Check for common typosquatting patterns
        typo_patterns = [
            (r'(.)\1{2,}', 'Repeated characters'),  # gooogle.com
            (r'\d', 'Numbers in brand name'),        # amaz0n.com
        ]
        
        for pattern, description in typo_patterns:
            if re.search(pattern, domain_lower):
                for brand in self.LEGITIMATE_DOMAINS.keys():
                    if brand in domain_lower:
                        score += 15
                        indicators.append({
                            'type': 'typosquatting',
                            'severity': 'high',
                            'description': f'{description}: {domain}'
                        })
                        break
        
        return score, indicators
    
    def analyze_all_urls(self, text):
        """Extract and analyze all URLs in text"""
        urls = self.extract_urls(text)
        
        if not urls:
            return 0, [], []
        
        total_score = 0
        all_indicators = []
        
        for url in urls:
            score, indicators = self.analyze_url(url)
            total_score += score
            all_indicators.extend(indicators)
        
        # Don't let URL score exceed 40
        return min(total_score, 40), all_indicators, urls