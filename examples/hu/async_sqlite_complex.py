import asyncio
import datetime
from easedb import AsyncDatabase

async def async_sqlite_complex_example():
    """Komplex Aszinkron SQLite Adatkezelés"""
    # Aszinkron SQLite kapcsolat létrehozása
    db = AsyncDatabase('sqlite:///adatbazis.db')
    
    async with db:
        # Táblák létrehozása
        await db.execute('''
            CREATE TABLE IF NOT EXISTS konyvek (
                id INTEGER PRIMARY KEY,
                cim TEXT NOT NULL,
                szerzo TEXT NOT NULL,
                kiadas_eve INTEGER,
                elerheto BOOLEAN DEFAULT TRUE
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS kolcsonzesek (
                id INTEGER PRIMARY KEY,
                konyv_id INTEGER,
                kolcsonzo_neve TEXT,
                kolcsonzes_datuma DATETIME,
                visszahozatal_datuma DATETIME,
                FOREIGN KEY(konyv_id) REFERENCES konyvek(id)
            )
        ''')
        
        # Könyvek beszúrása
        konyvek_adatai = [
            {
                'cim': 'Python Programozás',
                'szerzo': 'Kovács János',
                'kiadas_eve': 2020,
                'elerheto': True
            },
            {
                'cim': 'Adatbázis Tervezés',
                'szerzo': 'Nagy Eszter',
                'kiadas_eve': 2019,
                'elerheto': True
            }
        ]
        
        await db.set('konyvek', konyvek_adatai)
        
        # Komplex lekérdezés
        elerheto_uj_konyvek = await db.get_all('konyvek', {
            'elerheto': True,
            'kiadas_eve': {'>=': 2019}
        }, order_by='kiadas_eve DESC')
        
        print("Elérhető új könyvek:", elerheto_uj_konyvek)
        
        # Könyv kölcsönzése
        kolcsonzendo_konyv = elerheto_uj_konyvek[0]
        
        try:
            await db.execute('START TRANSACTION')
            
            # Kölcsönzés rögzítése
            await db.set('kolcsonzesek', {
                'konyv_id': kolcsonzendo_konyv['id'],
                'kolcsonzo_neve': 'Szabó Anna',
                'kolcsonzes_datuma': datetime.datetime.now(),
                'visszahozatal_datuma': None
            })
            
            # Könyv elérhetőségének frissítése
            await db.update('konyvek', 
                {'id': kolcsonzendo_konyv['id']}, 
                {'elerheto': False}
            )
            
            await db.execute('COMMIT')
            print("Könyv kölcsönzése sikeres")
        
        except Exception as e:
            await db.execute('ROLLBACK')
            print(f"Kölcsönzés sikertelen: {e}")
        
        # Kölcsönzött könyvek lekérdezése
        kolcsonzott_konyvek = await db.execute('''
            SELECT k.cim, k.szerzo, kol.kolcsonzo_neve, kol.kolcsonzes_datuma
            FROM konyvek k
            JOIN kolcsonzesek kol ON k.id = kol.konyv_id
            WHERE k.elerheto = FALSE
        ''')
        
        print("Jelenleg kölcsönzött könyvek:")
        for konyv in kolcsonzott_konyvek:
            print(f"Cím: {konyv['cim']}, Szerző: {konyv['szerzo']}, Kölcsönző: {konyv['kolcsonzo_neve']}")

async def main():
    await async_sqlite_complex_example()

if __name__ == '__main__':
    asyncio.run(main())
