import pygame as pg
import sys
from random import randint, random


#練習１+ main関数内でScreenクラスを使うように変更
class Screen:
    def __init__(self, title, scsize:tuple, bg_fname):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(scsize)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bg_fname)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self, some_sfc, some_rct):
        self.sfc.blit(some_sfc, some_rct)

        
#練習2 + main関数をBirdクラスを使うように変更
class Bird(pg.sprite.Sprite):
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_fname, rate_mag, first_place:tuple):
        pg.sprite.Sprite.__init__(self, self.containers) #
        self.image = pg.image.load(img_fname)
        self.image = pg.transform.rotozoom(self.image, 0, rate_mag)
        self.rect = self.image.get_rect()
        self.rect.center = first_place

    def blit(self, scr):
        scr.blit(self.image, self.rect)

    def update(self, scr):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
                
                if check_bound(self.rect, scr.rct) != (+1, +1):
                    self.rect.centerx -= delta[0]
                    self.rect.centery -= delta[1]
        self.blit(scr) 


#練習3 + main関数でBombクラスを使うように変更
class Bomb(pg.sprite.Sprite):
    def __init__(self, rgb:tuple, hankei, speed:tuple, scr):
        pg.sprite.Sprite.__init__(self, self.containers) #
        self.image = pg.Surface((20, 20))
        pg.draw.circle(self.image, rgb, (10, 10), hankei)
        self.rect = self.image.get_rect()
        self.rect.center = randint(0, scr.rct.width), randint(0, scr.rct.height)
        self.vx, self.vy = speed

    def blit(self, scr):
        scr.blit(self.image, self.rect)

    def update(self, scr):
        if randint(0, 500) == 0:
            self.vx *= 2 
            self.vy *= 2
        yoko, tate = check_bound(self.rect, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.rect.move_ip(self.vx, self.vy) 
        self.blit(scr) 


class Shote(pg.sprite.Sprite):
    def __init__(self, first_place, xy):
        pg.sprite.Sprite(self, self.containers)
        self.image = pg.image.load("ex05/fig/egg_toumei.png")
        self.image = pg.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = first_place
        self.vx, self.vy = xy

    def blit(self, scr):
        scr.blit(self.image, self.rect)   

    def update(self, scr):
        self.rect.move_ip(self.vx, self.vy)
        if not(scr.rect.contains(self.rect)):
            self.kill()
        self.blit(scr)
        
        
def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    scrn = Screen("負けるな！こうかとん", (1600, 900), "ex05/fig/pg_bg.jpg")

    all = pg.sprite.RenderUpdates()
    toris = pg.sprite.Group()
    bombs = pg.sprite.Group()
    egs = pg.sprite.Group()

    Shote.containers = egs, all
    Bird.containers = toris, all
    Bomb.containers = bombs, all
    
    tori = Bird("ex05/fig/6.png", 2.0, (900, 400))

    for _ in range(5):
        bomb = Bomb((255, 0, 0), 10, (+1, +1), scrn) 
        bomb.image.set_colorkey((0, 0, 0)) 
        
    clock = pg.time.Clock() 
    while True:
        scrn.blit(scrn.bgi_sfc, scrn.bgi_rct) # 練習1
        all.update(scrn)   
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                tanni = (x**2+y**2)**0.5
                shot = Shote(tori.rect, (x/tanni+2, y/tanni+2))

        if randint(0, 500) == 0:
            bomb = Bomb((255, 0, 0), 10, (+1, +1), scrn)
            bomb.image.set_colorkey((0, 0, 0))

        
        a = pg.sprite.groupcollide(toris, bombs, False, False)
        if len(a) >= 1:
            return

        pg.display.update() 
        clock.tick(1000)

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()