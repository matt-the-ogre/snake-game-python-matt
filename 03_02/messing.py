# Import the Turtle Graphics and random modules
import turtle
import random
import time

# Define program constants
SEGMENT_SIZE = 20
STARTING_SEGMENTS = 20
STARTING_FOOD = 5
step_size = 5
WIDTH = 1920 # * SEGMENT_SIZE
HEIGHT = 1080 # * SEGMENT_SIZE
DELAY = int(1000/30)  # Milliseconds (the divisor is frames per second)
FOOD_SIZE = SEGMENT_SIZE / 2
quit_next = False
last_frame_time = time.time()

offsets = {
    "up": (0, step_size),
    "down": (0, -step_size),
    "left": (-step_size, 0),
    "right": (step_size, 0)
}


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # No self-collision simply by pressing wrong key.
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"


def stop_game():
    global quit_next
    quit_next = True

def game_loop():
    if quit_next:
        turtle.bye()
        return

    global last_frame_time
    this_time = time.time()
    frame_delta = this_time - last_frame_time
    last_frame_time = this_time

    stamper.clearstamps()  # Remove existing stamps made by stamper.
    food.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if new_head in snake or new_head[0] < (-WIDTH / 2) + SEGMENT_SIZE / 2 or new_head[0] > (WIDTH / 2)  - SEGMENT_SIZE / 2 \
            or new_head[1] < (-HEIGHT / 2)  + SEGMENT_SIZE / 2 or new_head[1] > (HEIGHT / 2)  - SEGMENT_SIZE / 2:
        reset()
    else:
        # Add new head to snake body.
        snake.append(new_head)

        # Check food collision
        if not food_collision():
            snake.pop(0)  # Keep the snake the same length unless fed.

        # Draw snake
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # draw food
        for foodItem in food_list:
            food.goto(foodItem)
            food.stamp()

        # Refresh screen
        screen.title(f"Snake Game. Score: {score} Speed: {step_size} Requested game speed: {DELAY}ms Actual game speed {int(frame_delta * 1000)}ms")
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, food_list, score, step_size
    for foodItem in food_list:
        if get_distance(snake[-1], foodItem) < SEGMENT_SIZE:
            score += 1  # score = score + 1
            step_size += 2 # increase speed
            food_list.remove(foodItem)
            food_list.append(get_random_food_pos())
            # food_pos = get_random_food_pos()
            # food.goto(food_pos)
            return True
    return False


def get_random_food_pos():
    # generate new random food position, but not too close to the end of the window
    x = random.randint(- WIDTH / 2 + FOOD_SIZE + SEGMENT_SIZE, WIDTH / 2 - FOOD_SIZE - SEGMENT_SIZE)
    y = random.randint(- HEIGHT / 2 + FOOD_SIZE + SEGMENT_SIZE, HEIGHT / 2 - FOOD_SIZE - SEGMENT_SIZE)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras' Theorem
    return distance


def reset():
    global score, snake, food_list, snake_direction, food_pos, step_size
    score = 0
    step_size = 5
    snake = []
    for i in range(0, STARTING_SEGMENTS):
        snake.append([i * step_size, 0])
    snake_direction = "up"
    food_list = []
    for i in range(0, STARTING_FOOD):
        food_list.append(get_random_food_pos())
    # food_pos = get_random_food_pos()
    # food.goto(food_pos)
    game_loop()


# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.title("Snake")
screen.bgcolor("green")
screen.tracer(0)  # Turn off automatic animation.

# Event handlers
screen.listen()
bind_direction_keys()
screen.onkey(stop_game, "q")
screen.onkey(reset, "r")

# Create a turtle to do your bidding
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color("coral")
stamper.shapesize(SEGMENT_SIZE / 20)
stamper.penup()

# Food
food = turtle.Turtle()
food.shape("triangle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Set animation in motion
reset()

# Finish nicely
turtle.done()
