# Import the Turtle Graphics module
import turtle

# Define program constants
SEGMENT_SIZE = 10
WIDTH = 192 * SEGMENT_SIZE
HEIGHT = 108 * SEGMENT_SIZE
DELAY = int(1000/60)  # Milliseconds

offsets = {
    "up": (0, SEGMENT_SIZE),
    "down": (0, -SEGMENT_SIZE),
    "left": (-SEGMENT_SIZE, 0),
    "right": (SEGMENT_SIZE, 0)
}


def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"


def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"


def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"


def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

def stop_game():
    turtle.bye()

def game_loop():
    stamper.clearstamps()  # Remove existing stamps made by stamper.

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        turtle.bye()
    else:
        # Add new head to snake body.
        snake.append(new_head)

        # Remove last segment of snake.
        snake.pop(0)

        # Draw snake for the first time.
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # Refresh screen
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, DELAY)


# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.title("Snake")
screen.bgcolor("pink")
screen.tracer(0)  # Turn off automatic animation.

# Event handlers
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(stop_game, "q")

# Create a turtle to do your bidding
stamper = turtle.Turtle()
stamper.shape("square")
stamper.shapesize(SEGMENT_SIZE / 20)
stamper.penup()

# Create snake as a list of coordinate pairs.
snake = [[0, 0], [SEGMENT_SIZE, 0], [SEGMENT_SIZE * 2, 0], [SEGMENT_SIZE * 3, 0]]
snake_direction = "up"

# Draw snake for the first time.
for segment in snake:
    stamper.goto(segment[0], segment[1])
    stamper.stamp()

# Set animation in motion
game_loop()

# Finish nicely
turtle.done()
