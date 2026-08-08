"""
Analytics Module
Generates statistics and charts data for dashboard
"""
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsGenerator:
    """Generate analytics data from database"""
    
    def __init__(self, db):
        self.db = db
    
    def get_dashboard_stats(self) -> dict:
        """
        Get comprehensive dashboard statistics
        
        Returns:
            dict: Dashboard analytics data
        """
        # Get basic stats
        stats = self.db.get_statistics()
        
        # Calculate additional metrics
        total_scans = stats.get('total_scans', 0)
        scams_detected = stats.get('scams_detected', 0)
        
        detection_rate = (scams_detected / total_scans * 100) if total_scans > 0 else 0
        
        # Get classification breakdown for pie chart
        classification_breakdown = self._get_classification_breakdown()
        
        # Get scans over time for line chart
        scans_timeline = self._get_scans_timeline(days=7)
        
        # Get top scam types for bar chart
        top_scam_types = self.db.get_top_scam_types(5)
        
        return {
            'overview': {
                'total_scans': total_scans,
                'scams_detected': scams_detected,
                'suspicious': stats.get('suspicious', 0),
                'safe': stats.get('safe', 0),
                'detection_rate': round(detection_rate, 1),
                'avg_risk_score': stats.get('avg_risk_score', 0)
            },
            'classification_breakdown': classification_breakdown,
            'scans_timeline': scans_timeline,
            'top_scam_types': top_scam_types
        }
    
    def _get_classification_breakdown(self) -> dict:
        """Get breakdown of scans by classification for pie chart"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        classification,
                        COUNT(*) as count
                    FROM scans
                    GROUP BY classification
                """
                
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                
                # Format for chart
                breakdown = {
                    'labels': [],
                    'data': [],
                    'colors': []
                }
                
                color_map = {
                    'safe': '#10B981',      # Green
                    'suspicious': '#F59E0B', # Yellow
                    'scam': '#EF4444'       # Red
                }
                
                for row in results:
                    classification = row[0]
                    count = row[1]
                    
                    breakdown['labels'].append(classification.upper())
                    breakdown['data'].append(count)
                    breakdown['colors'].append(color_map.get(classification, '#6B7280'))
                
                return breakdown
                
        except Exception as e:
            print(f"Error getting classification breakdown: {e}")
            return {'labels': [], 'data': [], 'colors': []}
    
    def _get_scans_timeline(self, days: int = 7) -> dict:
        """Get scans over time for line chart"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get scans from last N days
                query = """
                    SELECT 
                        DATE(created_at) as scan_date,
                        COUNT(*) as count
                    FROM scans
                    WHERE created_at >= NOW() - INTERVAL '%s days'
                    GROUP BY DATE(created_at)
                    ORDER BY scan_date
                """
                
                cursor.execute(query, (days,))
                results = cursor.fetchall()
                cursor.close()
                
                # Create timeline with all days (fill missing with 0)
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=days-1)
                
                # Initialize all dates with 0
                date_counts = {}
                current_date = start_date
                while current_date <= end_date:
                    date_counts[current_date] = 0
                    current_date += timedelta(days=1)
                
                # Fill in actual counts
                for row in results:
                    scan_date = row[0]
                    count = row[1]
                    date_counts[scan_date] = count
                
                # Format for chart
                timeline = {
                    'labels': [],
                    'data': []
                }
                
                for date in sorted(date_counts.keys()):
                    timeline['labels'].append(date.strftime('%b %d'))
                    timeline['data'].append(date_counts[date])
                
                return timeline
                
        except Exception as e:
            print(f"Error getting scans timeline: {e}")
            # Return empty timeline with last 7 days
            end_date = datetime.now().date()
            labels = []
            for i in range(days-1, -1, -1):
                date = end_date - timedelta(days=i)
                labels.append(date.strftime('%b %d'))
            
            return {
                'labels': labels,
                'data': [0] * days
            }