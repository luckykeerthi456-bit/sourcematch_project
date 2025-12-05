#!/usr/bin/env python3
"""
Migration script to normalize historical scores in the sourcematch.db database.

Purpose:
  - Normalize Application.score values >1 (divide by 100)
  - Normalize MatchResult.score values >1 (divide by 100)
  - Clamp all scores to [0.0, 1.0]
  - Create a backup before making changes

Usage:
  python migrate_normalize_scores.py
"""

import sqlite3
import shutil
import os
from pathlib import Path

DB_PATH = "sourcematch.db"
BACKUP_PATH = "sourcematch.db.bak"


def backup_database():
    """Create a backup of the database before migration."""
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f"✓ Backup created: {BACKUP_PATH}")
    else:
        print(f"✗ Database not found: {DB_PATH}")
        return False
    return True


def normalize_score(value):
    """Normalize a score to [0.0, 1.0] range."""
    if value is None:
        return 0.0
    try:
        val = float(value)
    except (ValueError, TypeError):
        return 0.0
    
    # If already within 0..1, clamp it
    if 0.0 <= val <= 1.0:
        return max(0.0, min(1.0, val))
    
    # If value >1, divide by 100 (likely a mis-scaled percent like 8.86)
    if val > 1.0:
        val = val / 100.0
    
    # Clamp to [0, 1]
    return max(0.0, min(1.0, val))


def migrate_application_scores(cursor):
    """Normalize scores in the Application table."""
    # Fetch all applications with scores
    cursor.execute("SELECT id, score FROM applications WHERE score IS NOT NULL")
    rows = cursor.fetchall()
    
    updated = 0
    for app_id, score in rows:
        normalized = normalize_score(score)
        # Only update if the value changed
        if abs(normalized - float(score)) > 0.0001:
            cursor.execute("UPDATE applications SET score = ? WHERE id = ?", (normalized, app_id))
            updated += 1
            print(f"  Application {app_id}: {score:.6f} → {normalized:.6f}")
    
    return updated


def migrate_match_result_scores(cursor):
    """Normalize scores in the MatchResult table."""
    # Fetch all match results with scores
    cursor.execute("SELECT id, score FROM match_results WHERE score IS NOT NULL")
    rows = cursor.fetchall()
    
    updated = 0
    for result_id, score in rows:
        normalized = normalize_score(score)
        # Only update if the value changed
        if abs(normalized - float(score)) > 0.0001:
            cursor.execute("UPDATE match_results SET score = ? WHERE id = ?", (normalized, result_id))
            updated += 1
            print(f"  MatchResult {result_id}: {score:.6f} → {normalized:.6f}")
    
    return updated


def main():
    print("=" * 70)
    print("Score Normalization Migration")
    print("=" * 70)
    
    # Step 1: Backup
    print("\n[1/4] Creating backup...")
    if not backup_database():
        print("Migration aborted.")
        return
    
    # Step 2: Connect to DB
    print("\n[2/4] Connecting to database...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print(f"✓ Connected to {DB_PATH}")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return
    
    # Step 3: Migrate Application scores
    print("\n[3/4] Normalizing Application.score...")
    try:
        app_count = migrate_application_scores(cursor)
        print(f"✓ Updated {app_count} application records")
    except Exception as e:
        print(f"✗ Error updating applications: {e}")
        conn.close()
        return
    
    # Step 4: Migrate MatchResult scores
    print("\n[4/4] Normalizing MatchResult.score...")
    try:
        result_count = migrate_match_result_scores(cursor)
        print(f"✓ Updated {result_count} match result records")
    except Exception as e:
        print(f"✗ Error updating match results: {e}")
        conn.close()
        return
    
    # Commit and close
    print("\n[Finalizing] Committing changes...")
    try:
        conn.commit()
        conn.close()
        print("✓ Migration complete!")
        print(f"\nSummary:")
        print(f"  - Applications updated: {app_count}")
        print(f"  - MatchResults updated: {result_count}")
        print(f"  - Backup saved to: {BACKUP_PATH}")
        print(f"\nYou can restore the backup if needed:")
        print(f"  cp {BACKUP_PATH} {DB_PATH}")
    except Exception as e:
        print(f"✗ Error committing: {e}")
        conn.close()


if __name__ == "__main__":
    main()
