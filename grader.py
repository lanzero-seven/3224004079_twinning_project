# grader.py
"""批改：读取题目和用户答案，重新计算标准答案并比较。"""
from expr_parser import ExpressionParser
from utils import parse_number


def _read_exercises(filename):
    """返回 {题号: 表达式字符串}。格式 '1. 3 + 5 ='。"""
    items = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or '.' not in line:
                continue
            idx_str, rest = line.split('.', 1)
            try:
                idx = int(idx_str.strip())
            except ValueError:
                continue
            rest = rest.strip()
            if rest.endswith('='):
                rest = rest[:-1].strip()
            items[idx] = rest
    return items


def _read_answers(filename):
    """返回 {题号: Fraction 或 None}。格式 '1) 8'。"""
    items = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ')' not in line:
                continue
            idx_str, rest = line.split(')', 1)
            try:
                idx = int(idx_str.strip())
            except ValueError:
                continue
            try:
                items[idx] = parse_number(rest.strip())
            except Exception:
                items[idx] = None
    return items


def grade(exercise_file="Exercises.txt",
          answer_file="Answers.txt",
          output_file="Grade.txt"):
    exercises = _read_exercises(exercise_file)
    answers = _read_answers(answer_file)

    correct, wrong = [], []

    for idx in sorted(exercises.keys()):
        expr_text = exercises[idx]
        try:
            node = ExpressionParser(expr_text).parse()
            std = node.evaluate()
        except Exception:
            wrong.append(idx)
            continue

        user = answers.get(idx)
        if user is not None and user == std:
            correct.append(idx)
        else:
            wrong.append(idx)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")

    print(f"批改完成：正确 {len(correct)}，错误 {len(wrong)}")
    print(f"结果写入 {output_file}")