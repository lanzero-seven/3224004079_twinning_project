# test_grader.py
"""必做 5：批改功能测试。"""
import os
from fractions import Fraction

from grader import grade


EX = "Exercises_test.txt"
AN = "Answers_test.txt"
GR = "Grade_test.txt"


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run_case(name, ex_content, an_content, expect_correct, expect_wrong):
    """
    expect_correct/expect_wrong: 期望的题号列表（有序）。
    """
    write(EX, ex_content)
    write(AN, an_content)
    grade(EX, AN, GR)
    text = read(GR)
    print(f"--- {name} ---")
    print(text.rstrip())

    expect = (
        f"Correct: {len(expect_correct)} "
        f"({', '.join(map(str, expect_correct))})"
    )
    assert expect in text, f"Correct 行不对: 期望 {expect}"

    expect_w = (
        f"Wrong: {len(expect_wrong)} "
        f"({', '.join(map(str, expect_wrong))})"
    )
    assert expect_w in text, f"Wrong 行不对: 期望 {expect_w}"

    print(f"✅ {name} 通过\n")


# ============================================================
# 用例 1：全对
# ============================================================
def case_all_correct():
    run_case(
        "用例 1：全对",
        "1. 3 + 5 =\n2. 1/2 + 3/4 =\n3. 8 ÷ 4 =\n",
        "1) 8\n2) 1'1/4\n3) 2\n",
        [1, 2, 3], []
    )


# ============================================================
# 用例 2：全错
# ============================================================
def case_all_wrong():
    run_case(
        "用例 2：全错",
        "1. 3 + 5 =\n2. 1/2 + 3/4 =\n",
        "1) 99\n2) 99\n",
        [], [1, 2]
    )


# ============================================================
# 用例 3：部分对部分错
# ============================================================
def case_partial():
    run_case(
        "用例 3：部分对部分错",
        "1. 3 + 5 =\n2. 1/2 + 3/4 =\n"
        "3. 8 ÷ 4 =\n4. 1/3 + 1/6 =\n5. 7 - 2 =\n",
        "1) 8\n2) 99\n3) 2\n4) 99\n5) 5\n",
        [1, 3, 5], [2, 4]
    )


# ============================================================
# 用例 4：等价但形式不同的答案应判对
# ============================================================
def case_equivalent_forms():
    # 1/2 写成 2/4、4/8；1'1/4 写成 5/4、10/8
    run_case(
        "用例 4：等价形式（应判对）",
        "1. 1/2 + 0 =\n2. 1/2 + 0 =\n3. 1/2 + 0 =\n4. 1 + 1/4 =\n",
        "1) 1/2\n2) 2/4\n3) 4/8\n4) 10/8\n",
        [1, 2, 3, 4], []
    )


# ============================================================
# 用例 5：用户漏答某题，应判错但不崩
# ============================================================
def case_missing_answer():
    run_case(
        "用例 5：用户漏答第 2 题",
        "1. 3 + 5 =\n2. 1/2 + 3/4 =\n3. 8 ÷ 4 =\n",
        "1) 8\n3) 2\n",            # 缺第 2 题
        [1, 3], [2]
    )


# ============================================================
# 用例 6：用户答案格式非法，应判错但不崩
# ============================================================
def case_invalid_answer():
    run_case(
        "用例 6：非法答案文本",
        "1. 3 + 5 =\n2. 1/2 + 3/4 =\n3. 8 ÷ 4 =\n",
        "1) 8\n2) abc\n3) 2\n",     # 第 2 题是垃圾字符串
        [1, 3], [2]
    )


# ============================================================
# 用例 7：用户答案 0 与标准答案 0 匹配
# ============================================================
def case_zero_answer():
    # 手工构造一道答案为 0 的题：1 - 1 = 0
    run_case(
        "用例 7：答案为 0",
        "1. 1 - 1 =\n2. 3 + 5 =\n",
        "1) 0\n2) 8\n",
        [1, 2], []
    )


# ============================================================
# 主流程
# ============================================================
if __name__ == "__main__":
    case_all_correct()
    case_all_wrong()
    case_partial()
    case_equivalent_forms()
    case_missing_answer()
    case_invalid_answer()
    case_zero_answer()

    # 清理临时文件（也可以不清理，留作报告截图）
    # for p in (EX, AN, GR):
    #     if os.path.exists(p):
    #         os.remove(p)

    print("=== 必做 5 全部通过 ✓ ===")