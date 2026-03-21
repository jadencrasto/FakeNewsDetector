"""
Database Models
SQLAlchemy ORM models for database tables
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from contextlib import contextmanager

class Database:
    """Database connection and operations"""
    
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        if not self.connection_string:
            raise ValueError("DATABASE_URL not set in environment variables")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = psycopg2.connect(self.connection_string)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def save_scan(self, scan_data: dict) -> int:
        """
        Save scan result to database
        
        Args:
            scan_data: Dictionary containing scan results
            
        Returns:
            scan_id: ID of the saved scan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO scans 
                (input_text, input_hash, risk_score, classification, 
                 indicators, recommendations, urls_found, score_breakdown,
                 analysis_time_ms, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING scan_id
            """
            
            cursor.execute(query, (
                scan_data.get('input'),
                scan_data.get('input_hash'),
                scan_data.get('risk_score'),
                scan_data.get('classification'),
                json.dumps(scan_data.get('indicators', [])),
                json.dumps(scan_data.get('recommendations', [])),
                scan_data.get('urls_found', []),
                json.dumps(scan_data.get('score_breakdown', {})),
                scan_data.get('analysis_time_ms'),
                scan_data.get('ip_address')
            ))
            
            scan_id = cursor.fetchone()[0]
            cursor.close()
            
            return scan_id
    
    def get_statistics(self) -> dict:
        """Get overall detection statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    COUNT(*) as total_scans,
                    SUM(CASE WHEN classification = 'scam' THEN 1 ELSE 0 END) as scams_detected,
                    SUM(CASE WHEN classification = 'suspicious' THEN 1 ELSE 0 END) as suspicious,
                    SUM(CASE WHEN classification = 'safe' THEN 1 ELSE 0 END) as safe,
                    ROUND(AVG(risk_score), 2) as avg_risk_score
                FROM scans
            """
            
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else {}
    
    def get_recent_scans(self, limit: int = 10) -> list:
        """Get recent scans"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    scan_id,
                    LEFT(input_text, 100) as input,
                    risk_score,
                    classification,
                    created_at
                FROM scans
                ORDER BY created_at DESC
                LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
    
    def get_top_scam_types(self, limit: int = 5) -> list:
        """Get most common scam types from known_scams"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    scam_type as type,
                    reporter_count as count
                FROM known_scams
                WHERE active = TRUE
                ORDER BY reporter_count DESC
                LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
    
    def check_blacklisted_domain(self, domain: str) -> dict:
        """Check if domain is blacklisted"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT * FROM blacklisted_domains
                WHERE domain = %s AND active = TRUE
            """
            
            cursor.execute(query, (domain,))
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else None
    
    def save_report(self, report_data: dict) -> int:
        """Save user report"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO user_reports 
                (scan_id, report_type, is_scam, comments)
                VALUES (%s, %s, %s, %s)
                RETURNING report_id
            """
            
            cursor.execute(query, (
                report_data.get('scan_id'),
                report_data.get('report_type', 'user_report'),
                report_data.get('is_scam', True),
                report_data.get('comments', '')
            ))
            
            report_id = cursor.fetchone()[0]
            cursor.close()
            
            return report_id
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False