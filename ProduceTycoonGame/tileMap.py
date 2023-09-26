import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector

from enum import IntEnum

class Type(IntEnum):
    WALKABLE = 1
    BOUNDARY = 2
    EDGE = 3

WALKABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/FloorTile.png')

class Tile:
    id: int
    pos: Vector
    typeTile: Type = Type.WALKABLE
    rect: pygame.Rect
    parent: 'Tile' = None
    cost: int = 0
    vector: Vector = Vector(0, 0)
    changed: bool = False

    # Sattic Variables
    size = 0
    currentTile = 0
    image = WALKABLE_TILE_IMG

    @staticmethod
    def setSize(size):
        Tile.size = size

    @staticmethod
    def scaleImage():
        Tile.image = pygame.transform.scale(WALKABLE_TILE_IMG, (Tile.size, Tile.size))

    def __init__(self, pos: Vector, typeTile: Type = Type.WALKABLE):
        self.pos = pos
        self.typeTile = typeTile
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (Tile.size, Tile.size))
        self.setID()

    def setID(self):
        self.id = Tile.currentTile
        Tile.currentTile += 1

class TileMap:
    pos: Vector
    rows: int
    columns: int
    tileSize: int
    grid: list[Tile]

    # Static variables
    screen = pygame.Surface((0, 0))
    linesSurface = pygame.Surface((0, 0))
    staticSurface = pygame.Surface((0, 0))

    # Static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        TileMap.screen = screen

    @staticmethod
    def drawTileLines():
        TileMap.screen.blit(TileMap.lineSurface, (0, 0))

    @staticmethod
    def drawTiles():
        TileMap.screen.blit(TileMap.staticSurface, (0, 0))

    # Instance methods
    def __init__(self, pos: Vector):
        self.pos = pos
        self.rows = self.getRows()
        self.columns = self.getColumns()
        self.tileSize = self.createTileSize()

        # Tile static variables
        Tile.setSize(self.tileSize)
        Tile.scaleImage()
        
        self.grid = []
        self.createGrid()

        TileMap.lineSurface = createStaticLineSurface(self, 800, 600)
        TileMap.staticSurface = createStaticTileSurface(self.grid, 800, 600)

    def getRows(self):
        return int(TileMap.screen.get_height() / 25)

    def getColumns(self):
        return int(TileMap.screen.get_width() / 25)

    def createTileSize(self):
        return int(TileMap.screen.get_width() / self.columns)

    # Creating the grid of tiles
    def createGrid(self):
        for row in range(self.rows):
            y = row * self.tileSize
            for column in range(self.columns):
                x = column * self.tileSize
                # Check if edge tile
                if row == 0 or row == self.rows - 1 or column == 0 or column == self.columns - 1:
                    self.grid.append(Tile(Vector(x, y), Type.EDGE))
                # Else make a walkable tile
                else:
                    self.grid.append(Tile(Vector(x, y)))

    def getTileByID(self, tileID: int):
        return self.grid[tileID]

    def getTileByPos(self, pos: Vector):
        for tile in self.grid:
            rect = tile.rect
            if rect.collidepoint(pos.x, pos.y):
                return tile

    def getTilesInRect(self, rect: pygame.Rect) -> list[Tile]:
        tiles: list[Tile] = []
        for tile in self.grid:
            if rect.colliderect(tile.rect):
                tiles.append(tile)
        return tiles

    def draw(self):
        TileMap.drawTiles()
        
    # returns the neighbors of a tile
    def getNeighbors(self, tile: Tile) -> list[Tile]:
        neighbors: list[Tile] = []
        maxTile = len(self.grid) - 1
        minTile = 0

        # determine the neighbors by using the id
        topLeft = tile.id - self.columns - 1
        if  topLeft >= minTile:
            neighbors.append(self.getTileByID(topLeft))

        topCenter = tile.id - self.columns
        if topCenter >= minTile:
            neighbors.append(self.getTileByID(topCenter))

        topRight = tile.id - self.columns + 1
        if topRight >= minTile:
            neighbors.append(self.getTileByID(topRight))

        leftCenter = tile.id - 1
        if leftCenter >= minTile:
            neighbors.append(self.getTileByID(leftCenter))

        rightCenter = tile.id + 1
        if rightCenter <= maxTile:
            neighbors.append(self.getTileByID(rightCenter))

        bottomLeft = tile.id + self.columns - 1
        if bottomLeft <= maxTile:
            neighbors.append(self.getTileByID(bottomLeft))

        bottomCenter = tile.id + self.columns
        if bottomCenter <= maxTile:
            neighbors.append(self.getTileByID(bottomCenter))

        bottomRight = tile.id + self.columns + 1
        if bottomRight <= maxTile:
            neighbors.append(self.getTileByID(bottomRight))

        return neighbors

def createStaticTileSurface(tiles: list[Tile], width: int, height: int) -> pygame.Surface:
    staticSurface = pygame.Surface((width, height))
    staticSurface.fill((0, 0, 0))

    for tile in tiles:
        staticSurface.blit(tile.image, (tile.pos.x, tile.pos.y))

    return staticSurface

# create static surface of tile lines
def createStaticLineSurface(tileMap: TileMap, width: int, height: int) -> pygame.Surface:
    staticSurface = pygame.Surface((width, height))
    staticSurface.fill((0, 0, 0))

    # the surface should be transparent
    staticSurface.set_colorkey((0, 0, 0))

    numCols = tileMap.columns
    numRows = tileMap.rows

    color = (50, 50, 50)

    # draw horizontal lines
    for row in range(numRows):
        pygame.draw.line(staticSurface, color, (0, row * tileMap.tileSize), (width, row * tileMap.tileSize))

    # draw vertical lines
    for col in range(numCols):
        pygame.draw.line(staticSurface, color, (col * tileMap.tileSize, 0), (col * tileMap.tileSize, height))

    return staticSurface

def getMainTile(tile: Tile, currentObject):
        # Gets the first tile that collides with the object it sets it as the main tile
        if tile.rect.colliderect(currentObject.info.rect) and currentObject.info.mainTileID == -1:
            currentObject.setMainTileID(tile.id)

def changeTileType(tile: Tile, currentObject):
    # If the tile is walkable and the tile is colliding with the current object, change the tile type toboundary
    if tile.rect.colliderect(currentObject.info.rect):
        if tile.typeTile == Type.WALKABLE:
            tile.typeTile = Type.BOUNDARY
            tile.changed = True

def updateTileMap(tileMap, objects):
    # Loop through each object and 
    for currentObject in objects:
        if currentObject.info.placed:
            for tile in tileMap.grid:  
                getMainTile(tile, currentObject)
                changeTileType(tile, currentObject)