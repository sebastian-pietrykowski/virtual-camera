import pygame

from WorkMode import WorkMode
from view.Perspective import Perspective
from view.PhotoMaker import PhotoMaker
from view.World import World
from view.Camera import Camera
from FigureInitializer import FigureInitializer


def handle_keydown_event():
    match event.key:
        case pygame.K_r:
            photo_maker.make_photo()
        case pygame.K_i:
            world.rotate_up()
            camera.render()
        case pygame.K_k:
            world.rotate_down()
            camera.render()
        case pygame.K_j:
            world.rotate_left()
            camera.render()
        case pygame.K_l:
            world.rotate_right()
            camera.render()


def handle_key_pressed():
    key_pressed = pygame.key.get_pressed()
    actions = {
        pygame.K_w: lambda: (world.move_front(), camera.render()),
        pygame.K_s: lambda: (world.move_back(), camera.render()),
        pygame.K_a: lambda: (world.move_left(), camera.render()),
        pygame.K_d: lambda: (world.move_right(), camera.render()),
        pygame.K_3: lambda: (world.move_up(), camera.render()),
        pygame.K_x: lambda: (world.move_down(), camera.render()),
        pygame.K_EQUALS: lambda: (camera.zoom_in(), camera.render()),  # same key as '+' on keyboard
        pygame.K_MINUS: lambda: (camera.zoom_out(), camera.render())
    }

    for key, action in actions.items():
        if key_pressed[key]:
            action()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Virtual camera")
    screen = pygame.display.set_mode((Camera.SCREEN_WIDTH, Camera.SCREEN_HEIGHT))

    world = World(FigureInitializer.initialize_figures())
    camera = Camera(world, Perspective(), screen, WorkMode.WALLS)
    photo_maker = PhotoMaker(screen, camera)

    pygame.display.flip()
    camera.render()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown_event()
        handle_key_pressed()
        clock.tick(Camera.FRAME_RATE)
