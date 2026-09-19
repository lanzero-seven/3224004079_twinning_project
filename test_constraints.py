# test_constraints.py
"""
约束抽样测试:
  生成 3000 道题，递归检查每个节点是否满足需求 2~5 的所有约束。
"""
import random
from fractions import Fraction

from generator import generate_expression


def check_node(node, r, path="root"):
    """
    递归检查一个表达式树的所有节点。
    返回该节点算出的值。
    违规立刻 assert。
    """
    # 叶子：数值必须 0 <= v < r（r=1 时允许 0）
    if node.is_number():
        v = node.value
        assert v >= 0, f"[{path}] 负数值: {v}"
        assert v < r or (r == 1 and v == 0), \
            f"[{path}] 数值 {v} 越界 r={r}"
        return v

    # 内节点：先算左右
    lv = check_node(node.left, r, path + ".left")
    rv = check_node(node.right, r, path + ".right")

    op = node.operator

    if op == '+':
        return lv + rv
    if op == '-':
        assert lv >= rv, \
            f"[{path}] 减法为负: {lv} - {rv}（题面: {node.to_string()}）"
        return lv - rv
    if op == '*':
        return lv * rv
    if op == '/':
        assert rv != 0, \
            f"[{path}] 除零: 题面 {node.to_string()}"
        result = lv / rv
        assert 0 < result < 1, \
            f"[{path}] 除法结果非真分数: {lv} ÷ {rv} = {result} " \
            f"（题面: {node.to_string()}）"
        return result
    raise ValueError(f"未知运算符 {op}")


def count_ops(node):
    if node.is_number():
        return 0
    return 1 + count_ops(node.left) + count_ops(node.right)


def run(n_iters=3000, seed=42):
    random.seed(seed)
    stats = {"r_min": 10**9, "r_max": 0, "ops": {1: 0, 2: 0, 3: 0}}

    for i in range(n_iters):
        r = random.randint(2, 30)
        stats["r_min"] = min(stats["r_min"], r)
        stats["r_max"] = max(stats["r_max"], r)

        op_count = random.randint(1, 3)
        root = generate_expression(op_count, r)

        # 约束 5: 运算符个数 <= 3，且实际值要和声明一致或更少
        actual = count_ops(root)
        assert actual <= 3, f"运算符 {actual} 个，超过上限 3"
        stats["ops"][actual] = stats["ops"].get(actual, 0) + 1

        # 约束 1~4: 递归检查
        try:
            check_node(root, r)
        except AssertionError as e:
            print(f"❌ 第 {i} 次生成违规（r={r}, op_count={op_count}）:")
            print(f"   题面: {root.to_string()}")
            print(f"   详情: {e}")
            return False

    print(f"✅ {n_iters} 次生成全部合规（seed={seed}）")
    print(f"   r 范围: {stats['r_min']} ~ {stats['r_max']}")
    print(f"   运算符个数分布: {stats['ops']}")
    return True


if __name__ == "__main__":
    ok = True
    for seed in [42, 1, 7, 2024, 999]:
        ok &= run(n_iters=3000, seed=seed)
    print("\n" + ("全部通过 ✓" if ok else "存在违规 ✗"))