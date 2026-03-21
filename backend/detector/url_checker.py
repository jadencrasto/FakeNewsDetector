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
        # Pattern for full URLs with http/https
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        # Pattern for domains without http/https (e.g., "paytm-prize.tk")
        self.domain_pattern = re.compile(
            r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:tk|ml|ga|cf|gq|com|in|org|net|xyz|top|click|link)\b',
            re.IGNORECASE
        )
    
    def extract_urls(self, text):
        """Extract all URLs from text"""
        # Find URLs with http/https
        urls = self.url_pattern.findall(text)
        
        # Also find domains without http/https and add http:// prefix
        domains = self.domain_pattern.findall(text)
        for domain in domains:
            # Don't add duplicates
            if domain not in urls and f'http://{domain}' not in urls and f'https://{domain}' not in urls:
                urls.append(f'http://{domain}')  # Add http:// prefix for analysis
        
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
        
        # NEW: Check if it's a known legitimate domain - give it a pass
        domain_full = f"{extracted.domain}.{extracted.suffix}".lower()
        trusted_domains = ['amazon.in', 'amazon.com', 'flipkart.com', 'paytm.com', 
                        'onlinesbi.sbi', 'sbi.co.in', 'hdfcbank.com', 'icicibank.com',
                        'gov.in', 'nic.in', 'india.gov.in']
    
        if any(trusted in domain_full for trusted in trusted_domains):
            # It's a legitimate domain - minimal score
            if parsed.scheme == 'http':
                score += 5  # Still penalize HTTP a bit
                indicators.append({
                    'type': 'security',
                    'severity': 'low',
                    'description': 'Known legitimate site but using HTTP instead of HTTPS'
                })
            return min(score, 10), indicators  # Max 10 points for legitimate domains
    
        # Check 1: HTTP vs HTTPS (kept at 15)
        if parsed.scheme == 'http':
            score += 15
            indicators.append({
                'type': 'security',
                'severity': 'medium',
                'description': f'URL not using HTTPS (insecure): {url[:50]}...'
            })
        
        # Check 2: IP address instead of domain (kept at 30)
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.search(ip_pattern, parsed.netloc):
            score += 30
            indicators.append({
                'type': 'url_structure',
                'severity': 'critical',
                'description': 'URL uses IP address instead of domain name'
            })
        
        # Check 3: Suspicious TLD (increased from 20 to 35)
        if extracted.suffix in self.SUSPICIOUS_TLDS:
            score += 35
            indicators.append({
                'type': 'domain',
                'severity': 'critical',
                'description': f'Suspicious domain extension: .{extracted.suffix}'
            })
        
        # Check 4: URL shortener (kept at 15)
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
        
        # Check 7: Typosquatting detection (increased scoring)
        typosquat_score, typosquat_indicators = self._check_typosquatting(extracted.domain)
        score += typosquat_score
        indicators.extend(typosquat_indicators)
        
        # Check 8: Suspicious keywords in URL (increased from 5 to 10)
        suspicious_url_keywords = ['verify', 'secure', 'account', 'update', 'login', 'banking', 'confirm']
        for keyword in suspicious_url_keywords:
            if keyword in url.lower():
                score += 10
                indicators.append({
                    'type': 'url_content',
                    'severity': 'medium',
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
        
        # Check for common typosquatting patterns (increased from 15 to 20)
        typo_patterns = [
            (r'(.)\1{2,}', 'Repeated characters'),  # gooogle.com
            (r'\d', 'Numbers in brand name'),        # amaz0n.com
        ]
        
        for pattern, description in typo_patterns:
            if re.search(pattern, domain_lower):
                for brand in self.LEGITIMATE_DOMAINS.keys():
                    if brand in domain_lower:
                        score += 20
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