"""Custom functions for various operations."""
import random
import datetime


def get_seed():
    seed = datetime.datetime.today()
    seed_origin = datetime.datetime(2010, 5, 4, 18, 10, 40)
    seed = seed - seed_origin
    seed = int(seed.total_seconds())
    return seed


def get_random_num(bottom_range, top_range):
    """Gets a random int between x and y inclusive."""
    seed = get_seed()
    random.seed(seed)
    return random.randint(bottom_range, top_range)


def get_random_sample(bottom_range, top_range, amount):
    """Gets {amount} of random values between {bottom_range} and {top_range}"""
    seed = get_seed()
    random.seed(seed)
    return random.sample(range(bottom_range, top_range), amount)
