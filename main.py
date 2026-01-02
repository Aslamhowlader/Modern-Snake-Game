import tkinter as tk
import random

WIDTH = 600
HEIGHT = 500
SIZE = 20
SPEED = 100

class BeautifulSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Beautiful Modern Snake 🐍")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0f172a")
        self.canvas.pack()

        self.direction = "Right"
        self.running = True
        self.score = 0

        self.snake = [(100,100),(80,100),(60,100)]
        self.food = self.create_food()

        self.root.bind("<Key>", self.change_direction)
        self.root.bind("<space>", self.pause)

        self.game_loop()

    def create_food(self):
        return (
            random.randint(0,(WIDTH-SIZE)//SIZE)*SIZE,
            random.randint(1,(HEIGHT-SIZE)//SIZE)*SIZE
        )

    def change_direction(self, e):
        opp = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}
        if e.keysym in opp and opp[e.keysym] != self.direction:
            self.direction = e.keysym

    def pause(self, e=None):
        self.running = not self.running
        if self.running:
            self.game_loop()

    def move_snake(self):
        x,y = self.snake[0]
        if self.direction=="Up": y-=SIZE
        if self.direction=="Down": y+=SIZE
        if self.direction=="Left": x-=SIZE
        if self.direction=="Right": x+=SIZE

        x %= WIDTH
        y %= HEIGHT

        return (x,y)

    def game_loop(self):
        if not self.running:
            return

        new_head = self.move_snake()

        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0,new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(SPEED, self.game_loop)

    def draw_snake(self):
        for i,(x,y) in enumerate(self.snake):
            if i == 0:
                # Head
                self.canvas.create_oval(
                    x+2,y+2,x+SIZE-2,y+SIZE-2,
                    fill="#22c55e", outline=""
                )
                # Eyes
                self.canvas.create_oval(x+6,y+6,x+9,y+9, fill="black")
                self.canvas.create_oval(x+11,y+6,x+14,y+9, fill="black")
            else:
                self.canvas.create_oval(
                    x+3,y+3,x+SIZE-3,y+SIZE-3,
                    fill="#4ade80", outline=""
                )

    def draw(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            WIDTH//2,15,
            fill="white",
            font=("Segoe UI",13,"bold"),
            text=f"Score : {self.score}"
        )

        self.draw_snake()

        fx,fy = self.food
        self.canvas.create_oval(
            fx,fy,fx+SIZE,fy+SIZE,
            fill="#fb7185",outline=""
        )

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WIDTH//2,HEIGHT//2 - 10,
            fill="red",
            font=("Segoe UI",28,"bold"),
            text="GAME OVER"
        )
        self.canvas.create_text(
            WIDTH//2,HEIGHT//2 + 25,
            fill="white",
            font=("Segoe UI",14),
            text="Press R to Restart"
        )
        self.root.bind("r", self.restart)

    def restart(self, e=None):
        self.score = 0
        self.direction = "Right"
        self.snake = [(100,100),(80,100),(60,100)]
        self.food = self.create_food()
        self.running = True
        self.game_loop()

root = tk.Tk()
BeautifulSnakeGame(root)
root.mainloop()
