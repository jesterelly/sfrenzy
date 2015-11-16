import bge
import random
import time


class Food:
    def __init__(self, own):
        self.owner = own
        own.collisionCallbacks.append(self.collide)

        for c in own.children:
            if c.name.endswith('armature'):
                c.playAction('FoodScale_Fast', 0, 5)

        self.mouth = None
        self.scale = 1.0

    def collide(self, other):
        if 'floor' in other:
            self.owner.endObject()
            bge.logic.foodspawner.food.remove(self)

    def update(self):
        own = self.owner
        if self.mouth is not None:

            pos = self.mouth.worldPosition.copy()
            pos[1] += 1.0
            own.worldPosition = own.worldPosition.lerp(pos, 0.1)
            self.scale -= 0.05
            own.scaling = [self.scale, self.scale, self.scale]
            if self.scale < 0.1:
                own.endObject()
                bge.logic.foodspawner.food.remove(self)

            return

        if own.worldPosition[2] < 0.0:
            own.endObject()
            bge.logic.foodspawner.food.remove(self)
            return

        own.applyMovement((0, 0, -0.01), False)
        own.applyRotation((0, 0, 0.017), False)


class FoodSpawner:
    def __init__(self, own):
        bge.logic.foodspawner = self
        self.owner = own
        self.items = ['banana', 'bread', 'lemon', 'orange']
        self.food = []
        self.next_spawn_time = time.monotonic()
        self.spawn_delay = 0.5  # Seconds

    def check(self, mouth):
        for f in list(self.food):
            if f.mouth is None:
                d = mouth.getDistanceTo(f.owner)
                if d < 1.0:
                    print ("eat")
                    f.mouth = mouth
                    f.owner.suspendDynamics()

    def update(self):
        now = time.monotonic()
        if now > self.next_spawn_time:
            self.next_spawn_time = now + self.spawn_delay

            obj = random.choice(self.items)
            spawn = random.choice(self.owner.children)

            scene = bge.logic.getCurrentScene()
            ob = scene.addObject(obj, spawn)
            self.food.append(Food(ob))

        for f in list(self.food):
            f.update()


def main(cont):
    own = cont.owner
    fs = own.get('FoodSpawner', None)
    if fs is None:
        own['FoodSpawner'] = FoodSpawner(own)
        return

    fs.update()