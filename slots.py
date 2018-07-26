import pygame,os
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)
LIGHTBLUE = (0, 255, 255)
GREEN = (0, 204, 0)
YELLOW = (255, 255, 0)
DARKER_YELLOW=(255,150,0)
GRAY=(200,200,200)

FRAMERATE=480
SCREENWIDTH=600
SCREENHEIGHT=500
def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)

def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    #image = image.convert()        #For faster screen updating
    image = image.convert_alpha()   #Not as fast as .convert(), but works with transparent backgrounds
    return image, image.get_rect()

def draw_text(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Game():

    def __init__(self,emotes):
        pygame.mixer.music.load('musictrack.mp3')
        pygame.mixer.music.play(1,0.0)
        pygame.mixer.music.set_endevent(QUIT)
        self.num=len(emotes)
        self.current=[0,0,0]
        self.timelist=[240,480,720,960,1200,1440,1680,1920]
        self.slot,self.slotrect=load_image('Slot Machine.png')
        self.counter=[3*FRAMERATE,3*FRAMERATE,3*FRAMERATE]
        self.lever=0
        self.second=False
        self.text="It's Raffle Time!"
        self.text2="A WINNER IS YOU!!"
        self.color=True
        self.textfont=pygame.font.SysFont('Courier New',22)
        self.textcolor=GREEN
        self.textposx=195
        self.slotrect=(0,0)
        self.wheelspeed=[1,2,4]
        self.y=[0,0,0]
        self.spincount=[0,0,0]
        self.spin=[0,0,0]
        self.top=['','','']
        self.mid=['','','']
        self.bot=['','','']
        self.toprect=['','','']
        self.midrect=['','','']
        self.botrect=['','','']
        for i in range(0,3):
            self.top[i],self.toprect[i]=load_image(emotes[(self.current[i]+1)%self.num])
            self.mid[i],self.midrect[i]=load_image(emotes[self.current[i]])
            self.bot[i],self.botrect[i]=load_image(emotes[(self.current[i]-1)%self.num])
            self.toprect[i].topleft=(32+212*i,self.y[i])
            self.midrect[i].topleft=(32+212*i,self.y[i]+112)
            self.botrect[i].topleft=(32+212*i,self.y[i]+224)
                
    def process_events(self,screen):
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYUP:
                if event.key==K_ESCAPE:
                    terminate()
    def run_logic(self,screen,emotes):
        for i in range(0,3):
            if self.spin[i]:
                if self.y[i]>28:
                    self.y[i]-=(112-self.wheelspeed[i])
                    self.current[i]+=1
                    self.top[i],self.toprect[i]=load_image(emotes[(self.current[i]+1)%self.num])
                    self.mid[i],self.midrect[i]=load_image(emotes[self.current[i]%self.num])
                    self.bot[i],self.botrect[i]=load_image(emotes[(self.current[i]-1)%self.num])
                else:
                    self.y[i]+=self.wheelspeed[i]
                if (self.current[i]%self.num)==0:
                    if self.y[i]==0:
                        self.spincount[i]=self.current[i]/self.num
                if ((self.spincount[i]-i*i)*1.0/self.wheelspeed[i])==3.0:
                    self.spin[i]=False
                    self.current[i]=0
                    self.spincount[i]=0
                    self.counter[i]=4*FRAMERATE
            self.toprect[i].topleft=(50+194*i,self.y[i]+82)
            self.midrect[i].topleft=(50+194*i,self.y[i]+194)
            self.botrect[i].topleft=(50+194*i,self.y[i]+306)
            if self.counter[i]>0:
                if not self.spin[2]:
                    if self.counter[2]>3*FRAMERATE:
                        self.text=self.text2
                    self.counter[i]-=1  
            else:
                self.spin[i]=True
                self.color=False
            if self.color:
                self.textcolor=GREEN
            else:
                self.textcolor=BLACK
        if self.counter[2]<652 and self.counter[2]>0:
            if self.counter[2]>326:
                self.lever+=1
            else:
                self.lever-=1
        if not self.spin[2]:
            if self.counter[2]>3*FRAMERATE:
                self.second=True
        if self.second:
            if self.counter[2]==240 or self.counter[2]==480 or self.counter[2]==720 or self.counter[2]==960 or self.counter[2]==1200 or self.counter[2]==1440 or self.counter[2]==1680 or self.counter[2]==1920:
                self.color = not self.color
                    
    def display_frame(self,screen,emotes):
        screen.fill(WHITE)
        for i in range(0,3):
            screen.blit(self.top[i],self.toprect[i])
            screen.blit(self.mid[i],self.midrect[i])
            screen.blit(self.bot[i],self.botrect[i])
            pygame.draw.rect(screen,BLACK,[50+194*i,self.y[i]+82+110,112,4])
            pygame.draw.rect(screen,BLACK,[50+194*i,self.y[i]+82+222,112,4])
        screen.blit(self.slot,self.slotrect)
        pygame.draw.line(screen,GRAY,[575,250],[575,self.lever+87],5)
        pygame.draw.circle(screen,DARKER_YELLOW,[575,self.lever+87],16,0)
        pygame.draw.circle(screen,YELLOW,[575,self.lever+87],14,0)
        draw_text(self.text,self.textfont,screen,self.textposx,26,self.textcolor)
        pygame.display.update()
def main():

    pygame.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT,),0,32)
    emotes=['1.png','2.png','3.png','4.png','5.png','6.png','7.png']
    start=False
    while not start:
        for event in pygame.event.get():
            if event.type==KEYUP:
                if event.key==K_SPACE:
                    start=True
                    game=Game(emotes)
                elif event.key==K_ESCAPE:
                    terminate()
            elif event.type==QUIT:
                terminate()
    while True:
        game.process_events(screen)
        game.run_logic(screen,emotes)
        game.display_frame(screen,emotes)
        clock.tick(FRAMERATE)
main()
