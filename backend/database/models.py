"""
Database Models
SQLAlchemy ORM models for database tables
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from contextlib import contextmanager
import hashlib  # ← ADD THIS LINE
from datetime import datetime

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
        """Save scan result to database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Generate hash of input for duplicate detection
                input_hash = hashlib.md5(scan_data['input'].encode()).hexdigest()
                
                # Get URLs as a Python list (not JSON string)
                urls = scan_data.get('urls_found', [])
                if isinstance(urls, str):
                    urls = json.loads(urls)

                # Prepare data
                query = """
                    INSERT INTO scans (
                        input_text, input_hash, risk_score, classification,
                        indicators, recommendations, urls_found,
                        score_breakdown, ip_address, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    RETURNING scan_id
                """

                cursor.execute(query, (
                    scan_data['input'],
                    input_hash,
                    scan_data.get('risk_score') or scan_data.get('credibility_score', 0),
                    scan_data.get('classification', 'unknown'),
                    json.dumps(scan_data.get('indicators', [])),
                    json.dumps(scan_data.get('recommendations', [])),
                    urls,  # ← FIXED - Pass as Python list, PostgreSQL will convert to ARRAY
                    json.dumps(scan_data.get('score_breakdown', {})),
                    scan_data.get('ip_address', '0.0.0.0')
                ))
                
                scan_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                
                return scan_id
                
        except Exception as e:
            print(f"Error saving scan: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_statistics(self):
        """Get overall statistics from database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get overall stats
                stats_query = """
                    SELECT 
                        COUNT(*) as total_scans,
                        COUNT(CASE WHEN classification = 'scam' THEN 1 END) as scams,
                        COUNT(CASE WHEN classification = 'suspicious' THEN 1 END) as suspicious,
                        COUNT(CASE WHEN classification = 'safe' THEN 1 END) as safe,
                        COALESCE(AVG(risk_score), 0) as avg_risk_score
                    FROM scans
                """
                
                cursor.execute(stats_query)
                result = cursor.fetchone()
                cursor.close()
                
                if result:
                    return {
                        'total_scans': result[0],
                        'scams_detected': result[1],
                        'suspicious': result[2],
                        'safe': result[3],
                        'avg_risk_score': round(result[4], 1)
                    }
                else:
                    return {
                        'total_scans': 0,
                        'scams_detected': 0,
                        'suspicious': 0,
                        'safe': 0,
                        'avg_risk_score': 0
                    }
                    
        except Exception as e:
            print(f"Error getting statistics: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_scans': 0,
                'scams_detected': 0,
                'suspicious': 0,
                'safe': 0,
                'avg_risk_score': 0
            }
    
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
    
    def get_top_scam_types(self, limit=5):
        """Get top scam types by frequency"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use input_text column (not input!)
                query = """
                    SELECT 
                        'Lottery/Prize Scams' as scam_type,
                        COUNT(*) as count
                    FROM scans
                    WHERE classification = 'scam' 
                    AND (input_text ILIKE '%%lottery%%' OR input_text ILIKE '%%won%%' OR input_text ILIKE '%%prize%%')
                    
                    UNION ALL
                    
                    SELECT 
                        'Banking Fraud' as scam_type,
                        COUNT(*) as count
                    FROM scans
                    WHERE classification = 'scam' 
                    AND (input_text ILIKE '%%bank%%' OR input_text ILIKE '%%account%%' OR input_text ILIKE '%%sbi%%' OR input_text ILIKE '%%hdfc%%')
                    
                    UNION ALL
                    
                    SELECT 
                        'Payment Scams' as scam_type,
                        COUNT(*) as count
                    FROM scans
                    WHERE classification = 'scam' 
                    AND (input_text ILIKE '%%upi%%' OR input_text ILIKE '%%paytm%%' OR input_text ILIKE '%%pin%%')
                    
                    UNION ALL
                    
                    SELECT 
                        'Government Impersonation' as scam_type,
                        COUNT(*) as count
                    FROM scans
                    WHERE classification = 'scam' 
                    AND (input_text ILIKE '%%government%%' OR input_text ILIKE '%%tax%%' OR input_text ILIKE '%%kyc%%')
                    
                    UNION ALL
                    
                    SELECT 
                        'Job Scams' as scam_type,
                        COUNT(*) as count
                    FROM scans
                    WHERE classification = 'scam' 
                    AND (input_text ILIKE '%%job%%' OR input_text ILIKE '%%work from home%%')
                    
                    ORDER BY count DESC
                    LIMIT 5
                """
                
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                
                # Format results
                top_types = []
                for row in results:
                    if row[1] > 0:
                        top_types.append({
                            'type': row[0],
                            'count': row[1]
                        })
                
                if not top_types:
                    top_types = [{'type': 'No scams detected yet', 'count': 0}]
                
                return top_types
                
        except Exception as e:
            print(f"Error getting top scam types: {e}")
            import traceback
            traceback.print_exc()
            return [{'type': 'Error loading data', 'count': 0}]
    
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