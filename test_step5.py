# test_step5.py
from fractions import Fraction
from expr_parser import ExpressionParser

def p(s):
    return ExpressionParser(s).parse()

def test_basic():
    assert p("3 + 5").evaluate() == Fraction(8)
    assert p("1/2 + 3/4").evaluate() == Fraction(5, 4)
    assert p("2'3/8 + 1/8").evaluate() == Fraction(5, 2)
    print("[OK] 基本解析")

def test_priority():
    # 3 + 5 × 2 = 13，不是 16
    assert p("3 + 5 × 2").evaluate() == Fraction(13)
    # (3 + 5) × 2 = 16
    assert p("(3 + 5) × 2").evaluate() == Fraction(16)
    print("[OK] 优先级")

def test_left_assoc():
    # 8 - 3 - 1 = 4，不是 6
    assert p("8 - 3 - 1").evaluate() == Fraction(4)
    # 8 ÷ 4 ÷ 2 = 1，不是 4
    assert p("8 ÷ 4 ÷ 2").evaluate() == Fraction(1)
    print("[OK] 左结合")

def test_paren_required():
    assert p("8 - (3 - 1)").evaluate() == Fraction(6)
    assert p("8 ÷ (4 ÷ 2)").evaluate() == Fraction(4)
    print("[OK] 括号")

def test_compat_symbols():
    assert p("3 * 5").evaluate() == Fraction(15)
    assert p("3 / 5").evaluate() == Fraction(3, 5)
    assert p("3 + 5").evaluate() == Fraction(8)
    print("[OK] 兼容 */")

if __name__ == "__main__":
    test_basic()
    test_priority()
    test_left_assoc()
    test_paren_required()
    test_compat_symbols()
    print("第 5 步全部通过 ✓")