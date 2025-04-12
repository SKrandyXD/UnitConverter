from converters.base_converter import BaseConverter
from units.base_unit import BaseUnit

class NumeralSystemConverter(BaseConverter):
    """
    A converter for numeral systems (e.g., binary, octal, decimal, hexadecimal, etc.).
    Can convert between any two bases from 2 to 36.
    """

    def __init__(self):
        units = [
            BaseUnit(name=str(i), description=f"Base-{i} numeral system.") for i in range(2, 37)
        ]
        super().__init__(units)

    def convert(self, value: str, from_base: str, to_base: str) -> str:
        from_base = int(from_base)
        to_base = int(to_base)

        if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
            raise ValueError("Bases must be between 2 and 36")

        # Split into integer and fractional parts
        if '.' in value:
            int_part_str, frac_part_str = value.split('.')
        else:
            int_part_str, frac_part_str = value, ''

        # Convert integer part to decimal
        int_part_dec = int(int_part_str, from_base) if int_part_str else 0

        # Convert fractional part to decimal
        frac_part_dec = 0
        for i, digit in enumerate(frac_part_str):
            digit_value = int(digit, base=from_base) if digit.isdigit() else int(digit.lower(), 36)
            if digit_value >= from_base:
                raise ValueError(f"Invalid digit '{digit}' for base {from_base}")
            frac_part_dec += digit_value / (from_base ** (i + 1))

        # Combine both parts
        decimal_value = int_part_dec + frac_part_dec

        # Convert integer part to target base
        def int_to_base(n: int, base: int) -> str:
            if n == 0:
                return '0'
            digits = []
            while n > 0:
                remainder = n % base
                digits.append("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[remainder])
                n //= base
            return ''.join(reversed(digits))

        # Convert fractional part to target base
        def frac_to_base(f: float, base: int, precision: int = 10) -> str:
            result = []
            count = 0
            while f > 0 and count < precision:
                f *= base
                digit = int(f)
                result.append("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[digit])
                f -= digit
                count += 1
            return ''.join(result)

        int_part_out = int_to_base(int_part_dec, to_base)
        frac_part_out = frac_to_base(frac_part_dec, to_base)

        return f"{int_part_out}.{frac_part_out}" if frac_part_out else int_part_out
