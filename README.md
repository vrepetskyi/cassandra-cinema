# Cassandra Cinema

A system for _viewing screening times_, _making reservations for the available ones_, and _managing your reservations_.

## How to run

### 1. Install the dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Refresh the data

Programmatically scrape screening times from [Charlie Monroe Kino Malta](https://www.kinomalta.pl/seanse) in Poznań.

```bash
python data/scrape.py
```

### 3. Start Cassandra nodes

```bash
docker compose up
```

### 4. Initialize Cassandra with fresh data

WARNING: existing data will be wiped from the DB.

```bash
python init.py
```

### 5. Run the CLI application

```bash
python main.py
```

## Database schema

```sql
CREATE KEYSPACE cinema
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};

CREATE TABLE cinema.screenings (
    screening_id UUID PRIMARY KEY,
    screening_date TEXT,
    screening_time TEXT,
    room TEXT,
    title TEXT
);

CREATE TABLE cinema.reservations (
    reservation_id UUID PRIMARY KEY,
    screening_id UUID,
    user_id TEXT,
    ticket_number INT
);
```

## Encountered problems

The approach to working with a _distributed database_ is highly different from the one with a _relational database_. _Cassandra Query Language_ imposes a lot of restrictions compared to regular _SQL_.
