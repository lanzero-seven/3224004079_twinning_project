# gui.py
"""
图形界面入口。
直接运行: python gui.py
使用 tkinter，无需安装第三方库。
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# 复用你已有的模块
from generator import generate_exercises
from utils import (fraction_to_string,
                   save_exercises, save_answers)
from grader import grade


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("小学四则运算题目生成程序")
        self.geometry("640x600")
        self.resizable(False, False)

        self._build_ui()

    # ---------------- UI 构建 ----------------
    def _build_ui(self):
        pad = {'padx': 8, 'pady': 4}

        # ===== 出题模式区域 =====
        gen_frame = ttk.LabelFrame(self, text="出题模式")
        gen_frame.pack(fill="x", padx=10, pady=(10, 5))

        # -n 行
        row1 = ttk.Frame(gen_frame)
        row1.pack(fill="x", **pad)
        ttk.Label(row1, text="题目数量 -n:", width=14, anchor="e").pack(side="left")
        self.entry_n = ttk.Entry(row1, width=20)
        self.entry_n.insert(0, "10")
        self.entry_n.pack(side="left", padx=(4, 0))
        ttk.Label(row1, text="（正整数，如 10）",
                  foreground="gray").pack(side="left", padx=(8, 0))

        # -r 行
        row2 = ttk.Frame(gen_frame)
        row2.pack(fill="x", **pad)
        ttk.Label(row2, text="数值上界 -r:", width=14, anchor="e").pack(side="left")
        self.entry_r = ttk.Entry(row2, width=20)
        self.entry_r.insert(0, "10")
        self.entry_r.pack(side="left", padx=(4, 0))
        ttk.Label(row2, text="（所有数值 < r，r ≥ 1）",
                  foreground="gray").pack(side="left", padx=(8, 0))

        # 生成按钮
        row3 = ttk.Frame(gen_frame)
        row3.pack(fill="x", **pad)
        ttk.Button(row3, text="生成题目",
                   command=self.on_generate).pack(side="left")

        # ===== 批改模式区域 =====
        grd_frame = ttk.LabelFrame(self, text="批改模式")
        grd_frame.pack(fill="x", padx=10, pady=(5, 5))

        # -e 行
        row4 = ttk.Frame(grd_frame)
        row4.pack(fill="x", **pad)
        ttk.Label(row4, text="题目文件 -e:", width=14, anchor="e").pack(side="left")
        self.entry_e = ttk.Entry(row4, width=38)
        self.entry_e.insert(0, "Exercises.txt")
        self.entry_e.pack(side="left", padx=(4, 0))
        ttk.Button(row4, text="浏览",
                   command=lambda: self._pick_file(self.entry_e)
                   ).pack(side="left", padx=(4, 0))

        # -a 行
        row5 = ttk.Frame(grd_frame)
        row5.pack(fill="x", **pad)
        ttk.Label(row5, text="答案文件 -a:", width=14, anchor="e").pack(side="left")
        self.entry_a = ttk.Entry(row5, width=38)
        self.entry_a.insert(0, "Answers.txt")
        self.entry_a.pack(side="left", padx=(4, 0))
        ttk.Button(row5, text="浏览",
                   command=lambda: self._pick_file(self.entry_a)
                   ).pack(side="left", padx=(4, 0))

        # 批改按钮
        row6 = ttk.Frame(grd_frame)
        row6.pack(fill="x", **pad)
        ttk.Button(row6, text="批改",
                   command=self.on_grade).pack(side="left")

        # ===== 输出区 =====
        out_frame = ttk.LabelFrame(self, text="输出")
        out_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.output = scrolledtext.ScrolledText(
            out_frame, wrap="word", height=18,
            font=("Consolas", 10)
        )
        self.output.pack(fill="both", expand=True, padx=4, pady=4)

        self._log("欢迎使用小学四则运算题目生成程序。")
        self._log("提示：出题模式请填 -n 和 -r，点击『生成题目』。")
        self._log("      批改模式请选择 -e 和 -a 文件，点击『批改』。")

    # ---------------- 工具函数 ----------------
    def _log(self, msg: str):
        self.output.insert("end", msg + "\n")
        self.output.see("end")

    def _pick_file(self, entry: ttk.Entry):
        path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)

    # ---------------- 出题 ----------------
    def on_generate(self):
        # 校验 -n
        n_str = self.entry_n.get().strip()
        try:
            n = int(n_str)
        except ValueError:
            messagebox.showerror("参数错误", "-n 必须是正整数")
            return
        if n <= 0:
            messagebox.showerror("参数错误", "-n 必须为正整数")
            return

        # 校验 -r
        r_str = self.entry_r.get().strip()
        try:
            r = int(r_str)
        except ValueError:
            messagebox.showerror("参数错误", "-r 必须是整数")
            return
        if r < 1:
            messagebox.showerror("参数错误", "-r 必须 ≥ 1")
            return

        self._log(f"\n[出题] n={n}, r={r}")
        try:
            exercises = generate_exercises(n, r)
        except RuntimeError as e:
            self._log(f"[失败] {e}")
            messagebox.showerror("生成失败", str(e))
            return

        # 输出到当前工作目录
        try:
            save_exercises(exercises, "Exercises.txt")
            save_answers(exercises, "Answers.txt")
        except Exception as e:
            self._log(f"[保存失败] {e}")
            messagebox.showerror("保存失败", str(e))
            return

        cwd = os.getcwd()
        self._log(f"[成功] 已生成 {len(exercises)} 道题")
        self._log(f"       {os.path.join(cwd, 'Exercises.txt')}")
        self._log(f"       {os.path.join(cwd, 'Answers.txt')}")
        self._log("预览前 5 道：")
        for i, ex in enumerate(exercises[:], start=1):
            self._log(f"  {i}. {ex.expression.to_string()} "
                      f"= {fraction_to_string(ex.answer)}")

        messagebox.showinfo("完成",
                            f"已生成 {len(exercises)} 道题。\n"
                            f"文件已写入：\n{cwd}")

    # ---------------- 批改 ----------------
    def on_grade(self):
        e_path = self.entry_e.get().strip()
        a_path = self.entry_a.get().strip()

        if not e_path or not a_path:
            messagebox.showerror("参数错误", "请选择 -e 和 -a 两个文件")
            return
        if not os.path.exists(e_path):
            messagebox.showerror("文件不存在", f"找不到题目文件：\n{e_path}")
            return
        if not os.path.exists(a_path):
            messagebox.showerror("文件不存在", f"找不到答案文件：\n{a_path}")
            return

        self._log(f"\n[批改] e={e_path}, a={a_path}")
        try:
            grade(e_path, a_path)
        except Exception as e:
            self._log(f"[批改失败] {e}")
            messagebox.showerror("批改失败", str(e))
            return

        # 把 Grade.txt 内容显示到输出区
        cwd = os.getcwd()
        grade_path = os.path.join(cwd, "Grade.txt")
        self._log(f"[成功] 结果已写入 {grade_path}")
        if os.path.exists(grade_path):
            with open(grade_path, encoding="utf-8") as f:
                for line in f:
                    self._log("  " + line.rstrip())
        messagebox.showinfo("完成", "批改完成，结果已写入 Grade.txt")


if __name__ == "__main__":
    app = App()
    app.mainloop()