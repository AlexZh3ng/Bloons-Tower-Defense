'''
Name: Alex Zheng
Date: May 28, 2019
Description: This is the sprite module for BTD
'''

import pygame, math
class Balloon(pygame.sprite.Sprite):
    '''This class defines the sprite for our Balloon.'''
    def __init__(self, screen, balloonType): #Colour, type
        '''This initializer takes a screen surface as a parameter and the type of balloon, initializes
        the image and rect attributes.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load balloon images 
        self.red = pygame.image.load("sprites/balloons/red.png").convert()
        self.blue = pygame.image.load("sprites/balloons/blue.png").convert()
        self.green = pygame.image.load("sprites/balloons/green.png").convert()
        self.yellow = pygame.image.load("sprites/balloons/yellow.png").convert()
        self.black = pygame.image.load("sprites/balloons/black.png").convert()
        #Set colour and other information
        self.path = [100, -120, 115, 245, -150, 80, 360, -125, -115, -115, 115, -130, -160, -80]
        self.pathNum = 0
        self.travelx = 0
        self.travely = 0
        self.types = [None, self.red, self.blue, self.green, self.yellow, self.black] #red, blue, green, yellow, magenta   
        self.health = balloonType
        # Set the image and rect attributes for the balloon
        self.image = self.types[balloonType]
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centery = 235
        self.rect.right = 0 
 
        # Instance variables to keep track of the screen surface
        self.window = screen
        #Set other balloon stats
        self.speed = 3 + self.health        
        self.dx = 3 + self.health
        self.dy = 0
        self.frozen = 0 
        
    def getPosition(self):
        '''This function returns the position of the balloon in 3 frames'''
        return (self.rect.centerx + self.dx * 3, self.rect.centery + self.dy*3)
    
    def takeDamage(self, damage):
        '''This function takes in the damage, updates the balloon when a balloon 
        is hit, and will either make it take damage, or kill it depending on it's HP'''
        if damage >= self.health:
            self.kill()
            return self.health
        else:
            self.health -= damage
            self.speed = 3 + self.health
            #Update it's direction based on if it is travelling horizontally or  vertically
            if self.dx:
                self.dx = self.speed * (self.path[self.pathNum]/abs(self.path[self.pathNum]))
            else:
                self.dy = self.speed * (self.path[self.pathNum]/abs(self.path[self.pathNum]))
            self.image = self.types[self.health]
            self.image.set_colorkey((255, 255, 255))
            
    def freeze(self, time):
        '''This function takes in time and freezes the balloon for that number 
        of frames'''
        self.frozen += time
        
    def targetable(self):
        '''This function returns whether the balloon is targetable or not'''
        return not self.frozen
        
    def update(self):
        '''This method will be called automatically to reposition the
        balloon sprite on the screen.'''
        #If the balloon has travelled a >= distance of it's current path
        if self.travelx > abs(self.path[self.pathNum]) or self.travely > abs(self.path[self.pathNum]):
            #reset variables
            self.travelx = 0
            self.travely = 0
            #New path
            self.pathNum += 1
            #Check if it is going horizontally or vertical
            if (self.pathNum-1) % 2: 
                self.dx = self.speed * (self.path[self.pathNum]/abs(self.path[self.pathNum]))
                self.dy = 0
            else:
                self.dx = 0
                self.dy = self.speed * (self.path[self.pathNum]/abs(self.path[self.pathNum]))
        if self.frozen > 0:
            self.frozen -= 1
        else:
            self.rect.right += self.dx
            self.rect.bottom += self.dy 
            self.travelx += abs(self.dx)
            self.travely += abs(self.dy)
            
    
