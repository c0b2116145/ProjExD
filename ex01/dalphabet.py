from random import randint

def shutudai():
    global ts, ks
    ts = [chr(randint(65, 90))for i in range(10)]
    ks = [ts[randint(0, 9)]for j in range(2)]
    hs = [s for s in ts if s != ks[0] or s != ks[1]]
    print("対象文字")
    print("".join(ts))
    print("表示文字")
    print("".join(hs))

def kaitou(ks):
    global mc
    kk = int(input("欠損文字はいくつあるでしょうか？："))
    if kk == 2:
        print("正解です。それでは、具体的に欠損文字を1つずつ入力してください")
    else:
        print("不正解です。またチャレンジしてください")
    for i in range(1,3):
        k = input(f"{i}つ目の文字を入力してください")
        if k not in ks:
            mc += 1
            print("不正解です。またチャレンジしてください")
            print("="*20)
            break
    else:
        mc = -1
        print("正解です。")

if __name__=="__main__":
    mc = 1
    while mc <= 3:
        shutudai()
        kaitou()
        if mc == -1:
            break