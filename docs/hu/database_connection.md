# Adatbázis Kapcsolat

## Áttekintés
Az EaseDB könyvtár rugalmas adatbázis-kapcsolódási módszereket biztosít különböző adatbázis-típusokhoz.

## Támogatott Kapcsolódási Típusok
- SQLite
- MySQL
- PostgreSQL
- Egyéb SQL adatbázisok

## Szinkron Kapcsolat
```python
from easedb import Database

# SQLite Kapcsolat
db_sqlite = Database('sqlite:///pelda.db')

# MySQL Kapcsolat
db_mysql = Database('mysql://felhasznalo:jelszo@localhost/adatbazis')
```

## Aszinkron Kapcsolat
```python
from easedb import AsyncDatabase

# SQLite Aszinkron Kapcsolat
async_db_sqlite = AsyncDatabase('sqlite:///async_pelda.db')

# MySQL Aszinkron Kapcsolat
async_db_mysql = AsyncDatabase('mysql://felhasznalo:jelszo@localhost/adatbazis')
```

## Kapcsolati Karakterlánc Formátuma
A kapcsolati karakterlánc a következő formátumot követi:
`dialektus://felhasznalonev:jelszo@host:port/adatbazis_neve`

### Paraméterek
- `dialektus`: Adatbázis típusa (sqlite, mysql, postgresql)
- `felhasznalonev`: Adatbázis felhasználó
- `jelszo`: Felhasználó jelszava
- `host`: Adatbázis szerver címe
- `port`: Adatbázis szerver portja
- `adatbazis_neve`: Az adatbázis neve

## Ajánlott Gyakorlatok
- Mindig környezeti változókat használjon érzékeny hitelesítő adatokhoz
- Zárja be az adatbázis-kapcsolatokat, ha már nem használja
- Használjon context managereket az automatikus kapcsolatkezeléshez

## Hibakezelés
```python
try:
    db = Database('sqlite:///pelda.db')
except ConnectionError as e:
    print(f"Adatbázis-kapcsolódás sikertelen: {e}")
```

## Biztonsági Megfontolások
- Soha ne rögzítse mereven az adatbázis hitelesítő adatait
- Használjon biztonságos kapcsolódási módszereket
- Implementáljon megfelelő hozzáférés-vezérlést
