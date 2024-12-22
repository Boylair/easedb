import asyncio
import datetime
import decimal
from easedb import AsyncDatabase

async def async_mysql_advanced_example():
    """Speciális Aszinkron MySQL Műveletek"""
    # Aszinkron MySQL kapcsolat létrehozása
    db = AsyncDatabase('mysql://username:password@host:port/dbname')
    
    async with db:
        # Tábla létrehozása
        await db.execute('''
            CREATE TABLE IF NOT EXISTS termekek (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nev VARCHAR(100) NOT NULL,
                kategoria VARCHAR(50),
                ar DECIMAL(10,2),
                keszlet_mennyiseg INT,
                utolso_frissites DATETIME
            )
        ''')
        
        # Több termék beszúrása batch műveletben
        termek_adatok = [
            {
                'nev': 'Laptop',
                'kategoria': 'Elektronika',
                'ar': decimal.Decimal('1250.00'),
                'keszlet_mennyiseg': 50,
                'utolso_frissites': datetime.datetime.now()
            },
            {
                'nev': 'Okostelefon',
                'kategoria': 'Elektronika',
                'ar': decimal.Decimal('750.50'),
                'keszlet_mennyiseg': 100,
                'utolso_frissites': datetime.datetime.now()
            }
        ]
        
        # Batch beszúrás
        await db.set('termekek', termek_adatok)
        
        # Komplex lekérdezés
        elektronikai_termekek = await db.get_all('termekek', {
            'kategoria': 'Elektronika',
            'keszlet_mennyiseg': {'>': 20},
            'ar': {'<': decimal.Decimal('2000')}
        }, order_by='ar ASC')
        
        print("Elektronikai termékek:", elektronikai_termekek)
        
        # Tranzakció kezelés
        try:
            await db.execute('START TRANSACTION')
            
            # Termék árának frissítése
            await db.update('termekek', 
                {'nev': 'Laptop'}, 
                {'ar': decimal.Decimal('1200.00')}
            )
            
            # Készlet csökkentése
            await db.execute('''
                UPDATE termekek 
                SET keszlet_mennyiseg = keszlet_mennyiseg - 1 
                WHERE nev = 'Laptop'
            ''')
            
            await db.execute('COMMIT')
            print("Tranzakció sikeres")
        
        except Exception as e:
            await db.execute('ROLLBACK')
            print(f"Tranzakció sikertelen: {e}")
        
        # Termék törlése
        await db.delete('termekek', {'nev': 'Okostelefon'})

async def main():
    await async_mysql_advanced_example()

if __name__ == '__main__':
    asyncio.run(main())
