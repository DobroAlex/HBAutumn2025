"""list->set->list MAY or MAY NOT lose order."""
import pytest


# noinspection PySetFunctionToLiteral
@pytest.mark.repeat(1000)
def test_loss_of_order():
    """
    Run it several times with multiple workers (n >= 10) to see the flaky behaviour.

    N.B. Running it with a single worker (n == 1) may often cause test to fail
    with constant results 😅
    """
    assert ["one", "two", "three"] == list(set(["one", "two", "three"]))


# noinspection PySetFunctionToLiteral
@pytest.mark.repeat(100)
def test_no_loss_of_order():
    """This one doesnt fail."""
    assert sorted(["one", "two", "three"]) == \
           sorted(list(set(["one", "two", "three"])))
