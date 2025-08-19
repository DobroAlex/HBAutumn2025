import pytest


def __piglets_in_the_house_provider() -> set[str]:
    """Gives the piglets in the house."""
    return {"Ниф-Ниф", "Наф-Наф", "Нуф-Нуф"}


@pytest.mark.xfail
def test_unordered_collections_comparison():
    """"""
    # We need to check whether all piglets are in the house.
    actual_piglets = __piglets_in_the_house_provider()
    expected_piglets = ["Ниф-Ниф", "Нуф-Нуф", "Наф-Наф"]
    with pytest.raises(AssertionError):
        # Can't compare like this due to type mismatch!
        assert expected_piglets == actual_piglets
    with pytest.raises(AssertionError):
        # Can't compare like this since the order is not guaranteed
        # when converting from list to set!

        # This is flaky as hell! Uncomment the @pytest.mark.xfail to see it flaking
        assert expected_piglets == list(actual_piglets)
    with pytest.raises(TypeError):
        # Can't compare like this -- list is unhashable
        assert expected_piglets in actual_piglets

    # Solution 1:
    # - Convert both collections to unordered type; risk of losing repetitive elements
    assert set(expected_piglets) == actual_piglets
    # Solution 2:
    # - Sort the items using the same idempotent rule
    assert sorted(expected_piglets) == sorted(list(actual_piglets))


# noinspection PySetFunctionToLiteral
@pytest.mark.xfail
def test_bad_ordered_to_unordered_to_ordered_conversion():
    """This fails pretty much always due to loss of order"""
    assert ["Биба", "Бобы", "Пупсени", "Вупсень"] == \
           list(set(["Биба", "Бобы", "Пупсени", "Вупсень"]))
