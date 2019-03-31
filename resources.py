import pyglet

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(2)

image_racoon = pyglet.resource.image('racoon.png')
image_racoon.anchor_x = image_racoon.width/2
racoon_sprite = pyglet.sprite.Sprite(image_racoon)

background_image = pyglet.resource.image('background.png')
background_sprite = pyglet.sprite.Sprite(background_image, batch=batch, group=background)

image_sprites = pyglet.resource.image('sprites.png')

image_shadow = image_sprites.get_region(65, 370, 150, 60)
center_image(image_shadow)
shadow_sprite = pyglet.sprite.Sprite(image_shadow)
shadow_sprite.opacity = 64

image_melon = image_sprites.get_region(36, 740, 130, 130)
center_image(image_melon)
melon_sprite = pyglet.sprite.Sprite(image_melon)

#music = pyglet.resource.media('music.mp3')
sound = pyglet.resource.media('eating.ogg', streaming=False)