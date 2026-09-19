# expression.py
"""表达式树：节点、计算、字符串化、标准化。"""
from fractions import Fraction
from utils import fraction_to_string

# 优先级：加减 1，乘除 2
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}


class ExpressionNode:
    def __init__(self, value=None, operator=None, left=None, right=None):
        self.value = value            # Fraction，叶子节点
        self.operator = operator      # '+', '-', '*', '/'
        self.left = left
        self.right = right

    def is_number(self) -> bool:
        return self.operator is None

    # ---------- 计算 ----------
    def evaluate(self) -> Fraction:
        if self.is_number():
            return self.value

        lv = self.left.evaluate()
        rv = self.right.evaluate()

        if self.operator == '+':
            return lv + rv
        if self.operator == '-':
            return lv - rv
        if self.operator == '*':
            return lv * rv
        if self.operator == '/':
            if rv == 0:
                raise ZeroDivisionError("除以零")
            return lv / rv
        raise ValueError(f"未知运算符: {self.operator}")

    # ---------- 字符串化 ----------
    def to_string(self, parent_op=None, is_right=False) -> str:
        """
        根据父运算符与自己是左/右孩子决定是否加括号。
        规则：
          1. 自己优先级 < 父优先级        -> 加括号
          2. 优先级相同且自己是右孩子，
             且父是 '-' 或 '/'             -> 加括号
          3. 其他不加
        """
        if self.is_number():
            return fraction_to_string(self.value)

        need_paren = False
        if parent_op is not None:
            my_prec = PRECEDENCE[self.operator]
            pa_prec = PRECEDENCE[parent_op]
            if my_prec < pa_prec:
                need_paren = True
            elif my_prec == pa_prec and is_right and parent_op in ('-', '/'):
                need_paren = True

        left_str = self.left.to_string(self.operator, is_right=False)
        right_str = self.right.to_string(self.operator, is_right=True)

        # 显示时 * -> ×, / -> ÷（分数里的 / 已由 fraction_to_string 处理完）
        op_display = {'*': '×', '/': '÷'}.get(self.operator, self.operator)
        s = f"{left_str} {op_display} {right_str}"

        return f"({s})" if need_paren else s

    # ---------- 标准化（用于去重） ----------
    def canonical(self) -> str:
        """
        + 和 * 左右可交换；- 和 / 不可交换。
        注意：不能展开成 n 元加法，只允许交换当前节点的左右子树。
        """
        if self.is_number():
            return f"{self.value.numerator}/{self.value.denominator}"

        left = self.left.canonical()
        right = self.right.canonical()

        if self.operator in ('+', '*'):
            if left > right:
                left, right = right, left

        return f"{self.operator}({left},{right})"