import tkinter as tk
from tkinter import messagebox
import random

class Cell:
    """Represents a single cell in the Minesweeper grid."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Minesweeper:
    """Main Minesweeper game class with GUI and logic."""
    def __init__(self, root, rows=10, cols=10, mines=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.flags_left = mines

        self.grid = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.create_widgets()
        self.place_mines()
        self.calculate_adjacents()

    def create_widgets(self):
        """Create button widgets for each cell."""
        for x in range(self.rows):
            for y in range(self.cols):
                btn = tk.Button(self.frame, width=3, height=1,
                                command=lambda x=x, y=y: self.reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.flag_cell(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

    def place_mines(self):
        """Randomly place mines in the grid."""
        mines_placed = 0
        while mines_placed < self.total_mines:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            cell = self.grid[x][y]
            if not cell.is_mine:
                cell.is_mine = True
                mines_placed += 1

    def calculate_adjacents(self):
        """Calculate adjacent mine counts for each cell."""
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y].is_mine:
                    continue
                count = 0
                for i in range(max(0, x - 1), min(self.rows, x + 2)):
                    for j in range(max(0, y - 1), min(self.cols, y + 2)):
                        if self.grid[i][j].is_mine:
                            count += 1
                self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, x, y):
        """Reveal a cell and handle game logic."""
        cell = self.grid[x][y]
        btn = self.buttons[x][y]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        btn.config(relief=tk.SUNKEN)

        if cell.is_mine:
            btn.config(text='💣', bg='red')
            self.game_over(False)
        else:
            btn.config(text=str(cell.adjacent_mines) if cell.adjacent_mines > 0 else '', bg='lightgrey')
            if cell.adjacent_mines == 0:
                for i in range(max(0, x - 1), min(self.rows, x + 2)):
                    for j in range(max(0, y - 1), min(self.cols, y + 2)):
                        if not self.grid[i][j].is_revealed:
                            self.reveal_cell(i, j)

        if self.check_win():
            self.game_over(True)

    def flag_cell(self, x, y):
        """Flag or unflag a cell."""
        cell = self.grid[x][y]
        btn = self.buttons[x][y]

        if cell.is_revealed:
            return

        if not cell.is_flagged:
            if self.flags_left == 0:
                return
            cell.is_flagged = True
            btn.config(text='🚩', fg='red')
            self.flags_left -= 1
        else:
            cell.is_flagged = False
            btn.config(text='', fg='black')
            self.flags_left += 1

    def check_win(self):
        """Check for win condition."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def game_over(self, won):
        """Handle end of the game and restart."""
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.grid[x][y]
                btn = self.buttons[x][y]
                if cell.is_mine:
                    btn.config(text='💣', bg='red' if not won else 'green')
                btn.config(state=tk.DISABLED)

        message = "🎉 You won!" if won else "💥 You lost!"
        self.root.after(1000, lambda: messagebox.showinfo("Game Over", message))
        self.root.after(1500, self.restart_game)

    def restart_game(self):
        """Restart the game: reset all buttons and logic."""
        self.grid = [[Cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
        self.flags_left = self.total_mines

        for x in range(self.rows):
            for y in range(self.cols):
                btn = self.buttons[x][y]
                btn.config(text='', bg='SystemButtonFace', relief=tk.RAISED, state=tk.NORMAL, fg='black')

        self.place_mines()
        self.calculate_adjacents()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper - Python Edition")
    game = Minesweeper(root, rows=10, cols=10, mines=15)
    root.mainloop()
