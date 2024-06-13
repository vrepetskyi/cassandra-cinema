from core.cinema import Cinema


class CinemaCLI:
    def print_screenings(self, screenings, reserved_screenings=None):
        for index, screening in enumerate(screenings):
            print(
                "#%02d | %s | %s | %-12s | %s" % (index + 1, *screening[1:])
                + (
                    " — SOLD OUT"
                    if reserved_screenings
                    and screening.screening_id in reserved_screenings
                    else ""
                )
            )

    def list_screenings(self):
        screenings = self.cinema.get_all_screenings()
        reserved_screenings = self.cinema.get_all_reserved_screening_ids()

        print("\nAll the screenings:")
        self.print_screenings(screenings, reserved_screenings)

    def make_reservation(self):
        screenings = self.cinema.get_all_screenings()
        reserved_screenings = self.cinema.get_all_reserved_screening_ids()

        available_screenings = [
            screening
            for screening in screenings
            if screening.screening_id not in reserved_screenings
        ]

        print("\nAvailable screenings:")
        self.print_screenings(available_screenings)

        try:
            index = (
                int(
                    input(
                        "\nEnter the number of a screening to reserve (0 to abort and go back): "
                    )
                )
                - 1
            )

            if index == -1:
                return

            if not -1 < index < len(available_screenings):
                raise ValueError()

            self.cinema.make_reservation(available_screenings[index].screening_id)
            print("The reservation was made successfully.")
        except ValueError:
            print("Invalid choice.")

    def print_reservations(self, reservations, screenings):
        print()

        if not reservations:
            print("You have no reservations.")
            return

        mapped = [
            screenings[
                next(
                    i
                    for i, v in enumerate(screenings)
                    if v.screening_id == reservation.screening_id
                )
            ]
            for reservation in reservations
        ]

        print("Your reservations:")
        self.print_screenings(mapped)

    def list_reservations(self):
        reservations = self.cinema.get_own_reservations()
        screenings = self.cinema.get_all_screenings()

        self.print_reservations(reservations, screenings)

    def cancel_reservation(self):
        reservations = self.cinema.get_own_reservations()
        screenings = self.cinema.get_all_screenings()

        self.print_reservations(reservations, screenings)

        if not reservations:
            return

        try:
            index = (
                int(
                    input(
                        "\nEnter the number of a reservation to cancel (0 to abort and go back): "
                    )
                )
                - 1
            )

            if index == -1:
                return

            if not -1 < index < len(reservations):
                raise ValueError()

            self.cinema.cancel_reservation(reservations[index].screening_id)
            print("The reservation was cancelled successfully.")
        except ValueError:
            print("Invalid choice.")

    def run(self):
        print("Welcome to the Cinema Malta reservation system!")
        user_id = input("Please, enter your User ID: ")
        print("Logging in...")
        self.cinema = Cinema(user_id)

        while True:
            options = (
                ("List all the screenings", self.list_screenings),
                ("Make a reservation", self.make_reservation),
                ("List my reservations", self.list_reservations),
                ("Cancel a reservation", self.cancel_reservation),
                ("Exit", exit),
            )

            print("\nAvailable actions:")
            for index, option in enumerate(options):
                print(f"#{index + 1:02d} | {option[0]}")

            try:
                index = int(input("\nEnter the number of an action: ")) - 1

                if not -1 < index < len(options):
                    raise ValueError()

                options[index][1]()
            except ValueError:
                print("Invalid choice.")


if __name__ == "__main__":
    cinema_cli = CinemaCLI()
    cinema_cli.run()
