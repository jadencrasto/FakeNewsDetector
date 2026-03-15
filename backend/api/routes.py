"""
API routes for scam detection
"""
from flask import Blueprint, request, jsonify
import hashlib
import time
from detector.analyzer import ScamAnalyzer

# Create Blueprint
api_bp = Blueprint('api', __name__)
analyzer = ScamAnalyzer()

# We'll import the detector in Part 3B
# For now, we'll use mock responses

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Main endpoint to analyze text/URL for scams
    
    Request Body (JSON):
    {
        "input": "text or URL to analyze"
    }
    
    Response (JSON):
    {
        "risk_score": 85,
        "classification": "scam",
        "indicators": [...],
        "recommendations": [...]
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate input
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input',
                'message': 'Please provide an "input" field with text or URL to analyze'
            }), 400
        
        input_text = data['input'].strip()
        
        # Validate input length
        if len(input_text) == 0:
            return jsonify({
                'error': 'Empty input',
                'message': 'Input cannot be empty'
            }), 400
        
        if len(input_text) > 5000:
            return jsonify({
                'error': 'Input too long',
                'message': 'Input exceeds maximum length of 5000 characters'
            }), 400
        
        # 🎯 ACTUAL ANALYSIS HAPPENS HERE!
        result = analyzer.analyze(input_text)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

@api_bp.route('/report', methods=['POST'])
def report_scam():
    """
    Allow users to report scams or provide feedback
    
    Request Body (JSON):
    {
        "input": "scam message or URL",
        "report_type": "false_positive|new_scam|verify_scam",
        "comments": "user comments"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing input',
                'message': 'Please provide the scam content to report'
            }), 400
        
        # TODO: Save to database in Part 3C
        # For now, just acknowledge
        
        return jsonify({
            'message': 'Report submitted successfully',
            'status': 'pending_review',
            'thank_you': 'Thank you for helping make the internet safer!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Report submission failed',
            'message': str(e)
        }), 500


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get detection statistics
    
    Response (JSON):
    {
        "total_scans": 1000,
        "scams_detected": 350,
        "safe": 500,
        "suspicious": 150
    }
    """
    try:
        # TODO: Get from database in Part 3C
        # For now, return mock data
        
        stats = {
            'total_scans': 1247,
            'scams_detected': 423,
            'suspicious': 135,
            'safe': 689,
            'avg_risk_score': 42.5,
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'top_scam_types': [
                {'type': 'UPI Fraud', 'count': 156},
                {'type': 'Fake Job Offers', 'count': 89},
                {'type': 'Phishing', 'count': 178}
            ]
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch statistics',
            'message': str(e)
        }), 500


@api_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get scan history
    (In production, this would require user authentication)
    """
    try:
        # TODO: Get from database in Part 3C
        # Mock data for now
        
        history = [
            {
                'scan_id': 1,
                'input': 'You won ₹50,000 in lottery...',
                'risk_score': 85,
                'classification': 'scam',
                'timestamp': '2024-02-16 09:30:00'
            },
            {
                'scan_id': 2,
                'input': 'Your Amazon order has been shipped...',
                'risk_score': 15,
                'classification': 'safe',
                'timestamp': '2024-02-16 10:15:00'
            }
        ]
        
        return jsonify({
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch history',
            'message': str(e)
        }), 500