import pygame as py
import random
import asyncio

async def main():
    py.init()
    py.display.set_caption('Egg Game')
    screen = py.display.set_mode((720, 720))
    clock = py.time.Clock()
    running = True

    rectLen = 130
    cells = []
    activeCell = False
    otherCell = False

    font = py.font.Font(None, 69)

    class Cell:
        def __init__(self, pose, value):
            self.value = value
            self.pose = pose
            self.hover = False
            self.selected = False
            self.rect = py.Rect((80 + pose[0] * (rectLen + 10)), (80 + pose[1] * (rectLen + 10)), rectLen, rectLen)
        
        def render(self):
            color = 'red'
            if self.selected == True:
                color = 'green'
            elif self.value == 100:
                color = 'grey'

            py.draw.rect(screen, color, self.rect)
            if self.hover == True:
                py.draw.rect(screen, 'yellow', self.rect, 2, -2)

            text_surface = font.render(str(self.value), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        
        def cellOn(self, activeCell, otherCell):
            self.selected = True
            if activeCell == False:
                activeCell = self
            elif otherCell == False:    
                otherCell = self
            return activeCell, otherCell
        
        def cellOff(self):
            self.selected = False
            
    def compCells(activeCell, otherCell):
        x1, y1 = activeCell.pose
        x2, y2 = otherCell.pose

        if ajacent(x1, y1, x2, y2):
            if activeCell.value + otherCell.value <= 100:
                activeCell.value += otherCell.value

                for i in range(y2): # fix this part with animation
                    cells[x2][y2 - i].value = cells[x2][y2 - 1 - i].value
                cells[x2][0].value = random.randint(1,20)

    def ajacent(x1, y1, x2, y2):
        return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)

    for x in range(4):
        rows = []
        for y in range(4):
            cell = Cell((x, y), random.randint(1,20))

            rows.append(cell)
        cells.append(rows)

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                for x in cells:
                    for y in x:
                        if y.rect.collidepoint(event.pos) and y.value != 100:
                            activeCell, otherCell = y.cellOn(activeCell, otherCell)

        mouse_pos = py.mouse.get_pos()
        for x in cells:
            for y in x:
                if activeCell == False:
                    if y.rect.collidepoint(mouse_pos) and y.value != 100:
                        y.hover = True
                    else:
                        y.hover = False
                else:
                    if y.rect.collidepoint(mouse_pos) and y.value != 100 and ajacent(activeCell.pose[0], activeCell.pose[1], y.pose[0], y.pose[1]):
                        y.hover = True
                    else:
                        y.hover = False

        if otherCell != False:
            compCells(activeCell, otherCell)
            activeCell.cellOff()
            otherCell.cellOff()
            activeCell = False
            otherCell = False


        screen.fill("black")

        for x in cells:
            for y in x:
                y.render()

        py.display.flip()
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)


asyncio.run(main())
py.quit()