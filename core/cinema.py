from uuid import UUID, uuid4

from .helpers import get_cassandra_session


class Cinema:
    MAX_RESERVATIONS = 3

    def __init__(self, user_id: str) -> None:
        self.session = get_cassandra_session()
        self.user_id = user_id

    def get_all_screening_times(self):
        return list(
            self.session.execute("""
            SELECT
                screening_time_id,
                date,
                time,
                room,
                title
            FROM cinema.screening_times;
            """)
        )

    def is_screening_time_available(self, screening_time_id: UUID):
        return (
            self.session.execute(
                """
            SELECT COUNT(*) 
            FROM cinema.reservations 
            WHERE screening_time_id = %s ALLOW FILTERING
            """,
                (screening_time_id,),
            )[0][0]
            < Cinema.MAX_RESERVATIONS
        )

    def make_reservation(self, screening_time_id: UUID):
        self.session.execute(
            """
            INSERT INTO cinema.reservations (
                reservation_id,
                screening_time_id,
                user_id
            )
            VALUES (%s, %s, %s);
            """,
            (
                uuid4(),
                screening_time_id,
                self.user_id,
            ),
        )

    def get_reservations(self):
        return list(
            self.session.execute(
                """
                SELECT reservation_id, screening_time_id
                FROM cinema.reservations
                WHERE user_id = %s ALLOW FILTERING;
                """,
                (self.user_id,),
            )
        )

    def cancel_reservation(self, reservation_id: UUID):
        self.session.execute(
            """
            DELETE FROM cinema.reservations
            WHERE reservation_id = %s;
            """,
            (reservation_id,),
        )
