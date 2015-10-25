from bge import logic
from random import randint, shuffle
from time import time


def main(cont):
    scene = logic.getCurrentScene()
    spawner = cont.owner
    spawners = [ob for ob in spawner.children]
    shuffle(spawners)

    if not hasattr(logic, 'zero_t'):
        logic.zero_t = time()
        logic.done = 0
        logic.score = 0

    t = time() - logic.zero_t

    items = ['banana', 'bread', 'lemon', 'orange']
    num = round(t / 100000) + 3

    if round(t) != logic.done:
        for e in range(num):
            obj = items[randint(0,len(items)-1)]
            scene.addObject(obj, spawners[e], 1500)
        logic.done = round(t)
