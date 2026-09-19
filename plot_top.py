# plot_top.py
"""从 profile.prof 里提取 Top N 函数耗时，画横向柱状图。"""
import pstats
import matplotlib.pyplot as plt

stats = pstats.Stats("profile.prof")
stats.sort_stats("tottime")

# 提取前 15 个函数的 tottime
items = []
for func, (cc, nc, tt, ct, callers) in stats.stats.items():
    filename, lineno, name = func
    items.append((name, tt))

items.sort(key=lambda x: x[1], reverse=True)
top = items[:15]

names = [x[0] for x in top][::-1]
times = [x[1] for x in top][::-1]

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]  # 中文
plt.rcParams["axes.unicode_minus"] = False

plt.figure(figsize=(10, 6))
plt.barh(names, times, color="steelblue")
plt.xlabel("自身耗时 tottime (秒)")
plt.title("函数耗时 Top 15")
plt.tight_layout()
plt.savefig("top_functions.png", dpi=150)
print("已生成 top_functions.png")