import pygame as pg
import random
import sys

#複数の爆弾の初期値を設定するクラス
class Bom:
    def __init__(self):
        self.bx, self.by = (random.randint(20, 1600-20), 
                            random.randint(20, 900-20))
        self.bvx, self.bvy = random.choice([-2,- 1, 1, 2]), random.choice([-2,- 1, 1, 2])
        self.bom = pg.Surface((40, 40))
        self.bom_rec = self.bom.get_rect()
    #Bomクラスのインスタンス同士で「!=」で比較したとき、どのインスタンス変数を比較するかの設定
    def __nq__(self, other):
        return self.bom_rec != other.bom_rec
#爆弾を作る
def bom_maker():
    global boms
    bom_ = Bom()
    radius = random.randint(5, 15)
    pg.draw.circle(bom_.bom, (255, 0, 0), (20, 20), radius)
    bom_.bom.set_colorkey((0, 0, 0))   
    bom_.bom_rec.center = bom_.bx, bom_.by
    boms.append(bom_)

#テキストを表示する関数
def text(txm, x, y, rgb):
    font = pg.font.Font(None, 100)
    txt = font.render(str(txm), True, (255, 255, 255), rgb)
    txt_rec = txt.get_rect()
    txt_rec.center = x, y
    scrn_sfc.blit(txt, txt_rec)



def main():
    global scrn_sfc, koukaton_rec
    pg.display.set_caption("逃げろ！こうかとん") #ゲームのタイトル設定
    scrn_sfc = pg.display.set_mode((1600, 900)) #画面用のsurface

    #こうかとん生成
    koukaton = pg.image.load("ex04/fig/6.png") #こうかとんのロード
    koukaton = pg.transform.rotozoom(koukaton, 0, 2.0) #こうかとんの拡大
    koukaton_rec = koukaton.get_rect()
    koukaton_rec.center = 800, 450

    #爆弾生成
    bom_maker()

    #スタート画面の表示と処理
    bg = pg.image.load("ex04/fig/pg_bg.jpg") #背景画像のロード
    scrn_sfc.blit(bg, (0, 0))
    text("START", 800, 450, (0, 0, 0))
    text("Please push \"space\"", 800, 550, (0, 0, 0))
    pg.display.update()
    flag = True
    while flag:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: #スペースボタンを押してスタート
                flag = False
            elif event.type == pg.QUIT: #×ボタンを押したときmain関数を抜けて終了
                return
                

    #一定時間でeventを発生させる
    pg.time.set_timer(30, 2000) #爆弾生成
    pg.time.set_timer(31, 1000) #タイマーとクリアの処理

    #爆発画面の生成
    explosion = pg.image.load("ex04/fig/bakuhatu_r.png")
    explosion_rec = explosion.get_rect()

    limit_time = 30 #制限時間の設定

    #メインのループ
    while True:
        cvx, cvy = 0, 0
        scrn_sfc.blit(bg, (0, 0))
        scrn_sfc.blit(koukaton, koukaton_rec)

        #残り時間の表示
        text(limit_time, 50, 50, (0, 0, 0))

        #爆弾の表示、移動、こうかとんとの当たり判定
        for bom in boms:
            scrn_sfc.blit(bom.bom, bom.bom_rec) #表示

            if bom.bom_rec.top-1<0:        #壁との跳ね返り
                bom.bvy *= -1
                bom.bvy += 1
            elif bom.bom_rec.bottom+1>900:
                bom.bvy *= -1
                bom.bvy -= 1
            elif bom.bom_rec.left-1<0:
                bom.bvx *= -1
                bom.bvx += 1
            elif bom.bom_rec.right+1>1600:
                bom.bvx *= -1
                bom.bvx -= 1
            bom.bom_rec.move_ip(bom.bvx, bom.bvy)
            #こうかとんと爆弾の当たり判定
            if koukaton_rec.colliderect(bom.bom_rec): #こうかとんと爆弾の当たり判定
                explosion_rec.center = ((bom.bom_rec.centerx+koukaton_rec.centerx)/2, 
                                        (bom.bom_rec.centery+koukaton_rec.centery)/2) #爆発画像の位置設定
                scrn_sfc.blit(explosion, explosion_rec) #爆発画像を表示
                text("GAME OVER", 800, 450, (255, 0, 0)) #game overのテキストを表示
                pg.display.update()
                pg.time.wait(2000) #2秒表示する
                return

        #爆弾と爆弾の当たり判定
        for bom_1 in boms:    
            for bom_2 in boms:
                if bom_1 != bom_2 and bom_1.bom_rec.colliderect(bom_2.bom_rec): #2つの爆弾が当たると
                    explosion_rec.center = ((bom_1.bom_rec.centerx+bom_2.bom_rec.centerx)/2, 
                                            (bom_1.bom_rec.centery+bom_2.bom_rec.centery)/2)
                    scrn_sfc.blit(explosion, explosion_rec) #爆発画像を表示して
                    boms.remove(bom_1) #当たった爆弾を消す
                    boms.remove(bom_2)
                    pg.display.update()
                    clock2 = pg.time.Clock() #爆発画像を表示する時間を稼ぐ
                    clock2.tick(10)
                    break

        pg.display.update()
        
        #ボタン操作
        key_lit = pg.key.get_pressed()
        if key_lit[pg.K_UP] and koukaton_rec.top-1>=0:
            cvy = -1
        elif key_lit[pg.K_DOWN] and koukaton_rec.bottom+1<=900:
            cvy = 1
        elif key_lit[pg.K_LEFT] and koukaton_rec.left-1>=0:
            cvx = -1
        elif key_lit[pg.K_RIGHT] and koukaton_rec.right+1<=1600:
            cvx = 1
        koukaton_rec.move_ip(cvx, cvy) #ここで動かしている


        for event in pg.event.get():
            if event.type == pg.QUIT: #×ボタンを押したときの処理
                return
            elif event.type == 30: #一定時間経つと爆弾が生成する
                bom_maker()
            elif event.type == 31: #タイマーの設定とクリアしたときの処理
                limit_time -= 1
                if limit_time == 0:
                    text(limit_time, 50, 50, (0, 0, 0))
                    text("CLEAR", 800, 450, (0, 0, 255))
                    pg.display.update()
                    pg.time.wait(2000)
                    return
        
        clock = pg.time.Clock()
        clock.tick(1000)
        



if __name__ == "__main__":
    boms = []
    pg.init() #初期化
    main()
    pg.quit()
    sys.exit() #プログラム終了