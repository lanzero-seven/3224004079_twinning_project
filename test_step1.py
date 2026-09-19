# test_step1.py
from fractions import Fraction
from utils import fraction_to_string, parse_number

def test_fraction_to_string():
    assert fraction_to_string(Fraction(3, 5)) == "3/5"
    assert fraction_to_string(Fraction(8, 4)) == "2"
    assert fraction_to_string(Fraction(11, 8)) == "1'3/8"
    assert fraction_to_string(Fraction(0, 1)) == "0"
    assert fraction_to_string(Fraction(-11, 8)) == "-1'3/8"
    print("[OK] fraction_to_string")

def test_parse_number():
    assert parse_number("3") == Fraction(3, 1)
    assert parse_number("3/5") == Fraction(3, 5)
    assert parse_number("2'3/8") == Fraction(19, 8)
    assert parse_number("-2'3/8") == Fraction(-19, 8)
    assert parse_number("6/8") == Fraction(3, 4)  # 自动约分
    print("[OK] parse_number")

def test_roundtrip():
    for v in [Fraction(0), Fraction(1), Fraction(3, 5), Fraction(11, 8), Fraction(7, 2)]:
        s = fraction_to_string(v)
        assert parse_number(s) == v, f"{v} -> {s} -> {parse_number(s)}"
    print("[OK] roundtrip")

if __name__ == "__main__":
    test_fraction_to_string()
    test_parse_number()
    test_roundtrip()
    print("第 1 步全部通过 ✓")