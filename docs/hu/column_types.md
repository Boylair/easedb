# Adatbázis Oszlop Típusok Útmutató

## Áttekintés
Az oszlop típusok megértése kulcsfontosságú hatékony és robusztus adatbázis sémák tervezéséhez. Ez az útmutató a leggyakoribb és leghasznosabb adattípusokat mutatja be a különböző adatbázis rendszerekben.

## Elsődleges Oszlop Típusok

| Type | Leírás | Range/Size | Felhasználási Esetek | Példa Értékek | Constraints/Modifiers |
|------|-------------|------------|-----------|---------------|----------------------|
| **INTEGER** | Egész számok | -2^63 to 2^63-1 | Számolás, azonosítók, indexek | 42, -17, 0 | PRIMARY KEY, AUTOINCREMENT, NOT NULL |
| **TEXT** | Változó hosszúságú karakterláncok | Legfeljebb 2GB | Nevek, leírások, szövegek | "Hello World", "User123" | NOT NULL, UNIQUE |
| **VARCHAR(n)** | Változó hosszúságú karakterlánc maximális hosszal | 0-65,535 karakter | Rövid szövegek, felhasználónevek | "John", "example@email.com" | LENGTH LIMIT |
| **DECIMAL(p,s)** | Pontos tizedes számok | p: összes számjegy, s: tizedes helyek | Pénzügyi számítások, árak | 1234.56, -0.01 | PRECISION CONTROL |
| **FLOAT/REAL** | Lebegőpontos számok | ±1.7E +/- 308 | Tudományos számítások | 3.14159, -2.5 | APPROXIMATE PRECISION |
| **BOOLEAN** | Igaz/hamis értékek | TRUE/FALSE vagy 1/0 | Zászlók, státuszok | TRUE, FALSE | DEFAULT VALUES |
| **DATETIME** | Dátum és idő | '1000-01-01' - '9999-12-31' | Időbélyegek, naplók | '2024-12-22 20:30:00' | DEFAULT CURRENT_TIMESTAMP |
| **DATE** | Csak dátum | '1000-01-01' - '9999-12-31' | Születésnapok, esemény dátumok | '2024-12-22' | YEAR, MONTH, DAY |
| **TIME** | Csak idő | '-838:59:59' - '838:59:59' | Specifikus időpontok | '14:30:00' | HOURS, MINUTES, SECONDS |

## Átfogó Constraints és Modifiers

### Alapvető Constraints

| Constraint | Leírás | Használat | Példa |
|-----------|-------------|-------|---------|
| `NOT NULL` | Megakadályozza az üres/null értékeket | Biztosítja, hogy az oszlopnak mindig legyen értéke | `username VARCHAR(50) NOT NULL` |
| `UNIQUE` | Biztosítja, hogy minden érték egyedi legyen | Nem enged duplikált értékeket | `email VARCHAR(100) UNIQUE` |
| `PRIMARY KEY` | Egyedi azonosító minden sorhoz | Automatikusan indexet hoz létre | `id INTEGER PRIMARY KEY` |
| `DEFAULT` | Alapértelmezett értéket állít be, ha nem adunk meg értéket | Automatikus értékbeállítás | `status BOOLEAN DEFAULT TRUE` |
| `AUTOINCREMENT` | Automatikusan növeli az értéket új soroknál | Szekvenciális azonosítókhoz | `id INTEGER PRIMARY KEY AUTOINCREMENT` |

### Speciális Validation Constraints

| Constraint | Leírás | Használat | Példa |
|-----------|-------------|-------|---------|
| `CHECK` | Egyedi érvényesítési szabályokat ad hozzá | Specifikus feltételek kikényszerítése | `age INTEGER CHECK (age >= 18)` |
| `FOREIGN KEY` | Kapcsolatot hoz létre táblák között | Hivatkozási integritás biztosítása | `user_id INTEGER REFERENCES users(id)` |

## Speciális Validation Technikák

### Komplex Check Constraints
```sql
-- Több feltétel ellenőrzése
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    age INTEGER CHECK (age BETWEEN 18 AND 65),
    email TEXT CHECK (email LIKE '%@%.%')
)
```

### Validation Példák EaseDB-ben
```python
# Komplex validation tábla létrehozásakor
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'VARCHAR(50) NOT NULL UNIQUE',
    'email': 'VARCHAR(100) NOT NULL CHECK (email LIKE "%@%.%")',
    'age': 'INTEGER CHECK (age >= 18 AND age <= 120)',
    'salary': 'DECIMAL(10,2) CHECK (salary >= 0)',
    'registration_date': 'DATETIME CHECK (registration_date <= CURRENT_TIMESTAMP)'
})
```

