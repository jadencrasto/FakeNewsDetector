"""
Scam Detection Indicators
Keywords and patterns for detecting Indian scams
"""

class ScamIndicators:
    """
    Comprehensive scam detection indicators for Indian context
    """
    
    # Urgency and pressure tactics
    URGENCY_KEYWORDS = [
        # English
        'urgent', 'immediately', 'hurry', 'act now', 'limited time',
        'expires today', 'last chance', 'don\'t miss', 'within 24 hours',
        'time sensitive', 'instant', 'right now', 'asap', 'expire soon',
        'limited offer', 'today only', 'hurry up', 'quick', 'fast',
        # Hindi (Romanized)
        'turant', 'jaldi', 'abhi', 'shighra'
    ]
    
    # Money and rewards
    MONEY_KEYWORDS = [
        'won', 'prize', 'reward', 'free', 'cash', 'lottery',
        'jackpot', 'winner', 'selected', 'lucky', 'congratulations',
        'lakh', 'crore', 'thousand', 'million', 'earn',
        '₹', 'rs', 'rupees', 'inr', 'money', 'payment',
        # Hindi
        'jeeta', 'inaam', 'muft', 'nagad', 'paisa'
    ]
    
    # Action requests (social engineering)
    ACTION_KEYWORDS = [
        'click here', 'verify now', 'confirm', 'update', 'download',
        'install', 'activate', 'register', 'claim', 'redeem',
        'enter', 'provide', 'submit', 'send', 'share',
        'tap here', 'follow link', 'visit', 'go to', 'open link',
        # Hindi
        'click karen', 'verify karen', 'confirm karen'
    ]
    
    # Threats and fear tactics
    THREAT_KEYWORDS = [
        'blocked', 'suspended', 'locked', 'terminated', 'deactivated',
        'frozen', 'expired', 'cancelled', 'unauthorized', 'violation',
        'legal action', 'police', 'arrest', 'fine', 'penalty',
        'court', 'lawsuit', 'fraud', 'investigation', 'criminal',
        # Hindi
        'band', 'nilambit', 'bandh'
    ]
    
    # Personal information requests (MAJOR RED FLAG)
    PERSONAL_INFO_KEYWORDS = [
        'password', 'pin', 'otp', 'cvv', 'atm pin', 'passcode',
        'card number', 'account number', 'upi pin', 'mpin',
        'aadhaar', 'aadhar', 'pan', 'pan card', 'pan number',
        'social security', 'ssn', 'date of birth', 'dob',
        'mother\'s name', 'maiden name', 'security question',
        'login credentials', 'username and password'
    ]
    
    # Indian payment systems
    PAYMENT_KEYWORDS = [
        'upi', 'paytm', 'phonepe', 'gpay', 'google pay',
        'bhim', 'whatsapp pay', 'bank transfer', 'neft', 'rtgs',
        'imps', 'wallet', 'qr code', 'scan and pay', 'payment link',
        'netbanking', 'upi id', 'vpa', 'mobile banking'
    ]
    
    # Government/institutional impersonation
    IMPERSONATION_KEYWORDS = [
        'income tax', 'tax department', 'gst', 'customs', 'it department',
        'rbi', 'reserve bank', 'sebi', 'uidai', 'epfo',
        'aadhaar center', 'pan office', 'passport office',
        'government of india', 'sarkari', 'government scheme',
        'pradhan mantri', 'pm scheme', 'central government',
        'state government', 'ministry'
    ]
    
    # Job scam indicators
    JOB_SCAM_KEYWORDS = [
        'work from home', 'part time job', 'data entry',
        'earn money online', 'registration fee', 'training fee',
        'security deposit', 'guarantee job', 'no experience needed',
        'high salary', 'guaranteed income', 'easy work',
        'copy paste job', 'form filling', 'survey job'
    ]
    
    # Too-good-to-be-true offers
    UNREALISTIC_OFFERS = [
        'guaranteed', 'risk free', '100% success', '100% genuine',
        'double your money', 'triple your income', 'get rich',
        'unlimited', 'lifetime', 'exclusive offer', 'limited seats',
        'secret method', 'insider tip', 'proven system',
        'no investment', 'zero risk', 'instant profit'
    ]
    
    # Bank names (for impersonation detection)
    INDIAN_BANKS = [
        'sbi', 'state bank', 'hdfc', 'icici', 'axis', 'kotak',
        'pnb', 'punjab national bank', 'bank of baroda', 'boba', 'canara',
        'union bank', 'indian bank', 'idbi', 'yes bank', 'rbl',
        'indusind', 'idfc', 'federal bank', 'south indian bank',
        'axis bank', 'icici bank', 'hdfc bank'
    ]
    
    # E-commerce platforms
    ECOMMERCE_PLATFORMS = [
        'amazon', 'flipkart', 'myntra', 'snapdeal', 'meesho',
        'ajio', 'nykaa', 'bigbasket', 'swiggy', 'zomato',
        'ola', 'uber', 'rapido', 'dunzo', 'blinkit'
    ]
    
    # Popular brands often impersonated
    POPULAR_BRANDS = [
        'google', 'facebook', 'whatsapp', 'instagram', 'twitter',
        'apple', 'samsung', 'mi', 'xiaomi', 'oppo', 'vivo',
        'airtel', 'jio', 'vodafone', 'idea', 'bsnl',
        'tata', 'reliance', 'adani', 'birla'
    ]
    
    @classmethod
    def get_all_keywords(cls):
        """Get all keywords as a flat list"""
        all_keywords = []
        all_keywords.extend(cls.URGENCY_KEYWORDS)
        all_keywords.extend(cls.MONEY_KEYWORDS)
        all_keywords.extend(cls.ACTION_KEYWORDS)
        all_keywords.extend(cls.THREAT_KEYWORDS)
        all_keywords.extend(cls.PERSONAL_INFO_KEYWORDS)
        all_keywords.extend(cls.PAYMENT_KEYWORDS)
        all_keywords.extend(cls.IMPERSONATION_KEYWORDS)
        all_keywords.extend(cls.JOB_SCAM_KEYWORDS)
        all_keywords.extend(cls.UNREALISTIC_OFFERS)
        return list(set(all_keywords))  # Remove duplicates
    
    @classmethod
    def get_all_brands(cls):
        """Get all brand names"""
        all_brands = []
        all_brands.extend(cls.INDIAN_BANKS)
        all_brands.extend(cls.ECOMMERCE_PLATFORMS)
        all_brands.extend(cls.POPULAR_BRANDS)
        return list(set(all_brands))