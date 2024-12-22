from easedb import Database

def getting_started_example():
    """
    EaseDB Kezdő Útmutató
    
    Ez a példa bemutatja az EaseDB alapvető műveleteit:
    1. Adatbázis kapcsolat létrehozása
    2. Tábla létrehozása EaseDB módszerrel
    3. Adatok beszúrása
    4. Adatok lekérdezése
    5. Adatok frissítése
    6. Adatok törlése
    """
    
    # 1. Adatbázis kapcsolat létrehozása (SQLite memória adatbázis)
    db = Database('sqlite:///pelda.db')
    
    # 2. Könyvek tábla létrehozása EaseDB módszerrel
    db.create_table('konyvek', {
        'id': 'INTEGER PRIMARY KEY',
        'cim': 'TEXT NOT NULL',
        'szerzo': 'TEXT',
        'kiadas_eve': 'INTEGER'
    })
    
    # 3. Egy könyv beszúrása
    db.set('konyvek', {
        'cim': 'Python Alapok',
        'szerzo': 'Kovács János',
        'kiadas_eve': 2022
    })
    
    # Több könyv beszúrása
    db.set('konyvek', [
        {
            'cim': 'Adattudomány Kézikönyv',
            'szerzo': 'Nagy Eszter',
            'kiadas_eve': 2021
        },
        {
            'cim': 'Webfejlesztés',
            'szerzo': 'Szabó Péter',
            'kiadas_eve': 2020
        }
    ])
    
    # 4. Adatok lekérdezése: Egy könyv
    konyv = db.get('konyvek', {'cim': 'Python Alapok'})
    print("Egy Könyv:", konyv)
    
    # Összes könyv lekérdezése
    osszes_konyv = db.get_all('konyvek')
    print("Összes Könyv:", osszes_konyv)
    
    # Egyszerű lekérdezés: Könyvek 2020 után
    uj_konyvek = db.get_all('konyvek', {
        'kiadas_eve': {'>=': 2021}
    }, order_by='kiadas_eve DESC')
    print("Új Könyvek:", uj_konyvek)
    
    # 5. Könyv adatainak frissítése
    db.update('konyvek', 
        {'cim': 'Python Alapok'}, 
        {'kiadas_eve': 2023}
    )
    
    # 6. Könyv törlése
    db.delete('konyvek', {'cim': 'Webfejlesztés'})
    
    # Törlés ellenőrzése
    torölt_konyv = db.get('konyvek', {'cim': 'Webfejlesztés'})
    print("Törölt Könyv:", torölt_konyv)  # None-t kell mutatnia

if __name__ == '__main__':
    getting_started_example()