### Validation Minták

1. **Tartomány Validation**
   - Numerikus értékek korlátozása
   - Értékek elfogadható tartományon belül tartása
   ```sql
   CHECK (value >= min_value AND value <= max_value)
   ```

2. **Minta Illesztés**
   - Szövegformátumok érvényesítése
   - LIKE vagy REGEX használata
   ```sql
   CHECK (email LIKE '%@%.%')
   CHECK (phone_number REGEXP '^[0-9]{10}$')
   ```

3. **Feltételes Logika**
   - Komplex, több feltételes ellenőrzések
   ```sql
   CHECK (
     (status = 'active' AND last_login IS NOT NULL) OR 
     (status = 'inactive' AND last_login IS NULL)
   )
   ```

## Teljesítményi Megfontolások a Constraints-nél
- A constraints validációs terhelést adnak
- Használja körültekintően és stratégiailag
- Indexelje a komplex ellenőrzési feltételeket
- Vegye figyelembe az alkalmazásszintű validációt teljesítménykritikus rendszereknél

## Gyakori Validation Forgatókönyvek

| Forgatókönyv | SQL Constraint | Leírás |
|----------|----------------|-------------|
| Életkor Ellenőrzés | `CHECK (age >= 18)` | Felhasználó nagykorúságának biztosítása |
| Pozitív Értékek | `CHECK (value > 0)` | Negatív árak/mennyiségek megakadályozása |
| Email Formátum | `CHECK (email LIKE '%@%.%')` | Alapvető email érvényesítés |
| Dátum Tartományok | `CHECK (start_date < end_date)` | Dátum logika ellenőrzése |
| Enum-szerű Validation | `CHECK (status IN ('active', 'inactive', 'suspended'))` | Specifikus értékekre korlátozás |

## Biztonság és Adatintegritás
- A constraints megakadályozzák az érvénytelen adatbevitelt
- Csökkentik az adatsérülés kockázatát
- Üzleti szabályok kikényszerítése adatbázis szinten
- Kiegészítik az alkalmazásszintű validációkat

## Ajánlott Gyakorlatok
1. Használjon constraints-eket az adatszabályok kikényszerítésére
2. Tartsa egyszerűnek a validation logikát
3. Egyensúlyozzon az adatbázis és alkalmazás szintű validation között
4. Vegye figyelembe a teljesítményre gyakorolt hatást
5. Használjon értelmes hibaüzeneteket

## Példa: Komplex Felhasználói Regisztráció Validation
```python
db.create_table('user_profiles', {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'VARCHAR(50) NOT NULL UNIQUE CHECK (LENGTH(username) >= 3)',
    'email': 'VARCHAR(100) NOT NULL UNIQUE CHECK (email LIKE "%@%.%")',
    'age': 'INTEGER CHECK (age >= 18 AND age <= 120)',
    'registration_date': 'DATETIME DEFAULT CURRENT_TIMESTAMP CHECK (registration_date <= CURRENT_TIMESTAMP)',
    'account_type': 'VARCHAR(20) CHECK (account_type IN ("basic", "premium", "corporate"))'
})
```

## Speciális Oszlop Módosítók

### Constraints
- `NOT NULL`: Megakadályozza az üres értékeket
- `UNIQUE`: Biztosítja, hogy minden érték egyedi legyen
- `DEFAULT`: Alapértelmezett értéket állít be
- `CHECK`: Egyedi érvényesítési szabályokat ad hozzá
- `PRIMARY KEY`: Egyedi azonosító a sorhoz

## Ajánlott Gyakorlatok
- Válassza a lehető legkisebb adattípust, amely illeszkedik az adataihoz
- Használjon constraints-eket az adatok integritásának fenntartásához
- Vegye figyelembe a tárolási és teljesítménybeli vonatkozásokat
- Legyen konzisztens az adatbázis sémában

## Teljesítmény és Tárolási Megfontolások
- **INTEGER** a leggyorsabb numerikus műveletekhez
- **TEXT** lassabb lehet nagy mennyiségű adat esetén
- **DECIMAL** pontos, de lassabb mint a FLOAT
- Válasszon a specifikus felhasználási eset és teljesítményi igények alapján

## Gyakori Buktatók
- Kerülje a TEXT használatát fix hosszúságú adatoknál
- Legyen óvatos a lebegőpontos pontossággal
- Ne normalizálja túl a sémát
- Vegye figyelembe az adatbázis-specifikus típus árnyalatokat
