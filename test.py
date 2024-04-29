import time

from automation import Automation


def test_ratelimit():
    """
    the second call must be delayed by 1 minute
    """
    a = Automation()

    for _ in range(2):
        start_time = time.time()
        a.access_site()

        print("Access successful")
        end_time = time.time()
        print(f"Call duration: {end_time - start_time} seconds")


if __name__ == "__main__":
    test_ratelimit()
