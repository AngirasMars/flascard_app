import sqlite3

def view_flashcards():
    # Connect to the SQLite database
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()

    # Execute a query to select all rows from the flashcards table
    cursor.execute("SELECT * FROM flashcards")
    
    # Fetch all rows and print them
    flashcards = cursor.fetchall()
    for flashcard in flashcards:
        print(f"ID: {flashcard[0]}, Question: {flashcard[1]}, Answer: {flashcard[2]}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    view_flashcards()  # Call the function to print flashcards
