import pygame

class Map:
    def __init__(self, file):
        self.file = file
        self.data = []
        with open(self.file, 'r') as e:
            for line in e:
                self.data.append(line.strip())
        
        self.Map_Width = len(self.data[0]) #number of items in the first list
        self.Map_Height = len(self.data) #number of lists in self.data
        self.Width = self.Map_Width * 32 #gets the official width 
        self.Height = self.Map_Height * 32 #gets the official height

        
class Camera:
    def __init__(self, w, h):
        self.camera = pygame.Rect(0,0,w,h)
        self.width = w
        self.height = h

    def user(self, sprite):
        return sprite.rect.move(self.camera.topleft)

    def update(self, sprite):
        #Updates the camera relative to the sprite
        x = -sprite.rect.x + int(640/2)
        y = -sprite.rect.y + int(640/2)

        #sets Limits for the Camera so that once it hits the edge it stops
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - 640), x)
        y = max(-(self.height - 640), y)
        
        self.camera = pygame.Rect(x,y,self.width, self.height)
