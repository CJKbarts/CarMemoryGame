import pygame_functions as pyf
import pygame
from utilities import classes
import random

pyf.screenSize(1280, 720)


car = pyf.makeSprite('Pictures/Car1.png')
x = 640
y = 505
velocity = 3
pyf.moveSprite(car, x, y, True)
current_direction = 'up'

direction_list = ['up', 'left', 'right']
difficulty = classes.Difficulty()


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


kill = False
start = False

while not kill:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kill = True

    pyf.setBackgroundImage([['Pictures/Road_pics/crossroads.jpg', 'Pictures/Road_pics/horizontal.jpg'],
                            ['Pictures/Road_pics/vertical.jpg', 'Pictures/Road_pics/concrete.png']])

    pyf.showSprite(car)
    if current_direction == 'right':
        turn_car('left', 90)
    elif current_direction == 'left':
        turn_car('right', -90)
    current_direction = 'up'
    if y != 505:
        for i in range(-505, -350):
            pyf.pause(10)
            y += 1
            pyf.moveSprite(car, x, y, True)

    system_directions = []
    user_directions = []

    value_error = False
    difficulty_correct = False
    difficulty.choose_difficulty_succeeded = False
    instructional_label = pyf.makeLabel("Please enter your difficulty level", 40, 50, 50, "white", )
    difficulty_textbox = pyf.makeTextBox(50, 100, 50, 2, "", 3, 30)
    while not difficulty_correct or not difficulty.choose_difficulty_succeeded and not kill:
        pyf.showLabel(instructional_label)
        pyf.showTextBox(difficulty_textbox)
        try:
            difficulty.choose_difficulty(int(pyf.textBoxInput(difficulty_textbox)))
            pyf.hideTextBox(difficulty_textbox)
        except ValueError:
            value_error_message = pyf.makeLabel('Level can only be a number', 40, 50, 50, 'white', )
            pyf.hideLabel(instructional_label)
            pyf.hideTextBox(difficulty_textbox)
            pyf.showLabel(value_error_message)
            pyf.pause(2000)
            pyf.hideLabel(value_error_message)
            value_error = True
        else:
            difficulty_correct = True

        if not difficulty.choose_difficulty_succeeded and not value_error:
            level_error_message = pyf.makeLabel(f'You have only unlocked level {difficulty.unlocked_level}', 40, 50, 50,
                                                'white', )
            pyf.hideLabel(instructional_label)
            pyf.hideTextBox(difficulty_textbox)
            pyf.showLabel(level_error_message)
            pyf.pause(1500)
            pyf.hideLabel(level_error_message)
    pyf.hideLabel(instructional_label)
    pyf.hideTextBox(difficulty_textbox)

    instructional_label = pyf.makeLabel('Follow the following directions', 40, 50, 50, 'white')
    pyf.showLabel(instructional_label)
    for i in range(difficulty.number_of_turns):
        new_direction = random.choice(direction_list)
        directions_label = pyf.makeLabel(f'{i + 1}.{new_direction}', 30, 50, 100, 'white',)
        pyf.showLabel(directions_label)
        pyf.pause(1250)
        pyf.hideLabel(directions_label)
        system_directions.append(new_direction)
    pyf.changeLabel(instructional_label, 'Press enter to begin')

    turns_left = difficulty.number_of_turns

    while not start:
        if kill:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill = True

        if pyf.keyPressed("return"):
            pyf.changeLabel(instructional_label, 'Number of turns left:')
            for i in range(-505, -350):
                pyf.pause(10)
                y -= 1
                pyf.moveSprite(car, x, y, True)
                start = True

    turn_countdown = pyf.makeLabel(f'{turns_left}', 30, 50, 100, 'white')

    while start and turns_left != 0:
        if kill:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False

        pyf.changeLabel(turn_countdown, f'{turns_left}')
        pyf.showLabel(turn_countdown)

        if pyf.keyPressed("up"):
            if current_direction == 'right':
                turn_car('left', 90)
                current_direction = 'up'

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
                current_direction = 'right'

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
                current_direction = 'left'

            elif current_direction == 'right':
                turn_car('left', 90)
                turn_car('left', 0)
                current_direction = 'left'
            for i in range(513):
                pyf.pause(2)
                pyf.scrollBackground(5, 0)
            user_directions.append('left')
            turns_left -= 1
        directions_label = pyf.makeLabel(f'{i + 1}.{new_direction}', 30, 50, 100, 'white', )

    pyf.hideLabel(turn_countdown)
    pyf.hideLabel(instructional_label)

    pyf.pause(500)
    pyf.hideSprite(car)
    if user_directions == system_directions:
        pyf.setBackgroundImage('Pictures/win_pic.jpg')
        difficulty.unlock_level()
    else:
        pyf.setBackgroundImage('Pictures/lose_pic.jpg')

    pyf.pause(2000)

pygame.quit()