class Tower(pygame.sprite.Sprite):
    '''This class defines the sprite for the tower sprite.'''
    def __init__(self, screen, position, towerType): #image is currently color
        '''This initializer takes a screen surface as a parameter, it's y and x
        position relative to the center in a tuple, the type of tower initializes
        the image and rect attributes.'''
        #Load images
        self.normal = pygame.image.load("sprites/towers/normal.png")
        self.tack = pygame.image.load("sprites/towers/tack.png")
        self.freeze = pygame.image.load("sprites/towers/freeze.png")
        self.bomb = pygame.image.load("sprites/towers/bomb.png")
        self.superr = pygame.image.load("sprites/towers/super.png")
        self.images = [None, self.normal, self.tack, self.freeze, self.bomb, self.superr]        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the tower
        image = self.images[towerType]
        self.towerType = towerType
        self.org_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        #Upgrades
        self.upgraded1 = False
        self.upgraded2 = False
        
    def setTowerRangeObj(self, obj):
        '''This function takes in a towerRange object and sets a variable to it'''
        self.towerRange = obj
        
    def setTowerCircleObj(self, obj):
        '''This function takes in a towerCircle object and sets a variable to it'''
        self.towerCircle = obj
        
    def rotate(self, angle):
        '''This function takes in an angle and rotates the image.'''
        self.image = pygame.transform.rotate(self.org_image, angle)
        
    def setUpgrade(self, num):
        '''This function takes in a number and sets the relative upgrade variable
        to true'''
        if num == 1:
            self.upgraded1 = True
        else:
            self.upgraded2 = True
            
    def clicked(self, position):
        '''This function takes in a position and see if it collides with it's own rect'''
        return self.rect.collidepoint(position)

 
class TowerRange(pygame.sprite.Sprite):
    '''This class defines the sprite for a towerRange object, which is the main
    object for tower interactions'''
    def __init__(self, position, towerObject):
        '''This initializer takes a position and towerImage object. It initializes
        many stats and image properties.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image and rect attributes for the towerRange
        self.image = pygame.Surface((self.diameter, self.diameter))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.towerObject = towerObject
        #Universal stats of tower
        self.cooldown = 0
        
    def canAttack(self):
        '''This function returns True if the tower can attack, otherwise False'''
        return not self.cooldown
    
    def attack(self):
        '''This function adds its frame cooldown after attackign'''
        self.cooldown += self.attackSpeed    
            
    def getPosition(self):
        '''This function returns the position to create the bullet class'''
        return (self.rect.center, self.diameter)
    
    def getUpgradeCost(self, num):
        '''This function takes in an upgrade number and returns the cost of that 
        upgrade'''
        return self.upgradeCosts[num-1]    
    
    def update(self): 
        '''This method updates the tower's attack speed cooldown every frame'''
        if self.cooldown > 0: 
            self.cooldown -= 1   

class TowerCircle(pygame.sprite.Sprite):
    '''This class defines the sprite for the towerCircle object, which 
    shows the range of a tower.'''
    def __init__(self, position, diameter):
        '''This initializer takes a tuple as a position, diameter of the tower
        and intializes image properties.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load, Set the image and rect attributes for the Ball 
        self.image = pygame.image.load("sprites/circle.png")
        self.image = self.image = pygame.transform.scale(self.image, (diameter, diameter))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.centerPos = position
        
    def setVisible(self, visible):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''
        if visible:
            self.rect.center = self.centerPos
        else:
            self.rect.left = 800  
            
    def setRange(self, diameter):
        '''This function takes in a new diameter value and sets the diameter of 
        the object accordingly'''        
        self.image = pygame.image.load("sprites/circle.png")
        self.image = pygame.transform.scale(self.image, (diameter, diameter))
        self.rect = self.image.get_rect()
        self.rect.center = self.centerPos
            
class NormalTower(TowerRange):
    def __init__(self, position, towerObject):
        """Initializer for Normal Tower class, using parent __init__()
        method to make unique properties of the TowerRange"""
        #Tower stats
        self.diameter = 200
        self.radius = 100
        TowerRange.__init__(self, position, towerObject)
        #More tower stats
        self.attackSpeed = 20
        self.damage = 1
        self.piercing = False
        self.towerType = 1
        self.upgradeCosts = [250, 100]
        self.speed = "Normal"
        
    def upgrade(self, num):
        '''A function that takes in the upgrade number and gives unique properties
        to the tower'''
        if num == 1:
            self.piercing = True
        else:
            self.diameter = 250
            self.radius = 125
            TowerRange.__init__(self, self.rect.center, self.towerObject)
    
class TackTower(TowerRange):
    def __init__(self, position, towerObject):
        """Initializer for TackTower class, using parent __init__()
        method to make unique properties of the tack tower"""
        #Tower stats
        self.diameter = 140
        self.radius = 70
        TowerRange.__init__(self, position, towerObject)
        #More tower stats 
        self.attackSpeed = 60
        self.damage = 1
        self.piercing = False 
        self.towerType = 2
        #Using the radius and center of the object, a circle function is made. Using 5 different x values (left, mid-left, middle, mid-right, and right) the positive and negative y values are obtained. self.bulletPositions contains a list of 8 different positions that the tack tower must shoot towards. 
        self.bulletPositions = [(x * (self.radius/2) + (self.rect.centerx - self.radius), (self.radius**2 - (x * (self.radius/2) -self.radius)**2)**0.5 + self.rect.centery) for x in range(5)] + [(x * (self.radius/2) + (self.rect.centerx - self.radius), -(self.radius**2 - (x * (self.radius/2) -self.radius)**2)**0.5 + self.rect.centery) for x in range(1, 4)]
        self.upgradeCosts = [300, 150]
        self.speed = "Slow"
        
    def upgrade(self, num):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if num == 1:
            self.attackSpeed = 45
        else:
            self.diameter = 160
            self.radius = 80
            TowerRange.__init__(self, self.rect.center, self.towerObject)
    
class FreezeTower(TowerRange):
    def __init__(self, position, towerObject):
        """Initializer for FreezeTower class, using parent __init__()
        method to make unique properties of the freezeTower"""
        #Tower stats
        self.diameter = 120
        self.radius = 60
        TowerRange.__init__(self, position, towerObject)
        #Tower stats
        self.attackSpeed = 120
        self.damage = 1
        self.piercing = False      
        self.towerType = 3
        self.freezeTime = 60
        self.upgradeCosts = [400, 250]
        self.speed = "Very Slow"
            
    def upgrade(self, num):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if num == 1:
            self.freezeTime = 90
        else:
            self.diameter = 150
            self.radius = 75
            TowerRange.__init__(self, self.rect.center, self.towerObject) 
        
class BombTower(TowerRange):
    def __init__(self, position, towerObject):
        """Initializer for BombTower class, using parent __init__()
        method to make unique properties of the bomb tower"""
        #Tower stats
        self.diameter = 240
        self.radius = 120
        TowerRange.__init__(self, position, towerObject)
        #Tower stats
        self.attackSpeed = 70
        self.damage = 1
        self.piercing = False      
        self.towerType = 4
        self.upgradeCosts = [900, 150]
        self.speed = "Very Slow"
        
    def upgrade(self, num):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if num == 1:
            self.damage = 4
        else:
            self.diameter = 280
            self.radius = 140
            TowerRange.__init__(self, self.rect.center, self.towerObject)
        
class Explosion(pygame.sprite.Sprite):
    '''This class defines the sprite for the explosion class'''
    def __init__(self, position):
        '''This initializer takes in a position and creates an explosion there'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        #Set image
        self.image = pygame.Surface((95, 95)).convert()
         
        # Set the rect attributes 
        self.rect = self.image.get_rect()
        self.rect.center = position

class SuperTower(TowerRange):
    def __init__(self, position, towerObject):
        '''Initializer for SuperTower class, using parent __init__()
        method to make unique properties of the supertower'''
        #Tower stats
        self.diameter = 280
        self.radius = 140
        TowerRange.__init__(self, position, towerObject)
        #Tower stats
        self.attackSpeed = 3
        self.damage = 1
        self.piercing = False
        self.towerType = 1
        self.upgradeCosts = [2200, 5000]
        self.speed = "Wader fast"
    
    def upgrade(self, num):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if num == 1:
            self.diameter = 480
            self.radius = 240
            TowerRange.__init__(self, self.rect.center, self.towerObject)
        else:
            self.attackSpeed = 1
        
