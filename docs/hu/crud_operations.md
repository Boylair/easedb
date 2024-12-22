# CRUD Műveletek

## Áttekintés
Az EaseDB egyszerű és intuitív módszereket biztosít a Create, Read, Update és Delete (CRUD) műveletekhez.

## Létrehozás (Beszúrás) Műveletek
### Egyedi Rekord Beszúrása
```python
# Szinkron
db.set('felhasznalok', {
    'nev': 'Kovács János',
    'email': 'janos@pelda.com',
    'kor': 30
})

# Aszinkron
await async_db.set('felhasznalok', {
    'nev': 'Nagy Eszter',
    'email': 'eszter@pelda.com',
    'kor': 25
})
```

### Több Rekord Beszúrása
```python
# Szinkron
db.set('felhasznalok', [
    {'nev': 'Alice', 'email': 'alice@pelda.com'},
    {'nev': 'Bob', 'email': 'bob@pelda.com'}
])

# Aszinkron
await async_db.set('felhasznalok', [
    {'nev': 'Károly', 'email': 'karoly@pelda.com'},
    {'nev': 'Dávid', 'email': 'david@pelda.com'}
])
```

## Olvasás (Lekérdezés) Műveletek
### Egyedi Rekord Lekérése
```python
# Szinkron
felhasznalo = db.get('felhasznalok', {'nev': 'Kovács János'})

# Aszinkron
felhasznalo = await async_db.get('felhasznalok', {'nev': 'Nagy Eszter'})
```

### Több Rekord Lekérése
```python
# Szinkron: Összes felhasználó
osszes_felhasznalo = db.get_all('felhasznalok')

# Szinkron: Szűrt felhasználók
aktiv_felhasznalok = db.get_all('felhasznalok', {
    'aktiv': True,
    'kor': {'>=': 18}
}, order_by='kor DESC', limit=10)

# Aszinkron megfelelők
osszes_felhasznalo = await async_db.get_all('felhasznalok')
aktiv_felhasznalok = await async_db.get_all('felhasznalok', {...})
```

## Frissítés Műveletek
```python
# Szinkron: Egyedi rekord frissítése
db.update('felhasznalok', 
    {'nev': 'Kovács János'},  # Szűrő
    {'kor': 31, 'email': 'janos.uj@pelda.com'}  # Frissítések
)

# Aszinkron
await async_db.update('felhasznalok', 
    {'nev': 'Nagy Eszter'},
    {'kor': 26}
)
```

## Törlés Műveletek
```python
# Szinkron
db.delete('felhasznalok', {'nev': 'Kovács János'})

# Aszinkron
await async_db.delete('felhasznalok', {'nev': 'Nagy Eszter'})
```

## Speciális Lekérdezések
### Komplex Szűrők
```python
# Felhasználók 25 és 35 év között, regisztrációs dátum szerint rendezve
komplex_felhasznalok = db.get_all('felhasznalok', {
    'kor': {'>=': 25, '<=': 35},
    'regisztracio_datuma': {'>=': '2022-01-01'}
}, order_by='regisztracio_datuma DESC')
```

## Ajánlott Gyakorlatok
- Mindig ellenőrizze az adatokat CRUD műveletek előtt
- Használjon paraméteres lekérdezéseket az SQL injection megelőzésére
- Kezelje a lehetséges kivételeket adatbázis-műveletek során
- Használjon tranzakciókat összetett, több lépéses műveleteknél
