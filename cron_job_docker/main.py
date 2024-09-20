# random_numbers.py

# import pandas
import random
from datetime import datetime

def print_random_numbers():
    random_numbers = [random.randint(1, 100) for _ in range(5)]
    print(f"{datetime.now()}: {random_numbers}")

if __name__ == "__main__":
    for i in range(20):
        print_random_numbers()


