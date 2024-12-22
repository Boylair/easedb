from easedb import Database

def getting_started_example():
    """
    EaseDB Getting Started Guide
    
    This example demonstrates the basic operations of EaseDB:
    1. Creating a database connection
    2. Creating a table using EaseDB methods
    3. Inserting data
    4. Querying data
    5. Updating data
    6. Deleting data
    """
    
    # 1. Create a database connection (SQLite in-memory database)
    db = Database('sqlite:///example.db')
    
    # 2. Create a table for books using EaseDB method
    db.create_table('books', {
        'id': 'INTEGER PRIMARY KEY',
        'title': 'TEXT NOT NULL',
        'author': 'TEXT',
        'published_year': 'INTEGER'
    })
    
    # 3. Insert a single book
    db.set('books', {
        'title': 'Python Basics',
        'author': 'John Smith',
        'published_year': 2022
    })
    
    # Insert multiple books
    db.set('books', [
        {
            'title': 'Data Science Handbook',
            'author': 'Jane Doe',
            'published_year': 2021
        },
        {
            'title': 'Web Development',
            'author': 'Mike Johnson',
            'published_year': 2020
        }
    ])
    
    # 4. Query data: Get a single book
    book = db.get('books', {'title': 'Python Basics'})
    print("Single Book:", book)
    
    # Query all books
    all_books = db.get_all('books')
    print("All Books:", all_books)
    
    # Simple query: Find books after 2020
    recent_books = db.get_all('books', {
        'published_year': {'>=': 2021}
    }, order_by='published_year DESC')
    print("Recent Books:", recent_books)
    
    # 5. Update book data
    db.update('books', 
        {'title': 'Python Basics'}, 
        {'published_year': 2023}
    )
    
    # 6. Delete a book
    db.delete('books', {'title': 'Web Development'})
    
    # Verify deletion
    deleted_book = db.get('books', {'title': 'Web Development'})
    print("Deleted Book:", deleted_book)  # Should print None

if __name__ == '__main__':
    getting_started_example()
