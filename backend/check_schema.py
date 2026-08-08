"""
Check database schema
"""
from database.models import Database
from dotenv import load_dotenv
load_dotenv()
db = Database()

try:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Get column names from scans table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'scans'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        print("=" * 70)
        print("SCANS TABLE SCHEMA")
        print("=" * 70)
        
        for col in columns:
            print(f"  {col[0]}: {col[1]}")
        
        print("=" * 70)
        
        cursor.close()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()