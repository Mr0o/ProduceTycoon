import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Tile, Type
from ProduceTycoonGame.placeableObject import PlaceableObject, Direction


class TileMap():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos
        self.mov = Vector(0, 0)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.zoom = self.screen.get_width()

        self.rows = self.screen.get_height() // 25
        self.cols = self.screen.get_width() // 25
        self.tileMapStartingPos = self.pos.copy()

        # create grid of tiles
        self.tileSize = self.zoom // self.cols
        
        # create the grid of tiles
        self.tileMapGrid = self.createTileGrid() 

        # creates rectangle size of screen for border
        self.rect = pygame.Rect((0, 0), (self.width, self.height))

        # highlighted tile
        self.highlightedTile = None

        # selected tile
        self.selectedTile = None

        # static surface for drawing tileMap
        self.staticSurface: pygame.Surface
        self.updateStaticImage()

        # tile lines surface (created once on init, assuming it will not change)
        self.tileLinesSurface = createStaticTileLineSurface(self, self.width, self.height)

    def createTileGrid(self) -> list[Tile]:
        Tile.static_id = 0 # reset the static id for assignment of the tiles

        # create a list of tiles (skipping the first row, to make room for buttons at the top)
        tileMapGrid: list[Tile] = []
        for row in range(1, self.rows):
            for col in range(self.cols):
                tileMapGrid.append(Tile(self.screen, Vector(self.tileMapStartingPos.x + col * self.tileSize, self.tileMapStartingPos.y + row * self.tileSize), self.tileSize))
        
        # set the edges of the tileMapGrid to be EDGE tiles
        for tile in tileMapGrid:
            if tile.pos.x == self.tileMapStartingPos.x or tile.pos.x == self.tileMapStartingPos.x + (self.cols - 1) * self.tileSize or tile.pos.y == self.tileMapStartingPos.y or tile.pos.y == self.tileMapStartingPos.y + (self.rows - 1) * self.tileSize:
                tile.type = Type.EDGE
            if tile.pos.y == self.tileMapStartingPos.y + self.tileSize:
                tile.type = Type.EDGE

        return tileMapGrid

    def selectTile(self, tile: Tile, mouseClicked: bool = False):
        if mouseClicked:
            if self.selectedTile is not None:
                # deselecting selected tile
                self.selectedTile.isSelected = False
            if self.selectedTile == tile:
                # deselecting tile
                tile.isSelected = False
                self.selectedTile = None
            else:
                # selecting tile
                self.selectedTile = tile
                self.selectedTile.isSelected = True
        

    def events(self, mouseClicked: bool = False):
        # checking if mouse is hovering over tile
        self.highlightedTile = None
        for tile in self.tileMapGrid:
            tile.isHighlighted = False
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.highlightedTile = tile
                tile.isHighlighted = True
                self.selectTile(tile, mouseClicked)

    def changeTileType(self, tile: Tile, placeableObject: PlaceableObject):
        if placeableObject.isPlaced and tile.rect.colliderect(placeableObject.rect):
            if tile.type == Type.WALKABLE:
                tile.type = Type.BOUNDARY

    def getTilesInRect(self, rect: pygame.Rect) -> list[Tile]:
        collidedTiles: list[Tile] = []
        for tile in self.tileMapGrid:
            if rect.colliderect(tile.rect):
                collidedTiles.append(tile)
        return collidedTiles

    def getMainTile(self, tile: Tile, placeableObject: PlaceableObject):
        if tile.rect.colliderect(placeableObject.rect) and placeableObject.mainTileID == -1 and placeableObject.isPlaced:
            placeableObject.mainTileID = tile.id

    def update(self, placeableObjects: list[PlaceableObject] = None):
        if placeableObjects is not None:
            for placeableObject in placeableObjects:
                for tile in self.tileMapGrid:  
                    self.getMainTile(tile, placeableObject)
                    self.changeTileType(tile, placeableObject)


        changed = False
        for tile in self.tileMapGrid:
            # check for any changes to tiles
            if tile.changed:
                tile.changed = False
                changed = True

        # update static surface if any tiles changed
        if changed:
            self.updateStaticImage()

    # update the static surface, use this instead of importing createStaticTileSurface in other files
    def updateStaticImage(self):
        self.staticSurface = createStaticTileSurface(self.tileMapGrid, self.width, self.height)

    def draw(self):
        # drawing tileMap
        self.screen.blit(self.staticSurface, (self.pos.x, self.pos.y))

        # # drawing highlighted tile
        # if self.highlightedTile is not None:
        #     self.highlightedTile.draw()

        # # drawing selected tile
        # if self.selectedTile is not None:
        #     self.selectedTile.draw()

        # draws border
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

    def drawTileLines(self):
        self.screen.blit(self.tileLinesSurface, (self.pos.x, self.pos.y))

    def getTileByID(self, tileID: int):
        return self.tileMapGrid[tileID]
    
    def getTileByPos(self, pos: Vector):
        for tile in self.tileMapGrid:
            # if pos collides with tile rect
            if tile.rect.collidepoint(pos.x, pos.y):
                return tile

    # returns the neighbors of a tile
    def getNeighbors(self, tile: Tile) -> list[Tile]:
        neighbors: list[Tile] = []

        # determine the neighbors by using the id
        # top left
        if tile.id - self.cols - 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - self.cols - 1))
        # top center
        if tile.id - self.cols >= 0:
            neighbors.append(self.getTileByID(tile.id - self.cols))
        # top right
        if tile.id - self.cols + 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - self.cols + 1))
        # left center
        if tile.id - 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - 1))
        # right
        if tile.id + 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + 1))

        # bottom left
        if tile.id + self.cols - 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.cols - 1))
        # bottom
        if tile.id + self.cols < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.cols))
        # bottom right
        if tile.id + self.cols + 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.cols + 1))

        return neighbors

        # get walkable tiles
    def getWalkableTiles(self) -> list[Tile]:
        walkableTiles: list[Tile] = []
        for tile in self.tileMapGrid:
            if tile.type == Type.WALKABLE:
                walkableTiles.append(tile)
        return walkableTiles
    
    def getNonWalkableTiles(self) -> list[Tile]:
        boundaryTiles: list[Tile] = []
        for tile in self.tileMapGrid:
            if tile.type != Type.WALKABLE:
                boundaryTiles.append(tile)
        return boundaryTiles
    
    def setTileType(self, tile: Tile, type: Type):
        tile.type = type
        self.updateStaticImage()


