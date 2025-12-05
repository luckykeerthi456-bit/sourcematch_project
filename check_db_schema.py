import sqlite3
conn = sqlite3.connect('sourcematch.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", [t[0] for t in tables])

# Check if applications table exists and show sample scores
if any(t[0] == 'applications' for t in tables):
    cursor.execute("SELECT id, score FROM applications WHERE score IS NOT NULL LIMIT 5")
    apps = cursor.fetchall()
    print("Sample Application scores:")
    for app_id, score in apps:
        print(f"  App {app_id}: {score}")

# Check if match_results table exists and show sample scores
if any(t[0] == 'match_results' for t in tables):
    cursor.execute("SELECT id, score FROM match_results WHERE score IS NOT NULL LIMIT 5")
    results = cursor.fetchall()
    print("Sample MatchResult scores:")
    for result_id, score in results:
        print(f"  Result {result_id}: {score}")

conn.close()
