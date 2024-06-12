import os
from uuid import uuid4

import pandas as pd
from cassandra.cluster import Session

from core.helpers import get_cassandra_session


def create_schema(session: Session):
    print('Dropping the existing "cinema" keyspace...')
    session.execute("DROP KEYSPACE IF EXISTS cinema;")

    print('Creating a new "cinema" keyspace...')
    session.execute("""
    CREATE KEYSPACE cinema
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};
    """)

    print('Creating the "screening_times" table...')
    session.execute("""
    CREATE TABLE cinema.screening_times (
        screening_time_id UUID PRIMARY KEY,
        date TEXT,
        time TEXT,
        room TEXT,
        title TEXT
    );
    """)

    print('Creating the "reservations" table...')
    session.execute("""
    CREATE TABLE cinema.reservations (
        reservation_id UUID PRIMARY KEY,
        screening_time_id UUID,
        user_id TEXT
    );
    """)


def load_data(session: Session):
    SCREENING_TIMES_CSV = "data/screening_times.csv"

    if not os.path.exists(SCREENING_TIMES_CSV):
        raise FileNotFoundError("Screening time data is not found")

    df = pd.read_csv(SCREENING_TIMES_CSV)

    print("Inserting the new data...")
    for row in df.itertuples():
        session.execute(
            """
            INSERT INTO cinema.screening_times (
                screening_time_id,
                date,
                time,
                room,
                title
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (uuid4(), *row[2:]),
        )


def init():
    session = get_cassandra_session()
    create_schema(session)
    load_data(session)


if __name__ == "__main__":
    init()
