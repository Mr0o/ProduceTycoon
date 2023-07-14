# this is where we will handle all of the collision physics
import pymunk

class Physics():
    def __init__(self):
        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.sleep_time_threshold = 0.3

    # run every frame
    def update(self, dt: float):
        self.space.step(dt)

    # apply a force to a person
    def applyForce(self, person, force):
        # apply the force to the person in pymunk space
        person.body.apply_force_at_local_point((force.x, force.y), (0, 0))
    