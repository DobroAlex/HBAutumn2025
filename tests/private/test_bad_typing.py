from enum import Enum
from typing import TypeVar, runtime_checkable, Protocol

import pytest
from pydantic import BaseModel


def do_addition(a, b):
    return a + b


def test_surprising_type():
    assert do_addition(1, 2) == 3
    assert do_addition(1.2, 3.4) == 4.6
    assert do_addition("10", "12") == "1012"
    assert do_addition([1, ], [2, ]) == [1, 2, ]
    assert do_addition((1,), [2, ])


@runtime_checkable
class SupportAddition(Protocol):
    def __add__(self: 'T', other: 'T') -> 'T':
        ...


T = TypeVar('T', bound=SupportAddition)


def __do_addition_new(a: T, b: T) -> T:
    return a + b


def test_better_type_check() -> None:
    assert __do_addition_new(5, 10) == 15
    assert __do_addition_new("5", "10") == "510"
    with pytest.raises(TypeError):
        assert __do_addition_new(5, "10") == "510"  # Is not caught by mypy but caught by IDE

    __do_addition_new(7, {'a': 1})  # Caught by mypy


def test_dont_abuse_the_dict():
    """Excessive use of nested dicts is usually a bad idea."""
    # Now let's look at IDE's derived typehint
    # ...
    # and see it's insanely long and doesn't provide anything about the dict structure.
    response = {
        [
            {
                "manufacturer": "BibiMobiles",
                "model": "Bibika",
                "color": "red",
                "type": "hot-hatchback",
                "seats": 5,
                "trunk_vol": 300,
                "engine":
                    {
                        "size": 1.6,
                        "horse_power": 125,
                        "fuel": "gasoline",
                    },
                "drive_base":
                    {
                        "drive": "FWD",
                        "wheels": 4,
                        "suspension": "independent",
                    },
                "gear":
                    {
                        "box": "robot",
                        "gears": 6,
                        "has_rear": True,
                    },
            },
        ]
    }


class CarManufacturers(Enum):
    BIBI_MOBILES = "BibiMobiles"
    BIBI_MOTORS = "BibiMotors"


class Colors(Enum):
    RED = "red"
    ORANGE = "orange"


class CarType(Enum):
    SEDAN = "sedan"
    HATCHBACK = "hatchback"
    HOT_HATCHBACK = "hot-hatchback"


class Fuel(Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    LEGS = "legs"


class Engine(BaseModel):
    size: int | float
    horse_power: int
    fuel: Fuel


class Suspensions(Enum):
    INDEPENDENT = "independent"
    DUNNO = "others"


class Drives(Enum):
    FWD = "FWD"
    RWD = "RWD"
    FOUR_WHD = "4WD"


class DriveBase(BaseModel):
    drive: Drives
    wheels: int
    suspension: Suspensions


class GearBox(Enum):
    MANUAL = "manual"
    ROBOT = "robot"
    AUTO = "AUTO"


class Gear(BaseModel):
    box: GearBox
    gears: int
    has_rear: bool = True


class CarInfo(BaseModel):
    manufacturer: CarManufacturers
    model: str
    color: Colors
    type: CarType
    seats: int
    trunk_vol: int
    engine: Engine
    drive_base: DriveBase
    gear: Gear


def test_rewrite_dict_to_model():
    """Let's rewrite the model to be readable."""
    my_car = CarInfo.model_validate({
        "manufacturer": "BibiMobiles",
        "model": "Bibika",
        "color": "red",
        "type": "hot-hatchback",
        "seats": 5,
        "trunk_vol": 300,
        "engine":
            {
                "size": 1.6,
                "horse_power": 125,
                "fuel": "gasoline",
            },
        "drive_base":
            {
                "drive": "FWD",
                "wheels": 4,
                "suspension": "independent",
            },
        "gear":
            {
                "box": "robot",
                "gears": 6,
                "has_rear": True,
            },
    })

    # Let's inspect the auto-completion features from IDE and the validation!
    print(my_car)

    my_car.model_dump()
