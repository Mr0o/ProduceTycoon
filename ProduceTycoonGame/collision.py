# this is where we will handle all of the collision physics
import pymunk

class Physics():
    def __init__(self, tiles: list, people: list):
        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.sleep_time_threshold = 0.3

        # add tiles to the pymunk space
        for tile in tiles:
            self.space.add(tile.body, tile.shape)

        # add people to the pymunk space
        for person in people:
            self.space.add(person.body, person.shape)
        

    # run every frame
    def update(self, dt: float):
        self.space.step(dt)

    # apply a force to a person
    def applyForce(self, person, force):
        # apply the force to the person in pymunk space
        person.body.apply_force_at_local_point((force.x, force.y), (0, 0))
        # set the person's velocity to the pymunk space velocity
        person.vel = person.body.velocity

    def addPerson(self, person):
        self.space.add(person.body, person.shape)

    def removePerson(self, person):
        self.space.remove(person.body, person.shape)

    def addTile(self, tile):
        self.space.add(tile.body, tile.shape)

    def removeTile(self, tile):
        self.space.remove(tile.body, tile.shape)
    