"""Some cases to show off how random the random can be."""
import random
import time
import uuid

import pytest


def test_bad_seed():
    shared_seed = time.monotonic()
    random.seed(shared_seed)
    generated_by_first_test = tuple(random.random() for _ in range(5))
    random.seed(shared_seed)
    generated_by_second_test = tuple(random.random() for _ in range(5))
    assert generated_by_first_test == generated_by_second_test


@pytest.fixture(scope="function")
def insementaor() -> bytes:
    """Build a unique seed for each test param."""
    seed = uuid.uuid4().bytes
    random.seed(seed)
    return seed


@pytest.mark.parametrize("generation", (1, 2, 3), )
def test_with_proper_unique_seed(insementaor, generation):
    print(f"seed == {insementaor}")
    print(tuple(random.random() for _ in range(5)))
