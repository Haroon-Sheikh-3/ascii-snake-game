import tkinter as tk
import random


#WIDTH N HEIGHT
WIDTH = 40
HEIGHT = 30


#CREATE GAME WINDOW
window = tk.Tk()
window.title("ASCII SNAKEE")
window.geometry("800x600")
window.configure(bg = "black")

#GAME CANVAS
canvas = tk.Canvas(
    window,
    width = WIDTH * 20,
    height = HEIGHT * 20,
    bg = "black",
    highlightthickness= 0
)
canvas.pack()

# DRAW ASCII BORDER

# TOP AND BOTTOM BORDERS
for x in range(WIDTH):
    canvas.create_text(
        x * 20 + 10, 10,
        text="-",
        fill="white",
        font=("Consolas", 14)
    )

    canvas.create_text(
        x * 20 + 10, HEIGHT * 20 - 10,
        text="-",
        fill="white",
        font=("Consolas", 14)
    )

# SIDE BORDERS
for y in range(1, HEIGHT - 1):
    canvas.create_text(
        10, y * 20 + 10,
        text="|",
        fill="white",
        font=("Consolas", 14)
    )

    canvas.create_text(
        WIDTH * 20 - 10, y * 20 + 10,
        text="|",
        fill="white",
        font=("Consolas", 14)
    )


#BORDER CORNERS
canvas.create_text(10, 10, text = "+", fill = "white", font=("Consolas",14))
canvas.create_text(WIDTH * 20 - 10, 10, text = "+", fill = "white", font=("Consolas",14))

canvas.create_text(10, HEIGHT * 20 - 10, text = "+", fill = "white", font =("Consolas", 14) )
canvas.create_text(WIDTH * 20 - 10, HEIGHT * 20 - 10, text="+", fill="white", font=("Consolas", 14))


#SNAKE START POINT
snake = [
    (WIDTH // 2, HEIGHT // 2),
    (WIDTH // 2 - 1, HEIGHT // 2),
    (WIDTH // 2 - 2, HEIGHT // 2)
]


#SNAKE DIRECTION
direction = (1,0)

#CAN TURN
can_turn = True

#FOOD POSITION
food = (10,5)

#DRAW FOOD
canvas.create_text(
    food[0] * 20 + 10,
    food[1] * 20 + 10,
    text = "$", 
    fill = "red",
    font = ("Consolas", 15, "bold"),
    tags = "food"
)


#SCORE 
score = 0

#GAME LOOP CONTROL
running = True

#GAME OVER VALUE
game_over = False

#GAME STARTED
started = False

#TIS STOPS THE SNAKE FROM GETTIN FASTER
after_id = None

#GAME UPDATE FUNCTION
def update_game():
    global food, score, after_id, game_over, can_turn
    after_id = None

    #GET SNAKE HEAD POSITION
    head_x, head_y = snake[0]

    #CALCULATE NEW HEAD POSITION
    new_head = (
        head_x + direction [0],
        head_y + direction [1],

    )

    #WRAP AROUND MOVEMENT
    new_head = (
        (new_head[0] - 1) % (WIDTH - 2) + 1,
        (new_head[1] - 1) % (HEIGHT - 2) + 1
    )


    #ADD NEW HEAD TO THE SNAKE
    snake.insert(0, new_head)

    #CHECK SELF COLLISION
    if new_head in snake[1:]:
        game_over = True

        canvas.create_text(
            WIDTH * 10,
            HEIGHT * 10,
            text = "GAME OVER!!!",
            fill = "red",
            font = ("Consolas", 30, "bold"),
            tags = "game_over"
        )
        return

    #CHECK IF SNAKE ATE DA FOOD
    if new_head == food:
        score += 1
        window.title(f"ASCII SNAKE | Score: {score}")
        food = (
            random.randint(1, WIDTH - 2),
            random.randint(1, HEIGHT - 2)
        )

        while food in snake:
            food = (
                random.randint(1, WIDTH -2),
                random.randint(1, HEIGHT -2)
            )
        draw_food()
    else:
        snake.pop()

    #REDRAW SNAKE
    draw_snake()
    can_turn = True

    #SCHEDULE NEXT MOVEMENT
    after_id = window.after(150, update_game)


#CHANGE SNAKE DIRECTION
def change_direction(event):
    global direction, can_turn

    if not can_turn: 
        return

    if event.keysym == "Up" and direction != (0,1):
        direction = (0, -1)
        can_turn = False
    elif event.keysym == "Down" and direction != (0,-1):
        direction = (0, 1)
        can_turn = False
    elif event.keysym == "Left" and direction != (1,0):
        direction = (-1, 0)
        can_turn = False
    elif event.keysym == "Right" and direction != (-1,0):
        direction = (1, 0)
        can_turn = False


#DRAW SNAKE FUNCTION
def draw_snake():
    canvas.delete("snake")

    for index, (x, y) in enumerate(snake):
        if index == 0:
            color = "lime"
        else:
            color = "white"
            
        canvas.create_text(
            x * 20 + 10,
            y * 20 + 10,
            text = "@",
            fill = color, 
            font = ("Consolas", 15, "bold"),
            tags = "snake"
        )

    

#DRAW FOOD FUNCTION
def draw_food():
    canvas.delete("food")

    canvas.create_text(
        food[0] * 20 + 10,
        food[1] * 20 + 10,
        text = "$",
        fill = "red",
        font = ("Consolas", 15, "bold"),
        tags = "food"
    )

#RESTART FUNCTION
def restart_game():
    global snake, direction, food, score, after_id, game_over, can_turn

    if not game_over:
        return

    if after_id is not None:
        window.after_cancel(after_id)
        after_id = None

    canvas.delete("game_over")

    snake = [
        (WIDTH // 2, HEIGHT // 2),
        (WIDTH // 2 - 1, HEIGHT // 2),
        (WIDTH // 2 - 2, HEIGHT // 2)
    ]

    direction = (1,0)
    can_turn = True
    food = (10, 5)
    score = 0
    game_over = False
  

    window.title("ASCII SNAKE | SCORE : 0")

    draw_snake()
    draw_food()

    after_id = window.after(10, update_game)

#START GAME FUNCTION
def start_game():
    global started, after_id

    if started or game_over:
        return

    started = True
    canvas.delete("start_message")
    after_id = window.after(10, update_game)


window.bind("<KeyPress>", change_direction)
window.bind("r", lambda event: restart_game() )
window.bind("<space>", lambda event: start_game())
window.focus_set()

draw_snake()
draw_food()

canvas.create_text(
    WIDTH * 10,
    HEIGHT * 10, 
    text = "PRESS SPACE TO START!",
    fill = "yellow", 
    font = ("Consolas", 20, "bold"),
    tags = "start_message"
)

# after_id = window.after(10, update_game)

#DONT START MOVING YET
window.mainloop()