import base64
from converters.base_converter import BaseConverter
from units.base_unit import BaseUnit

class Base64Converter(BaseConverter):
    """
    A converter for Base64 encoding and decoding.
    Converts between UTF-8 strings and Base64-encoded strings.
    """

    def __init__(self):
        units = [
            BaseUnit(name="utf-8", description="Plain UTF-8 text"),
            BaseUnit(name="base64", description="Base64-encoded text")
        ]
        super().__init__(units)

    def convert(self, value: str, from_unit: str, to_unit: str) -> str:
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit == "utf-8" and to_unit == "base64":
            encoded_bytes = base64.b64encode(value.encode("utf-8"))
            return encoded_bytes.decode("ascii")

        elif from_unit == "base64" and to_unit == "utf-8":
            try:
                decoded_bytes = base64.b64decode(value)
                return decoded_bytes.decode("utf-8")
            except Exception as e:
                raise ValueError(f"Invalid base64 input: {e}")
        
        elif from_unit == to_unit:
            return value

        else:
            raise ValueError(f"Unsupported conversion: {from_unit} -> {to_unit}")
