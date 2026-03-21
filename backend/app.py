"""
Main Flask application
AI Scam Detector API
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
import os

def create_app(config_name=None):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS (Cross-Origin Resource Sharing)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Rate limiting to prevent abuse
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config['RATELIMIT_STORAGE_URL'],
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )
    
    # Register blueprints (routes)
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Route not found',
            'message': 'The requested URL was not found on the server.'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'error': 'Internal server error',
            'message': 'Something went wrong on our end.'
        }), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Handle rate limit exceeded"""
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Check if API is running"""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'environment': config_name,
            'message': 'AI Scam Detector API is running'
        }), 200
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint with API info"""
        return jsonify({
            'name': 'AI Scam Detector API',
            'version': '1.0.0',
            'description': 'Detect scams, fake news, and phishing attempts',
            'endpoints': {
                'health': '/health',
                'analyze': '/api/analyze',
                'report': '/api/report',
                'stats': '/api/stats',
                'history': '/api/history'
            }
        }), 200
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Run the application
    port = app.config['PORT']
    debug = app.config['DEBUG']
    host = app.config['HOST']
    
    print("=" * 60)
    print("🚀 AI SCAM DETECTOR API")
    print("=" * 60)
    print(f"📊 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🌐 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📡 CORS enabled for: {app.config['CORS_ORIGINS']}")
    print("=" * 60)
    print("Endpoints:")
    print(f"  → Health Check:    http://localhost:{port}/health")
    print(f"  → Scam Detection:  http://localhost:{port}/api/analyze")
    print(f"  → News Verify:     http://localhost:{port}/api/verify-news")
    print(f"  → Stats:           http://localhost:{port}/api/stats")
    print(f"  → History:         http://localhost:{port}/api/history")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )