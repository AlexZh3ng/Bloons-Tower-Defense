'''
Name: Alex Zheng
Date: May 28, 2019
Description: This is a remake of Ninja Kiwi's Classic Balloon Tower Defense
Must pip install pygame to play!
'''

# I - IMPORT AND INITIALIZE
import pygame, btdSprites, random
pygame.init()
pygame.mixer.init()
     
def main():
    '''This function defines the 'mainline logic' for BTD'''
    #This list represents the levels (starting at 1) with each index representing the health of the balloon
    levels = [
        [16, 0, 0, 0, 0],
        [16, 5, 0, 0, 0],
        [22, 8, 0, 0, 0],
        [22, 8, 5, 0, 0], 
        [28, 11, 8, 0, 0],
        [22, 8, 4, 5, 0],
        [28, 11, 8, 8, 0],
        [56, 24, 0, 0, 0],
        [36, 30, 0, 0, 8],
        [40, 30, 15, 8, 0]
        ]
    
    # D - DISPLAY
    screen = pygame.display.set_mode((638, 505))
    pygame.display.set_caption("BTD")
     
    # ENTITIES
    # Background Image 
    background = pygame.image.load("sprites/map.png").convert()
    #Balloon test
    balloons = pygame.sprite.Group()
    #Tower test
    towers = pygame.sprite.Group() 
    #Tower range test
    towerRanges = pygame.sprite.Group()
    #Endzone
    endzone = btdSprites.EndZone(screen)
    #Bullets 
    bullets = pygame.sprite.Group()
    #User interface
    userInterface = pygame.sprite.Group()
    #banner
    banner = btdSprites.Banner()
    #Scorekeeper
    #Each stat is individualized because pygame font render doesn't recognise \n as an escape character
    levelText = btdSprites.ScoreKeeper(1, True, 630, 10, 25)
    cash = btdSprites.ScoreKeeper(650, True, 630, 35, 25)
    lives = btdSprites.ScoreKeeper(40, True, 630, 60, 25)
    speed = btdSprites.ScoreKeeper("Normal", False, 550, 185, 15)
    radius = btdSprites.ScoreKeeper("80", False, 550, 205, 15)
    speed.setVisible(False)
    radius.setVisible(False)
    label1 = btdSprites.TextLabel("Round:", 488, 10)
    label2 = btdSprites.TextLabel("Money:", 488, 35)
    label3 = btdSprites.TextLabel("Lives:", 488, 60)
    label4 = btdSprites.TextLabel("Build Towers", 488, 100)
    #Buttons 
    startBut = btdSprites.Button(488, 425,(140, 50),(89, 202, 87))
    #tower button
    towerButtons = pygame.sprite.Group()
    for num in range(1, 6):
        tower = btdSprites.TowerButton(num)
        towerButtons.add(tower)    
    #Upgrades
    upgrades = pygame.sprite.Group()
    upgrade1 = btdSprites.Upgrade(1)
    upgrade2 = btdSprites.Upgrade(2)    
    upgrades.add(upgrade1, upgrade2)
    #Tower descriptions
    description = btdSprites.Description()
    description2 = btdSprites.Description2()
    userInterface.add(banner, levelText, cash, lives, label1, label2, label3, label4, description2, upgrade1, upgrade2, speed, radius, description)
    #Explosion Group
    explosions = pygame.sprite.Group()
    #Animations 
    animations = pygame.sprite.Group()
    #Sounds
    pop = pygame.mixer.Sound("sprites/sounds/pop.wav")
    boom = pygame.mixer.Sound("sprites/sounds/boom.wav")
    clink = pygame.mixer.Sound("sprites/sounds/clink.wav")
    freezeSound = pygame.mixer.Sound("sprites/sounds/freeze.wav")
    #Mouse Image
    currentImage = btdSprites.mouseImage()
    #Collision groups
    towerButtonGroup = pygame.sprite.OrderedUpdates(towerButtons)
    towerGroup = pygame.sprite.OrderedUpdates(towerRanges) #Tower diameters
    balloonGroup = pygame.sprite.OrderedUpdates(balloons) #Balloons
    bulletGroup = pygame.sprite.OrderedUpdates(bullets)
    explosionGroup = pygame.sprite.OrderedUpdates(explosions)
    allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, userInterface, endzone, startBut, towerButtons, currentImage, animations)
    
    # ACTION
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    level = 0 
    lastSpawn = 0 #Used for balloon spawning
    frames = 10 #Difference of each frame before each spawn
    levelComplete = True 
    spawning = False
    placing = False
    rewarded = True
    # LOOP
    while keepGoing:
        # TIME
        clock.tick(30)
        # EVENT HANDLING: 
        pos = pygame.mouse.get_pos()  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONUP: 
                #Represents if the player is placing a tower onto the map 
                if placing and pos[0] < 488:
                    color = background.get_at(pos)
                    #Check if mouse is hovering a tower
                    hoveringTower = [tow for tow in towers if tow.clicked(pos)]
                    #Checks if the player places the tower on the road
                    if color[0] != color[1] != color[2] and not hoveringTower:
                        #Update cash
                        cash.updateValue(-towerInfo[1])
                        towerType = towerInfo[0]
                        #Create tower, tower range and tower circle object
                        newTower = btdSprites.Tower(screen, pos, towerInfo[0]) 
                        towers.add(newTower)
                        #Check for tower type and see which tower to spawn
                        if towerType == 1: #Normal tower
                            newTowerRange = btdSprites.NormalTower(pos, newTower) 
                        elif towerType == 2: #Tack tower
                            newTowerRange = btdSprites.TackTower(pos, newTower)
                        elif towerType == 3: #Freeze tower
                            newTowerRange = btdSprites.FreezeTower(pos, newTower)
                        elif towerType == 4: #Bomb tower
                            newTowerRange = btdSprites.BombTower(pos, newTower)
                        elif towerType == 5: #Super tower
                            newTowerRange = btdSprites.SuperTower(pos, newTower)
                        newTower.setTowerRangeObj(newTowerRange)
                        towerRanges.add(newTowerRange)                    
                        newTowerCircle = btdSprites.TowerCircle(newTower.rect.center, newTowerRange.diameter)
                        newTower.setTowerCircleObj(newTowerCircle)
                        userInterface.add(newTowerCircle)
                        #Update mouse image
                        currentImage.setImage(0)
                        #Update groups
                        towerGroup = pygame.sprite.OrderedUpdates(towerRanges)
                        allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations) 
                        placing = False
                #Check if player clicked the start button to spawn balloons
                elif startBut.clicked(pos) and levelComplete:
                    level += 1
                    levelText.setValue(level)
                    levelComplete = False
                    rewarded = False
                    spawning = True
                    #Copy balloon list to currentLevel
                    if level <= 10:
                        currentLevel = levels[level-1]
                    else:
                        #Infinite spawning algorithm (linear)
                        currentLevel = list(map(lambda x: x + 2* (level-9), [40, 30, 15, 8, 0]))
                #Check if player tried purchasing a new tower
                for tow in towerButtonGroup:               
                    if tow.clicked(pos):
                        #Make sure to make current tower circle invisible if it exists
                        try:
                            selectedTower.towerCircle.setVisible(False) 
                        except UnboundLocalError:
                            pass                             
                        towerInfo = tow.getTowerInfo()
                        if cash.value >= towerInfo[1]:
                            currentImage.setImage(towerInfo[0])
                            placing = True
                #Check if an already placed tower is clicked
                for tow in towers:
                    if tow.clicked(pos):
                        #Make sure to make current tower circle invisible if it exists
                        try:
                            selectedTower.towerCircle.setVisible(False) 
                        except UnboundLocalError:
                            pass                                            
                        selectedTower = tow
                        #Make UI for that certain tower(upgrades, stats, etc.) visible
                        description2.setVisible(True)
                        radius.setVisible(True)
                        radius.setValue(tow.towerRange.radius)
                        speed.setVisible(True)
                        speed.setValue(tow.towerRange.speed)
                        selectedTower.towerCircle.setVisible(True)
                        #Check if upgrades need to be displayed if not bought
                        if not tow.upgraded1: 
                            upgrade1.setVisible(True)
                            upgrade1.setImage(tow.towerType)
                        if not tow.upgraded2: 
                            upgrade2.setVisible(True)     
                            upgrade2.setImage(tow.towerType)
                #Check if upgrades are clicked
                for upgrade in upgrades:
                    if upgrade.clicked(pos) and cash.value > selectedTower.towerRange.getUpgradeCost(upgrade.num):
                        selectedTower.setUpgrade(upgrade.num)
                        #Make upgrade invisible
                        upgrade.setVisible(False)
                        #Update stats of towers and subtract cash
                        selectedTower.towerRange.upgrade(upgrade.num)     
                        cash.updateValue(-selectedTower.towerRange.getUpgradeCost(upgrade.num))
                        radius.setValue(selectedTower.towerRange.radius)
                        #Update circle visual
                        selectedTower.towerCircle.setRange(selectedTower.towerRange.diameter)
            elif event.type == pygame.KEYDOWN:
                #Check if escape key was pressed
                if event.key == pygame.K_ESCAPE:
                    placing = False 
                    #Remove mouse image
                    currentImage.setImage(0)
                    #Make sure to make current tower circle invisible if it exists
                    try:
                        selectedTower.towerCircle.setVisible(False) 
                    except UnboundLocalError:
                        pass
                    #Make other UI invisible
                    upgrade1.setVisible(False)
                    upgrade2.setVisible(False)
                    description2.setVisible(False)  
                    radius.setVisible(False)
                    speed.setVisible(False)
            elif event.type == pygame.MOUSEMOTION:
                #Check if tower buttons are hovered
                hovered = [tow.towerType for tow in towerButtons if tow.clicked(pos)]
                if hovered:             
                    #Set descriptions to be visible, else they will not
                    description.setVisible(True)
                    description.setImage(hovered[0])
                elif not hovered and description.towerType != 6:
                    description.setVisible(False)
        
        #Check if game has ended
        if lives.getValue() <= 0:
            keepGoing = False
        
        #Balloon spawning
        if not levelComplete:
            lastSpawn += 1
            #Check if balloons have stopped spawning
            if currentLevel == [0, 0, 0, 0, 0]:
                spawning = False
            #If a certain amount of frames have not been passed since the last balloon spawn, do nothing
            elif lastSpawn % frames:
                pass
            else:
                #Spawn a balloon of random health
                randomBalloon = random.randint(0, 4)
                while not currentLevel[randomBalloon]:
                    randomBalloon = random.randint(0, 4)
                currentLevel[randomBalloon] -= 1
                #Create balloon object and update groups
                balloon = btdSprites.Balloon(screen, randomBalloon + 1)
                balloons.add(balloon)
                balloonGroup = pygame.sprite.OrderedUpdates(balloons) #Balloons
                allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations)     
        
        #Check if level has been complete
        if not spawning and not balloons:
            levelComplete = True
            #Reward player for completing level
            if not rewarded:
                #Reduce spawn difference every 2 levels
                if not level % 2 and frames > 2:
                    frames -= 1
                cash.updateValue(100 + level)
                rewarded = True
            
        # Balloon endzone detection
        balloonEnd = pygame.sprite.spritecollide(endzone, balloonGroup, False)
        if balloonEnd:
            for collide in balloonEnd:
                lives.updateValue(-collide.health)
                collide.kill()
                balloons.remove(collide)

        #Tower ranges/balloon collision
        for tow in towerGroup:
            towerCollide = pygame.sprite.spritecollide(tow, balloonGroup, False)
            #Get a list of balloons that are not frozen
            targets = [ballo for ballo in towerCollide if ballo.targetable()]
            #Check if there are targets and there is no cooldown on tower
            if targets and tow.canAttack(): 
                tow.attack()
                towerPosition = tow.getPosition()
                towerType = tow.towerType
                #If it is a bomb/super/normal tower
                if towerType == 1 or towerType == 4:
                    #Check the farthest path for all the balloons within range
                    maxPath = max([target.pathNum for target in targets])
                    maxIndex = 0
                    maxDistance = 0
                    for index, bal in enumerate(targets):
                        #For each balloon, check if they are on the maximum path and find the highest distance travelled for that path
                        if bal.pathNum == maxPath and bal.travelx + bal.travely > maxDistance:
                            maxDistance = bal.travelx + bal.travely
                            maxIndex = index
                    #Create the bullet object to attack the farthest balloon, update groups
                    bullet = btdSprites.Bullet(screen, towerPosition, targets[maxIndex].getPosition(), towerType, tow.damage, tow.piercing)
                    bullets.add(bullet)
                    bulletGroup = pygame.sprite.OrderedUpdates(bullets)
                    allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations)  
                    #Rotate the tower relative to the balloon
                    tow.towerObject.rotate(bullet.angle + 90 - (towerType - 1) * 30 )
                #Check if the tower is a tack tower
                elif towerType == 2:
                    #Shoot in 8 directions
                    for position in tow.bulletPositions:
                        bullet = btdSprites.Bullet(screen, towerPosition, position, towerType, 1, False)
                        bullets.add(bullet)
                        bulletGroup = pygame.sprite.OrderedUpdates(bullets)
                        allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations)
                #Check if the tower is a freeze tower
                elif towerType == 3:
                    #Animation and sound
                    freezeSound.play()
                    freezeAnimation = btdSprites.FreezeAnimation(tow.rect.center)
                    animations.add(freezeAnimation)
                    allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations)   
                    #Freeze all balloons in collision
                    for ballo in targets: 
                        ballo.freeze(tow.freezeTime)
                
        #Bullet balloon collision
        for bullet in bulletGroup:
            balloonCollide = pygame.sprite.spritecollide(bullet, balloonGroup, False)
            #Check for collision and if balloon has not been already hit by the bullet (for piercing darts)
            if balloonCollide and balloonCollide[0] not in bullet.hitBalloons:
                #If the balloon is targetable or the tower is a bomb tower(since they can target frozen balloons)
                if balloonCollide[0].targetable() or bullet.bulletType == 4:
                    #Check if the balloon will die from the bullet
                    dead = balloonCollide[0].takeDamage(bullet.damage)
                    if dead:
                        cash.updateValue(dead)
                    else:
                        cash.updateValue(bullet.damage)
                    #If the bullet is a bomb create an explosion object and update groups
                    if bullet.bulletType == 4:
                        boom.play()
                        newExplosion = btdSprites.Explosion(bullet.rect.center)
                        explosions.add(newExplosion)
                        explosionGroup = pygame.sprite.OrderedUpdates(explosions)
                        explosionAnimation = btdSprites.ExplosionAnimation(bullet.rect.center)
                        animations.add(explosionAnimation)
                        allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations) 
                    else:
                        #Otherwise, play sounds and animations
                        pop.play()
                        newPop = btdSprites.popImage(balloonCollide[0].rect.center)
                        animations.add(newPop)   
                        allSprites = pygame.sprite.OrderedUpdates(towerRanges, towers, balloons, userInterface, endzone, startBut, bullets, towerButtons, currentImage, animations) 
                    #Check for piercing
                    if not bullet.piercing:
                        bullet.kill()
                    else:
                        bullet.addBalloon(balloonCollide[0])
                else:
                    clink.play()
                    
                
        #Explosion balloon collision
        for explode in explosionGroup:
            balloonCollide = pygame.sprite.spritecollide(explode, balloonGroup, False)
            for ballo in balloonCollide:
                dead = ballo.takeDamage(1)
                if dead:
                    cash.updateValue(dead)
                else:
                    cash.updateValue(1)
            explode.kill()
            
        # REFRESH SCREEN
        screen.blit(background, (0, 0)) #Refresh background is necessary for weird background glitches
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
    
    pygame.display.flip()
    pygame.mouse.set_visible(True)
 
    # Close the game window after 3 seconds
    pygame.time.delay(3000)
    pygame.quit()    
    
# Call the main function
main()        
