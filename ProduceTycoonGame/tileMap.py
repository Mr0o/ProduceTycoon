import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Tile, Type, resetIDtiles


class TileMap():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos
        self.mov = Vector(0, 0)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.zoom = self.screen.get_width()

        self.rows = self.screen.get_height() // 25
        self.col = self.screen.get_width() // 25
        self.tileMapStartingPos = self.pos.copy()
        
        # create the grid of tiles
        self.tileMapGrid = self.createTileGrid(self.zoom, self.rows, self.col, self.tileMapStartingPos) 

        # creates rectangle size of screen for border
        self.rect = pygame.Rect((0, 0), (self.width, self.height))

        # highlighted tile
        self.highlightedTile = None

        # selected tile
        self.selectedTile = None

        # static surface for drawing tileMap
        self.staticSurface: pygame.Surface
        self.updateStaticImage()

    def createTileGrid(self, zoom: int, numRows: int, numCols: int, tileMapStartingPos: Vector) -> list[Tile]:
        resetIDtiles()
        # create grid of tiles
        tileSize = zoom // numCols

        # create a list of tiles (skipping the first row, to make room for buttons at the top)
        tileMapGrid: list[Tile] = []
        for row in range(1, numRows):
            for col in range(numCols):
                tileMapGrid.append(Tile(self.screen, Vector(tileMapStartingPos.x + col * tileSize, tileMapStartingPos.y + row * tileSize), tileSize))
        

        return tileMapGrid

    def events(self, mouseClicked: bool = False):
        # checking if mouse is hovering over tile
        self.highlightedTile = None
        for tile in self.tileMapGrid:
            tile.isHighlighted = False
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.highlightedTile = tile
                tile.isHighlighted = True
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

    def update(self):
        changed = False
        for tile in self.tileMapGrid:    
            tile.update()
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

        # drawing highlighted tile
        if self.highlightedTile is not None:
            self.highlightedTile.draw()

        # drawing selected tile
        if self.selectedTile is not None:
            self.selectedTile.draw()

        # draws border
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
        

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
        if tile.id - self.col - 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - self.col - 1))
        # top center
        if tile.id - self.col >= 0:
            neighbors.append(self.getTileByID(tile.id - self.col))
        # top right
        if tile.id - self.col + 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - self.col + 1))
        # left center
        if tile.id - 1 >= 0:
            neighbors.append(self.getTileByID(tile.id - 1))
        # right
        if tile.id + 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + 1))

        # bottom left
        if tile.id + self.col - 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.col - 1))
        # bottom
        if tile.id + self.col < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.col))
        # bottom right
        if tile.id + self.col + 1 < len(self.tileMapGrid):
            neighbors.append(self.getTileByID(tile.id + self.col + 1))

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
        self.updateStaticImage


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