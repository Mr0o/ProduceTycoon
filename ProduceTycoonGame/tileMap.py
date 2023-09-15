import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.objectRegister import Object

from enum import Enum, IntEnum

class Type(IntEnum):
    WALKABLE = 1
    BOUNDARY = 2
    EDGE = 3

WALKABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/FloorTile.png')
BOUNDARY_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Barrier.png')

class TileInfo():
    pos: Vector
    typeTile: Type = Type.WALKABLE
    rect: pygame.Rect

    # Static variables
    size = 0
    screen = pygame.Surface((0, 0))

    def __init__(self, pos, typeTile):
        self.pos = pos
        self.typeTile = typeTile
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (TileInfo.size, TileInfo.size))

    @staticmethod
    def setSize(size):
        TileInfo.size = size

    @staticmethod
    def setScreen(screen):
        TileInfo.screen = screen

class Tile():
    id: int
    info: TileInfo
    image: pygame.Surface
    currentTile: int = -1

    # Sattic Variables
    tiles = []
    WALKABLE_TILE_IMG_SCALED = pygame.transform.scale(WALKABLE_TILE_IMG.copy(), (TileInfo.size, TileInfo.size))
    BOUNDARY_TILE_IMG_SCALED = pygame.transform.scale(BOUNDARY_TILE_IMG.copy(), (TileInfo.size, TileInfo.size))

    def __init__(self, pos: Vector, typeTile: Type = Type.WALKABLE):
        self.info = TileInfo(pos, typeTile)
        self.setImage()
        self.setID()
        Tile.tiles.append(self)

    def setType(self, typeTile: Type):
        self.info.type = typeTile
        self.changed = True

    def setImage(self):
        match self.info.typeTile:
            case Type.WALKABLE:
                self.image = Tile.WALKABLE_TILE_IMG_SCALED
            case Type.EDGE:
                self.image = Tile.WALKABLE_TILE_IMG_SCALED
            case Type.BOUNDARY:
                self.image = Tile.BOUNDARY_TILE_IMG_SCALED

    def setID(self):
        self.id = Tile.currentTile
        Tile.currentTile += 1

    def draw(self):
        TileInfo.screen.blit(self.image, (self.info.pos.x, self.info.pos.y))

class TileMapInfo():
    pos: Vector
    rows: int
    columns: int
    tileSize: int

    # Static variables
    screen = pygame.Surface((0, 0))

    # Static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        TileMapInfo.screen = screen

    def __init__(self, pos, rows, columns):
        self.pos = pos
        self.rows = rows
        self.columns = columns

        self.tileSize = self.createTileSize()

        # Define TileInfo static variables
        TileInfo.setSize(self.tileSize)
        TileInfo.setScreen(TileMapInfo.screen)

    def createTileSize(self):
        return int(TileMapInfo.screen.get_width() / self.columns)

class TileMap():
    info: TileMapInfo
    pos: Vector
    grid: []

    # Static variables
    linesSurface = pygame.Surface((0, 0))

    # Static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        TileMapInfo.setScreen(screen)
    
    @staticmethod
    def drawTileLines():
        TileMapInfo.screen.blit(TileMap.lineSurface, (0, 0))

    # Instance methods
    def __init__(self, pos: Vector):
        # Initializing the tileMap
        self.pos = pos
        rows = self.getRows()
        columns = self.getColumns()
        self.info = TileMapInfo(self.pos, rows, columns)
        TileMap.lineSurface = createStaticLineSurface(self, 800, 600)

        self.createGrid()
        self.grid = Tile.tiles

    def getRows(self):
        return int(TileMapInfo.screen.get_height() / 25)

    def getColumns(self):
        return int(TileMapInfo.screen.get_width() / 25)

    # Creating the grid of tiles
    def createGrid(self):
        for row in range(self.info.rows):
            x = row * self.info.tileSize
            for column in range(self.info.columns):
                y = column * self.info.tileSize
                # Check if edge tile
                if row == 0 or row == self.info.rows - 1 or column == 0 or column == self.info.columns - 1:
                    Tile(Vector(x, y), Type.EDGE)
                # Else make a walkable tile
                else:
                    Tile(Vector(x, y))

    def getTileByID(self, tileID: int):
        return self.grid[tileID]

    def getTileByPos(self, pos: Vector):
        for tile in self.grid:
            rect = tile.info.rect
            if rect.collidepoint(pos.x, pos.y):
                return tile

    def getTilesInRect(self, rect: pygame.Rect) -> list[Tile]:
        tiles: list[Tile] = []
        for tile in self.grid:
            if rect.colliderect(tile.info.rect):
                tiles.append(tile)
        return tiles


    # Main methods
    def events(self, mouseClicked: bool = False):
        pass

    def draw(self):
        for tile in self.grid:
            tile.setImage()
            tile.draw()

# returns the neighbors of a tile
def getNeighbors(tile: Tile) -> list[Tile]:
    neighbors: list[Tile] = []
    maxTile = len(self.tileMapGrid) - 1
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

# create static surface of tile lines
def createStaticLineSurface(tileMap: TileMap, width: int, height: int) -> pygame.Surface:
    staticSurface = pygame.Surface((width, height))
    staticSurface.fill((0, 0, 0))

    # the surface should be transparent
    staticSurface.set_colorkey((0, 0, 0))

    numCols = tileMap.info.columns
    numRows = tileMap.info.rows

    color = (50, 50, 50)

    # draw horizontal lines
    for row in range(numRows):
        pygame.draw.line(staticSurface, color, (0, row * tileMap.info.tileSize), (width, row * tileMap.info.tileSize))

    # draw vertical lines
    for col in range(numCols):
        pygame.draw.line(staticSurface, color, (col * tileMap.info.tileSize, tileMap.info.tileSize), (col * tileMap.info.tileSize, height))

    return staticSurface