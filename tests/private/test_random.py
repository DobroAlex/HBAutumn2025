"""Some cases to show off how random the random can be."""
import random
import time
import uuid

import pytest


def test_bad_seed():
    """
    When two tests share a week random seed generator
    it can cause those tests to unexpectedly generate the same random values.
    """
    shared_seed = time.monotonic()
    random.seed(shared_seed)
    generated_by_first_test = tuple(random.random() for _ in range(5))
    random.seed(shared_seed)
    generated_by_second_test = tuple(random.random() for _ in range(5))
    assert generated_by_first_test == generated_by_second_test


@pytest.fixture(scope="function")
def insemination() -> bytes:
    """Build a unique seed for each test param."""
    seed = uuid.uuid4().bytes
    random.seed(seed)
    return seed


@pytest.mark.parametrize("generation", (1, 2, 3), )
def test_with_proper_unique_seed(insemination, generation):
    """This test uses much safer generator and thus tests won't suffer from common random."""
    print(f"seed == {insemination}")
    print(tuple(random.random() for _ in range(5)))
