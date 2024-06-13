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

    print('Creating the "screenings" table...')
    session.execute("""
    CREATE TABLE cinema.screenings (
        screening_id UUID PRIMARY KEY,
        screening_date TEXT,
        screening_time TEXT,
        room TEXT,
        title TEXT
    );
    """)

    print('Creating the "reservations_by_user" table...')
    session.execute("""
    CREATE TABLE cinema.reservations_by_user (
        user_id TEXT,
        screening_id UUID,
        reservation_id UUID,
        PRIMARY KEY(user_id, screening_id)
    );
    """)

    print('Creating the "reservations_by_screening" table...')
    session.execute("""
    CREATE TABLE cinema.reservations_by_screening (
        screening_id UUID PRIMARY KEY,
        user_id TEXT,
        reservation_id UUID
    );
    """)


def load_data(session: Session):
    screeningS_CSV = "data/screenings.csv"

    if not os.path.exists(screeningS_CSV):
        raise FileNotFoundError("Screening time data is not found")

    df = pd.read_csv(screeningS_CSV)

    print("Inserting the new data...")
    for row in df.itertuples():
        session.execute(
            """
            INSERT INTO cinema.screenings (
                screening_id,
                screening_date,
                screening_time,
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
