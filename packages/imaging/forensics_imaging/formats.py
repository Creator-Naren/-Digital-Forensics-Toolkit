from enum import Enum

class ImageFormat(str, Enum):
    E01 = "E01"
    RAW = "RAW"
    DD = "DD"

FORMAT_CONFIG = {
    ImageFormat.E01: {"extension": ".e01", "compressed": True, "split": True},
    ImageFormat.RAW: {"extension": ".raw", "compressed": False, "split": False},
    ImageFormat.DD: {"extension": ".dd", "compressed": False, "split": True},
}