# pygame_functions

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs at https://github.com/StevePaget/Pygame_Functions/issues


import pygame, sys, os

from pathlib import Path
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\', '/')
os.chdir(DIR)

pygame.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
hiddenSprites = pygame.sprite.OrderedUpdates()
screenRefresh = True
background = None


class Background():
    def __init__(self):
        self.colour = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        screen.blit(self.tiles[row][col], [xOff, yOff])
        screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()


class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, altDims = None):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        if altDims:
            img = pygame.transform.scale(img, (altDims[0]*frames, altDims[1]))
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        if screenRefresh:
            updateDisplay()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parseColour(fontColour)
        if background:
            self.background = parseColour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screenRefresh:
            updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColour))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pygame.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception(f"Error loading image: {fileName} – Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{xpos}, {ypos + 50}"
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(monitorWidth - sizex) // 2}, {(monitorHeight - sizey) // 2}"
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screenRefresh:
        updateDisplay()


def transformSprite(sprite, angle, scale, hflip=False, vflip=False):
    oldmiddle = sprite.rect.center
    if hflip or vflip:
        tempImage = pygame.transform.flip(sprite.images[sprite.currentImage], hflip, vflip)
    else:
        tempImage = sprite.images[sprite.currentImage]
    if angle != 0 or scale != 1:
        sprite.angle = angle
        sprite.scale = scale
        tempImage = pygame.transform.rotozoom(tempImage, -angle, scale)
    sprite.image = tempImage
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    sprite.mask = pygame.mask.from_surface(sprite.image)
    if screenRefresh:
        updateDisplay()


def setBackgroundColour(colour):
    background.setColour(colour)
    if screenRefresh:
        updateDisplay()


def setBackgroundImage(img):
    global background
    background.setTiles(img)
    if screenRefresh:
        updateDisplay()


def hideSprite(sprite):
    hiddenSprites.add(sprite)
    spriteGroup.remove(sprite)
    if screenRefresh:
        updateDisplay()


def showSprite(sprite):
    spriteGroup.add(sprite)
    if screenRefresh:
        updateDisplay()


def makeSprite(filename, frames=1, altDims = None):
    thisSprite = newSprite(filename, frames, altDims)
    return thisSprite


def pause(milliseconds, allowEsc=True):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    waittime = current_time + milliseconds
    updateDisplay()
    while not (current_time > waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and allowEsc):
            pygame.quit()
            sys.exit()
        current_time = pygame.time.get_ticks()


def makeLabel(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def changeLabel(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)
    updateDisplay()


def showLabel(labelName):
    textboxGroup.add(labelName)
    if screenRefresh:
        updateDisplay()


def hideLabel(labelName):
    textboxGroup.remove(labelName)
    if screenRefresh:
        updateDisplay()


def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    spriteGroup.clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)


def mousePressed():
    #pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def spriteClicked(sprite):
    action = False
    clicked = False
    pos = pygame.mouse.get_pos()

    if sprite.rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True
            action = True

    if pygame.mouse.get_pressed()[0] == 0:
        clicked = False
        action = False

    return action


def parseColour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def scrollBackground(x, y):
    global background
    background.scroll(x, y)


def setWindowTitle(string):
    pygame.display.set_caption(string)


if __name__ == "__main__":
    print("pygame_functions is not designed to be run directly.\n" \
        "See the wiki at https://github.com/StevePaget/Pygame_Functions/wiki/Getting-Started for more information.")
