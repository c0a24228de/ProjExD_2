import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = { #移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0), #最後のコロンは付ける無くてもいいが、付けたほうが推奨されてる
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]: #初期値:画面の中
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True #初期値：画面内
    
    if rct.left < 0 or WIDTH < rct.right: #横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦方向の画面外判定
        tate = False

    return yoko, tate #横方向、縦方向の画面内判定結果を返す

def gameover(screen: pg.Surface) -> None:
    """
    引数：black_surface
    """
    black_surface = pg.Surface((WIDTH, HEIGHT))
    black_surface.set_alpha(128)
    black_surface.fill((0, 0, 0))
    fonto = pg.font.Font(None, 130)
    txt = fonto.render("Game Over",
                       True, (255, 255, 255))
    screen.blit(black_surface, [0, 0])
    screen.blit(txt, [300, 300])
    img8 = pg.image.load("fig/8.png")
    screen.blit(img8, (230, 310))
    screen.blit(img8, (820, 310))
    pg.display.update()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のsurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0),(10, 10), 10) #赤い円を描く
    bb_img.set_colorkey((0, 0, 0)) #黒を透明色に設定
    bb_rct = bb_img.get_rect() #爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH) #横座標用乱数
    bb_rct.centery = random.randint(0, HEIGHT) #縦座標用乱数
    vx, vy = +5, +5 #爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # if bb_img.colliderect(kk_rct):
        #     gameover(screen)
        if kk_rct.colliderect(bb_rct): #こうかとんRextと爆弾Rectの衝突判定
            print("ゲームオーバー")
            gameover(screen)
            time.sleep(5)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] #合計移動量
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
