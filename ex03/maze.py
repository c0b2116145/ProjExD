import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker
import random
import sys




class Enemy:  #敵初期値の設定
    num = 0
    def __init__(self, mx, my):
        Enemy.num += 1
        self.mx = mx
        self.my = my
        self.ecx = 50 + mx*100
        self.ecy = 50 + my*100
        self.tag = str(Enemy.num) + "enemy" 

        
        
def mk_enemy(): #敵を作成
    global ei
    _ = Enemy(13, 7)
    ei.append(_)
    canva.create_image(_.ecx, _.ecy, image=e_koukaton, tag = _.tag)
    root.after(10000, mk_enemy)


def count_up(): #時間を数える関数
    global tmr
    tmr += 1
    label["text"] = tmr 
    root.after(1000, count_up)

def key_down(event): #keyが押された時の反応
    global key
    key = event.keysym
    

def key_up(event): #keyが離れた時の時の反応
    global key, jid
    key = ""


def main_proc(): #リアルタイム処理
    global cx, cy, mx, my, ei, tmr, key

    if key == "Up" and mp[my-1][mx] == 0: #自分のキャラを操作
        my -= 1
    elif key == "Down" and mp[my+1][mx] == 0:    
        my += 1
    elif key == "Left" and mp[my][mx-1] == 0:
        mx -= 1
    elif key == "Right" and mp[my][mx+1] == 0:
        mx += 1
    cx, cy = 50+mx*100, 50+my*100
    canva.coords("koukaton", cx, cy)

    for ene in ei:   #敵のキャラの操作
        direc = random.choice(["Up", "Down", "Left", "Right"])
        if direc == "Up" and mp[ene.my-1][ene.mx] == 0:
            ene.my -= 1
        elif direc == "Down" and mp[ene.my+1][ene.mx] == 0:    
            ene.my += 1
        elif direc == "Left" and mp[ene.my][ene.mx-1] == 0:
            ene.mx -= 1
        elif direc == "Right" and mp[ene.my][ene.mx+1] == 0:
            ene.mx += 1
        ene.ecx, ene.ecy = 50 + ene.mx*100, 50 + ene.my*100
        canva.coords(ene.tag, ene.ecx, ene.ecy)
        
    for ene in ei:  #敵との当たり判定
        if mx == ene.mx and  my==ene.my:
            tkm.showinfo("ゲームオーバー", "敵にぶつかりました。")
            ans = tkm.askyesno("もう一度プレーしますか？")
            if ans == False:
                sys.exit()
            else:
                mx, my = 1, 1
                for ene in ei:
                    canva.delete(ene.tag)
                ei =[]
                tmr = 0
                key = ""
                mk_enemy()

        
    canva.coords("koukaton", cx, cy)

    if mx == 13 and  my==7: #ゴール判定と処理
        tkm.showinfo("ゴール", "ゴールできました！")
        re = tkm.askyesno("もう一度プレーしますか？")
        if re == False:
            sys.exit()
        else:
            mx, my = 1, 1
            for ene in ei:
                canva.delete(ene.tag)
            ei =[]
            tmr = 0
            key = ""
            mk_enemy()
            


    root.after(100, main_proc)

     

if __name__=="__main__":
    mx, my = 1, 1   #グローバル変数の設定
    cx, cy = 50+mx*100, 50+my*100
    key = ""
    mp = maze_maker.make_maze(15, 9)
    tmr = 0
    ei = []
    

    root = tk.Tk()
    label = tk.Label(root, font=("", 80))
    label.pack()


    canva = tk.Canvas(root, width =1500, height=900, bg="black")
    canva.pack()
    koukaton = tk.PhotoImage(file="./ex03/fig/0.png")   #画像の設定
    e_koukaton = tk.PhotoImage(file="./ex03/fig/1.png")
    maze_maker.show_maze(canva, mp)

    canva.create_image(cx, cy, image=koukaton, tag = "koukaton")

    
    root.bind("<KeyPress>", key_down) #関数の呼び出し
    root.bind("<KeyRelease>", key_up)
    mk_enemy()
    root.after(1000, count_up)
    main_proc()
    root.mainloop()
