import pygame
import time
import random

pygame.init()
white = (255, 255, 255)
black = (0,0,0)
grey = (210,210,210)
red = (255,0,0)
green = (0, 255, 0)
background = (138, 146, 221)
width = 800
height = 600

mwidth = width
mheight = 2*height/3
fps = 8

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Game")

logo = pygame.image.load("LOGO.png")
head = pygame.image.load("snakehead.png")
body1 = pygame.image.load("snakebody1.png")
body2 = pygame.image.load("snakebody2.png")
body3 = pygame.image.load("snakebody3.png")
apple = pygame.image.load("apple.png")

pygame.display.set_icon(apple)
    
clock = pygame.time.Clock()
gameExit = False

def message(msg, color, ft, wd, ht):
        font = pygame.font.SysFont("comicsansms", ft)
        text = font.render(msg, True, color)
        gameDisplay.blit(text, (wd, ht))
        
def intro():
        introduction = True
        while introduction:
                points = 0
                gameDisplay.fill(background)
                gameDisplay.blit(logo, (width/2-290, height/2-270))
                message("Snake Game", green, 100, width/2-290,height/2-200)
                message("Objective: Eat Apples to Score", black, 22, width/2-170, height/2-70)
                message("The More Apples You Eat, The Longer you Get", black, 22, width/2-230, height/2-40)
                message("Don't Collide With Your Body Or The Edges, Otherwise YOU DIE", black, 22,width/2-335, height/2-5)
                message("Controls", black, 25, 15, height-140)
                message("Move Up: W", black, 20, 15, height - 110)
                message("Move Down: S", black, 20, 15, height - 85)
                message("Move Left: A", black, 20, 15, height - 60)
                message("Move Right: D", black, 20, 15, height - 35)
                message("Pause: P", black, 20, width-80, height - 35)
                message("Press Enter To Start The Game", red, 30, width/2-210, height/2+60)
                pygame.display.update()
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                if points > highScore:
                                        file = open("confi.txt","w")
                                        file.write(chr(points))
                                        file.close()
                                pygame.quit()
                                quit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                        introduction = False
                                elif event.key == pygame.K_q:
                                        pygame.quit()
                                        quit()
        clock.tick(10)

def pause():
        paused = True
        while paused:
                pygame.draw.rect(gameDisplay, white, (30, 30, mwidth-60,mheight-60))
                message("Paused", black, 80, mwidth/4+50, mheight/4)
                message("Press P to Resume or Q to quit", black, 30, mwidth/4-30, mheight/4+110)
                pygame.display.update()
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                if points > highScore:
                                        file = open("confi.txt","w")
                                        file.write(hex(points))
                                        file.close()

                                pygame.quit()
                                quit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        if points > highScore:
                                                file = open("confi.txt","w")
                                                file.write(hex(points))
                                                file.close()
                                        pygame.quit()
                                        quit()
                                if event.key == pygame.K_p:
                                        paused = False
        clock.tick(15)

