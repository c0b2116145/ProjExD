import pygame as pg
import sys
from random import randint, choice


#練習１+ main関数内でScreenクラスを使うように変更
class Screen:
    def __init__(self, title, scsize:tuple):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(scsize)
        self.rct = self.sfc.get_rect()

    def blit(self, some_sfc, some_rct):
        self.sfc.blit(some_sfc, some_rct)


class Image(pg.sprite.Sprite):
    def __init__(self, bg_fname):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.image.load(bg_fname)
        self.rect = self.image.get_rect()
        self.bg_x = 0

    def blit(self, scr):
        scr.blit(self.image, [self.bg_x-1600, 0])
        scr.blit(self.image, [self.bg_x, 0])

    def update(self, scr):
        self.bg_x = (self.bg_x+3)%480
        self.blit(scr)


        
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
        self.rect.clamp_ip(scr.rct)
        self.blit(scr) 


class Alien(pg.sprite.Sprite):
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.topright = (0, randint(0, 900-self.image.get_height()))
        self.vx, self.vy = choice([1, 2]), choice([1, 2])

    def blit(self, scr):
        scr.blit(self.image, self.rect)

    def update(self, scr):
        #画面の上下に出ないようにする
        if self.rect.centerx>0 and (self.rect.top<0 or self.rect.bottom>900):
            self.vy *= -1
        if randint(0, 500)==0:
            self.vy *= -1
        if not(scr.rct.contains(self.rect)):
            self.kill()
        self.rect.move_ip(self.vx, self.vy)
        self.blit(scr)
        


#練習3 + main関数でBombクラスを使うように変更
class Bomb(pg.sprite.Sprite):
    def __init__(self, rgb:tuple, hankei, alien):
        pg.sprite.Sprite.__init__(self, self.containers) #
        self.image = pg.Surface((20, 20))
        pg.draw.circle(self.image, rgb, (10, 10), hankei)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = alien.rect.center
        self.vx, self.vy = choice([2, 3]), choice([2, 3])

    def blit(self, scr):
        scr.blit(self.image, self.rect)

    def update(self, scr):
        if randint(0, 10000) == 0:
            self.vx *= 2 
            self.vy *= 2
        if (self.rect.top<0 or self.rect.bottom>900):
            self.vy *= -1
        if not(scr.rct.contains(self.rect)):
            self.kill()
        self.rect.move_ip(self.vx, self.vy) 
        self.blit(scr) 


class Shoot(pg.sprite.Sprite):
    def __init__(self, first_place, xy):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.image.load("ex06/fig/egg_toumei.png")
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = first_place
        self.vx, self.vy = xy

    def blit(self, scr):
        scr.blit(self.image, self.rect)   

    def update(self, scr):
        self.rect.move_ip(self.vx, self.vy)
        if not(scr.rct.contains(self.rect)):
            self.kill()
        self.blit(scr)

class LastEnemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.image.load("ex06/fig/last_enemy.png")
        self.image = pg.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 450)
        self.life = 500

    def blit(self, scr):
        scr.blit(self.image, self.rect)

    def update(self, scr):
        if self.rect.centerx < 400 :
            self.rect.move_ip(1, 0)
        self.blit(scr)

def culc_dir_egs(mx, my, tx, ty):
    """
    mx, my:マウスのクリック位置座標
    tx, ty:こうかとんの位置座標
    """
    dx = mx-tx #画面左上の原点からのマウスの座標から、
    dy = my-ty #こうかとん原点からのマウス座標に変換
    tanni = (dx**2+dy**2)**0.5
    return dx/tanni*4, dy/tanni*4



def main():
    scrn = Screen("KOUKATON-Shooting", (1600, 900))

    Alien.images = [pg.image.load(im) for im in ("ex06/fig/alien1.png", "ex06/fig/alien2.png", "ex06/fig/alien3.png")]

    all = pg.sprite.RenderUpdates()
    toris = pg.sprite.Group()
    bombs = pg.sprite.Group()
    egs = pg.sprite.Group()
    aliens = pg.sprite.Group()
    last_enemy = pg.sprite.Group()
    

    Image.containers = all
    Shoot.containers = egs, all
    Bird.containers = toris, all
    Alien.containers = aliens, all
    Bomb.containers = bombs, all
    LastEnemy.containers = last_enemy, all

    pg.time.set_timer(29, 1000)
    pg.time.set_timer(30, 2000)
    pg.time.set_timer(31, 1000)
    
    Image("ex06/fig/pg_bg.jpg")
    tori = Bird("ex06/fig/3.png", 2.0, (900, 400))
    arian = Alien()

    clock = pg.time.Clock() 
    while True:
        #scrn.blit(scrn.bgi_sfc, scrn.bgi_rct) # 練習1
        all.update(scrn)   
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mx,my = pg.mouse.get_pos()
                dir_egs = culc_dir_egs(mx, my, *tori.rect.center)
                shot = Shoot(tori.rect.center, dir_egs)
            if event.type == 29:
                l_enemy = LastEnemy()
            if event.type == 30:
                Alien()
            if event.type == 31:
                for spr in aliens.sprites():
                    Bomb((255, 0, 0), 10, spr)

        #当たり判定
        a_count = pg.sprite.groupcollide(egs, last_enemy, False, False)
        if len(a_count)>0:
            print(a_count)
            for s in a_count:
                print(s)
                s.remove(egs)
                l_enemy.life -= 1
                if l_enemy.life < 0:
                    return

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