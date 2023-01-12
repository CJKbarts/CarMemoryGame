import pygame
import pygame_functions as pyf
import random
from utilities import classes


pyf.screenSize(1280, 720)
car = pyf.makeSprite('Pictures/Car1.png')
x = 640
y = 505
velocity = 3
pyf.moveSprite(car, x, y, True)

current_direction = 'up'

pastel_blue = (57, 157, 207)
difficulty = classes.Difficulty()


def make_button(image, scale, xpos, ypos):
    button_name = pyf.makeSprite(image)
    pyf.moveSprite(button_name, xpos, ypos, True)
    pyf.transformSprite(button_name, 0, scale)
    pyf.showSprite(button_name)
    return button_name


def generate_route():
    pyf.setBackgroundImage('Pictures/directions/instructions.jpg')
    system_directions = []
    direction_syntax = ['right', 'left', 'up']
    pyf.pause(1000)
    turn_count = 0
    turn_count_label = pyf.makeLabel(f"Number of turns: {turn_count}", 50, 0, 0, 'black', 'aberus')
    try:
        for i in range(difficulty.number_of_turns):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            addition = random.choice(direction_syntax)
            system_directions.append(addition)
            if addition == 'up':
                pyf.setBackgroundImage('Pictures/directions/up.jpg')
            elif addition == 'left':
                pyf.setBackgroundImage('Pictures/directions/left.jpg')
            else:
                pyf.setBackgroundImage('Pictures/directions/right.jpg')
            pyf.pause(1300)
            pyf.setBackgroundColour('white')
            pyf.pause(500)
            turn_count += 1
            pyf.changeLabel(turn_count_label, f"Number of turns: {turn_count}")
            pyf.showLabel(turn_count_label)
        pyf.pause(1000)
        pyf.hideLabel(turn_count_label)
        pyf.setBackgroundImage('Pictures/Countdown/start.jpg')
        pyf.pause(1500)
    except Exception:
        pygame.quit()
        quit()
    return system_directions


def turn_car(direction, current_angle):
    if direction == 'right':
        for frame in range(6):
            pyf.pause(50)
            current_angle += 15
            pyf.transformSprite(car, current_angle, 1)

    elif direction == 'left':
        for frame in range(6):
            pyf.pause(50)
            current_angle -= 15
            pyf.transformSprite(car, current_angle, 1)


def get_directions(system_directions, y=y, x=x):
    start = False
    pyf.setBackgroundImage([['Pictures/Road_pics/crossroads.jpg', 'Pictures/Road_pics/horizontal.jpg'],
                            ['Pictures/Road_pics/vertical.jpg', 'Pictures/Road_pics/concrete.png']])
    pyf.showSprite(car)
    user_directions = []
    current_direction = 'up'

    instructional_label = pyf.makeLabel('Press enter to begin', 40, 50, 50, 'white')
    pyf.showLabel(instructional_label)
    turns_left = difficulty.number_of_turns
    turn_countdown = pyf.makeLabel(f'{turns_left}', 30, 50, 100, 'white')

    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if pyf.keyPressed("return"):
                pyf.changeLabel(instructional_label, 'Number of turns left:')
                for i in range(-505, -350):
                    pyf.pause(10)
                    y -= 1
                    pyf.moveSprite(car, x, y, True)
                    start = True

    while turns_left != 0:
        pyf.showLabel(turn_countdown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if pyf.keyPressed("up"):
                if current_direction == 'right':
                    turn_car('left', 90)
                elif current_direction == 'left':
                    turn_car('right', -90)
                current_direction = 'up'

                for i in range(285):
                    pyf.pause(2)
                    pyf.scrollBackground(0, 5)
                user_directions.append('up')
                turns_left -= 1

            elif pyf.keyPressed("right"):
                if current_direction == 'up':
                    turn_car('right', 0)
                elif current_direction == 'left':
                    turn_car('right', -90)
                    turn_car('right', 0)
                current_direction = 'right'

                for i in range(513):
                    pyf.pause(2)
                    pyf.scrollBackground(-5, 0)
                user_directions.append('right')
                turns_left -= 1

            elif pyf.keyPressed("left"):
                if current_direction == 'up':
                    turn_car('left', 0)
                elif current_direction == 'right':
                    turn_car('left', 90)
                    turn_car('left', 0)
                current_direction = 'left'

                for i in range(513):
                    pyf.pause(2)
                    pyf.scrollBackground(5, 0)
                user_directions.append('left')
                turns_left -= 1

            pyf.changeLabel(turn_countdown, f'{turns_left}')
            pyf.showLabel(turn_countdown)

    pyf.hideLabel(turn_countdown)
    pyf.hideLabel(instructional_label)

    pyf.pause(500)
    pyf.hideSprite(car)
    pyf.transformSprite(car, 0, 1)
    x = 640
    y = 505
    pyf.moveSprite(car, x, y, True)

    if user_directions == system_directions:
        pyf.setBackgroundImage('Pictures/win_pic.jpg')
        difficulty.unlock_level()
    else:
        pyf.setBackgroundImage('Pictures/lose_pic.jpg')

    pyf.pause(1000)


def main_game():
    quit_game = False
    current_difficulty = 1
    start = False
    pyf.setBackgroundColour(pastel_blue)
    level_button_label = pyf.makeLabel(str(current_difficulty), 80, 630, 337, 'black', 'aberus')
    difficulty_instructions = pyf.makeLabel('Choose your difficulty', 100, 0, 0, 'black', 'aberus')
    pyf.showLabel(level_button_label)
    pyf.showLabel(difficulty_instructions)
    level_button = make_button("Pictures/button.png", 3.5, 640, 360)
    left_button = make_button('Pictures/l-arrow.png', .5, 433, 360)
    right_button = make_button('Pictures/r-arrow.png', .5, 847, 360)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    def hide_buttons_and_text():
        pyf.hideSprite(level_button)
        pyf.hideSprite(left_button)
        pyf.hideSprite(right_button)
        pyf.hideLabel(difficulty_instructions)
        pyf.hideLabel(level_button_label)

    def show_buttons_and_text():
        pyf.showSprite(level_button)
        pyf.showSprite(left_button)
        pyf.showSprite(right_button)
        pyf.showLabel(difficulty_instructions)
        pyf.showLabel(level_button_label)

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if pyf.spriteClicked(left_button):
                if current_difficulty > 1:
                    current_difficulty -= 1
                    pyf.changeLabel(level_button_label, str(current_difficulty))
                    pyf.showLabel(level_button_label)
                else:
                    hide_buttons_and_text()
                    pyf.changeLabel(difficulty_instructions, "There is no level 0")
                    pyf.showLabel(difficulty_instructions)
                    pyf.pause(1000)
                    pyf.changeLabel(difficulty_instructions, "Choose your difficulty level")
                    show_buttons_and_text()

            if pyf.spriteClicked(right_button):
                if current_difficulty < difficulty.unlocked_level:
                    current_difficulty += 1
                    pyf.changeLabel(level_button_label, str(current_difficulty))
                    pyf.showLabel(level_button_label)
                else:
                    hide_buttons_and_text()
                    pyf.changeLabel(difficulty_instructions, f'You have only unlocked level {difficulty.unlocked_level}')
                    pyf.showLabel(difficulty_instructions)
                    pyf.pause(1000)
                    pyf.changeLabel(difficulty_instructions, "Choose your difficulty level")
                    show_buttons_and_text()

            if pyf.spriteClicked(level_button):
                hide_buttons_and_text()
                difficulty.choose_difficulty(current_difficulty)
                get_directions(generate_route())
                quit_game = True
