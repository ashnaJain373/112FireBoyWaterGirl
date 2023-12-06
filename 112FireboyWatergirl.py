from cmu_graphics import *
from PIL import Image
import os, pathlib
import random
import time
import copy

class Game:
    def __init__(self,gameWon,gameLost,score,level):
        self.gameWon=gameWon
        self.gameLost=gameLost
        self.score=score
        self.level=level

class State:
    def __init__(self,position,parent):
        self.position=position
        self.parent=parent
    
class Board:
    def __init__(self,boardpositions):
        self.boardpositions=boardpositions
    
    def getposition(self,row,col):
        return self.boardpositions[row][col]

class FireBoy:
    def __init__(self,positionx,positiony,row,col,AI):
        self.positionx=positionx
        self.positiony=positiony
        self.row=row
        self.col=col
        self.AI=AI
    
    def home_possiblePositionFireBoy(self,app):
        if isinstance(self.col,int) and isinstance(self.row,int):
            if self.row==9 or app.board[self.row+1][self.col]==1 or app.board[self.row+1][self.col]==2 or app.board[self.row+1][self.col]==4:
                return True
            else:
                return False
    
    def drawFireBoy(self,app):
        fireBoyX,fireBoyY=home_getCoordinates(app,self.row,self.col)
        drawImage(app.spriteList[app.spriteCounter], 
              fireBoyX, fireBoyY, align = 'center')

class WaterGirl:
    def __init__(self,positionx,positiony,row,col,AI):
        self.positionx=positionx
        self.positiony=positiony
        self.row=row
        self.col=col
        self.AI=AI
    
    def home_possiblePositionWaterGirl(self,app):
        if isinstance(self.row,int) and isinstance(self.col,int):
            if self.row==9 or app.board[self.row+1][self.col]==1 or app.board[self.row+1][self.col]==3 or app.board[self.row+1][self.col]==4:
                return True
            else:
                return False
    
    def drawWaterGirl(self,app):
        waterGirlX,waterGirlY=home_getCoordinates(app,self.row,self.col)
        drawImage(app.spriteList1[app.spriteCounter1], 
              waterGirlX,waterGirlY, align = 'center')


def home_generateBoard(app):
    #randomly generating the board
    board=[]
    for i in range(10):
        row = []
        for j in range(10):
            row.append(0) 
        board.append(row)
    
    for i in range(10):
        if i%2==1:
            wall = []
            for j in range(6):
                x=random.randint(0,9)
                while x in wall:
                    x=random.randint(0,9)
                wall.append(x)
            wall.sort(reverse=True)
            for y in range(10):
                if y in wall[1:]:
                    board[i][y]=1
                if i==3 or i==7:
                    board[i][wall[0]]=2
                elif i==5 or i==9:
                    board[i][wall[0]]=3
    #these values need to have walls so fireboy and watergirl can stand in their initial and final position
    board[1][8]=1
    board[1][9]=1
    board[7][0]=1
    board[9][0]=1
    #setting the wind fans position
    board[9][5]=4
                
    if home_isWinnableFireBoy(app,board) and home_isWinnableWaterGirl(app,board):
        return board 
    else:
        #generating new boards until the board is winnable for both water girl and fire boy
        return home_generateBoard(app)

