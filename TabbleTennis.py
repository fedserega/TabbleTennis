from tkinter import *
import random

WIDTH = 900
HEIGHT = 300
PAD_W = 10
PAD_H = 100
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 40
BALL_RADIUS = 30
INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
right_line_distance = WIDTH - PAD_W
MAX_SCORE = 10

game_running = False
playing_against_computer = False
pause_window = None

PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

root = Tk()
root.title("PythonicWay Pong")

computer_difficulty = StringVar(value="normal")

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE, game_running
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

    if PLAYER_1_SCORE >= MAX_SCORE or PLAYER_2_SCORE >= MAX_SCORE:
        game_running = False
        end_game()

def end_game():
    global game_over_text
    game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="Игра окончена", font="Arial 20", fill="red")
    c.unbind("<KeyPress>")
    c.unbind("<KeyRelease>")
    root.geometry(f"{WIDTH}x{HEIGHT + 100}")
    play_again_button.pack(pady=10)
    exit_button.pack(pady=10)
    pause_button.place_forget()

def reset_game():
    global PLAYER_1_SCORE, PLAYER_2_SCORE, BALL_X_SPEED, BALL_Y_SPEED, game_running
    PLAYER_1_SCORE = 0
    PLAYER_2_SCORE = 0
    BALL_X_SPEED = INITIAL_SPEED
    BALL_Y_SPEED = INITIAL_SPEED
    game_running = True
    c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
    c.bind("<KeyPress>", movement_handler)
    c.bind("<KeyRelease>", stop_pad)
    play_again_button.pack_forget()
    exit_button.pack_forget()
    c.delete(game_over_text)
    spawn_ball()
    main()

def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def start_game():
    global game_running, playing_against_computer
    game_running = True
    playing_against_computer = False
    start_menu.pack_forget()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    c.pack()
    pause_button.place(relx=0.5, rely=0.05, anchor=CENTER)
    main()

def start_game_vs_computer():
    global game_running, playing_against_computer
    game_running = True
    playing_against_computer = True
    start_menu.pack_forget()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    c.pack()
    pause_button.place(relx=0.5, rely=0.05, anchor=CENTER)
    main()

def exit_game():
    global pause_button, PLAYER_1_SCORE, PLAYER_2_SCORE, game_over_text
    PLAYER_1_SCORE = 0
    PLAYER_2_SCORE = 0
    c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

    try:
        c.delete(game_over_text)
    except:
        pass

    root.geometry("300x300")
    c.pack_forget()
    play_again_button.pack_forget()
    exit_button.pack_forget()
    pause_button.place_forget()
    start_menu.pack()

def exit_exit_game():
    root.quit()

start_menu = Frame(root)
start_button = Button(start_menu, text="Играть один на один", command=start_game)
start_vs_computer_button = Button(start_menu, text="Играть против компьютера", command=start_game_vs_computer)
exit_button_menu = Button(start_menu, text="Выход", command=exit_exit_game)

Label(start_menu, text="Выберите сложность компьютера:").pack(pady=10)
Radiobutton(start_menu, text="Простой", variable=computer_difficulty, value="easy").pack(anchor=W)
Radiobutton(start_menu, text="Нормальный", variable=computer_difficulty, value="normal").pack(anchor=W)
Radiobutton(start_menu, text="Сложный", variable=computer_difficulty, value="hard").pack(anchor=W)

start_button.pack(pady=10)
start_vs_computer_button.pack(pady=10)
exit_button_menu.pack(pady=10)
start_menu.pack()

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")

play_again_button = Button(root, text="Играть заново", command=reset_game)
exit_button = Button(root, text="Выход", command=exit_game)

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="white")
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4, text=PLAYER_1_SCORE, font="Arial 20", fill="white")
p_2_text = c.create_text(WIDTH/6, PAD_H/4, text=PLAYER_2_SCORE, font="Arial 20", fill="white")

BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0

def move_ball():
    if not game_running:
        return

    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score("left")
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)

    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, RIGHT_PAD: RIGHT_PAD_SPEED}

    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    if playing_against_computer:
        move_computer_pad()
    if game_running:
        root.after(30, main)

c.focus_set()

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "ц"):
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym in ("s", "ы"):
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

c.bind("<KeyPress>", movement_handler)

def pause_game():
    global game_running, pause_window
    if pause_window is not None and pause_window.winfo_exists():
        return

    game_running = False
    c.unbind("<KeyPress>")
    c.unbind("<KeyRelease>")
    pause_window = Toplevel(root)
    pause_window.title("Пауза")
    pause_window.geometry("200x100")

    def resume_game():
        global game_running
        pause_window.destroy()
        game_running = True
        c.bind("<KeyPress>", movement_handler)
        c.bind("<KeyRelease>", stop_pad)
        main()

    def exit_to_menu():
        pause_window.destroy()
        exit_game()

    resume_button = Button(pause_window, text="Продолжить", command=resume_game)
    exit_button = Button(pause_window, text="Выход в меню", command=exit_to_menu)
    resume_button.pack(pady=10)
    exit_button.pack(pady=10)

pause_button = Button(root, text="Пауза", command=pause_game)
game_over_text = None
pause_window = None

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)

def move_computer_pad():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    pad_top, pad_bottom = c.coords(RIGHT_PAD)[1:4:2]
    pad_center = (pad_top + pad_bottom) / 2

    if computer_difficulty.get() == "easy":
        if random.random() > 0.3:
            return
    elif computer_difficulty.get() == "normal":
        if random.random() > 0.45:
            return
    elif computer_difficulty.get() == "hard":
        if random.random() > 0.65:
            return

    if ball_center < pad_center:
        c.move(RIGHT_PAD, 0, -PAD_SPEED)
    elif ball_center > pad_center:
        c.move(RIGHT_PAD, 0, PAD_SPEED)

    if c.coords(RIGHT_PAD)[1] < 0:
        c.move(RIGHT_PAD, 0, -c.coords(RIGHT_PAD)[1])
    elif c.coords(RIGHT_PAD)[3] > HEIGHT:
        c.move(RIGHT_PAD, 0, HEIGHT - c.coords(RIGHT_PAD)[3])


root.geometry("300x300")


root.mainloop()
