"""
Usage of the same dict will cause test_1 & test_2 to fail with a single executor
(n == 1).

This test can be fixed by using a non-shared dict, see test_1_safe & test_2_safe.

N.B. Even test_1 and test_2 can be fixed by running with n >= 2,
although it's more of a dark magic.
"""

import pytest


@pytest.fixture(scope="session")
def shared_dict() -> dict:
    return {}


def test_1(shared_dict):
    shared_dict["a"] = 1
    assert shared_dict == {"a": 1}


def test_2(shared_dict):
    shared_dict["b"] = 2
    assert shared_dict == {"b": 2}


#######

@pytest.fixture(scope="function")
def shared_dict_safe() -> dict:
    return {}


def test_1_safe(shared_dict_safe):
    shared_dict_safe["a"] = 1
    assert shared_dict_safe == {"a": 1}


def test_2_safe(shared_dict_safe):
    shared_dict_safe["b"] = 2
    assert shared_dict_safe == {"b": 2}
