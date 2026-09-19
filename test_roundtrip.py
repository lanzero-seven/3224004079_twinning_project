# test_roundtrip.py
"""
闭环一致性测试:
  生成器算出的答案 == 题面字符串重新解析后算出的答案
"""
import random
from fractions import Fraction

from generator import generate_exercises
from utils import save_exercises, save_answers, parse_number
from expr_parser import ExpressionParser


def run_once(n=200, r=20, seed=2024):
    random.seed(seed)
    exs = generate_exercises(n, r)

    save_exercises(exs, "Exercises.txt")
    save_answers(exs, "Answers.txt")

    lines_e = open("Exercises.txt", encoding="utf-8").read().splitlines()
    lines_a = open("Answers.txt", encoding="utf-8").read().splitlines()

    assert len(lines_e) == n, f"Exercises 行数 {len(lines_e)} != {n}"
    assert len(lines_a) == n, f"Answers   行数 {len(lines_a)} != {n}"

    fails = []
    for i, (le, la) in enumerate(zip(lines_e, lines_a), start=1):
        # 拆题面: "1. 3 + 5 =" -> "3 + 5"
        expr_str = le.split(".", 1)[1].rsplit("=", 1)[0].strip()
        # 拆答案: "1) 8" -> "8"
        ans_str = la.split(")", 1)[1].strip()

        # 路径 A: 生成时写在文件里的答案
        file_ans = parse_number(ans_str)
        # 路径 B: 重新解析题面算出的答案
        try:
            re_ans = ExpressionParser(expr_str).parse().evaluate()
        except Exception as e:
            fails.append((i, expr_str, f"解析异常: {e}"))
            continue

        if re_ans != file_ans:
            fails.append((i, expr_str, f"文件 {file_ans} vs 重算 {re_ans}"))

    if fails:
        print(f"❌ {len(fails)} / {n} 道不一致：")
        for i, expr, msg in fails[:10]:
            print(f"  第 {i} 题: {expr}")
            print(f"    {msg}")
        return False

    print(f"✅ {n} 题闭环全部一致（seed={seed}）")
    return True


if __name__ == "__main__":
    ok = True
    # 多组不同 seed / r，覆盖更多情况
    for seed, r, n in [(1, 10, 200),
                       (2, 20, 200),
                       (3, 50, 200),
                       (42, 100, 200),
                       (99, 5, 200)]:
        ok &= run_once(n=n, r=r, seed=seed)
    print("\n" + ("全部通过 ✓" if ok else "存在失败 ✗"))
