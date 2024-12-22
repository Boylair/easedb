import datetime
from easedb import Database

def sqlite_transaction_example():
    """SQLite Tranzakció és Speciális Lekérdezések Bemutatása"""
    # SQLite adatbázis kapcsolat létrehozása
    db = Database('sqlite:///bank_tranzakciok.db')
    
    # Táblák létrehozása
    db.execute('''
        CREATE TABLE IF NOT EXISTS szamlak (
            id INTEGER PRIMARY KEY,
            nev TEXT NOT NULL,
            egyenleg REAL DEFAULT 0
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS tranzakciok (
            id INTEGER PRIMARY KEY,
            kuldo_szamla_id INTEGER,
            fogado_szamla_id INTEGER,
            osszeg REAL,
            tranzakcio_datuma DATETIME,
            FOREIGN KEY(kuldo_szamla_id) REFERENCES szamlak(id),
            FOREIGN KEY(fogado_szamla_id) REFERENCES szamlak(id)
        )
    ''')
    
    # Kezdeti számlák létrehozása
    db.set('szamlak', [
        {'nev': 'Alice', 'egyenleg': 1000.00},
        {'nev': 'Bob', 'egyenleg': 500.00}
    ])
    
    # Tranzakció kezelés
    try:
        # Tranzakció indítása
        db.execute('BEGIN TRANSACTION')
        
        # Pénz átutalás Alice-től Bob-nak
        kuldo = db.get('szamlak', {'nev': 'Alice'})
        fogado = db.get('szamlak', {'nev': 'Bob'})
        
        utalasi_osszeg = 200.00
        
        # Egyenlegek frissítése
        db.update('szamlak', 
            {'nev': 'Alice'}, 
            {'egyenleg': kuldo['egyenleg'] - utalasi_osszeg}
        )
        
        db.update('szamlak', 
            {'nev': 'Bob'}, 
            {'egyenleg': fogado['egyenleg'] + utalasi_osszeg}
        )
        
        # Tranzakció rögzítése
        db.set('tranzakciok', {
            'kuldo_szamla_id': kuldo['id'],
            'fogado_szamla_id': fogado['id'],
            'osszeg': utalasi_osszeg,
            'tranzakcio_datuma': datetime.datetime.now()
        })
        
        # Tranzakció véglegesítése
        db.execute('COMMIT')
        print("Tranzakció sikeres")
    
    except Exception as e:
        # Hiba esetén visszagörgetés
        db.execute('ROLLBACK')
        print(f"Tranzakció sikertelen: {e}")
    
    # Tranzakciók lekérdezése
    tranzakciok = db.get_all('tranzakciok', 
        order_by='tranzakcio_datuma DESC', 
        limit=5
    )
    
    print("Legutóbbi tranzakciók:")
    for tranzakcio in tranzakciok:
        kuldo_szamla = db.get('szamlak', {'id': tranzakcio['kuldo_szamla_id']})
        fogado_szamla = db.get('szamlak', {'id': tranzakcio['fogado_szamla_id']})
        print(f"Küldő: {kuldo_szamla['nev']}, Fogadó: {fogado_szamla['nev']}, Összeg: {tranzakcio['osszeg']}")

if __name__ == '__main__':
    sqlite_transaction_example()
