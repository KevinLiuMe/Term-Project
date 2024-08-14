
from cmu_graphics import *
import random 
from PIL import Image

def onAppStart(app):
    reset(app)

def reset(app):
    app.Energy = 1
    app.Stamina = 1
    app.isStartGame = True
    app.width = 540
    app.height = 1920
    app.start_Width = app.width
    app.start_Height = app.height 
    app.fall_X = random.randrange(0, 100, 2)
    step = 0
    app.projectile_list = []
    app.hone_projectile_list = []
    app.stepCounter = 0
    app.heart_Power_Opacity = 50
    app.speed_Power_Opacity = 50
    app.shield_power_Opacity = 50
    app.speed_factor = 0
    app.speed_timer = 0
    app.speed_activated = False
    app.shield_activated = False
    app.heartCount = 3 
    app.invicount = 0
    app.isinvincible = False 
    loadMap(app)
    loadHearts(app)
    loadTitleScreen(app)
    loadHeartPower(app)
    loadSpeedPower(app)
    loadShieldPower(app)
    loadEnergy(app)
    loadStamina(app)
    loadteleport(app)
    loadSHIELD(app)
    myGif = Image.open('dragon.gif')
    app.spriteList = []
    app.heartCounts = 3
    app.scroll_X = 0
    app.scroll_Y = 0
 

    for frame in range(myGif.n_frames):
        myGif.seek(frame)
        #Resize the image
        fr = myGif.resize((myGif.size[0]//3, myGif.size[1]//3))
        #Flip the image
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr = CMUImage(fr)
        #Put in our sprite list
        app.spriteList.append(fr)

    ##Fix for broken transparency on frame 0
    app.spriteList.pop(0)
    app.spriteCounter = 0
    app.stepsPerSecond = 4


class projectile:
    ##### regular projectiles #####
    def __init__(self, pos, app_temp):
        self.app_temp = app_temp
        self.position = pos
        self.markForDeletion = False
    def __repr__(self):
        return str(self.position)
    def moveDown(self):
        self.position = (self.position[0], self.position[1] + 12)
    def isBelowScreen(self):
        if self.position[1] > self.app_temp.height:
            return False 
        else:
            return True
    def drawprojectile(self):
        fireball = Image.open('Fireball.png')
        fireball = CMUImage(fireball)
        fire_Width, fire_Height = getImageSize(fireball)
        drawImage(fireball, self.position[0], self.position[1], align = 'center', width = fire_Width / 5, height = fire_Height / 5)
        

class hone_projectile:
    ##### honing projectiles #####
    def __init__(self, pos):
        self.position = pos
        self.x = pos[0]
        self.y = pos[1]
        self.dx = random.randint(-10, 10)
        self.dy = -3
        self.ddx = 0
        self.ddy = 0.1

    def __repr__(self):
        return str(self.position)
    
    def step(self, app):
        #Integrate position and velocity
        if self.y < app.start_Height / 4:
            self.ddx += 0.05 * (app.start_Width / 2 - self.x)
            self.ddy += 0.05 * (app.start_Height / 4 - self.y)
            self.dx = 0.05 * (app.start_Width / 2 - self.x) 
            self.dy = 0.05 * (app.start_Height / 4 - self.y) 
            self.x += self.dx
            self.y += self.dy
        else:
            self.y += 10

    def drawhone_projectile(self):
        hone_fireball = Image.open('hone_projectile.png')
        hone_fireball = CMUImage(hone_fireball)
        hone_fireball_Width, hone_fireball_Height = getImageSize(hone_fireball)
        drawImage(hone_fireball, self.x, self.y, align = 'center', width = hone_fireball_Width / 5, height = hone_fireball_Height / 5)
    

def redrawAll(app):
    #drawTitleScreen(app)
    drawMap(app)
    drawHearts(app)
    drawHeartPower(app)
    drawSpeedPower(app)
    drawShieldPower(app)
    drawTeleport(app)
    activate_shield(app)
    
    
    drawRect(343, 650, app.Energy, 44, fill = 'lime')
    drawRect(23, 650, app.Stamina, 44, fill = 'cyan')
    
    drawEnergy(app)
    drawStamina(app)

    drawLabel(f'{app.Energy}', 500, 50, fill = 'white', size = 50)

    for index in range(len(app.projectile_list)):
        app.projectile_list[index].drawprojectile()
    
    for index in range(len(app.hone_projectile_list)):
        app.hone_projectile_list[index].drawhone_projectile()
    
    drawImage(app.spriteList[app.spriteCounter], 
              app.start_Width/2, app.start_Height/4, align = 'center')
    

def loadSHIELD(app):
    ##### load shield #####
    app.SHIELDUrl = Image.open('shield.png')
    app.SHIELDUrl = CMUImage(app.SHIELDUrl)

def activate_shield(app):
    if app.shield_activated == True:
        SHIELDwidth, SHIELDheight = getImageSize(app.SHIELDUrl)
        drawImage(app.SHIELDUrl, app.start_Width/2, app.start_Height/4 - 30, align = 'center', width = SHIELDwidth / 4, height = SHIELDheight / 4)

def loadTitleScreen(app):
    app.titleUrl = Image.open('1.png')
    app.titleUrl = CMUImage(app.titleUrl)

def drawTitleScreen(app):
    if app.isStartGame == True:
        imageWidth, imageHeight = getImageSize(app.titleUrl)
        drawImage(app.titleUrl, app.width / 2, app.height / 2, align = 'center', width = imageWidth / 2 * 1.4, height = imageHeight / 2 * 1.2)
    

def loadMap(app):
    ##### import background #####
    app.mapUrl = Image.open('background.png')
    app.mapUrl = CMUImage(app.mapUrl)


def drawMap(app):
    ##### draw background #####
    imageWidth, imageHeight = getImageSize(app.mapUrl)
    drawImage(app.mapUrl, app.width/2 - app.scroll_Y, app.height/2 - app.scroll_X, align='center', width = imageWidth, height = imageHeight)


def loadHearts(app):
    ##### import hearts #####
    app.heartUrl = Image.open('hearts.png')
    app.heartUrl = CMUImage(app.heartUrl)


def drawHearts(app):
    ##### draw hearts #####
    for i in range(app.heartCount):
        heartWidth, heartHeight = getImageSize(app.heartUrl)
        drawImage(app.heartUrl, 30 + i * 50, 750, align = 'center', width = heartWidth/8, height = heartHeight/8)

def loadHeartPower(app):
    ##### import hearts power up icon #####
    app.heartPowerUrl = Image.open('heart ability.png')
    app.heartPowerUrl = CMUImage(app.heartPowerUrl)

def drawHeartPower(app):
    heartPowerWidth, heartPowerHeight = getImageSize(app.heartPowerUrl)
    drawImage(app.heartPowerUrl, 500, 745, align = 'center', width = heartPowerWidth*450/461/8, height = heartPowerHeight*550/541/8, opacity = app.heart_Power_Opacity)

def loadSpeedPower(app):
    ##### import speed power up icon #####
    app.speedPowerUrl = Image.open('speed ability.png')
    app.speedPowerUrl = CMUImage(app.speedPowerUrl)

def drawSpeedPower(app):
    speedPowerWidth, speedPowerHeight = getImageSize(app.speedPowerUrl)
    drawImage(app.speedPowerUrl, 430, 745, align = 'center', width = speedPowerWidth*450/454/8 , height = speedPowerHeight*550/549/8 , opacity = app.speed_Power_Opacity)

def loadShieldPower(app):
    ##### import shield power up icon #####
    app.shieldPowerUrl = Image.open('shield ability.png')
    app.shieldPowerUrl = CMUImage(app.shieldPowerUrl)

def drawShieldPower(app):
    shieldPowerWidth, shieldPowerHeight = getImageSize(app.shieldPowerUrl)
    drawImage(app.shieldPowerUrl, 360, 747, align = 'center', width = shieldPowerWidth/8 , height = shieldPowerHeight*550/555/8, opacity = app.shield_power_Opacity )

def loadEnergy(app):
    ##### import energy bar #####
    app.energyUrl = Image.open('energy bar.png')
    app.energyUrl = CMUImage(app.energyUrl)

def drawEnergy(app):
    energyWidth, energyHeight = getImageSize(app.energyUrl)
    drawImage(app.energyUrl, 430, 670, align = 'center', width = energyWidth / 3, height = energyHeight / 4)
    

def loadStamina(app):
    ##### import stamina bar #####
    app.staminaUrl = Image.open('stamina bar.png')
    app.staminaUrl = CMUImage(app.staminaUrl)


def drawStamina(app):
    staminaWidth, staminaHeight = getImageSize(app.staminaUrl)
    drawImage(app.staminaUrl, 108, 670, align = 'center', width = staminaWidth / 3, height = staminaHeight / 4)
    

def loadteleport(app):
    ##### import teleport icon #####
    app.teleportUrl = Image.open('teleport.png')
    app.teleportUrl = CMUImage(app.teleportUrl)

def drawTeleport(app):
    teleportWidth, teleportHeight = getImageSize(app.teleportUrl)
    drawImage(app.teleportUrl, app.width/2 , 680, align = 'center', width = teleportWidth / 4, height = teleportHeight / 4)

def onKeyPress(app, key):
    if key == 'r':
        app.isStartGame = not app.isStartGame  


def onKeyHold(app, button):

    ##### reset game #####
    if ('r' in button) and app.heartCount == 0:
        reset(app)

    if app.heartCount == 0:
        return 

    ##### wasd controls #####
    if ('a' in button) and app.start_Width >= 230:
        app.start_Width -= 20 + app.speed_factor * 40
        app.scroll_Y += 10 + app.speed_factor * 40
    elif ('a' in button) and app.start_Width < 230:
        app.scroll_Y += 10 + app.speed_factor * 40
    if ('d' in button) and app.start_Width <= 850:
        app.start_Width += 20 + app.speed_factor * 40
        app.scroll_Y += -10 - app.speed_factor * 40
    elif('d' in button) and app.start_Width > 850:
        app.scroll_Y += -10 - app.speed_factor * 40
    if ('w' in button) and app.start_Height >= 1000:
        app.start_Height -= 30 + app.speed_factor * 40
        app.scroll_X += -10 - app.speed_factor * 40
    elif ('w' in button) and app.start_Height < 1000:
        app.scroll_X += -10 - app.speed_factor * 40
    if ('s' in button) and app.start_Height <= 2000:
        app.start_Height += 30 + app.speed_factor * 40
        app.scroll_X += 10 + app.speed_factor * 40
    elif ('s' in button) and app.start_Height > 2000:
         app.scroll_X += 10 + app.speed_factor * 40


    ##### power ups #####
    if ('3' in button) and app.Energy >= 100 and app.heartCount < 5:
        app.heartCount += 1
        app.Energy -= 100
    if ('2' in button) and app.Energy >= 50:
        app.speed_activated = True
        app.Energy -= 50
        app.speed_factor += 1
    if ('1' in button) and app.Energy >= 30: 
        app.shield_activated = True
        app.Energy -= 60
         


    ##### create teleport control #####
    if ('space' in button) and ('a' in button) and app.start_Width >= 30 and app.Stamina > 30:
        app.start_Width -= 100
        app.Stamina -= 30
    if ('space' in button) and ('d' in button) and app.start_Width <= 1050 and app.Stamina > 30:
        app.start_Width += 100
        app.Stamina -= 30
    
    
    


def onStep(app):

    
    if app.heartCount == 0:
        return 

    GameOver(app)
    GameOver2(app)
    
    if app.isinvincible == True:
        app.invicount += 1

    if app.Stamina <= 174:
        app.Stamina += 1
    else: app.Stamina = 174


    if app.Energy <= 174:
        app.Energy = app.Energy
    elif app.Energy > 174:
        app.Energy = 174
        

    app.scroll_X -= 5

    if app.speed_activated == True:
         app.speed_timer += 1 
    if app.speed_timer >= 50:
        app.speed_timer = 0
        app.speed_activated = False
        if app.speed_factor >= 1:
            app.speed_factor -= 1

    app.Energy += .5
    if app.Energy >= 100:
        app.heart_Power_Opacity = 100
    elif app.Energy < 100:
        app.heart_Power_Opacity = 50
    
    if app.Energy >= 50:
        app.speed_Power_Opacity = 100
    elif app.Energy < 50:
        app.speed_Power_Opacity = 50
    
    if app.Energy >= 60:
        app.shield_power_Opacity = 100
    elif app.Energy < 60:
        app.shield_power_Opacity = 50
    
    app.stepCounter += 1
    ##### create the projectiles #####
    if app.stepCounter % 18 == 0:
        pos = (random.randint(0,app.width), 0)
        newProjectile = projectile(pos, app)
        app.projectile_list.append(newProjectile)
        

    for index in range(len(app.projectile_list)):
        app.projectile_list[index].moveDown()
        if app.projectile_list[index].isBelowScreen() == False:
            app.projectile_list[index].markForDeletion = True
            
    ##### delete projectiles if off screen #####
    index = 0
    curr_length = len(app.projectile_list)
    
    while index < curr_length:
        if app.projectile_list[index].markForDeletion:
            curr_length -= 1
            app.projectile_list.pop(index)
        index += 1
    
    ##### create the honing projectiles #####
    if app.stepCounter % 144 == 0:
        pos1 = (random.randint(0,app.width), 0)
        pos2 = (random.randint(0,app.width), 0)
        pos3 = (random.randint(0,app.width), 0)
        pos4 = (random.randint(0,app.width), 0)
        pos5 = (random.randint(0,app.width), 0)
        newhone_projectile1 = hone_projectile(pos1)
        newhone_projectile2 = hone_projectile(pos2)
        newhone_projectile3 = hone_projectile(pos3)
        newhone_projectile4 = hone_projectile(pos4)
        newhone_projectile5 = hone_projectile(pos5)
        app.hone_projectile_list.append(newhone_projectile1)
        app.hone_projectile_list.append(newhone_projectile2)
        app.hone_projectile_list.append(newhone_projectile3)
        app.hone_projectile_list.append(newhone_projectile4)
        app.hone_projectile_list.append(newhone_projectile5)

    
    for index in range(len(app.hone_projectile_list)):
        app.hone_projectile_list[index].step(app)

    #Set spriteCounter to next frame
    app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)

def RunGame(app):
    if app.isinvincible  == False:
        GameOver(app)
    else: 
        app.invicount += 1

    
def isContact(x1, y1, x2, y2):
    ##### check if projectile hits dragon #####
    if x2 >= x1 - 50 and x2 <= x1 + 50 and y2 <= y1 + 110 and y2 >= y1 - 110 :
        return True


def GameOver(app):
    ##### check if game is over for hit by regular#####
    for projectile in app.projectile_list:
        positions = projectile.position
        if app.isinvincible == False:
            if isContact(positions[0], positions[1], app.start_Width/2, app.start_Height/4) == True and app.heartCount != 0 and app.shield_activated == False:
                app.isinvincible = True
                app.heartCount -= 1
            if isContact(positions[0], positions[1], app.start_Width/2, app.start_Height/4) == True and app.heartCount != 0 and app.shield_activated == True:
                app.shield_activated = False
                app.isinvincible = True
        elif app.isinvincible == True and app.invicount >= 30:
            app.isinvincible = False
            app.invicount = 0

def GameOver2(app):
    ##### check if game is over for hit by honing #####
    for hone_projectile in app.hone_projectile_list:
        positions2 = (hone_projectile.x, hone_projectile.y)
        if app.isinvincible == False:
            if isContact(positions2[0], positions2[1], app.start_Width/2, app.start_Height/4) == True and app.heartCount != 0 and app.shield_activated == False:
                app.isinvincible = True
                app.heartCount -= 1
            if isContact(positions2[0], positions2[1], app.start_Width/2, app.start_Height/4) == True and app.heartCount != 0 and app.shield_activated == True:
                app.shield_activated = False 
                app.isinvincible = True
        elif app.isinvincible == True and app.invicount >= 30:
            app.isinvincible = False
            app.invicount = 0



def main():
    runApp()

main()

#sources:
#image for background: Shutterstock ID: 2041927331
#image for fireballs : Shutterstock ID: 2221999855 
#image for UI: Shuttertstock ID: 2253757379, 742386076, 2152383281
#image for gif of flying dragon: https://graystain.tumblr.com/post/132691311167/i-wanted-to-animate-something-kinda-cute-so-i