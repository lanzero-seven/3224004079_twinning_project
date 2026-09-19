# test_step2.py
from fractions import Fraction
from expression import ExpressionNode

def leaf(n, d=1):
    return ExpressionNode(value=Fraction(n, d))

def op(o, l, r):
    return ExpressionNode(operator=o, left=l, right=r)

def test_evaluate():
    # 3 + 5 = 8
    assert op('+', leaf(3), leaf(5)).evaluate() == Fraction(8)
    # 1/6 + 1/8 = 7/24
    assert op('+', leaf(1, 6), leaf(1, 8)).evaluate() == Fraction(7, 24)
    # (3 + 5) * (7 - 2) = 40
    t = op('*', op('+', leaf(3), leaf(5)), op('-', leaf(7), leaf(2)))
    assert t.evaluate() == Fraction(40)
    print("[OK] evaluate")

def test_to_string():
    # 3 + 5 × 2
    t1 = op('+', leaf(3), op('*', leaf(5), leaf(2)))
    assert t1.to_string() == "3 + 5 × 2", t1.to_string()

    # (3 + 5) × 2
    t2 = op('*', op('+', leaf(3), leaf(5)), leaf(2))
    assert t2.to_string() == "(3 + 5) × 2", t2.to_string()

    # 8 - (3 - 1)，右侧子表达式必须加括号
    t3 = op('-', leaf(8), op('-', leaf(3), leaf(1)))
    assert t3.to_string() == "8 - (3 - 1)", t3.to_string()

    # 8 ÷ (4 ÷ 2)
    t4 = op('/', leaf(8), op('/', leaf(4), leaf(2)))
    assert t4.to_string() == "8 ÷ (4 ÷ 2)", t4.to_string()

    # 分数格式
    t5 = op('+', leaf(11, 8), leaf(3, 5))
    assert t5.to_string() == "1'3/8 + 3/5", t5.to_string()
    print("[OK] to_string")

def test_canonical():
    # 加法交换等价
    a = op('+', leaf(3), leaf(5)).canonical()
    b = op('+', leaf(5), leaf(3)).canonical()
    assert a == b, (a, b)

    # 乘法交换等价
    a = op('*', leaf(6), leaf(8)).canonical()
    b = op('*', leaf(8), leaf(6)).canonical()
    assert a == b

    # 减法不交换
    a = op('-', leaf(8), leaf(3)).canonical()
    b = op('-', leaf(3), leaf(8)).canonical()
    assert a != b

    # 3+(2+1) 与 (1+2)+3 应等价
    t1 = op('+', leaf(3), op('+', leaf(2), leaf(1)))
    t2 = op('+', op('+', leaf(1), leaf(2)), leaf(3))
    assert t1.canonical() == t2.canonical(), (t1.canonical(), t2.canonical())

    # 1+2+3 与 3+2+1 不应等价
    t3 = op('+', op('+', leaf(1), leaf(2)), leaf(3))
    t4 = op('+', op('+', leaf(3), leaf(2)), leaf(1))
    assert t3.canonical() != t4.canonical(), (t3.canonical(), t4.canonical())
    print("[OK] canonical")

if __name__ == "__main__":
    test_evaluate()
    test_to_string()
    test_canonical()
    print("第 2 步全部通过 ✓")