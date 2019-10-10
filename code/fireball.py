import sys
import pygame
from random import *
import time
import sql_fireball

def minmax(val, minval, maxval):
    return min(max(val, minval), maxval)


class Constants:
    BLACK = 0, 0, 0
    RED=255,0,0
    WHITE = 255, 255, 255
    GREEN=0,255,100
    BLUE=0,100,255
    ORANGE=255,255,0
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

class Fireball:
    def __init__(self,speed):
        self.speed=speed
        self.vx = randint(-8, 8)
        self.vy = randint(-8, 8)
        self.x = randint(0, 600)
        self.y = randint(0, 600)
        self.fireimg = pygame.image.load("fireball.png")

    def update(self):
        self.x = minmax(self.x + self.vx*self.speed, 0, Constants.SCREEN_WIDTH - self.fireimg.get_width())
        self.y = minmax(self.y + self.vy*self.speed, 20, Constants.SCREEN_HEIGHT - self.fireimg.get_height())
        if self.x == 0 or self.x == Constants.SCREEN_WIDTH - self.fireimg.get_width():
            self.vx *= -1
        if self.y == 20 or self.y == Constants.SCREEN_HEIGHT - self.fireimg.get_height():
            self.vy *= -1

class Game:
    def __init__(self):
        pygame.init()
        self.fireballspeed=1
        self.colorscreen=Constants.WHITE
        self.provgold=True
        self.worktotalloop=True
        self.totalgold=0
        self.gx=100
        self.gy=100
        self.heartx=200
        self.hearty=200
        self.justrand=0
        self.countlife=3
        self.width=Constants.SCREEN_WIDTH
        self.height = Constants.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption("Fireball")
        self.men = pygame.image.load("water.png")
        self.space=pygame.image.load("space.png")
        self.gold=pygame.image.load("gold.png")
        self.heart=pygame.image.load("heart.png")
        pygame.key.set_repeat(10, 10)
        self.clk = pygame.time.Clock()
        self.loop = True
        self.x=0
        self.y = 0
        self.imgx=0
        self.imgy = 0
        self.timer = 0
        self.kolfireball=2
        self.check_sound=0
        self.level=1
        self.ball_list = []
        for x in range(self.kolfireball):
            self.ball_list.append(Fireball(self.fireballspeed))  # list of on-screen fireballs
    def message_display(self, text,number,sizex,sizey):
        txt = pygame.font.Font('srift.ttf', number)
        s = txt.render(text, True, Constants.RED)
        sr = s.get_rect(center = (sizex, sizey))
        self.screen.blit(s, sr)
    def fire_speed(self):
        if self.totalgold>=10 and self.totalgold<20:
            self.fireballspeed=1.5
        if self.totalgold>=20 and self.totalgold<30:
            self.firebalspeed=2
        if self.totalgold>=30 and self.totalgold<40:
            self.firebalspeed=3
        if self.totalgold>=40:
            self.firebalspeed=4
    def the_end(self):
        txt = pygame.font.Font('srift.ttf', 60)
        s = txt.render(str("GAME OVER"), True, Constants.RED)
        sr = s.get_rect(center=(300, 300))
        self.screen.fill(Constants.BLACK)
        self.screen.blit(s, sr)
        time.sleep(2)

    def the_win(self):
        txt = pygame.font.Font('srift.ttf', 120)
        s = txt.render(str("WIN!!!"), True, Constants.WHITE)
        sr = s.get_rect(center=(300, 300))
        self.screen.fill(Constants.RED)
        self.screen.blit(s, sr)
        time.sleep(2)

    def newscreencolor(self):
        if self.totalgold>=10 and self.totalgold<20:
              if self.check_sound==0:
                  Sound.new_level(self)
                  self.check_sound+=1
                  self.level+=1
              self.colorscreen=Constants.BLUE
        if self.totalgold >= 20 and self.totalgold < 30:
            if self.check_sound == 1:
                Sound.new_level(self)
                self.check_sound += 1
                self.level += 1
            self.colorscreen = Constants.GREEN
        if self.totalgold >= 30 and self.totalgold < 40:
            if self.check_sound == 2:
                Sound.new_level(self)
                self.check_sound += 1
                self.level += 1
            self.colorscreen = Constants.ORANGE
        if self.totalgold >= 40 :
            if self.check_sound == 3:
                Sound.new_level(self)
                self.check_sound += 1
                self.level += 1
            self.colorscreen = Constants.BLACK
    def run(self):
        while self.loop:
            self._loop()
        sql_fireball.record()
    def record_level(self,line):
        file = open(r'D:\Python(Pycharm)\untitled\Fireball\record_level.txt', 'w')
        file.write(line)
        file.close()
    def _loop(self):
        for event in pygame.event.get():
            self.timer += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.x = -10
                elif event.key == pygame.K_w:
                    self.y = -10
                elif event.key == pygame.K_d:
                    self.x = 10
                elif event.key == pygame.K_s:
                    self.y = 10
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,pygame.K_SPACE]:
                    self.x = 0
                    self.y = 0
                if event.key == pygame.K_q:
                     sys.exit()

        self.imgx = minmax(self.imgx + self.x, 0, self.width - self.men.get_width())
        self.imgy = minmax(self.imgy + self.y, 20, self.height - self.men.get_height())
        self.newscreencolor()
        self.screen.fill(self.colorscreen)
        self.screen.blit(self.men, (self.imgx, self.imgy))

        for i in self.ball_list:
            i.update()
            self.screen.blit(i.fireimg, (i.x, i.y))
            for j in range(self.imgx-40,self.imgx+self.men.get_width()):
                for l in range (self.imgy-40,self.imgy+self.men.get_height()):
                    if i.x==j and i.y==l:
                        self.imgx=randint(0,600)
                        self.imgy=randint(0,600)
                        Sound.crash(self)
                        self.countlife -= 1

        self.message_display(str("LIFE: "),22,200,10)
        self.message_display(str(self.countlife),22,232,10)

        self.message_display(str("LEVEL: "), 22, 475, 10)
        self.message_display(str(self.level), 22, 510, 10)

        self.screen.blit(self.gold, (self.gx, self.gy))
        for j in range(self.imgx - 30, self.imgx + self.men.get_width()):
           for l in range(self.imgy - 30, self.imgy + self.men.get_height()):
              if self.gx == j and self.gy == l:
                  self.gx=randint(0,600-self.gold.get_width())
                  self.gy=randint(20,600-self.gold.get_height())
                  self.totalgold +=1
                  Sound.move(self)

        self.fire_speed()

        if self.totalgold % 10 == 0 and self.worktotalloop == True:
            self.ball_list.append(Fireball(self.fireballspeed))
            self.worktotalloop = False
        if self.totalgold % 10 != 0:
            self.worktotalloop = True

        self.message_display(str("TOTAL:"), 22, 326, 10)
        self.message_display(str(self.totalgold), 22, 376, 10)

        self.justrand=randint(0,30)
        if self.justrand==30 and self.countlife<5:
            self.screen.blit(self.heart, (self.heartx, self.hearty))
            for j in range(self.imgx - 40, self.imgx + self.men.get_width()):
               for l in range(self.imgy - 40, self.imgy + self.men.get_height()):
                 if self.heartx == j and self.hearty == l:
                    self.heartx = randint(0, 600 - self.heart.get_width())
                    self.hearty = randint(20, 600 - self.heart.get_height())
                    self.countlife+=1
        self.record_level(str(self.totalgold))
        if self.countlife == 0:
            Sound.game_over(self)
            self.the_end()
            self.loop = False
        if self.totalgold==50:
            self.the_win()
            Sound.win(self)
            self.loop = False
        pygame.display.update()
        self.clk.tick(100)
