# Adatbázis Tranzakciók

## Áttekintés
A tranzakciók biztosítják az adatok integritását azáltal, hogy több adatbázis-műveletet egyetlen, atomikus egységbe csoportosítanak.

## Alapvető Tranzakció Használat
### Szinkron Tranzakciók
```python
# Manuális Tranzakció Kezelés
try:
    db.execute('BEGIN TRANSACTION')
    
    # Több művelet
    db.set('szamlak', {'nev': 'János', 'egyenleg': 1000})
    db.update('szamlak', 
        {'nev': 'János'}, 
        {'egyenleg': 500}
    )
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
    print(f"Tranzakció sikertelen: {e}")
```

### Aszinkron Tranzakciók
```python
async def penzkuldes():
    async with async_db:
        try:
            await async_db.execute('START TRANSACTION')
            
            # Pénz átutalás számlák között
            await async_db.update('szamlak', 
                {'nev': 'Küldő'}, 
                {'egyenleg': kuldo_egyenleg - osszeg}
            )
            await async_db.update('szamlak', 
                {'nev': 'Fogadó'}, 
                {'egyenleg': fogado_egyenleg + osszeg}
            )
            
            # Tranzakció rögzítése
            await async_db.set('tranzakciok', {
                'kuldo': 'Küldő',
                'fogado': 'Fogadó',
                'osszeg': osszeg
            })
            
            await async_db.execute('COMMIT')
        except Exception as e:
            await async_db.execute('ROLLBACK')
            print(f"Tranzakció sikertelen: {e}")
```

## Context Manager Tranzakciók
```python
# Szinkron Context Manager
with db:
    db.set('felhasznalok', {'nev': 'Alice'})
    db.update('felhasznalok', {'nev': 'Alice'}, {'allapot': 'aktiv'})

# Aszinkron Context Manager
async with async_db:
    await async_db.set('felhasznalok', {'nev': 'Bob'})
    await async_db.update('felhasznalok', {'nev': 'Bob'}, {'allapot': 'aktiv'})
```

## Mentéspontok
```python
# Mentéspontok létrehozása és visszaállítása
try:
    db.execute('BEGIN TRANSACTION')
    
    # Első művelet
    db.set('naplok', {'muvelet': 'kezdet'})
    
    # Mentéspont létrehozása
    db.execute('SAVEPOINT mentespont')
    
    # Kockázatos művelet
    db.update('szamlak', {'id': 1}, {'egyenleg': -500})
    
    # Ha valami nem stimmel, visszaállítás a mentéspontig
    db.execute('ROLLBACK TO SAVEPOINT mentespont')
    
    db.execute('COMMIT')
except Exception as e:
    db.execute('ROLLBACK')
```

## Ajánlott Gyakorlatok
- Tartsa a tranzakciókat minél rövidebbnek
- Csak a szükséges műveleteket foglalja bele a tranzakcióba
- Kezelje az összes lehetséges kivételt
- Használjon megfelelő elkülönítési szinteket
- Kerülje a hosszan futó tranzakciókat

## Gyakori Buktatók
- A beágyazott tranzakciók bonyolultak lehetnek
- Holtpontok fordulhatnak elő egyidejű tranzakcióknál
- Teljesítménybeli többletterhelés gyakori tranzakcióknál

## Hibakezelés
```python
try:
    with db:
        # Tranzakció műveletek
        pass
except TranzakcioHiba as e:
    # Specifikus tranzakciós hibák kezelése
    print(f"Tranzakció hiba: {e}")
except Exception as e:
    # Váratlan hibák kezelése
    print(f"Váratlan hiba: {e}")
```

## Teljesítményi Megfontolások
- Minimalizálja a tranzakción belüli műveletek számát
- Használjon megfelelő indexelést
- Válasszon helyes elkülönítési szintet
- Figyelje és optimalizálja a hosszan futó tranzakciókat
