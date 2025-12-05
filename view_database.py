#!/usr/bin/env python
"""View SourceMatch database statistics"""

import sqlite3
import os

conn = sqlite3.connect('sourcematch.db')
cursor = conn.cursor()

print('╔════════════════════════════════════════════════════════════╗')
print('║          SOURCEMATCH DATABASE OVERVIEW                    ║')
print('╚════════════════════════════════════════════════════════════╝')
print()

# Tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print('📋 TABLES:')
for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table[0]};')
    count = cursor.fetchone()[0]
    print(f'   • {table[0]:<20} → {count} records')

print()

# Users
print('👥 USERS:')
cursor.execute('SELECT COUNT(*) FROM users;')
print(f'   Total users: {cursor.fetchone()[0]}')

print()

# Jobs
print('💼 JOBS:')
cursor.execute('SELECT COUNT(*) FROM jobs;')
count = cursor.fetchone()[0]
print(f'   Total jobs: {count}')
cursor.execute('SELECT title FROM jobs LIMIT 3;')
for title in cursor.fetchall():
    print(f'   • {title[0]}')

print()

# Database File Info
db_path = 'sourcematch.db'
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f'📁 DATABASE FILE:')
    print(f'   Location: {os.path.abspath(db_path)}')
    print(f'   Size: {size:,} bytes ({size/1024:.2f} KB)')

print()
print('═' * 62)

conn.close()
