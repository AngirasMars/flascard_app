import sqlite3

def create_db():
    conn = sqlite3.connect('flashcards.db')  # This creates a new database file named flashcards.db
    cursor = conn.cursor()
    
    # Create a table for flashcards (if it doesn't exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT
    )
    ''')
    
    conn.commit()  # Save changes
    conn.close()   # Close the database connection

if __name__ == '__main__':
    create_db()  # This will create the database and the flashcards table when run
