import datetime
import decimal
from easedb import Database

def mysql_crud_example():
    """Részletes MySQL CRUD Műveletek Bemutatása"""
    # MySQL adatbázis kapcsolat létrehozása
    db = Database('mysql://username:password@host:port/dbname')
    
    # Tábla létrehozása
    db.execute('''
        CREATE TABLE IF NOT EXISTS alkalmazottak (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nev VARCHAR(100) NOT NULL,
            kor INT,
            fizetes DECIMAL(10,2),
            felvetel_datuma DATETIME,
            aktiv BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create (Beszúrás) - Új alkalmazott hozzáadása
    print("1. Új alkalmazott beszúrása:")
    result = db.set('alkalmazottak', {
        'nev': 'Kovács János',
        'kor': 35,
        'fizetes': decimal.Decimal('75000.50'),
        'felvetel_datuma': datetime.datetime.now(),
        'aktiv': True
    })
    print(f"Beszúrás sikeres: {result}\n")
    
    # Read (Olvasás) - Alkalmazott lekérése
    print("2. Alkalmazott lekérése:")
    alkalmazott = db.get('alkalmazottak', {'nev': 'Kovács János'})
    print(f"Alkalmazott adatai: {alkalmazott}\n")
    
    # Update (Frissítés) - Alkalmazott adatainak módosítása
    print("3. Alkalmazott adatainak frissítése:")
    db.update('alkalmazottak', 
        {'nev': 'Kovács János'}, 
        {'fizetes': decimal.Decimal('80000.75'), 'kor': 36}
    )
    frissitett_alkalmazott = db.get('alkalmazottak', {'nev': 'Kovács János'})
    print(f"Frissített alkalmazott: {frissitett_alkalmazott}\n")
    
    # Komplex lekérdezés
    print("4. Komplex lekérdezés:")
    aktiv_idosebb_alkalmazottak = db.get_all('alkalmazottak', {
        'aktiv': True,
        'kor': {'>=': 30},
        'fizetes': {'>': decimal.Decimal('70000')}
    }, order_by='fizetes DESC', limit=5)
    print(f"Aktív, idősebb alkalmazottak (top 5 fizetés szerint): {aktiv_idosebb_alkalmazottak}\n")
    
    # Delete (Törlés)
    print("5. Alkalmazott törlése:")
    db.delete('alkalmazottak', {'nev': 'Kovács János'})
    torölt_alkalmazott = db.get('alkalmazottak', {'nev': 'Kovács János'})
    print(f"Törölt alkalmazott: {torölt_alkalmazott}\n")

if __name__ == '__main__':
    mysql_crud_example()
