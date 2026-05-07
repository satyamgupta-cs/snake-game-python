import tkinter as tk
import random

# ---------------- WINDOW SETUP ----------------
WINDOW_SIZE = 400
GRID_SIZE = 20
SPEED = 150

root = tk.Tk()
root.title("Snake Game")

canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="black")
canvas.pack()

score = 0
direction = "Right"
game_running = True

score_label = tk.Label(
    root,
    text=f"Score: {score}",
    font=("Arial", 14, "bold")
)
score_label.pack()

# ---------------- SNAKE SETUP ----------------

snake_positions = [
    (100, 100),
    (80, 100),
    (60, 100)
]

snake_squares = []

for x, y in snake_positions:
    square = canvas.create_rectangle(
        x,
        y,
        x + GRID_SIZE,
        y + GRID_SIZE,
        fill="lime",
        outline=""
    )
    snake_squares.append(square)

# ---------------- FOOD ----------------

def create_food():
    while True:
        x = random.randrange(0, WINDOW_SIZE, GRID_SIZE)
        y = random.randrange(0, WINDOW_SIZE, GRID_SIZE)

        if (x, y) not in snake_positions:
            break

    food = canvas.create_rectangle(
        x,
        y,
        x + GRID_SIZE,
        y + GRID_SIZE,
        fill="red",
        outline=""
    )

    return food, (x, y)


food, food_position = create_food()

# ---------------- CONTROLS ----------------

def change_direction(event):
    global direction

    new_direction = event.keysym

    opposite_directions = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }

    if new_direction in opposite_directions:
        if opposite_directions[new_direction] != direction:
            direction = new_direction


root.bind("<Key>", change_direction)

# ---------------- GAME OVER ----------------

def game_over():
    global game_running

    game_running = False

    canvas.create_text(
        WINDOW_SIZE // 2,
        WINDOW_SIZE // 2,
        text="GAME OVER",
        fill="white",
        font=("Arial", 24, "bold")
    )

# ---------------- MOVE SNAKE ----------------

def move_snake():
    global snake_positions
    global food
    global food_position
    global score

    if not game_running:
        return

    head_x, head_y = snake_positions[0]

    # Move head
    if direction == "Up":
        new_head = (head_x, head_y - GRID_SIZE)

    elif direction == "Down":
        new_head = (head_x, head_y + GRID_SIZE)

    elif direction == "Left":
        new_head = (head_x - GRID_SIZE, head_y)

    elif direction == "Right":
        new_head = (head_x + GRID_SIZE, head_y)

    # ---------------- WALL COLLISION ----------------

    x, y = new_head

    if (
        x < 0 or
        y < 0 or
        x >= WINDOW_SIZE or
        y >= WINDOW_SIZE
    ):
        game_over()
        return

    # ---------------- SELF COLLISION ----------------

    if new_head in snake_positions:
        game_over()
        return

    # Add new head
    snake_positions.insert(0, new_head)

    # ---------------- FOOD COLLISION ----------------

    if new_head == food_position:

        score += 1
        score_label.config(text=f"Score: {score}")

        canvas.delete(food)
        food, food_position = create_food()

    else:
        snake_positions.pop()

    # ---------------- UPDATE SNAKE UI ----------------

    for square in snake_squares:
        canvas.delete(square)

    snake_squares.clear()

    for x, y in snake_positions:
        square = canvas.create_rectangle(
            x,
            y,
            x + GRID_SIZE,
            y + GRID_SIZE,
            fill="lime",
            outline=""
        )
        snake_squares.append(square)

    root.after(SPEED, move_snake)

# ---------------- START GAME ----------------

move_snake()

root.mainloop()