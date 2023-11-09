from enum import Enum


class UtilityTypeEnum(Enum):
    def __init__(self, index: int, code: str, description: str):
        self.index = index
        self.code = code
        self.description = description

    @classmethod
    def from_index(cls, index: int):
        return next((item for item in cls if item.index == index), None)


class ResourceEnum(UtilityTypeEnum):
    ELECTRICITY = 1, "Wh", "Electricity"
    WATER = 2, "m³", "Water"
    GAS = 3, "m³", "Gas"


class MetricPrefixEnum(UtilityTypeEnum):
    def __init__(self, index: int, code: str, multiplier: float, description: str):
        super().__init__(index, code, description)
        self.multiplier = multiplier

    TERA = 1, "T", 1e12, "Tera(T) - x * 1,000,000,000,000"
    GIGA = 2, "G", 1e9, "Giga(G) - x * 1,000,000,000"
    MEGA = 3, "M", 1e6, "Mega(M) - x * 1,000,000"
    KILO = 4, "k", 1e3, "kilo(k) - x * 1,000"
    NONE = 5, "", 1, "no prefix - x * 1"
    CENTI = 6, "c", 1e-2, "centi(c) - x * 1/100"
    MILLI = 7, "m", 1e-3, "milli(m) - x * 1/1,000"
    MICRO = 8, "µ", 1e-6, "micro(µ) - x * 1/1,000,000"
    NANO = 9, "n", 1e-9, "nano(n) - x * 1/1,000,000,000"
    PICO = 10, "p", 1e-12, "pico(p) - x * 1/1,000,000,000,000"
