import cv2
import pygame
from random import randint


def rescale_position(window_size, image_size, max_val_position):
    scale = window_size[0]/image_size[0], window_size[1]/image_size[1]
    position = (max_val_position[0]*scale[0], max_val_position[1]*scale[1])
    return position


def get_image_lightest_pos(frame):
    frame_copy = frame.copy()
    frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_RGB2GRAY)
    frame_copy = cv2.GaussianBlur(frame_copy, (7, 7), 0)
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(frame_copy)
    # cv2.circle(frame, max_loc, 10, (0, 0, 255), 5)
    # cv2.imshow('FRUIT NINJA', frame)
    return max_loc


def main():
    pygame.init()
    window_size = win_x, win_y = 1280, 1024
    window = pygame.display.set_mode(window_size)
    camera = cv2.VideoCapture(0)

    shapes = []
    for i in range(20):
        pos = randint(50, win_x-50), randint(50, win_y-50)
        size = randint(0, 15)
        shapes.append(pygame.Rect(pos, (25 + size, 25 + size)))

    timer = pygame.time.Clock()
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

        #  cv2 part
        _, frame = camera.read()
        frame = cv2.flip(frame, 1)
        lightest_point_pos = get_image_lightest_pos(frame)

        #  pygame part
        knife_pos = rescale_position(window_size, (frame.shape[1], frame.shape[0]), lightest_point_pos)
        knife = pygame.Rect(knife_pos, (50, 50))
        timer.tick()
        print(timer.get_fps())

        for index, rect in enumerate(shapes):
            rect.move_ip(0, 1)
            if rect.y > win_y + 30:
                rect.y = -50

            if rect.colliderect(knife):
                pos = randint(50, win_x - 50), randint(50, win_y - 50)
                size = randint(0, 15)
                shapes[index] = pygame.Rect(pos, (25 + size, 25 + size))


        window.fill((10, 10, 10))
        pygame.draw.rect(window, (255, 0, 0), knife)
        for rect in shapes:
            pygame.draw.rect(window, (randint(0, 255), randint(0, 255), randint(0, 255)), rect)

        pygame.display.flip()

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

