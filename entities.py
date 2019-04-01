class BoundingBox:
    def __init__(self, radius, height, pos):
        self.radius = radius
        self.height = height
        self.pos = pos

    def isColliding(self, bb):
        d2 = (bb.pos[0] - self.pos[0]) ** 2 + (bb.pos[1] - self.pos[1]) ** 2  # distance squared from cylinder's axis
        dz = self.pos[2] + self.height * 0.5 - bb.pos[2] - bb.height * 0.5
        return (d2 < (self.radius ** 2 + bb.radius)) and dz ** 2 < (self.height * 0.5 + bb.height * 0.5) ** 2

    def isInside(self, pos):
        d2 = (pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2  # distance squared from cylinder's axis
        return (pos[2] > self.pos[2] and pos[2] < self.pos[2] + self.height) and d2 < self.radius ** 2


class EntityManadger():
    def __init__(self, *args, **kwargs):
        self.entities = {}
        self.deleted_entities = []

    def addEntity(self, name, entity):
        if not name in self.entities:
            self.entities[name] = entity

    def updateEntities(self):
        for e in self.entities:
            self.entities[e].update()
        self.check_collisions()
        self.deleted_entities

    def deleteEntities(self):
        for e in self.entities:
            if self.entities[e].disabled:
                self.deleted_entities.append(e)
        for e in self.deleted_entities:
            if e in self.entities:
                del self.entities[e]


    def getSpritesForRender(self):
        return sorted(self.entities, key=lambda k: self.entities[k].pos[1], reverse=True)

    def renderSprites(self):
        entities = self.getSpritesForRender()
        for e in entities:
            self.entities[e].render()

    def check_collisions(self):
        toCheck = self.entities.copy()
        for e in self.entities:
            entity = self.entities[e]
            del toCheck[e]
            for e2 in toCheck:
                entity2 = toCheck[e2]
                if entity.boundingBox.isColliding(entity2.boundingBox):
                    if isinstance(entity, Racoon) and isinstance(entity2, Food):
                        if not entity2.disabled:
                            entity2.disabled = True
                            entity.player.score += entity2.points

                    elif isinstance(entity2, Racoon) and isinstance(entity, Food):
                        if not entity.disabled:
                            entity.disabled = True
                            entity2.player.score += entity.points



class Entity:
    def __init__(self, name, *args, **kwargs):
        self.direction = kwargs.get('direction', +1)
        self.name = name
        self.pos = kwargs.get('pos', [0, 0, 0])
        self.isBouncy = kwargs.get('isBouncy', False)
        self.rot_speed = kwargs.get('rot_speed', 0)
        self.rotation = kwargs.get('rotation', 0)
        self.walk_velocity = [0, 0]
        self.life_spawn = kwargs.get('life_spawn', -1)
        self.age = 0
        self.velocity = kwargs.get('velocity', [0, 0, 0])
        self.sprite = kwargs.get('sprite', None)
        self.sprite_shadow = kwargs.get('sprite_shadow', None)
        self.limits = {'xmin': 0, 'xmax': 1600, 'ymin': 0, 'ymax': 300 * 1, 'zmin': 0}
        self.isPassable = kwargs.get('passable', True)
        self.boundingBox = kwargs.get('boundingbox', BoundingBox(50, 50, self.pos))
        self.disabled = False

    def update(self):
        self.age += 1
        self.apply_gravity()
        self.move()
        self.rotation += self.rot_speed
        self.boundingBox.pos = self.pos
        if self.age > self.life_spawn and self.life_spawn > -1:
            self.disabled = True

    def render(self):
        def transform(sprite, **kwarg):
            sprite.scale = (450 - self.pos[1] * 1.) / 450

            if sprite.scale_x * self.direction < 0:
                sprite.scale_x *= -1
            sprite.x = self.pos[0]
            sprite.y = self.pos[1]
            if not kwarg.get('isShadow', False):
                sprite.y += self.pos[2]
                sprite.rotation = self.rotation

        if self.sprite_shadow is not None:
            transform(self.sprite_shadow, isShadow=True)
            self.sprite_shadow.draw()
        if self.sprite is not None:
            transform(self.sprite)

        self.sprite.draw()

    def apply_gravity(self):
        if self.pos[2] > 0:
            self.velocity[2] -= 1

    def jump(self):
        if self.pos[2] == 0:
            self.velocity[2] += 20

    def walk(self, move):
        self.walk_velocity = move

    def move(self):

        if self.walk_velocity[0] > 0:
            self.direction = 1
        elif self.walk_velocity[0] < 0:
            self.direction = -1

        self.pos[0] += self.velocity[0] + self.walk_velocity[0]
        self.pos[1] += self.velocity[1] + self.walk_velocity[1]
        self.pos[2] += self.velocity[2]

        if self.pos[1] > self.limits['ymax']:
            self.pos[1] = self.limits['ymax']
            self.velocity[1] = 0
        if self.pos[1] < self.limits['ymin']:
            self.pos[1] = self.limits['ymin']
            self.velocity[1] = 0
        if self.pos[0] > self.limits['xmax']:
            self.pos[0] = self.limits['xmax']
            self.velocity[0] = 0
        if self.pos[0] < self.limits['xmin']:
            self.pos[0] = self.limits['xmin']
            self.velocity[0] = 0

        if self.pos[2] < self.limits['zmin']:
            self.pos[2] = self.limits['zmin']
            if self.isBouncy:
                if abs(self.velocity[2]) > 1:
                    self.velocity[0] *= 0.5
                    self.velocity[1] *= 0.5
                    self.velocity[2] *= -0.5
                    self.rot_speed *= 0.5
                else:
                    self.velocity[2] = 0
                    self.rot_speed = 0
            else:
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.velocity[2] = 0
                self.rot_speed = 0


class Food(Entity):
    def __init__(self, name, *args, **kwargs):
        Entity.__init__(self, name, *args, **kwargs)
        self.points = kwargs.get('points', 0)


class Racoon(Entity):
    def __init__(self, name, *args, **kwargs):
        Entity.__init__(self, name, *args, **kwargs)
        self.boundingBox = kwargs.get('boundingbox', BoundingBox(50, 100, self.pos))
        self.player = kwargs.get('player', None)

    def update(self):
        speed = 10
        move = [0, 0]
        if self.player is None:
            pass
        if self.player.held_keys['up']:
            move[1] += speed
        if self.player.held_keys['down']:
            move[1] -= speed
        if self.player.held_keys['left']:
            move[0] -= speed
        if self.player.held_keys['right']:
            move[0] += speed

        self.walk(move)

        if self.player.held_keys['jump']:
            self.jump()
        Entity.update(self)


