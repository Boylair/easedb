import asyncio
import datetime
from easedb import AsyncDatabase

async def async_sqlite_complex_example():
    """Complex Asynchronous SQLite Data Management"""
    # Create async SQLite database connection
    db = AsyncDatabase('sqlite:///database.db')
    
    async with db:
        # Create tables
        await db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER,
                is_available BOOLEAN DEFAULT TRUE
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS borrowings (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                borrower_name TEXT,
                borrow_date DATETIME,
                return_date DATETIME,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        ''')
        
        # Insert books
        books_data = [
            {
                'title': 'Python Programming',
                'author': 'John Smith',
                'publication_year': 2020,
                'is_available': True
            },
            {
                'title': 'Database Design',
                'author': 'Jane Doe',
                'publication_year': 2019,
                'is_available': True
            }
        ]
        
        await db.set('books', books_data)
        
        # Complex query
        available_recent_books = await db.get_all('books', {
            'is_available': True,
            'publication_year': {'>=': 2019}
        }, order_by='publication_year DESC')
        
        print("Available recent books:", available_recent_books)
        
        # Book borrowing
        book_to_borrow = available_recent_books[0]
        
        try:
            await db.execute('START TRANSACTION')
            
            # Record borrowing
            await db.set('borrowings', {
                'book_id': book_to_borrow['id'],
                'borrower_name': 'John Doe',
                'borrow_date': datetime.datetime.now(),
                'return_date': None
            })
            
            # Update book availability
            await db.update('books', 
                {'id': book_to_borrow['id']}, 
                {'is_available': False}
            )
            
            await db.execute('COMMIT')
            print("Book borrowing successful")
        
        except Exception as e:
            await db.execute('ROLLBACK')
            print(f"Borrowing failed: {e}")
        
        # Query borrowed books
        borrowed_books = await db.execute('''
            SELECT b.title, b.author, br.borrower_name, br.borrow_date
            FROM books b
            JOIN borrowings br ON b.id = br.book_id
            WHERE b.is_available = FALSE
        ''')
        
        print("Currently borrowed books:")
        for book in borrowed_books:
            print(f"Title: {book['title']}, Author: {book['author']}, Borrower: {book['borrower_name']}")

async def main():
    await async_sqlite_complex_example()

if __name__ == '__main__':
    asyncio.run(main())
