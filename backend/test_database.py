"""
Test Database Connection
"""
from dotenv import load_dotenv  # ← Add this import
import sys

# Load environment variables from .env file
load_dotenv()  # ← Add this line

from database.models import Database

print("=" * 60)
print("Testing Database Connection")
print("=" * 60)


try:
    db = Database()
    
    # Test connection
    print("\n1. Testing connection...")
    if db.test_connection():
        print("✓ Database connection successful!")
    else:
        print("✗ Database connection failed!")
        sys.exit(1)
    
    # Test statistics
    print("\n2. Getting statistics...")
    stats = db.get_statistics()
    print(f"✓ Total scans: {stats.get('total_scans', 0)}")
    print(f"✓ Scams detected: {stats.get('scams_detected', 0)}")
    
    # Test top scam types
    print("\n3. Getting top scam types...")
    scam_types = db.get_top_scam_types(3)
    for scam in scam_types:
        print(f"✓ {scam['type']}: {scam['count']} reports")
    
    print("\n" + "=" * 60)
    print("✓ All database tests passed!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)