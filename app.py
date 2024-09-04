import random
import time
import turtle

FRAME_RATE = 30  # Frames per second
TIME_FOR_1_FRAME = 1 / FRAME_RATE  # Seconds
CANNON_STEP = 20
LASER_LENGTH = 50
LASER_SPEED = 25
ALIEN_SPAWN_INTERVAL = 2  # Seconds
ALIEN_SPEED = 2
BACKGROUND_SPEED = 2  # Speed of background scroll

window = turtle.Screen()
window.tracer(0)
window.bgcolor(0.2, 0.2, 0.2)
window.title("The Real Python Space Invaders")

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 3
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# Create space background
background = turtle.Turtle()
background.hideturtle()
background.penup()
background.speed(0)
background.color(0.1, 0.1, 0.2)  # Darker background color
background.setposition(LEFT, TOP)
background.shapesize(stretch_wid=(window.window_height() / 20), stretch_len=(window.window_width() / 20))
background.shape("square")

def draw_background():
    global background_y
    background_y -= BACKGROUND_SPEED
    if background_y < -TOP:
        background_y = TOP
    background.setposition(LEFT, background_y)

# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("square")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0  # -1, 0 or 1 for left, stationary, right

# Create turtle for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []
level = 1  # Current level
hits_required = {}  # Dictionary to track hits required for each alien
hits_to_level_up = 3  # Hits required to level up

def create_alien(alien_size):
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(alien_size)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    alien.hits = level  # Set hits required based on the current level
    aliens.append(alien)
    hits_required[alien] = level

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(random.random(), random.random(), random.random())
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)  # Set the laser size to be short
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)  # Position laser above cannon
    laser.setheading(90)
    laser.showturtle()  # Show the laser
    lasers.append(laser)

def move_laser(laser_instance):
    laser_instance.forward(LASER_SPEED)
    # Remove laser if it goes off-screen
    if laser_instance.ycor() > TOP:
        remove_sprite(laser_instance, lasers)

window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def level_up():
    global level, hits_to_level_up
    level += 1
    hits_to_level_up += level
    for alien in aliens:
        hits_required[alien] = level

draw_cannon()

# Initialize background position
background_y = TOP

# Game loop
alien_timer = 0
game_timer = time.time()
score = 0
hits = 0
game_running = True
while game_running:
    timer_this_frame = time.time()
    time_elapsed = time.time() - game_timer
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}\nLevel: {level}",
        font=("Courier", 20, "bold"),
    )

    # Draw and move background
    draw_background()

    # Update cannon position based on movement flag
    new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
    if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
        cannon.setx(new_x)
    draw_cannon()

    # Move all lasers
    for laser in lasers.copy():
        move_laser(laser)
        # Check for collision with aliens
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(laser, lasers)
                hits_required[alien] -= 1
                if hits_required[alien] <= 0:
                    remove_sprite(alien, aliens)
                    score += 1
                    hits += 1
                    if hits >= hits_to_level_up:
                        level_up()
                        hits = 0
                break

    # Spawn new aliens when time interval elapsed
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        alien_size = 1.5
        if hits >= hits_to_level_up:
            alien_size += level
        create_alien(alien_size)
        alien_timer = time.time()

    # Move all aliens
    for alien in aliens:
        alien.forward(ALIEN_SPEED)
        # Check for game over
        if alien.ycor() < FLOOR_LEVEL:
            game_running = False
            break

    time_for_this_frame = time.time() - timer_this_frame
    if time_for_this_frame < TIME_FOR_1_FRAME:
        time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
    window.update()

splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")

# Key bindings
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

turtle.done()
