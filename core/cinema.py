from uuid import UUID

from .helpers import get_cassandra_session


class CinemaClient:
    def __init__(self, user_id: str) -> None:
        self.session = get_cassandra_session()
        self.user_id = user_id

    def get_all_screenings(self):
        all_screenings = self.session.execute("""
        SELECT
            screening_id,
            screening_date,
            screening_time,
            room,
            title
        FROM cinema.screenings;
        """)

        return sorted(
            all_screenings,
            key=lambda x: x.screening_date,
        )

    def get_all_reserved_screening_ids(self):
        reserved_ids = self.session.execute(
            "SELECT screening_id FROM cinema.reservations_by_user;"
        )

        return set(map(lambda x: x.screening_id, reserved_ids))

    def make_reservation(self, screening_id: UUID):
        res = self.session.execute(
            """
            INSERT INTO cinema.reservations_by_screening (
                screening_id,
                user_id
            )
            VALUES (%s, %s)
            IF NOT EXISTS;
            """,
            (
                screening_id,
                self.user_id,
            ),
        )

        if res.was_applied:
            self.session.execute(
                """
                INSERT INTO cinema.reservations_by_user (
                    user_id,
                    screening_id
                )
                VALUES (%s, %s);
                """,
                (
                    self.user_id,
                    screening_id,
                ),
            )

    def get_own_reservations(self):
        return list(
            self.session.execute(
                """
                SELECT screening_id
                FROM cinema.reservations_by_user
                WHERE user_id = %s;
                """,
                (self.user_id,),
            )
        )

    def cancel_reservation(self, screening_id: UUID):
        self.session.execute(
            """
            DELETE FROM cinema.reservations_by_screening
            WHERE screening_id = %s;
            """,
            (screening_id,),
        )

        self.session.execute(
            """
            DELETE FROM cinema.reservations_by_user
            WHERE user_id = %s AND screening_id = %s;
            """,
            (self.user_id, screening_id),
        )
