# utils.py
"""分数与题目格式之间的转换工具。"""
from fractions import Fraction


def fraction_to_string(value: Fraction) -> str:
    """
    将 Fraction 转成题目要求的格式：
      整数    -> "8"
      真分数  -> "3/5"
      带分数  -> "1'3/8"
      负数    -> "-1'3/8"（正常流程不会出现，但保留支持）
    """
    n, d = value.numerator, value.denominator

    # 整数
    if d == 1:
        return str(n)

    # 真分数
    if abs(n) < d:
        return f"{n}/{d}"

    # 带分数
    sign = "-" if n < 0 else ""
    abs_n = abs(n)
    integer_part = abs_n // d
    remainder = abs_n % d
    return f"{sign}{integer_part}'{remainder}/{d}"


def parse_number(text: str) -> Fraction:
    """
    解析三种格式为 Fraction：
      "3"      -> Fraction(3,1)
      "3/5"    -> Fraction(3,5)
      "2'3/8"  -> Fraction(19,8)
      "-2'3/8" -> Fraction(-19,8)
    """
    text = text.strip()
    if not text:
        raise ValueError("空字符串无法解析为数字")

    negative = False
    if text.startswith('-'):
        negative = True
        text = text[1:].strip()

    if "'" in text:
        integer_part, frac_part = text.split("'", 1)
        num, den = frac_part.split("/", 1)
        value = Fraction(int(integer_part) * int(den) + int(num), int(den))
    elif "/" in text:
        num, den = text.split("/", 1)
        value = Fraction(int(num), int(den))
    else:
        value = Fraction(int(text), 1)

    return -value if negative else value

# utils.py 追加

def save_exercises(exercises, filename="Exercises.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, ex in enumerate(exercises, start=1):
            f.write(f"{i}. {ex.expression.to_string()} =\n")


def save_answers(exercises, filename="Answers.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, ex in enumerate(exercises, start=1):
            f.write(f"{i}) {fraction_to_string(ex.answer)}\n")