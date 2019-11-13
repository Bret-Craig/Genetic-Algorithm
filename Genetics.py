import pygame
import random
import numpy
import time
import math
from pygame import gfxdraw

pygame.init()

def main(dna, instanceadd):
    display_width = 800
    display_heigth = 600
    white = (255,255,255)
    black = (0,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    red = (255,0,0)
    yellow = (255,238,0)
    purple = (195,0,255)
    orange = (255,136,0)
    fps = 60
    gameDisplay = pygame.display.set_mode((display_width, display_heigth))
    clock = pygame.time.Clock()
    food_list = []
    poison_list = []
    base_dna = dna
    instance = 1 + instanceadd

    class create_bot():
        def __init__(self, x, y, color, num):
            self.position = numpy.array([x,y], dtype='float64')
            self.size = 5
            
            #food attraction/poison attraction/food sense/poison sense/x home/y home
            if base_dna == False:
                self.dna = [random.random(),random.random(),random.randint(15,75),random.randint(15,75),random.randint(5,795),random.randint(5,595)]
            elif num == 1:
                self.dna = base_dna
            else:
                fattract = base_dna[0]+random.uniform(-.3,.3)
                pattract = base_dna[1]+random.uniform(-.3,.3)
                if fattract > 1:
                    fattract = 1
                if fattract < 0:
                    fattract = 0
                if pattract > 1:
                    pattract = 1
                if pattract < 0:
                    pattract = 0

                fsense = base_dna[2]+random.randint(-15,15)
                psense = base_dna[3]+random.randint(-15,15)
                if fsense > 75:
                    fsense = 75
                if fsense < 15:
                    fsense = 15
                if psense > 75:
                    psense = 75
                if psense < 15:
                    psennse = 15

                
                self.dna = [fattract,pattract,fsense,psense,random.randint(5,795),random.randint(5,595)]
            
            self.health = 100
            self.color = color
            self.alive = 1

        def bot_update(self, food_list, poison_list):
            if self.health > 0:
                self.move()
                self.health -= 0.2
                self.draw()
            else:
                self.alive = 0
                
        def move(self):
            closest = 1000
            dist = 0
            x_food = -1
            y_food = -1
            x_pois = -1
            y_pois = -1
            for i in range(60):
                x2 = food_list[i].get_pos(0)
                y2 = food_list[i].get_pos(1)
                dist = distance(self.position[0],self.position[1],x2,y2)
                closest = 1000
                if dist <= self.dna[2]:
                    closest = dist
                    x_food = food_list[i].get_pos(0)
                    y_food = food_list[i].get_pos(1)
                if dist <= 5:
                    food_list.pop(i)
                    food_list.append(create_food(random.randint(5,795),random.randint(5,595)))
                    if self.health >= 80:
                        self.health = 100
                    else:
                        self.health += 20
                    
            for i in range(30):
                x2 = poison_list[i].get_pos(0)
                y2 = poison_list[i].get_pos(1)
                dist = distance(self.position[0],self.position[1],x2,y2)
                closest = 1000
                if dist <= self.dna[3]:
                    closest = dist
                    x_pois = poison_list[i].get_pos(0)
                    y_pois = poison_list[i].get_pos(1)
                if dist <= 5:
                    poison_list.pop(i)
                    poison_list.append(create_poison(random.randint(5,795),random.randint(5,595)))
                    self.health -= 70

            if self.dna[0] > self.dna[1] and x_food > 0:
                self.shift(x_food, y_food)
            elif self.dna[1] > self.dna[0] and x_pois > 0:
                self.shift(x_pois, y_pois)
            elif x_food > 0 and x_pois < 0:
                self.shift(x_food, y_food)
            elif x_pois > 0 and x_food < 0:
                self.shift(x_pois, y_pois)
            else:
                self.shift(self.dna[4], self.dna[5])
            
    
        def shift(self, x, y):
            if x > self.position[0]:
                self.position[0] += 1.2
            if x < self.position[0]:
                self.position[0] -= 1.2
            if y > self.position[1]:
                self.position[1] += 1.2
            if y < self.position[1]:
                self.position[1] -= 1.2
        
        def draw(self):
            pygame.gfxdraw.aacircle(gameDisplay, int(self.position[0]), int(self.position[1]), 10, self.color)
            pygame.gfxdraw.filled_circle(gameDisplay, int(self.position[0]), int(self.position[1]), 10, self.color)
            pygame.gfxdraw.aacircle(gameDisplay, int(self.position[0]), int(self.position[1]), self.dna[2], green)
            pygame.gfxdraw.aacircle(gameDisplay, int(self.position[0]), int(self.position[1]), self.dna[3], red)

        def get_state(self):
            return self.alive

        def get_dna(self):
            return self.dna

    class create_food():
        def __init__(self, x, y):
            self.position = numpy.array([x,y], dtype='float64')

        def draw(self):
            pygame.gfxdraw.aacircle(gameDisplay, int(self.position[0]), int(self.position[1]), 2, green)
            pygame.gfxdraw.filled_circle(gameDisplay, int(self.position[0]), int(self.position[1]), 2, green)

        def get_pos(self, num):
            if num == 0:
                return self.position[0]
            else:
                return self.position[1]

    class create_poison():
        def __init__(self, x, y):
            self.position = numpy.array([x,y], dtype='float64')

        def draw(self):
            pygame.gfxdraw.aacircle(gameDisplay, int(self.position[0]), int(self.position[1]),2, red)
            pygame.gfxdraw.filled_circle(gameDisplay, int(self.position[0]), int(self.position[1]), 2, red)

        def get_pos(self, num):
            if num == 0:
                return self.position[0]
            else:
                return self.position[1]

    one = create_bot(200,300,black,1)
    two = create_bot(300,300,orange,2)
    three = create_bot(400,300,blue,3)
    four = create_bot(500,300,yellow,4)
    five = create_bot(600,300,purple,5)

    for i in range(60):
        food_list.append(create_food(random.randint(5,795),random.randint(5,595)))
    for i in range(30):
        poison_list.append(create_poison(random.randint(5,795),random.randint(5,595)))

    def update():
        one.bot_update(food_list, poison_list)
        two.bot_update(food_list, poison_list)
        three.bot_update(food_list, poison_list)
        four.bot_update(food_list, poison_list)
        five.bot_update(food_list, poison_list)
        draw_objects()

    def draw_objects():
        for i in range(60):
            food_list[i-1].draw()

        for i in range(30):
            poison_list[i-1].draw()

    def distance(x1, y1, x2, y2):
        distance = 0
        x = math.pow((x1-x2), 2)
        y = math.pow((y1-y2), 2)
        distance = math.sqrt(x+y)
        return distance

    def round_num():
        font = pygame.font.Font(None, 25)
        text = font.render(str(instance), True, black)
        gameDisplay.blit(text, (0, 0))
        
    
    running = True
    while running == True:
        
        count = 0
        for i in range(1,5):
            if one.alive == 0:
                count += 1
            if two.alive == 0:
                count += 1
            if three.alive == 0:
                count += 1
            if four.alive == 0:
                count += 1
            if five.alive == 0:
                count += 1
                
        if count == 16:
            
            if one.alive == 1:
                print(one.dna)
                running = False
                time.sleep(5)
                main(one.dna,instance)
                
            if two.alive == 1:
                print(two.dna)
                running = False
                time.sleep(5)
                main(two.dna, instance)
                
            if three.alive == 1:
                print(three.dna)
                running = False
                time.sleep(5)
                main(three.dna,instance)
                
            if four.alive == 1:
                print(four.dna)
                running = False
                time.sleep(5)
                main(four.dna,instance)
                
            if five.alive == 1:
                print(five.dna)
                running = False
                time.sleep(5)
                main(five.dna,instance)
                
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gameDisplay.fill(white)
        update()
        round_num()
        pygame.display.update()
        clock.tick(60)

        
main(False,0)
        

    
        
        
            
            
            
            

    
