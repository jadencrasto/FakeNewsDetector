"""
View all scans in database
"""
from dotenv import load_dotenv
load_dotenv()

from database.models import Database

db = Database()

print("=" * 80)
print("ALL SCANS IN DATABASE")
print("=" * 80)

stats = db.get_statistics()
print(f"\n📊 STATISTICS:")
print(f"   Total scans: {stats.get('total_scans', 0)}")
print(f"   Scams: {stats.get('scams_detected', 0)}")
print(f"   Suspicious: {stats.get('suspicious', 0)}")
print(f"   Safe: {stats.get('safe', 0)}")
print(f"   Avg Risk Score: {stats.get('avg_risk_score', 0)}")

scans = db.get_recent_scans(100)
print(f"\n📝 ALL SCANS ({len(scans)}):")
print("=" * 80)

for i, scan in enumerate(scans, 1):
    print(f"\n{i}. Scan ID: {scan['scan_id']}")
    print(f"   Input: {scan['input'][:70]}...")
    print(f"   Risk Score: {scan['risk_score']}/100")
    print(f"   Classification: {scan['classification'].upper()}")
    print(f"   Time: {scan['created_at']}")
    print("-" * 80)

print("\n✅ Database is working perfectly!")