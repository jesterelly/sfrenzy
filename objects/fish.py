import bge
import mathutils


P1 = {}
P1['up'] = bge.events.WKEY
P1['down'] = bge.events.SKEY
P1['left'] = bge.events.AKEY
P1['right'] = bge.events.DKEY

P2 = {}
P2['up'] = bge.events.IKEY
P2['down'] = bge.events.KKEY
P2['left'] = bge.events.JKEY
P2['right'] = bge.events.LKEY

P3 = {}
P3['up'] = bge.events.UPARROWKEY
P3['down'] = bge.events.DOWNARROWKEY
P3['left'] = bge.events.LEFTARROWKEY
P3['right'] = bge.events.RIGHTARROWKEY

P4 = {}
P4['up'] = bge.events.PAD8
P4['down'] = bge.events.PAD5
P4['left'] = bge.events.PAD4
P4['right'] = bge.events.PAD6

CONTROLS = [P1, P2, P3, P4]


class Fish:
    def __init__(self, ob, controls):
        self.ob = ob
        self.controls = controls

        self.move_speed = 0.1
        self.rotate_leftright = 0.1
        self.rotate_updown = 0.05

        self.last_heading = 1.0

        self.idle = True

        self.idle_action = 'idle'
        self.idle_start = 1
        self.idle_end = 30

        self.swim_action = 'swim'
        self.swim_start = 40
        self.swim_end = 72

    def play_idle(self):
        self.ob.playAction(self.idle_action, self.idle_start, self.idle_end,
                blendin=5, play_mode=bge.logic.KX_ACTION_MODE_LOOP)

    def play_swim(self):
        self.ob.playAction(self.swim_action, self.swim_start, self.swim_end,
                blendin=5, play_mode=bge.logic.KX_ACTION_MODE_LOOP)

    def update(self):
        ob = self.ob
        c = self.controls

        events = bge.logic.keyboard.events
        ACTIVE = bge.logic.KX_INPUT_ACTIVE

        move = mathutils.Vector()
        if events[c['up']] == ACTIVE:
            move[2] += 1.0

        if events[c['down']] == ACTIVE:
            move[2] -= 1.0

        if events[c['left']] == ACTIVE:
            move[0] -= 1.0

        if events[c['right']] == ACTIVE:
            move[0] += 1.0

        move.normalize()

        # Determine animation to play
        if not move.length:
            if not self.idle:
                self.idle = True
                self.play_idle()
        else:
            if self.idle:
                self.idle = False
                self.play_swim()

        # Align the fish
        trackVector = mathutils.Vector(move)
        if move[0]:
            # Hack to make the fish spin on que
            trackVector[1] = 0.1
            self.last_heading = move[0]

        if not move.length:
            trackVector[0] = self.last_heading
            trackVector[2] = 0.0

        ob.alignAxisToVect(trackVector, 1, self.rotate_leftright)
        ob.alignAxisToVect((0, 0, 1), 2, self.rotate_updown)


        # Move the fish
        move = move * self.move_speed
        ob.applyMovement(move, False)


class Seahorse(Fish):
    def __init__(self, ob, controls):
        Fish.__init__(self, ob, controls)

        self.idle_action = 'ArmatureAction'
        self.idle_start = 1
        self.idle_end = 60

        self.swim_action = 'ArmatureAction'
        self.swim_start = 1
        self.swim_end = 60


def generic(cont):
    own = cont.owner
    f = own.get('Fish', None)
    if f is None:
        if 'player' in own:
            c = CONTROLS[own['player'] - 1]
        else:
            c = CONTROLS[0]

        own['Fish'] = Fish(own, c)
        own['Fish'].play_idle()
        return

    f.update()


def seahorse(cont):
    own = cont.owner
    f = own.get('Fish', None)
    if f is None:
        if 'player' in own:
            c = CONTROLS[own['player'] - 1]
        else:
            c = CONTROLS[0]

        own['Fish'] = Seahorse(own, c)
        own['Fish'].play_idle()
        return

    f.update()