class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for top endzone'''
    def __init__(self, screen):
        '''This initializer takes a screen surface. It's position is on the 
        top of the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel tall 
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = -10
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self, value, right, xPos, yPos, fontSize):
        '''This initializer takes in a text value, if the rect will use the left
        or right side, the x and y positions of the text and fontSize. It will
        load the system font "Helvetica", andsets the text values'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.font = pygame.font.SysFont("Helvetica", fontSize)
        self.value = value
        self.image = self.font.render(str(self.value), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = yPos        
        self.right = right
        self.xPos = xPos
        if right:
            self.rect.right = xPos
        else:
            self.rect.left = xPos
        
    def setValue(self, value):
        '''This function takes in an integer and sets the text value to it'''
        self.value = value
        
    def getValue(self):
        '''This function returns the current text value'''
        return self.value
    
    def updateValue(self, value):
        '''This function takes in a value and updates the current value based on it'''
        self.value += value  
        
    def setVisible(self, visible):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if visible:
            self.rect.left = 550
        else:
            self.rect.left = 800        
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        self.image = self.font.render(str(self.value), 1, (255, 255, 255))
        
class TextLabel(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self, text, xPos, yPos):
        '''This initializer takes in a text value, x and y positions 
        and loads the system font "Helvetica", and sets the the image to the 
        text'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.font = pygame.font.SysFont("Helvetica", 25)
        self.image = self.font.render(text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = yPos    
        self.rect.left = xPos

class Bullet(pygame.sprite.Sprite):
    '''This class defines the sprite for the Bullet.'''
    def __init__(self, screen, towerPos, balloonPos, bulletType, damage, piercing):
        '''This initializer takes in the screen, towerPosition, balloonPosition
        and bullet properties to create a bullet.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images 
        self.dart = pygame.image.load("sprites/bullets/dart.png").convert()
        self.tack = pygame.image.load("sprites/bullets/tack.png").convert()
        self.bomb = pygame.image.load("sprites/bullets/bomb.png").convert()
        self.images = [None, self.dart, self.tack, None, self.bomb]
        #Variables
        self.bulletType = bulletType
        self.diameter = towerPos[1]
        self.radius = int(self.diameter)/2
        self.distanceTravelled = 0
        self.damage = damage
        self.piercing = piercing
        self.dy, self.dx = (balloonPos[1] - towerPos[0][1])/3, (balloonPos[0] - towerPos[0][0])/3
        self.maxDistance = (self.dx**2 + self.dy**2)**0.5*3+20
        # Set the image and rect attributes for the image
        self.screen = screen
        self.image = self.images[bulletType]
        self.image.set_colorkey((255, 255, 255))
        #Check if they are on the same x axis (can't divide by 0)
        if not balloonPos[1] - towerPos[0][1]:
            if towerPos[0][0] < balloonPos[0]:
                self.angle = 270
            else:
                self.angle = 90
        else:
            self.angle = math.degrees(math.atan((balloonPos[0] - towerPos[0][0])/ (balloonPos[1] - towerPos[0][1]))) 
        if towerPos[0][1] < balloonPos[1]:
            self.angle += 180
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = towerPos[0]
        self.hitBalloons = []
        
    def addBalloon(self, balloon):
        '''This function adds its hit balloons to its list.'''
        self.hitBalloons.append(balloon)
        
    def update(self):
        '''This method will be called automatically to update the position of
        the bullets every frame.'''
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        self.distanceTravelled += math.sqrt(self.dx**2 + self.dy**2)
        if self.distanceTravelled >= self.maxDistance:
            self.kill()           
        if self.rect.top > self.screen.get_height() or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > self.screen.get_width():
            self.kill()

class Button(pygame.sprite.Sprite): 
    '''This class defines the sprite for a general button.''' 
    def __init__(self, left, top, size, colour):
        '''This initializer takes in the left, top, size and colour of the 
        button'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the Button
        self.image = pygame.Surface(size) 
        self.image = self.image.convert()
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left
        
    def clicked(self, position):
        '''This function takes in a position and see if it collides with it's own rect'''
        return self.rect.collidepoint(position)

class TowerButton(Button):
    '''This class is a tower button and inherits from the general button class.'''
    def __init__(self, towerType):
        '''This initializer takes in the towerType and makes a towerButton
        relative to it.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load sprite images 
        self.normal = pygame.image.load("sprites/icons/dart.png").convert()
        self.tack = pygame.image.load("sprites/icons/tack.png").convert()
        self.freeze = pygame.image.load("sprites/icons/ice.png").convert()
        self.bomb = pygame.image.load("sprites/icons/bomb.png").convert()
        self.superr = pygame.image.load("sprites/icons/super.png").convert()
        #Info of each tower pretaining to: type, cash, image
        self.towerInfo = [None, (1, 250, self.normal), (2, 400, self.tack), (3, 850, self.freeze), (4, 900, self.bomb), (5, 4000, self.superr)]  
        # Set the image and rect attributes for the Button
        self.image = self.towerInfo[towerType][2]
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (29, 29))
        self.rect = self.image.get_rect()
        self.rect.center = (towerType * 29 + 474, 145)
        #Variables
        self.towerType = towerType
    
    def getTowerInfo(self):
        '''This function returns information on the tower button'''
        return self.towerInfo[self.towerType]
    
class Banner(pygame.sprite.Sprite):
    '''This class is a visual banner sprite.'''
    def __init__(self):
        '''This initializer sets properties of the banner.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the Button
        self.image = pygame.Surface((150, 475))
        self.image.fill((114, 155, 113))
        self.rect = self.image.get_rect()
        self.rect.top = 5
        self.rect.left = 483
        
class mouseImage(pygame.sprite.Sprite):
    '''This class sets the mouse image.'''
    def __init__(self):
        '''This initializer sets properties of the mouseImage.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images
        self.normal = pygame.image.load("sprites/towers/normal.png")
        self.tack = pygame.image.load("sprites/towers/tack.png")
        self.freeze = pygame.image.load("sprites/towers/freeze.png")
        self.bomb = pygame.image.load("sprites/towers/bomb.png")
        self.superr = pygame.image.load("sprites/towers/super.png")
        self.images = [None, self.normal, self.tack, self.freeze, self.bomb, self.superr]        
        # Set the image and rect attributes for the image
        self.image = pygame.Surface((0, 0)).convert()
        self.rect = self.image.get_rect()
        
    def setImage(self, image):
        '''This function takes in an image and sets the image of the object.'''
        if image:
            self.image = self.images[image]
        else:
            self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        
    def update(self):
        '''Every frame, update the mouse image.'''
        self.rect.center = pygame.mouse.get_pos()
        
class FreezeAnimation(pygame.sprite.Sprite):
    '''This class defines the sprite for the freeze animation.'''
    def __init__(self, position):
        '''This initializer takes in the position to where it will be played.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images 
        self.images = []
        self.picNum = 0
        for picNum in range(2, 12):
            newPic = pygame.image.load("sprites/animations/freeze/"+str(picNum)+".png")
            self.images.append(newPic)
        # Set the image and rect attributes for the Button
        self.image = pygame.image.load("sprites/animations/freeze/1.png").convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = position
        
    def update(self):
        '''This update loops through the images and kills it once it ends'''
        self.image = self.images[self.picNum].convert()
        self.image.set_colorkey((255,255,255))
        self.picNum += 1
        if self.picNum == 10: 
            self.kill()
            
class ExplosionAnimation(pygame.sprite.Sprite):
    '''This class defines the sprite for the explosion animation.'''
    def __init__(self, position):
        '''This initializer takes in the position to where it will be played.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images 
        self.images = []
        self.picNum = 0
        for picNum in range(2, 16):
            newPic = pygame.image.load("sprites/animations/explosion/"+str(picNum)+".png")
            self.images.append(newPic)
        # Set the image and rect attributes for the Button
        self.image = pygame.image.load("sprites/animations/explosion/1.png").convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = position
        
    def update(self):
        '''This update loops through the images and kills it once it ends'''
        self.image = self.images[self.picNum].convert()
        self.image.set_colorkey((255,255,255))
        self.picNum += 1
        if self.picNum == 14: 
            self.kill()
            
class popImage(pygame.sprite.Sprite):
    '''This class defines the sprite the popping image of the balloon.'''
    def __init__(self, position):
        '''This initializer takes in the position to where it will be played.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes for the Button
        self.image = pygame.image.load("sprites/balloons/pop.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frames = 3
        
    def update(self):
        '''This update checks if 3 frames have passed and kills it once it ends'''
        if self.frames:
            self.frames -= 1
        else:
            self.kill()
            
class Description(pygame.sprite.Sprite):
    '''This class defines the sprite for the tower description class.'''
    def __init__(self):
        '''This intializer sets properties of the images.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images 
        self.dart = pygame.image.load("sprites/descriptions/dart.png").convert()
        self.tack = pygame.image.load("sprites/descriptions/tack.png").convert()
        self.ice = pygame.image.load("sprites/descriptions/ice.png").convert()
        self.bomb = pygame.image.load("sprites/descriptions/bomb.png").convert()
        self.superr = pygame.image.load("sprites/descriptions/super.png").convert()
        self.images = [self.dart, self.tack, self.ice, self.bomb, self.superr]
        # Set the image and rect attributes for the Button
        self.image = self.dart
        self.towerType = 1
        self.rect = self.image.get_rect()
        self.rect.left = 800 
        self.rect.top = 165
        
    def setVisible(self, visible):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''         
        if visible:
            self.rect.left = 488
        else:
            self.rect.left = 800
            
    def setImage(self, towerType):
        '''This function takes in an towerType and sets the image of the object.'''
        self.towerType = towerType 
        self.image = self.images[towerType-1]
        
class Description2(pygame.sprite.Sprite):
    '''This class defines the sprite for the bought tower description class.'''
    def __init__(self):
        '''This intializer sets properties of the description.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes 
        self.image = pygame.image.load("sprites/descriptions/description2.png").convert()
        self.towerType = 1
        self.rect = self.image.get_rect()
        self.rect.left = 800 
        self.rect.top = 165
        
    def setVisible(self, visible):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if visible:
            self.rect.left = 488
        else:
            self.rect.left = 800
        
class Upgrade(Description):
    '''This class is an upgrade class, displaying images for all upgrades.'''
    def __init__(self, num):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Load images 
        self.dart1 = pygame.image.load("sprites/upgrades/dart1.png").convert()
        self.tack1 = pygame.image.load("sprites/upgrades/tack1.png").convert()
        self.freeze1 = pygame.image.load("sprites/upgrades/freeze1.png").convert()
        self.bomb1 = pygame.image.load("sprites/upgrades/bomb1.png").convert()
        self.superr1 = pygame.image.load("sprites/upgrades/super1.png").convert()
        self.dart2 = pygame.image.load("sprites/upgrades/dart2.png").convert()
        self.tack2 = pygame.image.load("sprites/upgrades/tack2.png").convert()
        self.freeze2 = pygame.image.load("sprites/upgrades/freeze2.png").convert()
        self.bomb2 = pygame.image.load("sprites/upgrades/bomb2.png").convert()
        self.superr2 = pygame.image.load("sprites/upgrades/super2.png").convert()        
        #Put them in lists
        self.upgrades1 = [self.dart1, self.tack1, self.freeze1, self.bomb1, self.superr1]        
        self.upgrades2 = [self.dart2, self.tack2, self.freeze2, self.bomb2, self.superr2]
        #Set image and rect properties
        self.image = self.dart1
        self.num = num
        self.rect = self.image.get_rect()
        self.rect.left = 800
        self.rect.top = 225       
    
    def setVisible(self, visible):
        '''This function takes in a boolean value and sets the visiblity of 
        the object accordingly'''        
        if visible:
            self.rect.left = 492 + (self.num-1) * 70
        else:
            self.rect.left = 800
            
    def setImage(self, towerType):
        '''This function takes in an towerType and sets the image of the object.'''
        if self.num-1:
            self.image = self.upgrades2[towerType-1]
        else:
            self.image = self.upgrades1[towerType-1]
            
    def clicked(self, position):
        '''This function takes in a position and see if it collides with it's own rect'''
        return self.rect.collidepoint(position)