import pyglet
import pyglet.gl as gl
import random
from entities import *
from resources import *
from pyglet.window import key

window = pyglet.window.Window()
window.set_mouse_visible(False)

HEIGHT = 900
WIDTH = 1600

window.set_size(WIDTH, HEIGHT)

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

keys = key.KeyStateHandler()
window.push_handlers(keys)


class Player:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.score = 0
        self.held_keys = {'up': False, 'down': False, 'right': False, 'left': False, 'jump': False}
        self.commands = kwargs.get('commands', None)

    def detect_keys(self):
        # TO DO: add check for missing commands
        for k in self.held_keys:
            self.held_keys[k] = keys[self.commands[k]]


commands_1 = {'left': key.LEFT, 'right': key.RIGHT, 'up': key.UP, 'down': key.DOWN, 'jump': key.SPACE}
commands_2 = {'left': key.A, 'right': key.D, 'up': key.W, 'down': key.S, 'jump': key.E}
players = [Player('player1', commands=commands_1), Player('player2', commands=commands_2)]

def printScores():
    y0 = 0
    for p in players:
        score_label = pyglet.text.Label(p.name+': '+str(p.score),
                          font_name='Times New Roman',
                          font_size=36,
                          x=0, y=HEIGHT-20-y0,
                          anchor_x='left', anchor_y='center', color=(0, 0, 0, 255))
        y0 += 40
        score_label.draw()


entityManadger = EntityManadger()
entityManadger.addEntity('racoon', Racoon('racoon', pos=[WIDTH/2, 0, 0], sprite=racoon_sprite, sprite_shadow=shadow_sprite, player=players[0]))
entityManadger.addEntity('racoon_2', Racoon('racoon_2', pos=[WIDTH/2, 0, 0], sprite=racoon_sprite, sprite_shadow=shadow_sprite, player=players[1]))

spawned_items = 0

@window.event
def on_draw():
    window.clear()
    batch.draw()
    entityManadger.renderSprites()
    printScores()


def update(dt):
    global spawned_items
    global WIDTH

    for p in players:
        p.detect_keys()

    if random.randint(0, 100) < 1:
        speedy = random.random()*(-1)
        speedx = ((random.random() * 2) - 1) * 5
        rotation = 360*random.random()
        rot_speed = 5
        entityManadger.addEntity('melon'+str(spawned_items), Food('melon'+str(spawned_items), life_spawn=400, pos=[WIDTH/2, 250, 10], velocity=[speedx, speedy, 60],
                                                  sprite=melon_sprite, sprite_shadow=shadow_sprite, isBouncy=True, rotation=rotation, rot_speed=rot_speed, points=10))
        spawned_items += 1

    entityManadger.updateEntities()

pyglet.clock.schedule_interval(update, 1./60.)

player = pyglet.media.Player()
player.volume = 0.1
#player.queue(music)
player.play()


@window.event
def on_close():
    player.delete()


if __name__ == '__main__':
    pyglet.app.run()

