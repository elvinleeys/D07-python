import random
import tkinter as tk
from datetime import datetime

# 번호대별 공 색상 (동행복권 기준)
def ball_color(n):
    if n <= 10: return "#fbc400"
    if n <= 20: return "#69c8f2"
    if n <= 30: return "#ff7272"
    if n <= 40: return "#aaaaaa"
    return "#b0d840"

def draw():
    for w in frame.winfo_children():
        w.destroy()
    date_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for _ in range(5):
        row = tk.Frame(frame)
        row.pack(pady=4)
        for n in sorted(random.sample(range(1, 46), 6)):
            tk.Label(row, text=n, width=3, font=("맑은 고딕", 14, "bold"),
                     bg=ball_color(n), fg="white").pack(side="left", padx=3)

root = tk.Tk()
root.title("로또 번호 생성기")
date_label = tk.Label(root, text="", font=("맑은 고딕", 11))
date_label.pack(pady=(10, 0))
tk.Button(root, text="번호 생성", font=("맑은 고딕", 12), command=draw).pack(pady=10)
frame = tk.Frame(root)
frame.pack(padx=20, pady=(0, 15))
draw()
root.mainloop()
