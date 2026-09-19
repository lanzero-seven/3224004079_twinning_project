# main.py
"""
小学四则运算题目生成程序 —— 命令行入口

出题模式：
    python main.py -n 10 -r 10
批改模式：
    python main.py -e Exercises.txt -a Answers.txt
"""
import argparse
import os
import sys

from generator import generate_exercises
from utils import fraction_to_string, save_exercises, save_answers
from grader import grade


def run_generate_mode(args, parser):
    """出题模式：生成题目与答案文件，并打印预览。"""
    if args.n is None or args.r is None:
        parser.error("出题模式必须同时提供 -n 和 -r")
    if args.n <= 0:
        parser.error("-n 必须为正整数")
    if args.r < 1:
        parser.error("-r 必须 >= 1")

    print(f"正在生成 {args.n} 道题（r={args.r}）...")

    try:
        exercises = generate_exercises(args.n, args.r)
    except RuntimeError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

    save_exercises(exercises, "Exercises.txt")
    save_answers(exercises, "Answers.txt")
    print("已生成 Exercises.txt 和 Answers.txt")

    # 预览前 5 道（答案用 fraction_to_string，和 Answers.txt 保持一致）
    print("\n预览前 5 道：")
    for i, ex in enumerate(exercises[:], start=1):
        expr_str = ex.expression.to_string()
        ans_str = fraction_to_string(ex.answer)
        print(f"  {i}. {expr_str} = {ans_str}")


def run_grade_mode(args, parser):
    """批改模式：读取题目与用户答案，生成 Grade.txt。"""
    if args.e is None or args.a is None:
        parser.error("批改模式必须同时提供 -e 和 -a")
    if not os.path.exists(args.e):
        parser.error(f"题目文件不存在：{args.e}")
    if not os.path.exists(args.a):
        parser.error(f"答案文件不存在：{args.a}")

    grade(args.e, args.a)


def main():
    parser = argparse.ArgumentParser(
        description="小学四则运算题目生成程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  出题：python main.py -n 10 -r 10\n"
            "  批改：python main.py -e Exercises.txt -a Answers.txt\n"
        ),
    )
    parser.add_argument("-n", type=int, metavar="N",
                        help="生成题目数量（出题模式，必须与 -r 同用）")
    parser.add_argument("-r", type=int, metavar="R",
                        help="数值范围上界（所有数值 < R，必须与 -n 同用）")
    parser.add_argument("-e", type=str, metavar="FILE",
                        help="题目文件（批改模式，必须与 -a 同用）")
    parser.add_argument("-a", type=str, metavar="FILE",
                        help="答案文件（批改模式，必须与 -e 同用）")

    args = parser.parse_args()

    # 模式判断：
    #   只要有 -e 或 -a 任意一个 -> 批改模式
    #   否则                    -> 出题模式
    if args.e is not None or args.a is not None:
        run_grade_mode(args, parser)
    else:
        run_generate_mode(args, parser)


if __name__ == "__main__":
    main()