"""
API routes for scam detection
"""
from flask import Blueprint, request, jsonify
import time
from detector.analyzer import ScamAnalyzer
from detector.news_analyzer import FakeNewsAnalyzer
from database.models import Database
from flask import send_file
import io
from utils.pdf_generator import PDFReportGenerator
from utils.analytics import AnalyticsGenerator
from flask_limiter import Limiter  # ← ADD THIS
from flask_limiter.util import get_remote_address 

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize analyzer and database
analyzer = ScamAnalyzer()
news_analyzer = FakeNewsAnalyzer()
db = Database()
analytics = AnalyticsGenerator(db)
# Initialize PDF generator
pdf_generator = PDFReportGenerator()

limiter = Limiter(  # ← ADD THIS
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@api_bp.route('/verify-news', methods=['POST'])
def verify_news():
    """Analyze news article for credibility"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Please provide text to analyze'
            }), 400
        
        text = data['text']
        url = data.get('url', '')
        
        # Analyze news
        result = news_analyzer.analyze_news(text, url)
        result['input'] = text
        
        # ADD THIS SECTION - Save to database
        print("📝 Attempting to save news scan to database...")
        result['ip_address'] = request.remote_addr
        scan_id = db.save_scan(result)
        result['scan_id'] = scan_id
        print(f"✅ SUCCESS! News scan saved with ID: {scan_id}")
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'News verification failed',
            'message': str(e)
        }), 500

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """Main endpoint to analyze text/URL for scams"""
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input',
                'message': 'Please provide an "input" field with text or URL to analyze'
            }), 400
        
        input_text = data['input'].strip()
        
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
        
        # Analyze
        result = analyzer.analyze(input_text)
        
        # Save to database
        print(f"📝 Attempting to save scan to database...")
        try:
            result['ip_address'] = request.remote_addr
            scan_id = db.save_scan(result)
            result['scan_id'] = scan_id
            print(f"✅ SUCCESS! Scan saved with ID: {scan_id}")
        except Exception as db_error:
            print(f"❌ DATABASE SAVE FAILED!")
            print(f"Error: {db_error}")
            import traceback
            traceback.print_exc()
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@api_bp.route('/report', methods=['POST'])
def report_scam():
    """Allow users to report scams"""
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing input',
                'message': 'Please provide the scam content to report'
            }), 400
        
        # Save report to database
        try:
            report_data = {
                'scan_id': data.get('scan_id'),
                'report_type': data.get('report_type', 'user_report'),
                'is_scam': True,
                'comments': data.get('comments', '')
            }
            report_id = db.save_report(report_data)
            
            return jsonify({
                'message': 'Report submitted successfully',
                'report_id': report_id,
                'status': 'pending_review',
                'thank_you': 'Thank you for helping make the internet safer!'
            }), 200
        except Exception as db_error:
            print(f"⚠ Failed to save report: {db_error}")
            return jsonify({
                'message': 'Report acknowledged',
                'status': 'pending'
            }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Report submission failed',
            'message': str(e)
        }), 500


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get detection statistics from database"""
    try:
        stats = db.get_statistics()
        top_scams = db.get_top_scam_types(3)
        
        return jsonify({
            'total_scans': stats.get('total_scans', 0),
            'scams_detected': stats.get('scams_detected', 0),
            'suspicious': stats.get('suspicious', 0),
            'safe': stats.get('safe', 0),
            'avg_risk_score': float(stats.get('avg_risk_score', 0)) if stats.get('avg_risk_score') else 0,
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'top_scam_types': [
                {'type': scam['type'].replace('_', ' ').title(), 'count': scam['count']}
                for scam in top_scams
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch statistics',
            'message': str(e)
        }), 500


@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get recent scan history"""
    try:
        recent_scans = db.get_recent_scans(limit=10)
        
        history = []
        for scan in recent_scans:
            history.append({
                'scan_id': scan['scan_id'],
                'input': scan['input'],
                'risk_score': scan['risk_score'],
                'classification': scan['classification'],
                'timestamp': scan['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch history',
            'message': str(e)
        }), 500
    
@api_bp.route('/export-pdf', methods=['POST'])
def export_pdf():
    """
    Export scan result as PDF
    
    Request Body (JSON):
    {
        "result": { ... scan result data ... }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'result' not in data:
            return jsonify({
                'error': 'Missing result data',
                'message': 'Please provide scan result to export'
            }), 400
        
        result = data['result']
        
        # Generate PDF based on type
        if 'credibility_score' in result:
            # News verification report
            pdf_bytes = pdf_generator.generate_news_report(result)
            filename = 'news_credibility_report.pdf'
        else:
            # Scam detection report
            pdf_bytes = pdf_generator.generate_scam_report(result)
            filename = f"scam_report_{result.get('scan_id', 'unknown')}.pdf"
        
        # Create file-like object
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_file.seek(0)
        
        # Send file
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )   
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'PDF generation failed',
            'message': str(e)
        }), 500
    
@api_bp.route('/analytics', methods=['GET'])
@limiter.exempt
def get_analytics():
    """
    Get comprehensive analytics for dashboard
    
    Response includes:
    - Overview stats (total, detection rate, avg score)
    - Classification breakdown (pie chart data)
    - Scans timeline (line chart data)
    - Top scam types (bar chart data)
    """
    try:
        analytics_data = analytics.get_dashboard_stats()
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to fetch analytics',
            'message': str(e)
        }), 500