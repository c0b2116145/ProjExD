from random import randint

def shutudai():
    q = ["サザエの旦那の名前は？", "カツオの妹の名前は？", "タラオはカツオから見てどんな関係？"]
    n = randint(0, 2)
    print(q[n])
    return n

def kaito(i):
    k = input("答えるんだ：")
    m = [["ますお", "マスオ", "マスオさん", "ますおさん"], ["わかめ", "ワカメ", "ワカメちゃん", "わかめちゃん"], ["甥", "おい", "甥っ子", "おいっこ"]]
    if k in m[i]:
        print("正解！！！")
    else:
        print("出直してこい")
        
if __name__ == "__main__":
    n = shutudai()
    kaito(n)