def home_onAppStart(app):
    app.counter=0
    app.backgroundimage=Image.open("background.png")
    app.backgroundimage=CMUImage(app.backgroundimage)
    ##Fire Boy and Water Girl Wallpapers - Wallpaper Cave. (n.d.). https://wallpapercave.com/fire-boy-and-water-girl-wallpapers

    app.brickimage=Image.open("brick.png")
    app.brickimage=CMUImage(app.brickimage)
    ##Fire Boy and Water Girl Wallpapers - Wallpaper Cave. (n.d.). https://wallpapercave.com/fire-boy-and-water

    app.reddoorimage=Image.open("reddoor.png")
    app.reddoorimage=CMUImage(app.reddoorimage)
    ##Download premium png of Red panel png door sticker, modern architecture image on transparent background 
    ## by nywthn about red door, door, door interior design, door transparent, and architecture 6475462. (n.d.).
    ## Rawpixel. https://www.rawpixel.com/image/6475462/png-sticker-house

    app.bluedoorimage=Image.open("bluedoor.png")
    app.bluedoorimage=CMUImage(app.bluedoorimage)
    ##iconsdb.com - iconsdb Resources and Information. (n.d.). https://www.iconsdb.com/tropical-
    ## blue-icons/door-10-icon.html

    app.fireimage=Image.open("fire.png")
    app.fireimage=CMUImage(app.fireimage)
    ##Fire Clipart Images – browse 74,206 stock photos, vectors, and video. (n.d.). Adobe Stock. 
    # https://stock.adobe.com/search?k=fire+clipart

    app.waterimage=Image.open("water.png")
    app.waterimage=CMUImage(app.waterimage)
    ##Water splashes and drops isolated on transparent background. Abstract background with blue water 
    ## wave. (n.d.). Vecteezy. https://www.vecteezy.com/free-png/water
    
    fireboyimage=Image.open("Fireboy-idle.gif")
    ##Wiki, C. T. F. M. (n.d.). VS Fireboy & Watergirl. Funkipedia Mods Wiki. https://fridaynightfunking.
    ##fandom.com/wiki/VS_Fireboy_%26_Watergirl
    app.spriteList=[]
    for frame in range(fireboyimage.n_frames):
        fireboyimage.seek(frame)
        fr = fireboyimage.resize((fireboyimage.size[0]//8, fireboyimage.size[1]//8))
        #Flip the image
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr = CMUImage(fr)
        #Put in our sprite list
        app.spriteList.append(fr)
    app.spriteCounter=0
    #referred to demo posted on piazza for animated gifs

    watergirlimage=Image.open("WatergirlIdleAnim.gif")
    ##Wiki, C. T. F. M. (n.d.-b). VS Fireboy & Watergirl. Funkipedia Mods Wiki. https://fridaynightfunking.fandom.
    # com/wiki/VS_Fireboy_%26_Watergirl
    app.spriteList1=[]
    for frame in range(watergirlimage.n_frames):
        watergirlimage.seek(frame)
        fr1 = watergirlimage.resize((watergirlimage.size[0]//6, watergirlimage.size[1]//6))
        #Flip the image
        fr1 = fr1.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr1 = CMUImage(fr1)
        #Put in our sprite list
        app.spriteList1.append(fr1)
    app.spriteCounter1=0
    #referred to demo posted on piazza for animated gifs


    windimage=Image.open("wind.gif")
    ##Giphy. (n.d.). Vdb Windturbine GIFs - Get the best GIF on GIPHY. 
    # GIPHY. https://giphy.com/explore/vdb-windturbine
    app.spriteList2=[]
    for frame in range(windimage.n_frames):
        windimage.seek(frame)
        fr1 = windimage.resize((windimage.size[0]//7, windimage.size[1]//7))
        #Flip the image
        fr1 = fr1.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr1 = CMUImage(fr1)
        #Put in our sprite list
        app.spriteList2.append(fr1)
    app.spriteCounter2=0
    #referred to demo posted on piazza for animated gifs

    app.width=800
    app.height=800
    app.rows = 10
    app.cols = 10
    
 
    app.boardLeft = 100
    app.boardTop = 70
    app.boardWidth = 610
    app.boardHeight = 680
    app.cellWidth=(app.boardWidth-app.boardLeft)//app.rows
    app.cellHeight=(app.boardHeight-app.boardTop)//app.cols
    app.cellBorderWidth = 2

    app.board = home_generateBoard(app)
    app.isFireBoyAI=True
    app.isWaterGirlAI=True
    app.game=Game(False,False,0,0)
  
    if app.isFireBoyAI==True:
        app.fireBoy=FireBoy(150,580,7,0,True)
  
    elif app.isFireBoyAI==False:
        app.fireBoy=FireBoy(150,580,7,0,False)
    if app.isWaterGirlAI==True:
        app.waterGirl=WaterGirl(130,450,5,0,True)
    elif app.isFireBoyAI==False:
        app.waterGirl=WaterGirl(130,450,5,0,False)

    app.stepsPerSecond=12
    app.steps=0


def home_isWinnableFireBoy(app,board):
    #DFS algorithm to check if board is winnable
    queue=[(8,0)] #starting position of fireboy
    visited=set()
    while len(queue)>0:
        state=queue.pop(0)
        visited.add(state)
        if state==(0,8):
            return True
        children=home_getChildrenFireBoy(app,board,state)
        for i in children:
            if i not in visited:
                queue.append(i)
    return False # is not a winnable board for fireboy
    
def home_getChildrenFireBoy(app,board,state):
    children=[]
    actionList=['left','right','upleft','upright']
    for i in actionList:
        stateX,stateY=state
        #transition from x to neighbor based on action

        if i=='left':
            if stateY>=1:
                if board[stateX][stateY-1]==0:
                    stateY-=1
        elif i=='right':
            if stateY<=8:
                if  board[stateX][stateY+1]==0:
                    stateY+=1
        elif i=='upleft':
            if stateX>=1 and stateY>=1:
                if (board[stateX-1][stateY-1]==0 and board[stateX-1][stateY]==0):
                    stateX-=1
                    stateY-=1
                elif stateX>=2 and stateY>=1:
                    if (board[stateX-1-1][stateY-1]==0 and board[stateX-1][stateY]==0):
                        stateX-=2
                        stateY-=1
        elif i=='upright':
            if stateX>=1 and stateY<=8:
                if (board[stateX-1][stateY+1]==0 and board[stateX-1][stateY]==0):
                    stateX-=1
                    stateY+=1
                elif stateX>=2 and stateY<=8:
                    if (board[stateX-1-1][stateY+1]==0 and board[stateX-1][stateY]==0):
                        stateX-=2
                        stateY+=1
    
        if board[stateX][stateY]==3 or board[stateX][stateY]==2 or board[stateX][stateY]==4:
            continue
        if stateX!=9:
            if board[stateX+1][stateY]==3:
                continue
        while stateX!=9 and board[stateX+1][stateY]!=1 and board[stateX+1][stateY]!=2 and board[stateX+1][stateY]!=3 and board[stateX+1][stateY]!=4:
            stateX+=1
        if board[stateX][stateY]!=3:
            if stateX==9 or board[stateX+1][stateY]!=3:
               
                children.append((stateX,stateY))
    
    return children

def home_isWinnableWaterGirl(app,board):
    #DFS algorithm to check if board is winnable
    queue=[(6,0)] #starting position of watergirl
    visited=set()
    while len(queue)>0:
        state=queue.pop(0)
        visited.add(state)
        if state==(0,9):
            return True
        children=home_getChildrenWaterGirl(app,board,state)
        for i in children:
            if i not in visited:
                queue.append(i)
    return False # not a winnable board for watergirl

    
def home_getChildrenWaterGirl(app,board,state):
    children=[]
    actionList=['left','right','upleft','upright']
    for i in actionList:
        stateX,stateY=state
        #transition from x to neighbor based on action

        if i=='left':
            if stateY>=1:
                if board[stateX][stateY-1]==0:
                    stateY-=1

        elif i=='right':
            if stateY<=8:
                if  board[stateX][stateY+1]==0:
                    stateY+=1

        elif i=='upleft':
            if stateX>=1 and stateY>=1:
                if (board[stateX-1][stateY-1]==0 and board[stateX-1][stateY]==0):
                    stateX-=1
                    stateY-=1
                elif stateX>=2 and stateY>=1:
                    if (board[stateX-1-1][stateY-1]==0 and board[stateX-1][stateY]==0):
                        stateX-=2
                        stateY-=1

        elif i=='upright':
            if stateX>=1 and stateY<=8:
                if (board[stateX-1][stateY+1]==0 and board[stateX-1][stateY]==0):
                    stateX-=1
                    stateY+=1
                elif stateX>=2 and stateY<=8:
                    if (board[stateX-1-1][stateY+1]==0 and board[stateX-1][stateY]==0):
                        stateX-=2
                        stateY+=1
        if board[stateX][stateY]==2 or board[stateX][stateY]==3 or board[stateX][stateY]==4:
            continue
        if stateX!=9:
            if board[stateX+1][stateY]==2:
                continue
        while stateX!=9 and board[stateX+1][stateY]!=1 and board[stateX+1][stateY]!=2 and board[stateX+1][stateY]!=3 and board[stateX+1][stateY]!=4:
            stateX+=1
        if board[stateX][stateY]!=2:
            if stateX==9 or board[stateX+1][stateY]!=2:
                children.append((stateX,stateY))
    return children


def home_onStep(app):
    app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)
    app.spriteCounter1 = (app.spriteCounter1 + 1) % len(app.spriteList1)
    app.spriteCounter2 = (app.spriteCounter2 + 1) % len(app.spriteList2)
    app.steps+=1
    if app.steps%5==0:
        app.counter+=1

def home_getCoordinates(app,row,col):
    #getting the coordinates of fireboy or watergirl from their position in the board
    left,top= home_getCellLeftTop(app,row,col)
    right=left+app.cellWidth
    bottom=top+app.cellHeight
    xCord=(left+right)//2
    yCord=(top+bottom)//2
    return xCord,yCord

def welcome_onAppStart(app):
    app.backgroundimage=Image.open("background.png")
    app.backgroundimage=CMUImage(app.backgroundimage)

    app.fontimage=Image.open("font1.png").resize((400, 100), Image.BICUBIC)
    app.fontimage=CMUImage(app.fontimage)
    #Image from home screen of the game fireboy watergirl
    #Fireboy and Watergirl – play online at CoolMath Games. 
    #(n.d.). https://www.coolmathgames.com/0-fireboy-and-water-girl-in-the-forest-temple

def welcome_redrawAll(app):
    newWidth,newHeight=(app.width,app.height)
    drawImage(app.backgroundimage,0,0,width=newWidth,height=newHeight)

    newWidth,newHeight=(600,150)
    drawImage(app.fontimage,110,50,width=newWidth,height=newHeight)

    drawRect(250, 250, 300, 100, fill=None, border='black', borderWidth=10)
    drawLabel('Click here to play',390,300,size=32)

    drawRect(250, 450, 300, 100, fill=None, border='black', borderWidth=10)
    drawLabel('Click here to play with AI FireBoy',390,500,size=18)

    drawRect(250, 650, 300, 100, fill=None, border='black', borderWidth=10)
    drawLabel('Click here to play with AI WaterGirl',390,700,size=18)  

def welcome_onMousePress(app,mouseX,mouseY):
    if mouseX>=250 and mouseX<=550 and mouseY>=250 and mouseY<=350:
        app.isFireBoyAI=False
        app.isWaterGirlAI=False
        setActiveScreen('home')
    
    if mouseX>=250 and mouseX<=550 and mouseY>=450 and mouseY<=550:
        app.isFireBoyAI=True
        app.isWaterGirlAI=False
        setActiveScreen('home')
    
    if mouseX>=250 and mouseX<=650 and mouseY>=650 and mouseY<=750:
        app.isFireBoyAI=False
        app.isWaterGirlAI=True
        setActiveScreen('home')

def lost_onAppStart(app):
    app.backgroundimage=Image.open("background.png")
    app.backgroundimage=CMUImage(app.backgroundimage)


def won_onAppStart(app):
    app.backgroundimage=Image.open("background.png")
    app.backgroundimage=CMUImage(app.backgroundimage)

    

def lost_redrawAll(app):
    newWidth,newHeight=(app.width,app.height)
    drawImage(app.backgroundimage,0,0,width=newWidth,height=newHeight)

    drawLabel("You lost:(", app.width/2, app.height/2, size = 18)

def won_redrawAll(app):
    newWidth,newHeight=(app.width,app.height)
    drawImage(app.backgroundimage,0,0,width=newWidth,height=newHeight)

    drawLabel("You won:)", app.width/2, app.height/2, size = 24)

def getFireBoyPath(app):
    #getting the path for fireboy to win using depth first search
    state1= State((8,0),(8,0))
    queue=[state1]
    queuecopy=[state1]
    visited=set()
    while len(queue)>0:
        temp=queue.pop()
        state=temp.position
        visited.add(state)
        if state == (0,8):
            queue.append(temp)
            queuecopy.append(temp)

            return getFireBoyPathHelper(app,queuecopy)
        children=home_getChildrenFireBoy(app,app.board,state)
       
        for i in children:
            state2=State(i,state)
            if i not in visited:
                queue.append(state2)
            queuecopy.append(state2)

def getFireBoyPathHelper(app,visited):
    path=[]
    path.append(visited[len(visited)-1].position)
    parent=visited[len(visited)-1].parent

    for i in visited[::-1]:
        if i.position==parent:
            path.append(i.position)
            parent=i.parent
        if i.parent==(7,0):
            break
    return path[::-1]
    
def home_AIFireBoy(app):
    if app.fireBoy.row==0 and app.fireBoy.col==8:
        return (app.fireBoy.row,app.fireBoy.col)
    queue=getFireBoyPath(app)

    if queue!=None and app.counter<len(queue):
        return queue[app.counter]
    else:
        return (app.fireBoy.row,app.fireBoy.col)

def getWaterGirlPath(app):
    #getting the path for watergirl to win using depth first search
    state1= State((6,0),(6,0))
    queue=[state1]
    queuecopy=[state1]
    visited=set()
    while len(queue)>0:
        temp=queue.pop()
        state=temp.position
        visited.add(state)
        if state == (0,9):
            queue.append(temp)
            queuecopy.append(temp)
            return getWaterGirlPathHelper(app,queuecopy)
        children=home_getChildrenWaterGirl(app,app.board,state)
       
        for i in children:
            state2=State(i,state)
            if i not in visited:
                queue.append(state2)
            queuecopy.append(state2)

def getWaterGirlPathHelper(app,visited):

    path=[]
    path.append(visited[len(visited)-1].position)
    parent=visited[len(visited)-1].parent

    for i in visited[::-1]:
        if i.position==parent:
            path.append(i.position)
            parent=i.parent
        if i.parent==(5,0):
            break
    return path[::-1]
    
def home_AIWaterGirl(app):
    if app.waterGirl.row==0 and app.waterGirl.col==9:
        return (app.waterGirl.row,app.waterGirl.col)
    queue=getWaterGirlPath(app)

    if queue!=None and app.counter<len(queue):
        return queue[app.counter]
    else:
        return (app.waterGirl.row,app.waterGirl.col)

def home_redrawAll(app):
    if app.game.gameLost:
        setActiveScreen('lost')
    if app.game.gameWon:
        setActiveScreen('won')
    drawImage(app.backgroundimage,0,0)
    newWidth,newHeight=(app.width,app.height)
    drawImage(app.backgroundimage,0,0,width=newWidth,height=newHeight)
    if home_possiblePositionFireBoy(app):
        app.fireBoy.drawFireBoy(app)
    else:
        home_gravityFireBoy(app)
    
    if app.isFireBoyAI:
        fireBoyX,fireBoyY=home_AIFireBoy(app)
        app.fireBoy.row=fireBoyX
        app.fireBoy.col=fireBoyY
    elif app.isWaterGirlAI:
        waterGirlX,waterGirlY=home_AIWaterGirl(app)
        app.waterGirl.row=waterGirlX
        app.waterGirl.col=waterGirlY

    if home_possiblePositionWaterGirl(app):
        app.waterGirl.drawWaterGirl(app)
    else:
        home_gravityWaterGirl(app)

    if app.fireBoy.row!=9 and app.board[app.fireBoy.row+1][app.fireBoy.col]==3:

        app.game.gameLost=True
    if app.board[app.fireBoy.row][app.fireBoy.col]==3:
      
        app.game.gameLost=True
    if app.board[app.waterGirl.row][app.waterGirl.col]==2:
       
        app.game.gameLost=True
    if app.waterGirl.row!=9 and app.board[app.waterGirl.row+1][app.waterGirl.col]==2:

        app.game.gameLost=True

    if app.fireBoy.row==0 and app.fireBoy.col==8 and app.waterGirl.row==0 and app.waterGirl.col==9:

        app.game.gameWon=True
    if app.fireBoy.row==8 and app.fireBoy.col==5:
        home_windFireBoy(app)
    if app.waterGirl.row==8 and app.waterGirl.col==5:
        home_windWaterGirl(app)
    drawLabel('112 FireBoy WaterGirl', 200, 20, size=16)
    home_drawBoard(app)
    home_drawBoardBorder(app)

def home_gravityFireBoy(app):
    #implementing gravity. if fireboy is not standing on a wall then he falls down
    fireBoyX,fireBoyY=home_getCoordinates(app,app.fireBoy.row,app.fireBoy.col)
    fireBoyXFinal,fireBoyY= home_getCoordinates(app,app.fireBoy.row+1,app.fireBoy.col)
    diff=fireBoyXFinal-fireBoyX
    drawImage(app.spriteList[app.spriteCounter], fireBoyX, fireBoyY, align = 'center')
    for i in range(0,10):
        drawImage(app.spriteList[app.spriteCounter],(i/10)*diff+fireBoyX, fireBoyY, align = 'center')
    app.fireBoy.row+=1

def home_gravityWaterGirl(app):
    #implementing gravity. if watergirl is not standing on a wall then she falls down
    waterGirlX,waterGirlY=home_getCoordinates(app,app.waterGirl.row,app.waterGirl.col)
    waterGirlXFinal,waterGirlY= home_getCoordinates(app,app.waterGirl.row+1,app.waterGirl.col)
    diff=waterGirlXFinal-waterGirlX
    drawImage(app.spriteList1[app.spriteCounter1], waterGirlX, waterGirlY, align = 'center')
    for i in range(0,10):
        drawImage(app.spriteList1[app.spriteCounter1],(i/10)*diff+waterGirlX, waterGirlY, align = 'center')
    app.waterGirl.row+=1

def home_windFireBoy(app):
    #if fireboy falls on the wind tunnel then he keeps going up and down till he gets off it
    if app.board[app.fireBoy.row-1][app.fireBoy.col]!=0:
        return
    fireBoyX,fireBoyY=home_getCoordinates(app,app.fireBoy.row,app.fireBoy.col)
    fireBoyXFinal,fireBoyY= home_getCoordinates(app,app.fireBoy.row-1,app.fireBoy.col)
    diff=fireBoyXFinal-fireBoyX
    app.fireBoy.row-=1
    if app.board[app.fireBoy.row-1][app.fireBoy.col]==0:
        home_windFireBoy(app)
    else:
        return

def home_windWaterGirl(app):
    #if watergirl falls on the wind tunnel then she keeps going up and down till she gets off it
    if app.board[app.waterGirl.row-1][app.waterGirl.col]!=0:
        return
    waterGirlX,waterGirlY=home_getCoordinates(app,app.waterGirl.row,app.waterGirl.col)
    waterGirlXFinal,waterGirlY= home_getCoordinates(app,app.waterGirl.row-1,app.waterGirl.col)
    diff=waterGirlXFinal-waterGirlX
    app.waterGirl.row-=1
    if app.board[app.waterGirl.row-1][app.waterGirl.col]==0:
        home_windWaterGirl(app)
    
def home_drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            home_drawCell(app, row, col)

def home_drawBoardBorder(app):
  # draw the board outline
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None,border='black',
           borderWidth=2*app.cellBorderWidth)


def home_drawCell(app, row, col):
    cellLeft, cellTop = home_getCellLeftTop(app, row, col)
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    if app.board[row][col]==1:
        newWidth,newHeight=(cellWidth,cellHeight)
        drawImage(app.brickimage,cellLeft,cellTop,width=newWidth,height=newHeight)
    elif app.board[row][col]==2:
        newWidth,newHeight=(cellWidth,cellHeight)
        drawImage(app.fireimage,cellLeft,cellTop,width=newWidth,height=newHeight)
    elif app.board[row][col]==3:
        newWidth,newHeight=(cellWidth,cellHeight)
        drawImage(app.waterimage,cellLeft,cellTop,width=newWidth,height=newHeight)
    elif app.board[row][col]==4:
        newWidth,newHeight=(cellWidth,cellHeight)

        X,Y=home_getCoordinates(app,row,col)
        drawImage(app.spriteList2[app.spriteCounter2], 
              X, Y, align = 'center')

    if row==0 and col==8:
        newWidth,newHeight=(cellWidth,cellHeight)
        drawImage(app.reddoorimage,cellLeft,cellTop,width=newWidth,height=newHeight)
    elif row==0 and col==9:
        newWidth,newHeight=(cellWidth,cellHeight)
        drawImage(app.bluedoorimage,cellLeft,cellTop,width=newWidth,height=newHeight)

def home_getCellLeftTop(app, row, col):
    cellWidth, cellHeight = home_getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def home_getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def home_possiblePositionFireBoy(app):
    #checking if the current position of fireboy is a valid position
    if isinstance(app.fireBoy.col,int) and isinstance(app.fireBoy.row,int):
        if app.fireBoy.row==9 or app.board[app.fireBoy.row+1][app.fireBoy.col]==1 or app.board[app.fireBoy.row+1][app.fireBoy.col]==2 or app.board[app.fireBoy.row+1][app.fireBoy.col]==4:
            return True
    else:
        return False
    
def home_possiblePositionWaterGirl(app):
    #checking if the current position of watergirl is a valid position
    if isinstance(app.waterGirl.row,int) and isinstance(app.waterGirl.col,int):
        if app.waterGirl.row==9 or app.board[app.waterGirl.row+1][app.waterGirl.col]==1 or app.board[app.waterGirl.row+1][app.waterGirl.col]==3 or app.board[app.waterGirl.row+1][app.waterGirl.col]==4:
            return True
    else:
        return False

def home_onKeyHold(app,keys):
    #moving fireboy and watergirl around the board based on the keys held
    if app.steps % 2 ==0:
        if isinstance(app.fireBoy.col,int) and isinstance(app.fireBoy.row,int) and isinstance(app.waterGirl.row,int) and isinstance(app.waterGirl.col,int):
            if 'up' in keys and 'left' in keys:
        
                if app.fireBoy.row>=1 and app.fireBoy.col>=1:
                
                    if (app.board[app.fireBoy.row-1][app.fireBoy.col-1]==0):
                    
                        app.fireBoy.row-=1
                        app.fireBoy.col-=1
                    elif app.fireBoy.row>=2 and app.fireBoy.col>=1:
                        if (app.board[app.fireBoy.row-1-1][app.fireBoy.col-1]==0 and app.board[app.fireBoy.row-1][app.fireBoy.col]==0):
                        
                            app.fireBoy.row-=2
                            app.fireBoy.col-=1
                    
            elif ('down' in keys) and ('left' in keys):
                if app.fireBoy.row<=8 and app.fireBoy.col>=1:
                    if (app.board[app.fireBoy.row+1][app.fireBoy.col-1]==0):
                        app.fireBoy.row+=1
                        app.fireBoy.col-=1
                    elif app.fireBoy.row<=7 and app.fireBoy.col>=1:
                        if (app.board[app.fireBoy.row+1+1][app.fireBoy.col-1]==0 and app.board[app.fireBoy.row+1][app.fireBoy.col]==0):
                            app.fireBoy.row+=2
                            app.fireBoy.col-=1
            
            elif ('up' in keys) and ('right' in keys):
                if app.fireBoy.row>=1 and app.fireBoy.col<=8:
                    if (app.board[app.fireBoy.row-1][app.fireBoy.col+1]==0):
                        app.fireBoy.row-=1
                        app.fireBoy.col+=1
                    elif app.fireBoy.row>=2 and app.fireBoy.col<=8:
                        if (app.board[app.fireBoy.row-1-1][app.fireBoy.col+1]==0 and app.board[app.fireBoy.row-1][app.fireBoy.col]==0):
                            app.fireBoy.row-=2
                            app.fireBoy.col+=1

            elif ('down' in keys) and ('right' in keys):
                if app.fireBoy.row<=8 and app.fireBoy.col<=8:
                    if (app.board[app.fireBoy.row+1][app.fireBoy.col+1]==0):
                        app.fireBoy.row+=1
                        app.fireBoy.col+=1
                    elif (app.board[app.fireBoy.row+1+1][app.fireBoy.col+1]==0 and app.board[app.fireBoy.row+1][app.fireBoy.col]==0):
                        app.fireBoy.row+=2
                        app.fireBoy.col+=1

            elif 'right' in keys:
                if app.fireBoy.col<=8:
                    if  app.board[app.fireBoy.row][app.fireBoy.col+1]==0:
                        app.fireBoy.col+=1

            elif 'left' in keys:
                if app.fireBoy.col>=1:
                    if app.board[app.fireBoy.row][app.fireBoy.col-1]==0:
                        app.fireBoy.col-=1
            elif 'up' in keys:
                if app.fireBoy.row>=2:
                    if app.fireBoy.row==2 or app.board[app.fireBoy.row-1][app.fireBoy.col]==0:
                        app.fireBoy.row-=2
            elif 'down' in keys:
                if app.fireBoy.row<=7:
                    if app.fireBoy.row==9 or app.board[app.fireBoy.row+1][app.fireBoy.col]==0:
                        app.fireBoy.row+=2
            
            
                        
            if 'w' in keys and 'a' in keys:
                if app.waterGirl.row>=1 and app.waterGirl.col>=1:
                
                    if (app.board[app.waterGirl.row-1][app.waterGirl.col-1]==0):
                        
                        app.waterGirl.row-=1
                        app.waterGirl.col-=1
                    elif app.waterGirl.row>=2 and app.fireBoy.col>=1:
                        if (app.board[app.waterGirl.row-1-1][app.waterGirl.col-1]==0 and app.board[app.waterGirl.row-1][app.waterGirl.col]==0):
                            app.waterGirl.row-=2
                            app.waterGirl.col-=1
                    
            elif ('s' in keys) and ('a' in keys):
                if app.waterGirl.row<=8 and app.waterGirl.col>=1:
                    if (app.board[app.waterGirl.row+1][app.waterGirl.col-1]==0):
                        app.waterGirl.row+=1
                        app.waterGirl.col-=1
                    elif app.waterGirl.row<=7 and app.waterGirl.col>=1:
                        if app.board[app.waterGirl.row+1+1][app.waterGirl.col-1]==0:
                            app.waterGirl.row+=2
                            app.waterGirl-=1
            
            elif ('w' in keys) and ('d' in keys):
                if app.waterGirl.row>=1 and app.waterGirl.col<=8:
                    if (app.board[app.waterGirl.row-1][app.waterGirl.col+1]==0):
                        app.waterGirl.row-=1
                        app.waterGirl.col+=1
                    elif app.waterGirl.row>=2 and app.waterGirl.col<=8:
                        if (app.board[app.waterGirl.row-1-1][app.waterGirl.col+1]==0 and app.board[app.waterGirl.row-1][app.waterGirl.col]==0):
                            app.waterGirl.row-=2
                            app.waterGirl.col+=1
        
            elif ('s' in keys) and ('d' in keys):
                if app.waterGirl.row<=8 and app.waterGirl.col<=8:
                    if (app.board[app.waterGirl.row+1][app.waterGirl.col+1+1]==0):
                        app.waterGirl.row+=1
                        app.waterGirl.col+=1
                    elif (app.board[app.waterGirl.row+1+1][app.waterGirl.col+1+1]==0) and app.board[app.waterGirl.row+1][app.waterGirl.col]==0:
                        app.waterGirl.row+=2
                        app.waterGirl.col+=1
        
        
            elif 'd' in keys:
                if app.waterGirl.col<=8:
                    if app.board[app.waterGirl.row][app.waterGirl.col+1]==0:
                        app.waterGirl.col+=1

            elif 'a' in keys:
                if app.waterGirl.col>=1:
                    if app.board[app.waterGirl.row][app.waterGirl.col-1]==0:
                        app.waterGirl.col-=1

            elif 'w' in keys:
                if app.waterGirl.row>=2:
                    if app.waterGirl.row==2 or app.board[app.waterGirl.row-1][app.waterGirl.col]==0:
                        app.waterGirl.row-=2

            elif 's' in keys:
                if app.waterGirl.row<=7:
                    if app.waterGirl.row==9 or app.board[app.waterGirl.row+1][app.waterGirl.col]==0:
                        app.waterGirl.row+=2
    
def main():
    runAppWithScreens(initialScreen='welcome')
    #referred to demo posted on piazza for multiple screens 
main()