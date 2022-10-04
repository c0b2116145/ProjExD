import tkinter as tk
from tokenize import cookie_re

root = tk.Tk()
root.geometry("300x500") #練習1
for i in range(10): #練習2
    bt = tk.Button(root, text=f"{9-i}", width=4, height=2, font=("", 30))
    if i < 3:
        bt.grid(row=0, column=i)
    elif 3 <= i < 6:
        bt.grid(row=1, column=i-3)
    elif 6 <= i <9:
        bt.grid(row=2, column=i-6)
    else:
        bt.grid(row=3, column=i-9)

root.mainloop()