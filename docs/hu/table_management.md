# Tábla Kezelés

## Áttekintés
Az EaseDB rugalmas módszereket biztosít adatbázis-táblák létrehozásához, módosításához és kezeléséhez.

## Táblák Létrehozása
### `create_table()` Metódus Használata
```python
# Alapvető Tábla Létrehozás
db.create_table('felhasznalok', {
    'id': 'INTEGER PRIMARY KEY',
    'nev': 'TEXT NOT NULL',
    'email': 'TEXT UNIQUE',
    'kor': 'INTEGER'
})

# Aszinkron Verzió
await async_db.create_table('felhasznalok', {
    'id': 'INTEGER PRIMARY KEY',
    'nev': 'TEXT NOT NULL',
    'email': 'TEXT UNIQUE',
    'kor': 'INTEGER'
})
```

### Speciális Tábla Létrehozás
```python
# Komplex Korlátozásokkal Rendelkező Tábla
db.create_table('termekek', {
    'id': 'INTEGER PRIMARY KEY',
    'nev': 'TEXT NOT NULL',
    'ar': 'DECIMAL(10,2) CHECK (ar >= 0)',
    'keszlet': 'INTEGER DEFAULT 0',
    'kategoria': 'TEXT',
    'letrehozva': 'DATETIME DEFAULT CURRENT_TIMESTAMP'
})
```

## Táblák Módosítása
### Oszlopok Hozzáadása
```python
# Szinkron
db.execute('ALTER TABLE felhasznalok ADD COLUMN telefon TEXT')

# Aszinkron
await async_db.execute('ALTER TABLE felhasznalok ADD COLUMN telefon TEXT')
```

### Oszlopok Átnevezése
```python
db.execute('ALTER TABLE felhasznalok RENAME COLUMN nev TO felhasznalonev')
```

## Táblák Törlése
```python
# Szinkron
db.execute('DROP TABLE IF EXISTS felhasznalok')

# Aszinkron
await async_db.execute('DROP TABLE IF EXISTS felhasznalok')
```

## Tábla Létezésének Ellenőrzése
```python
# Tábla létezésének ellenőrzése (nyers SQL)
letezik = db.execute('''
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='felhasznalok'
''')
```

## Index Kezelés
```python
# Index létrehozása
db.execute('CREATE INDEX idx_felhasznalok_email ON felhasznalok(email)')

# Index törlése
db.execute('DROP INDEX IF EXISTS idx_felhasznalok_email')
```

## Ajánlott Gyakorlatok
- Mindig használja az `IF NOT EXISTS` opciót tábla létrehozásakor
- Ellenőrizze a tábla sémákat létrehozás előtt
- Használjon megfelelő adattípusokat és korlátozásokat
- Vegye figyelembe az indexek teljesítményre gyakorolt hatását
- Kezelje az adatbázis-specifikus szintaktikai különbségeket

## Hibakezelés
```python
try:
    db.create_table('felhasznalok', {...})
except AdatbazisHiba as e:
    print(f"Tábla létrehozása sikertelen: {e}")
```

## Teljesítményi Megfontolások
- Minimalizálja az oszlopok számát
- Használjon megfelelő indexelést
- Kerülje a túlzott normalizálást
- Vegye figyelembe az adatbázis-specifikus optimalizációs technikákat
