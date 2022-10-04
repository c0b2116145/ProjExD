import tkinter as tk
import tkinter.messagebox as tkm
def button_ref(event):  #練習3
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END, txt) #練習5

def button_eq(a): 
    siki = entry.get()
    num = eval(siki)
    entry.delete(0, tk.END)
    entry.insert(tk.END, num)

root = tk.Tk()
root.geometry("300x500") #練習1
for i in range(10): #練習2
    bt = tk.Button(root, text=f"{9-i}", width=4, height=2, font=("", 30))
    bt.bind("<1>", button_ref)
    if i < 3:
        bt.grid(row=1, column=i)
    elif 3 <= i < 6:
        bt.grid(row=2, column=i-3)
    elif 6 <= i <9:
        bt.grid(row=3, column=i-6)
    else:
        bt.grid(row=4, column=i-9)
bt_p = tk.Button(root, text="+", width=4, height=2, font=("", 30)) #練習6
bt_p.bind("<1>", button_ref)
bt_p.grid(row=4, column=1)

bt_e = tk.Button(root, text="=", width=4, height=2, font=("", 30)) #練習7
bt_e.bind("<1>", button_eq)
bt_e.grid(row=4, column=2)

entry = tk.Entry(justify="right", width=10, font=("", 40)) #練習4
entry.grid(row=0, column=0, columnspan=3)

root.mainloop()