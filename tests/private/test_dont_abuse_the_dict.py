from enum import Enum

from pydantic import BaseModel


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
