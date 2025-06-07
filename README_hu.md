# EaseDB 🚀

## Gyors, Egyszerű, Megbízható — Adatbázis-kezelés Egyszerűen

Az EaseDB egy hatékony, könnyűsúlyú adatbázis-kezelő könyvtár, amelynek célja az adatbázis-műveletek egyszerűsítése Pythonban. Tiszta, intuitív API-t biztosít, amely támogatja mind a szinkron, mind az aszinkron műveleteket több adatbázis-háttérrendszeren.

## 🌟 Főbb Jellemzők

- 🔄 Teljes Szinkron és Aszinkron Támogatás
- 🗃️ Több Adatbázis-háttérrendszer Kompatibilitás
  - MySQL/MariaDB
  - SQLite
  - PostgreSQL (Hamarosan)
- 🚀 Egyszerű, Pythonos API
- 🔒 Biztonságos Kapcsolatkezelés
- 📦 Könnyűsúlyú és Hatékony

## 🚀 Gyors Telepítés

```bash
pip install easedb
```

## 💡 Használati Példák

### Szinkron Adatbázis-műveletek (SQLite)

#### Alapvető Művelet

```python
from easedb import Database

# Adatbázis-kapcsolat létrehozása
db = Database('sqlite:///pelda.db')

# Rekord beszúrása
db.set('felhasznalok', {
    'nev': 'Kovács János',
    'kor': 30,
    'email': 'kovacs.janos@pelda.com'
})

# Rekord lekérése
felhasznalo = db.get('felhasznalok', {'nev': 'Kovács János'})
print(felhasznalo)
```

### Szinkron MySQL Adatbázis-műveletek 

#### Tábla Létrehozása és Alapvető CRUD Műveletek

```python
from easedb import Database
import datetime
import decimal

# MySQL kapcsolat létrehozása
db = Database('mysql://felhasznalo:jelszo@localhost/adatbazis')

# Tábla létrehozása
db.create_table('alkalmazottak', {
    'id': 'INT AUTO_INCREMENT PRIMARY KEY',
    'nev': 'VARCHAR(100) NOT NULL',
    'eletkor': 'INT',
    'fizetes': 'DECIMAL(10,2)',
    'alkalmazas_datuma': 'DATETIME',
    'aktiv': 'BOOLEAN DEFAULT TRUE'
})

# Rekord beszúrása
db.set('alkalmazottak', {
    'nev': 'Nagy Péter',
    'eletkor': 35,
    'fizetes': decimal.Decimal('450000.50'),
    'alkalmazas_datuma': datetime.datetime.now(),
    'aktiv': True
})

# Rekord lekérése
alkalmazott = db.get('alkalmazottak', {'nev': 'Nagy Péter'})
print("Alkalmazott adatai:", alkalmazott)

# Több rekord lekérése
minden_alkalmazott = db.get_all('alkalmazottak')
print("Összes alkalmazott:", minden_alkalmazott)

# Rekord frissítése
db.update('alkalmazottak', 
    {'nev': 'Nagy Péter'}, 
    {'fizetes': decimal.Decimal('475000.75')}
)

# Rekord törlése
db.delete('alkalmazottak', {'nev': 'Nagy Péter'})
```


### Aszinkron Adatbázis-műveletek (MySQL)

```python
from easedb import AsyncDatabase
import asyncio
import datetime
import decimal

async def main():
    # Aszinkron adatbázis-kapcsolat létrehozása
    db = AsyncDatabase('mysql://felhasznalo:jelszo@localhost/adatbazis')
    
    # Tábla létrehozása
    await db.create_table('termekek', {
        'id': 'INT AUTO_INCREMENT PRIMARY KEY',
        'nev': 'VARCHAR(100) NOT NULL',
        'ar': 'DECIMAL(10,2)',
        'letrehozva': 'DATETIME',
        'aktiv': 'BOOLEAN DEFAULT TRUE'
    })
    
    # Rekord beszúrása
    await db.set('termekek', {
        'nev': 'Laptop',
        'ar': decimal.Decimal('250000.00'),
        'letrehozva': datetime.datetime.now(),
        'aktiv': True
    })
    
    # Rekord lekérése
    termek = await db.get('termekek', {'nev': 'Laptop'})
    print("Termék adatai:", termek)

asyncio.run(main())
```

#### Komplex Lekérdezések

```python
# Összetett feltétellel lekérdezés
aktiv_alkalmazottak = db.get_all('alkalmazottak', {
    'aktiv': True, 
    'eletkor': {'>=': 30}
})

# Rendezés és korlátozás
top_5_fizetes = db.get_all('alkalmazottak', 
    order_by='fizetes DESC', 
    limit=5
)
```

