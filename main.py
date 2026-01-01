import tkinter as tk
import random

WIDTH = 500
HEIGHT = 500
SIZE = 20
SPEED = 100

class ModernSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Snake Game 🐍")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1e1e1e")
        self.canvas.pack()

        self.score = 0
        self.high_score = 0
        self.running = True
        self.direction = "Right"

        self.snake = [(100,100), (80,100), (60,100)]
        self.food = self.create_food()

        self.score_text = self.canvas.create_text(
            250, 15,
            fill="white",
            font=("Segoe UI", 12, "bold"),
            text="Score: 0 | High Score: 0"
        )

        self.root.bind("<Key>", self.change_direction)
        self.root.bind("<space>", self.pause_game)

        self.move_snake()

    def create_food(self):
        return (
            random.randint(0, (WIDTH-SIZE)//SIZE)*SIZE,
            random.randint(0, (HEIGHT-SIZE)//SIZE)*SIZE
        )

    def change_direction(self, event):
        key = event.keysym
        opposites = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}
        if key in opposites and opposites[key] != self.direction:
            self.direction = key

    def pause_game(self, event=None):
        self.running = not self.running
        if self.running:
            self.move_snake()

    def move_snake(self):
        if not self.running:
            return

        x, y = self.snake[0]

        if self.direction == "Up": y -= SIZE
        elif self.direction == "Down": y += SIZE
        elif self.direction == "Left": x -= SIZE
        elif self.direction == "Right": x += SIZE

        new_head = (x, y)

        if (
            x < 0 or y < 0 or
            x >= WIDTH or y >= HEIGHT or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.score, self.high_score)
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.update_ui()
        self.root.after(SPEED, self.move_snake)

    def update_ui(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            250, 15,
            fill="white",
            font=("Segoe UI", 12, "bold"),
            text=f"Score: {self.score} | High Score: {self.high_score}"
        )

        for x,y in self.snake:
            self.canvas.create_rectangle(
                x, y, x+SIZE, y+SIZE,
                fill="#00ff99", outline=""
            )

        fx, fy = self.food
        self.canvas.create_oval(
            fx, fy, fx+SIZE, fy+SIZE,
            fill="#ff4d4d", outline=""
        )

    def game_over(self):
        self.canvas.create_text(
            250, 230,
            fill="red",
            font=("Segoe UI", 28, "bold"),
            text="GAME OVER"
        )
        self.canvas.create_text(
            250, 270,
            fill="white",
            font=("Segoe UI", 14),
            text="Press R to Restart"
        )
        self.root.bind("r", self.restart)

    def restart(self, event=None):
        self.score = 0
        self.direction = "Right"
        self.snake = [(100,100),(80,100),(60,100)]
        self.food = self.create_food()
        self.running = True
        self.move_snake()

root = tk.Tk()
ModernSnakeGame(root)
root.mainloop()
