import tkinter as tk
import tkinter.messagebox as tkm
import math
def button_ref(event):  #練習3
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END, txt) #練習5

def button_eq(a): 
    siki = entry.get()
    num = eval(siki)
    entry.delete(0, tk.END)
    entry.insert(tk.END, num)

def button_del(d):
    entry.delete(0, tk.END)

def button_in(i):
    siki = entry.get()
    suu = eval(siki)
    factor = {}
    div = 2
    s = math.sqrt(suu)
    while div < s:
        div_cnt = 0
        while suu % div == 0:
            div_cnt += 1
            suu //= div
        if div_cnt != 0:
            factor[div] = div_cnt
        div += 1
    if suu > 1:
        factor[suu] = 1
        
    entry.delete(0, tk.END)
    for s, k in factor.items():
        num = f"{s}:{k}個"
        entry.insert(tk.END, num)

root = tk.Tk()
root.geometry("300x500") #練習1
for i in range(10): #練習2
    bt = tk.Button(root, text=f"{9-i}", width=4, height=1, font=("", 30))
    bt.bind("<1>", button_ref)
    if i < 3:
        bt.grid(row=1, column=i)
    elif 3 <= i < 6:
        bt.grid(row=2, column=i-3)
    elif 6 <= i <9:
        bt.grid(row=3, column=i-6)
    else:
        bt.grid(row=4, column=i-9)
n = ["+", "-", "/", "*", "=", "CA", "因"]
r = 4
for i, n in enumerate(n, 1):
    bt_p = tk.Button(root, text=n, width=4, height=1, font=("", 30)) #練習6
    i = i % 3
    if  i==0:
        r += 1
    if n=="=":
        bt_p.bind("<1>", button_eq)
        bt_p.grid(row=r, column=i)
    elif n=="CA":
        bt_p.bind("<1>", button_del)
        bt_p.grid(row=r, column=i)
    elif n=="因":
        bt_p.bind("<1>", button_in)
        bt_p.grid(row=r, column=i)
    else:
        bt_p.bind("<1>", button_ref)
        bt_p.grid(row=r, column=i)    

entry = tk.Entry(justify="right", width=10, font=("", 40)) #練習4
entry.grid(row=0, column=0, columnspan=3)

root.mainloop()