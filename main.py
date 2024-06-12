from core.cinema import Cinema


class CinemaCLI:
    def print_screening_times(self, screening_times, check_availability=False):
        for index, screening_time in enumerate(screening_times):
            print(
                "#%02d | %s | %s | %-12s | %s" % (index + 1, *screening_time[1:])
                + (
                    " — SOLD OUT"
                    if check_availability
                    and not self.cinema.is_screening_time_available(
                        screening_time.screening_time_id
                    )
                    else ""
                )
            )

    def list_screening_times(self):
        screening_times = self.cinema.get_all_screening_times()

        print("\nAll the screening times:")
        self.print_screening_times(screening_times, check_availability=True)

    def make_reservation(self):
        screening_times = self.cinema.get_all_screening_times()

        available_screening_times = [
            screening_time
            for screening_time in screening_times
            if self.cinema.is_screening_time_available(screening_time.screening_time_id)
        ]

        print("\nAvailable screening times:")
        self.print_screening_times(available_screening_times)

        try:
            print("\n#00 | Abort and go back")
            index = int(input("\nEnter the number of a screening time: ")) - 1

            if index == -1:
                return

            if not -1 < index < len(available_screening_times):
                raise ValueError()

            self.cinema.make_reservation(
                available_screening_times[index].screening_time_id
            )
            print("The reservation was made successfully.")
        except ValueError:
            print("Invalid choice.")

    def print_reservations(self, reservations, screening_times):
        print()

        if not reservations:
            print("NO RESERVATIONS")
            return

        mapped = [
            screening_times[
                next(
                    i
                    for i, v in enumerate(screening_times)
                    if v.screening_time_id == reservation.screening_time_id
                )
            ]
            for reservation in reservations
        ]

        print("Your reservations:")
        self.print_screening_times(mapped)

    def list_reservations(self):
        reservations = self.cinema.get_reservations()
        screening_times = self.cinema.get_all_screening_times()

        self.print_reservations(reservations, screening_times)

    def cancel_reservation(self):
        reservations = self.cinema.get_reservations()
        screening_times = self.cinema.get_all_screening_times()

        self.print_reservations(reservations, screening_times)

        if not reservations:
            return

        try:
            print("\n#00 | Abort and go back")
            index = int(input("\nEnter the number of a reservation: ")) - 1

            if index == -1:
                return

            if not -1 < index < len(reservations):
                raise ValueError()

            self.cinema.cancel_reservation(reservations[index].reservation_id)
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
                ("List all the screening times", self.list_screening_times),
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
