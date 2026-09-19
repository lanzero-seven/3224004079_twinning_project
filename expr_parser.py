# expr_parser.py
"""把题目字符串解析成表达式树（递归下降）。"""
from expression import ExpressionNode
from utils import parse_number


class ExpressionParser:
    def __init__(self, text: str):
        # 兼容 × ÷ 和 * /，以及中文括号
        text = text.replace('×', '*').replace('÷', '/')
        text = text.replace('（', '(').replace('）', ')')
        self.text = text
        self.pos = 0

    def _peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else None

    def _skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def parse(self) -> ExpressionNode:
        self._skip_ws()
        node = self._parse_expression()
        self._skip_ws()
        if self.pos != len(self.text):
            raise ValueError(
                f"解析错误：位置 {self.pos} 附近 '{self.text[self.pos:]}'"
            )
        return node

    # expression -> term (('+'|'-') term)*
    def _parse_expression(self) -> ExpressionNode:
        left = self._parse_term()
        while True:
            self._skip_ws()
            c = self._peek()
            if c in ('+', '-'):
                self.pos += 1
                right = self._parse_term()
                left = ExpressionNode(operator=c, left=left, right=right)
            else:
                break
        return left

    # term -> factor (('*'|'/') factor)*
    def _parse_term(self) -> ExpressionNode:
        left = self._parse_factor()
        while True:
            self._skip_ws()
            c = self._peek()
            if c in ('*', '/'):
                self.pos += 1
                right = self._parse_factor()
                left = ExpressionNode(operator=c, left=left, right=right)
            else:
                break
        return left

    # factor -> '(' expression ')' | number
    def _parse_factor(self) -> ExpressionNode:
        self._skip_ws()
        if self._peek() == '(':
            self.pos += 1
            node = self._parse_expression()
            self._skip_ws()
            if self._peek() != ')':
                raise ValueError("缺少右括号")
            self.pos += 1
            return node
        return self._parse_number_node()

    def _parse_number_node(self) -> ExpressionNode:
        """识别 3 / 3/5 / 2'3/8 / -2'3/8。"""
        self._skip_ws()
        start = self.pos

        if self._peek() == '-':
            self.pos += 1

        # 整数部分（可能为空，如 "-1/2" 中 "-" 之后是 "1"）
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1

        # 带分数
        if self._peek() == "'":
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            if self._peek() == '/':
                self.pos += 1
                while self.pos < len(self.text) and self.text[self.pos].isdigit():
                    self.pos += 1
        # 真分数
        elif self._peek() == '/':
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

        token = self.text[start:self.pos]
        if not token or token == '-':
            raise ValueError(f"无法解析数字：位置 {start}")

        return ExpressionNode(value=parse_number(token))