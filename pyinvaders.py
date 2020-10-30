from pygame import *
import random

# v0.2 from code in LXF 110, did easy part - added score
# v0.3 did medium part - detecting missile collisions
# v0.4 fix missile issue where if you shoot before the current missile is done, your missile resets to next to you
# v0.5 did hard part - added another row of aliens
# v0.6 added score via same code as PyRacer

class Sprite:
    def __init__(self,xpos,ypos,filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((0,0,0))
    def set_position(self,xpos,ypos):
        self.x = xpos
        self.y = ypos
    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))

def Intersect(s1_x,s1_y,s2_x,s2_y):
    """Collision detection code for sprites of size 32x32"""
    if(s1_x>s2_x-32) and (s1_x<s2_x+32) and (s1_y>s2_y-32) and (s1_y<s2_y+32):
        return 1
    else:
        return 0

init()
screen = display.set_mode((640,480))
key.set_repeat(1,1) #rapid keyboard repeat
display.set_caption('PyInvaders')
backdrop = image.load('data/backdrop.bmp')
enemies = []
enemies_row2 = []
x = 0
for count in range(10):
    enemies.append(Sprite(50*x+50,50,'data/baddie.bmp'))
    x += 1
x = 0
for count in range(10):
    enemies_row2.append(Sprite(50*x+50,85,'data/baddie.bmp'))
    x+=1
hero = Sprite(20,400, 'data/hero.bmp')
ourmissile = Sprite(0,480,'data/heromissile.bmp')
enemymissile = Sprite(0,480,'data/baddiemissile.bmp')
enemymissile_row2 = Sprite(0,480,'data/baddiemissile.bmp')

quit = 0
score = 0

scorefont = font.Font(None,60)

enemyspeed = 3
while quit == 0:
    screen.blit(backdrop,(0,0))
    for count in range(len(enemies)):
        enemies[count].x += enemyspeed
        enemies[count].render()

    for count in range(len(enemies_row2)):
        enemies_row2[count].x += enemyspeed
        enemies_row2[count].render()

    if len(enemies) != 0:
        if enemies[len(enemies)-1].x > 590:
            enemyspeed = -3
            for count in range(len(enemies)):
                enemies[count].y += 5

        if enemies[0].x < 10:
            enemyspeed = 3
            for count in range(len(enemies)):
                enemies[count].y += 5

    if len(enemies_row2) != 0:
        if enemies_row2[len(enemies_row2)-1].x > 590:
            enemyspeed = -3
            for count in range(len(enemies_row2)):
                enemies_row2[count].y += 5

        if enemies_row2[0].x < 10:
            enemyspeed = 3
            for count in range(len(enemies_row2)):
                enemies_row2[count].y += 5

    if ourmissile.y < 479 and ourmissile.y > 0:
        ourmissile.render()
        ourmissile.y -= 5

    if enemymissile.y >= 480 and len(enemies) > 0:
        enemymissile.x = enemies[random.randint(0,len(enemies)-1)].x
        enemymissile.y = enemies[0].y

    if enemymissile_row2.y >= 480 and len(enemies_row2) > 0:
        enemymissile_row2.x = enemies_row2[random.randint(0,len(enemies_row2)-1)].x
        enemymissile_row2.y = enemies_row2[0].y

    if Intersect(hero.x,hero.y,enemymissile.x,enemymissile.y):
        quit = 1 #you were hit by the baddie missile

    if Intersect(hero.x,hero.y,enemymissile_row2.x,enemymissile_row2.y):
        quit = 1 #you were hit by the baddie missile

    if Intersect(ourmissile.x,ourmissile.y,enemymissile.x,enemymissile.y):
        (ourmissile.x,ourmissile.y) = (0,480)
        (enemymissile.x, enemymissile.y) = (0,480)

    if Intersect(ourmissile.x,ourmissile.y,enemymissile_row2.x,enemymissile_row2.y):
        (ourmissile.x,ourmissile.y) = (0,480)
        (enemymissile_row2.x, enemymissile_row2.y) = (0,480)

    for count in range(0,len(enemies)):
        if Intersect(ourmissile.x, ourmissile.y, enemies[count].x, enemies[count].y):
            del enemies[count]
            score += 50
            (ourmissile.x,ourmissile.y) = (0,480)
            break

    for count in range(0,len(enemies_row2)):
        if Intersect(ourmissile.x, ourmissile.y, enemies_row2[count].x, enemies_row2[count].y):
            del enemies_row2[count]
            score += 50
            (ourmissile.x,ourmissile.y) = (0,480)
            break

    if len(enemies) == 0 and len(enemies_row2) == 0:
            quit = 1

    scoretext = scorefont.render('Score:' + str(score),True, (255,255,255),(0,0,0))
    screen.blit(scoretext,(5,5))
    
    for ourevent in event.get():
        if ourevent.type == QUIT:
            quit = 1 #if someone closes out via the X in the titlebar 
        if ourevent.type == KEYDOWN:
            if ourevent.key == K_RIGHT and hero.x < 590:
                hero.x += 5
            if ourevent.key == K_LEFT and hero.x > 10:
                hero.x -= 5
            if ourevent.key == K_SPACE:
                if (ourmissile.x,ourmissile.y) == (0,480) or ourmissile.y <=0:
                    (ourmissile.x,ourmissile.y) = (hero.x, hero.y)

    enemymissile.render()
    enemymissile_row2.render()
    enemymissile.y += 5
    enemymissile_row2.y += 5
    hero.render()
    display.update()
    time.delay(5)

print ("You Scored", score)