### Közvetlen SQL Végrehajtás

#### Nyers SQL Parancsok és Speciális Műveletek

```python
from easedb import Database
import datetime

# Adatbázis-kapcsolat létrehozása
db = Database('mysql://felhasznalo:jelszo@localhost/adatbazis')

# Komplex tábla létrehozása egyetlen execute paranccsal
db.execute('''
    CREATE TABLE IF NOT EXISTS fejlett_felhasznalok (
        id INT AUTO_INCREMENT PRIMARY KEY,
        felhasznalonev VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        regisztracio_datuma DATETIME,
        utolso_belepes DATETIME,
        belepes_szam INT DEFAULT 0,
        fiok_allapot ENUM('aktiv', 'inaktiv', 'felfuggesztett') DEFAULT 'aktiv',
        osszes_vasarlas DECIMAL(10,2) DEFAULT 0.00
    )
''')

# Több rekord beszúrása execute segítségével
db.execute('''
    INSERT INTO fejlett_felhasznalok 
    (felhasznalonev, email, regisztracio_datuma, utolso_belepes, belepes_szam, fiok_allapot, osszes_vasarlas)
    VALUES 
    ('kovacs_janos', 'janos@pelda.com', %s, %s, 5, 'aktiv', 1250.75),
    ('nagy_maria', 'maria@pelda.com', %s, %s, 12, 'aktiv', 3500.25)
''', (
    datetime.datetime.now(), 
    datetime.datetime.now(),
    datetime.datetime.now(), 
    datetime.datetime.now()
))

# Komplex lekérdezés join-okkal és aggregációkkal
eredmeny = db.execute('''
    SELECT 
        f.felhasznalonev, 
        f.email, 
        COUNT(v.id) as vasarlasok_szama, 
        SUM(v.osszeg) as teljes_koltes
    FROM 
        fejlett_felhasznalok f
    LEFT JOIN 
        vasarlasok v ON f.id = v.felhasznalo_id
    GROUP BY 
        f.id, f.felhasznalonev, f.email
    HAVING 
        teljes_koltes > 1000
    ORDER BY 
        teljes_koltes DESC
    LIMIT 10
''')

# Eredmények iterálása
for sor in eredmeny:
    print(f"Felhasználónév: {sor['felhasznalonev']}, Teljes költés: {sor['teljes_koltes']}")

# Tranzakció példa
try:
    db.execute('START TRANSACTION')
    
    # Több kapcsolódó művelet
    db.execute('UPDATE szamlak SET egyenleg = egyenleg - 500 WHERE id = 1')
    db.execute('UPDATE szamlak SET egyenleg = egyenleg + 500 WHERE id = 2')
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
    print(f"Tranzakció sikertelen: {e}")
```

#### Batch Műveletek és Előkészített Utasítások

```python
# Batch beszúrás előkészített utasítással
felhasznalok_adatai = [
    ('alice', 'alice@pelda.com'),
    ('bob', 'bob@pelda.com'),
    ('charlie', 'charlie@pelda.com')
]

db.execute(
    'INSERT INTO felhasznalok (felhasznalonev, email) VALUES (%s, %s)', 
    felhasznalok_adatai
)
```



## 🛠️ Speciális Funkciók

- CRUD Műveletek
- Aszinkron és Szinkron Támogatás
- Több Adatbázis-típus Támogatása
- Automatikus Kapcsolatkezelés
- Hibakezelés és Újrapróbálkozási Mechanizmusok
- Lekérdezés-builder (Tervezve)
- Kapcsolat-poolozás (Tervezve)

## 🧪 Tesztelés

A `pytest` keretrendszert használjuk átfogó teszteléshez.

### Tesztek Futtatása

```bash
# Tesztelési függőségek telepítése
pip install -r requirements.txt

# Összes teszt futtatása
pytest

# Kódlefedettségi jelentés generálása
pytest --cov=src/easedb
```

## 🤝 Közreműködés

A közreműködéseket szívesen fogadjuk! Kérjük, nézd meg a hibajegy-oldalunkat vagy küldj egy pull requestet!

## 📄 Licensz

MIT

## 🌐 Hivatkozások

- GitHub repo: https://github.com/Boylair/easedb 
- Dokumentáció: https://github.com/Boylair/easedb/blob/main/docs/hu/getting_started.md
- Hibajelentés: https://github.com/Boylair/easedb/issues

