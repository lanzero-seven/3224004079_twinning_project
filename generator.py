# generator.py
"""随机生成合法的四则运算题。"""
import random
from fractions import Fraction
from expression import ExpressionNode


def generate_number(r: int, force_fraction: bool = False) -> Fraction:
    """
    生成一个满足 0 <= value < r 的数。
    force_fraction=True 时，强制生成分数（值一定不是整数）。
    自然数从 1 开始（不含 0），避免 (0 + 9) 这种怪题。
    """
    if r < 1:
        raise ValueError("r 必须 >= 1")
    if r == 1:
        return Fraction(0, 1)   # r=1 只能返回 0

    # 需要分数时跳过整数分支
    if not force_fraction and random.choice([True, False]):
        return Fraction(random.randint(1, r - 1), 1)

    # 分数分支：拒绝生成"值恰好是整数"的分数（如 4/2）
    for _ in range(50):
        d = random.randint(2, r)
        n = random.randint(1, d * r - 1)
        v = Fraction(n, d)
        if v >= r:
            continue
        if force_fraction and v.denominator == 1:
            continue   # 保证是真分数/带分数，不是整数
        return v

    # 兜底
    return Fraction(random.randint(1, r - 1), 1)


def _is_valid(operator, lv, rv) -> bool:
    """判断一个 operator(lv, rv) 是否合法。"""
    if operator == '-':
        return lv >= rv
    if operator == '/':
        if rv == 0:
            return False
        result = lv / rv
        return 0 < result < 1
    return True  # + 和 * 无约束


def generate_expression(operator_count: int, r: int,
                        pure_integer: bool = True) -> ExpressionNode:
    """
    pure_integer=True  → 所有叶子都是整数
    pure_integer=False → 至少一个叶子是分数（用于保证"含分数题"真的有分数）
    """
    if operator_count == 0:
        return ExpressionNode(value=generate_number(r))

    for _ in range(50):
        operator = random.choice(['+', '-', '*', '/'])
        remaining = operator_count - 1
        left_count = random.randint(0, remaining)
        right_count = remaining - left_count

        left = generate_expression(left_count, r, pure_integer)
        right = generate_expression(right_count, r, pure_integer)

        try:
            lv = left.evaluate()
            rv = right.evaluate()
        except ZeroDivisionError:
            continue

        if not _is_valid(operator, lv, rv):
            continue

        return ExpressionNode(operator=operator, left=left, right=right)

    return ExpressionNode(value=generate_number(r))


class Exercise:
    def __init__(self, expression: ExpressionNode, answer: Fraction):
        self.expression = expression
        self.answer = answer


def _expression_has_fraction(node: ExpressionNode) -> bool:
    """递归检查表达式树里是否有分数（非整数值）叶子。"""
    if node.is_number():
        return node.value.denominator != 1
    return (_expression_has_fraction(node.left)
            or _expression_has_fraction(node.right))


def generate_exercises(n: int, r: int,
                       pure_integer_ratio: float = 0.7,
                       max_attempt_factor: int = 200):
    """
    生成 n 道不重复题。
    pure_integer_ratio：纯整数题的比例，默认 0.7（方案 B）。
    """
    exercises = []
    seen = set()
    max_attempts = n * max_attempt_factor
    attempts = 0

    # 先排好 n 道题的"类型序列"，保证比例准确
    # 0 = 纯整数题，1 = 含分数题
    type_seq = [0] * n
    num_fraction = int(round(n * (1 - pure_integer_ratio)))
    for i in range(num_fraction):
        type_seq[i] = 1
    random.shuffle(type_seq)

    type_idx = 0

    while len(exercises) < n:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError(
                f"无法生成足够不重复题目（已生成 {len(exercises)}/{n}，r={r}）"
            )

        want_pure = (type_seq[type_idx] == 0)
        operator_count = random.randint(1, 3)

        # 纯整数题：所有叶子都是整数
        if want_pure:
            root = _generate_pure_integer_expression(operator_count, r)
            if root is None:
                continue
        else:
            # 含分数题：先按普通方式生成，再检查是否真含分数
            root = generate_expression(operator_count, r, pure_integer=False)
            if not _expression_has_fraction(root):
                continue   # 生成出来恰好是纯整数题，重试

        key = root.canonical()
        if key in seen:
            continue

        seen.add(key)
        exercises.append(Exercise(root, root.evaluate()))
        type_idx += 1

    return exercises

def _generate_pure_integer_expression(operator_count: int,
                                      r: int):
    """
    生成一棵所有叶子都是整数的表达式树。
    r 太小时可能失败，返回 None。
    """
    if r < 2:
        return None   # r=1 无法生成纯整数题（不能出现 0，只能生成 0，没法运算）

    if operator_count == 0:
        return ExpressionNode(value=Fraction(random.randint(1, r - 1), 1))

    for _ in range(50):
        operator = random.choice(['+', '-', '*', '/'])
        remaining = operator_count - 1
        left_count = random.randint(0, remaining)
        right_count = remaining - left_count

        left = _generate_pure_integer_expression(left_count, r)
        right = _generate_pure_integer_expression(right_count, r)
        if left is None or right is None:
            continue

        try:
            lv = left.evaluate()
            rv = right.evaluate()
        except ZeroDivisionError:
            continue

        if not _is_valid(operator, lv, rv):
            continue

        return ExpressionNode(operator=operator, left=left, right=right)

    return None