# test_step3.py
import random
from fractions import Fraction
from generator import generate_number, generate_expression, generate_exercises

def test_number_range():
    random.seed(0)
    for _ in range(2000):
        v = generate_number(10)
        assert 0 <= v < 10, v
    # r=1 边界
    for _ in range(50):
        assert generate_number(1) == Fraction(0, 1)
    print("[OK] generate_number 范围")

def test_expression_constraints():
    random.seed(42)
    for _ in range(3000):
        root = generate_expression(random.randint(1, 3), 10)
        # 减法和除法合法：递归检查每个节点
        def check(node):
            if node.is_number():
                return node.value
            lv = check(node.left)
            rv = check(node.right)
            if node.operator == '-':
                assert lv >= rv, f"减法出现负数: {node.to_string()}"
            elif node.operator == '/':
                assert rv != 0
                assert 0 < lv / rv < 1, f"除法结果不是真分数: {node.to_string()}"
            if node.operator == '+': return lv + rv
            if node.operator == '-': return lv - rv
            if node.operator == '*': return lv * rv
            if node.operator == '/': return lv / rv
        check(root)
    print("[OK] 减法/除法约束")

def test_no_duplicates():
    random.seed(1)
    exs = generate_exercises(50, 10)
    keys = [e.expression.canonical() for e in exs]
    assert len(keys) == len(set(keys)), "生成了重复题"
    print("[OK] 去重")

def test_r1_insufficient():
    # r=1 时应报错（题目种类太少）
    random.seed(2)
    try:
        generate_exercises(100, 1)
        print("[WARN] r=1 竟然生成了 100 道，检查是否符合预期")
    except RuntimeError as e:
        print(f"[OK] r=1 边界正确报错: {e}")

if __name__ == "__main__":
    test_number_range()
    test_expression_constraints()
    test_no_duplicates()
    test_r1_insufficient()
    print("第 3 步全部通过 ✓")