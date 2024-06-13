import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from core.cinema import CinemaClient

ITERATIONS = 10000
DEBUG = False


def run_stress_test_1():
    client = CinemaClient("test_1")

    all = client.get_all_screenings()
    reserved = client.get_all_reserved_screening_ids()
    first = next(
        screening.screening_id
        for screening in all
        if screening.screening_id not in reserved
    )

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        for _ in range(ITERATIONS):
            executor.submit(client.make_reservation, first)
    print(f"Finished stress test 1 in {time.time() - start_time} seconds")


def run_stress_test_2():
    client_1 = CinemaClient("test_2_1")
    client_2 = CinemaClient("test_2_2")

    def perform_action(client: CinemaClient):
        r = random.randint(0, 3)
        if r == 0:
            client.get_all_screenings()
            client.get_all_reserved_screening_ids()
            if DEBUG:
                print("Get screenings")
        elif r == 1:
            client.get_own_reservations()
            if DEBUG:
                print("Get reservations")
        elif r == 2:
            all = client.get_all_screenings()
            reserved = client.get_all_reserved_screening_ids()
            available = random.choice(
                [
                    screening.screening_id
                    for screening in all
                    if screening.screening_id not in reserved
                ]
            )
            if DEBUG:
                print(f"Reserve {available}")
            client.make_reservation(available)
        elif r == 3:
            reservations = client.get_own_reservations()
            picked = random.choice(map(lambda x: x.screening_id, reservations))
            if picked:
                if DEBUG:
                    print(f"Cancel {picked}")
                client.cancel_reservation(picked)

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        for _ in range(ITERATIONS):
            executor.submit(perform_action, random.choice((client_1, client_2)))
    print(f"Finished stress test 2 in {time.time() - start_time} seconds")


def run_stress_test_3():
    client_1 = CinemaClient("test_3_1")
    client_2 = CinemaClient("test_3_2")

    all = client_1.get_all_screenings()

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        for screening in all:
            id = screening.screening_id
            executor.submit(client_1.make_reservation, id)
            executor.submit(client_2.make_reservation, id)
    print(f"Finished stress test 3 in {time.time() - start_time} seconds")


if __name__ == "__main__":
    test_number = int(sys.argv[1])
    if test_number == 1:
        run_stress_test_1()
    elif test_number == 2:
        run_stress_test_2()
    elif test_number == 3:
        run_stress_test_3()
