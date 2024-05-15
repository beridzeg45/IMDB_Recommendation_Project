import sqlite3
import datetime

# Create database and table
conn = sqlite3.connect('user_movie_searches.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS movie_searches;')
cursor.execute('CREATE TABLE IF NOT EXISTS movie_searches (search_id INTEGER PRIMARY KEY AUTOINCREMENT, movie_searched TEXT, timestamp TEXT)')
conn.commit()


