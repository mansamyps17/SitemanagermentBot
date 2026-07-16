import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_db():
    """បង្កើតតារាងទិន្នន័យ (Database) ប្រសិនបើមិនទាន់មាន"""
    try:
        conn = sqlite3.connect('samy_construction.db')
        cursor = conn.cursor()
        
        # បង្កើតតារាងគំរូសម្រាប់រក្សាទុកអ្នកប្រើប្រាស់
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                first_name TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