# create a surface of Tiles that can be used statically (this will not reflect changes to the tileMap unless a new static surface is created)
def createStaticTileSurface(tiles: list[Tile], width: int, height: int) -> pygame.Surface:
    staticSurface = pygame.Surface((width, height))
    staticSurface.fill((0, 0, 0))

    # get the original screen of the tiles
    ogScreen = tiles[0].screen

    for tile in tiles:
        tile.screen = staticSurface
        tile.draw()
        # restore the original screen of the tiles
        tile.screen = ogScreen

    return staticSurface


# create static surface of tile lines
def createStaticTileLineSurface(tileMap: TileMap, width: int, height: int) -> pygame.Surface:
    staticSurface = pygame.Surface((width, height))
    staticSurface.fill((0, 0, 0))

    # the surface should be transparent
    staticSurface.set_colorkey((0, 0, 0))

    numCols = tileMap.cols
    numRows = tileMap.rows

    color = (50, 50, 50)

    # draw horizontal lines
    for row in range(1, numRows-1):
        pygame.draw.line(staticSurface, color, (0, row * tileMap.tileSize), (width, row * tileMap.tileSize))

    # draw vertical lines
    for col in range(1, numCols):
        pygame.draw.line(staticSurface, color, (col * tileMap.tileSize, tileMap.tileSize), (col * tileMap.tileSize, height))

    return staticSurface