def gameLoop():
    global highScore
    try:
        file = open("confi.txt","r")
        highScore = int(file.read()[2:], 16)
        file.close()
    except:
        highScore = 0

    lead_x = mwidth/2
    lead_y = mheight/2

    lead_x_change = 0
    lead_y_change = 0
    snakeList = []

    gameExit = False
    gameOver = False

    global points
    points = 0
    appleX = round(random.randrange(50,mwidth-60)/20)*20
    appleY = round(random.randrange(50,mheight-60)/20)*20
    
    while not gameExit:
        while gameOver:
            pygame.draw.rect(gameDisplay, white, (30, 30, mwidth-60,mheight-60))
            message("Game Over!", red, 80, mwidth/4-10,mheight/4)
            message("Press Enter to Play Again or Q to quit", black, 30, mwidth/4-30, mheight/4+110)
            pygame.display.update()
            if points > highScore:
                    file = open("confi.txt","w")
                    file.write(hex(points))
                    file.close()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        gameExit == True
                        gameOver == False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_RETURN:
                        gameLoop()
                        
        preleadx = lead_x_change
        preleady = lead_y_change
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and lead_x_change != 20:
                    lead_x_change = -20
                    lead_y_change = 0
                elif event.key == pygame.K_d and lead_x_change != -20:
                    lead_x_change = 20
                    lead_y_change = 0
                elif event.key == pygame.K_w and lead_y_change != 20:
                    lead_y_change = -20
                    lead_x_change = 0
                elif event.key == pygame.K_s and lead_y_change != -20:
                    lead_y_change = 20
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                        pause()

        if (lead_x_change == 20 and preleady == 20) or (lead_y_change == -20 and preleadx == -20):
                ro = 2
        elif (lead_y_change == 20 and preleadx == -20) or (lead_x_change == 20 and preleady == -20):
                ro = 1
        elif (lead_x_change == -20 and preleady == -20) or (lead_y_change == 20 and preleadx == 20):
                ro = 4
        elif (lead_y_change == -20 and preleadx == 20) or (lead_x_change == -20 and preleady == 20):
                ro = 3
        else:
                ro = 0

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x == appleX and lead_y == appleY:
            appleX = round(random.randrange(40,mwidth-70)/20)*20
            appleY = round(random.randrange(40,mheight-70)/20)*20
            points += 1

        if lead_x > (mwidth-50) or lead_x < 30 or lead_y > (mheight-50) or lead_y < 30:
            gameOver = True

        else:
            gameDisplay.fill(grey)
            snakeHead = [lead_x, lead_y, lead_x_change, lead_y_change, ro]
            snakeList.append(snakeHead)
            if len(snakeList) != points + 1:
                    del snakeList[0]
            for xy in snakeList[:-1]:
                    if xy[:-3] == snakeHead[:-3]:
                            gameOver = True
                            
            gameDisplay.blit(apple, (appleX,appleY))
            snake(snakeList)
            pygame.draw.rect(gameDisplay, black, (0,0,mwidth,30))
            pygame.draw.rect(gameDisplay, black, (0,mheight-30,mwidth,30))
            pygame.draw.rect(gameDisplay, black, (0,0,30,mheight))
            pygame.draw.rect(gameDisplay, black, (mwidth-30,0,mwidth,mheight))
            
        pygame.draw.rect(gameDisplay, background, (0,mheight,width,height-mheight))
        message("Score: "+str(points), black, 50,300,mheight+50)
        if highScore > points:
                message("High Score: "+str(highScore), black, 25, 15, mheight+5)
        else:
                message("High Score: "+str(points), black, 25, 15, mheight+5)
        pygame.display.update()

        clock.tick(fps)

    if points > highScore:
        file = open("confi.txt","w")
        file.write(hex(points))
        file.close()

    pygame.quit()
    quit()

def snake(snakeList):
        if snakeList[-1][3] == 20:
                rhead = pygame.transform.rotate(head, 270)
        elif snakeList[-1][2] == -20:
                rhead = pygame.transform.rotate(head, 180)
        elif snakeList[-1][3] == -20:
                rhead = pygame.transform.rotate(head, 90)
        else:
                rhead = head

        gameDisplay.blit(rhead, (snakeList[-1][0], snakeList[-1][1]))

        for xy in snakeList[:-1]:
                if snakeList[snakeList.index(xy)+1][4] == 0:
                        if xy[2] == 20:
                                rbody1 = pygame.transform.rotate(body1, 270)
                                rbody2 = pygame.transform.rotate(body2, 270)
                        elif xy[2] == -20:
                                rbody1 = pygame.transform.rotate(body1, 90)
                                rbody2 = pygame.transform.rotate(body2, 90)
                        elif xy[3] == 20:
                                rbody1 = pygame.transform.rotate(body1, 180)
                                rbody2 = pygame.transform.rotate(body2, 180)
                        else:
                                rbody1 = body1
                                rbody2 = body2


                        if snakeList.index(xy)%2 == 0: 
                                gameDisplay.blit(rbody1, (xy[0], xy[1]))
                        else:
                                gameDisplay.blit(rbody2, (xy[0], xy[1]))

                elif snakeList[snakeList.index(xy)+1] != snakeList[-1]:
                        if snakeList[snakeList.index(xy)+1][4] == 1:
                                rbody3 = body3
                        elif snakeList[snakeList.index(xy)+1][4]== 2:
                                rbody3 = pygame.transform.rotate(body3, 90)
                        elif snakeList[snakeList.index(xy)+1][4] == 3:
                                rbody3 = pygame.transform.rotate(body3, 180)
                        else:
                                rbody3 = pygame.transform.rotate(body3, 270)

                        gameDisplay.blit(rbody3, (xy[0], xy[1]))

intro()
gameLoop()
