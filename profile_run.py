# profile_run.py
"""
性能分析专用入口。
运行: python profile_run.py
输出: profile.prof
"""
import cProfile
import pstats
import io
import time

from generator import generate_exercises
from utils import save_exercises, save_answers


def workload(n=10000, r=100):
    """一次完整出题流程。"""
    exercises = generate_exercises(n, r)
    save_exercises(exercises, "Exercises.txt")
    save_answers(exercises, "Answers.txt")
    return exercises


def main():
    # 1. 端到端计时（跑 3 次取平均）
    times = []
    for i in range(3):
        t0 = time.perf_counter()
        workload(10000, 100)
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f"第 {i+1} 次: {dt:.3f} s")
    print(f"平均: {sum(times)/len(times):.3f} s")

    # 2. cProfile 采样
    profiler = cProfile.Profile()
    profiler.enable()
    workload(10000, 100)
    profiler.disable()
    profiler.dump_stats("profile.prof")

    # 3. 打印文本版 Top 20
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())


if __name__ == "__main__":
    main()