class Sound:
    def game_over(self):
        pygame.mixer.music.load("game_over.mp3")
        pygame.mixer.music.play()

    def move(self):
        pygame.mixer.music.load("sss.mp3")
        pygame.mixer.music.play()

    def crash(self):
        pygame.mixer.music.load("crash.mp3")
        pygame.mixer.music.play()

    def win(self):
        pygame.mixer.music.load("win.mp3")
        pygame.mixer.music.play()

    def new_level(self):
        pygame.mixer.music.load("new_level.mp3")
        pygame.mixer.music.play()

class SplashScreen:

    def __init__(self):
        pygame.init()
        self.width = Constants.SCREEN_WIDTH
        self.height=Constants.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode([self.width,self.height])
        pygame.display.set_caption("Fireball")
        self.draw_text("Fireball", 48, Constants.ORANGE, self.width / 2, self.height / 4)
        self.draw_text("Press the arrow keys to move around.", 22, Constants.WHITE,
                       self.width / 2, self.height / 2.5)
        self.draw_text('Press P to play or Q to quit', 22, Constants.WHITE,
                       self.width/2, self.height / 2)
        self.clk = pygame.time.Clock()
        self.play_game = False
        pygame.display.flip()
        self.wait_for_key()
        self.input_name()


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font('srift.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clk.tick()
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                pygame.display.update()
                if event.type == pygame.KEYUP and event.key == pygame.K_q or event.type == pygame.QUIT:
                    waiting = False
                    self.play_game = False
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_p:
                    waiting = False
                    self.play_game = True
    def letter(self,let,size,word):
        self.draw_text(let, 28, Constants.RED, self.width / 2 + size-30, self.height / 1.5)
        self.word+=let
        pygame.display.update()

    def record_in_file(self, word):
        file = open(r'D:\Python(Pycharm)\untitled\Fireball\record_in_file.txt','r')
        list_for_data=[]
        for line in file:
            if line=='\n':
                continue
            list_for_data.append(line)
        file.close()
        list_for_data.append(word)
        file = open(r'D:\Python(Pycharm)\untitled\Fireball\record_in_file.txt', 'w')
        for line in list_for_data:
           file.write(line+'\n')
        file.close()
    def input_name(self):
        val=0

        self.word=''
        self.size=0
        self.clk.tick()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.draw_text('Input you name:',28,Constants.RED,self.width / 4-20, self.height / 1.5)
        self.draw_text('Press ESCAPE to continue...', 28, Constants.WHITE, self.width /2, self.height / 1.2)
        self.draw_text('TOP-5 players:', 28, Constants.WHITE, self.width / 2, self.height / 7)
        self.draw_text('1.', 28, Constants.WHITE, self.width / 7, self.height / 5)
        self.draw_text('2.', 28, Constants.WHITE, self.width / 7, self.height /5+40)
        self.draw_text('3.', 28, Constants.WHITE, self.width / 7, self.height /5+80)
        self.draw_text('4.', 28, Constants.WHITE, self.width / 7, self.height / 5+120)
        self.draw_text('5.', 28, Constants.WHITE, self.width / 7, self.height / 5+160)
        #i add list total
        self.draw_text(str(sql_fireball.record_2()[0][0]), 28, Constants.WHITE, self.width / 7+400,
                       self.height / 5)
        self.draw_text( str(sql_fireball.record_2()[1][0]), 28, Constants.WHITE, self.width / 7+400,
                       self.height / 5 + 40)
        self.draw_text(str(sql_fireball.record_2()[2][0]), 28, Constants.WHITE, self.width / 7+400,
                       self.height / 5 + 80)
        self.draw_text(str(sql_fireball.record_2()[3][0]), 28, Constants.WHITE, self.width / 7+400,
                       self.height / 5 + 120)
        self.draw_text(str(sql_fireball.record_2()[4][0]), 28, Constants.WHITE, self.width / 7+400,
                       self.height / 5 + 160)
        #i add list name
        self.draw_text(str(sql_fireball.record_2()[0][1]), 28, Constants.WHITE, self.width / 7 + 100,
                       self.height / 5)
        self.draw_text(str(sql_fireball.record_2()[1][1]), 28, Constants.WHITE, self.width / 7 + 100,
                       self.height / 5 + 40)
        self.draw_text(str(sql_fireball.record_2()[2][1]), 28, Constants.WHITE, self.width / 7 + 100,
                       self.height / 5 + 80)
        self.draw_text(str(sql_fireball.record_2()[3][1]), 28, Constants.WHITE, self.width / 7 + 100,
                       self.height / 5 + 120)
        self.draw_text(str(sql_fireball.record_2()[4][1]), 28, Constants.WHITE, self.width / 7 + 100,
                       self.height / 5 + 160)


        pygame.display.update()
        self.check=True
        while (val<10 and self.check==True):
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.check = False
                    break
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    self.letter('A',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_b:
                    self.letter('B',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_c:
                        self.letter('C', self.size,self.word)
                        val += 1
                        self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_d:
                    self.letter('D',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    self.letter('E',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_f:
                    self.letter('F',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_q:
                    self.letter('Q',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_g:
                    self.letter('G',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_h:
                    self.letter('H',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_i:
                    self.letter('I',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_j:
                    self.letter('J',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_k:
                    self.letter('K',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_l:
                    self.letter('L',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_m:
                    self.letter('M',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_n:
                    self.letter('N',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_o:
                    self.letter('O',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_p:
                    self.letter('P',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_r:
                    self.letter('R',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    self.letter('S',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_t:
                        self.letter('T', self.size,self.word)
                        val += 1
                        self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_u:
                    self.letter('U',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_v:
                    self.letter('V',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_w:
                    self.letter('W',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_x:
                    self.letter('X',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_y:
                    self.letter('Y',self.size,self.word)
                    val+=1
                    self.size += 20
                if event.type == pygame.KEYUP and event.key == pygame.K_z:
                    self.letter('Z',self.size,self.word)
                    val+=1
                    self.size += 20
        self.record_in_file(self.word)
while(True):
    time.sleep(2)
    splash = SplashScreen()
    if splash.play_game:
        game = Game()
        game.run()


