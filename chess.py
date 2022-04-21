import time

from solution import *
from tkinter import *
from PIL import Image, ImageTk
import os
from time import sleep


def click(event):
    global row, col, row1, col1
    if row is None:
        row, col = 7 - (root.winfo_pointery() - root.winfo_rooty() - 80) // 80, (root.winfo_pointerx() - root.winfo_rootx() - 80) // 80
        cell = board.field[row][col]
        if not cell:
            row, col = None, None
        elif cell.color != board.color:
            row, col = None, None
        else:
            for d in cell.moves:
                temp_row, temp_col = row, col
                while True:
                    temp_row += d[0]
                    temp_col += d[1]
                    if not correct_coords(temp_row, temp_col):
                        break
                    if cell.can_move(board, row, col, temp_row, temp_col):
                        Label(root, image=images[board.cell(temp_row, temp_col)], borderwidth=2, relief="solid", bg="#bcefd0").place(
                            x=120 + 80 * temp_col,
                            y=680 - 80 * temp_row,
                            anchor="center")
                    if cell.char == "P":
                        if cell.can_attack(board, row, col, temp_row, temp_col):
                            Label(root, image=images[board.cell(temp_row, temp_col)], borderwidth=2, relief="solid",
                                  bg="#bcefd0").place(
                                x=120 + 80 * temp_col,
                                y=680 - 80 * temp_row,
                                anchor="center")
                    if cell.one_move:
                        break


    else:
        row1, col1 = 7 - (root.winfo_pointery() - root.winfo_rooty() - 80) // 80, (
                    root.winfo_pointerx() - root.winfo_rootx() - 80) // 80
        if board.move_piece(row, col, row1, col1):
            root.title("Ход: "+ {WHITE: "белые", BLACK: "черные"}[board.color])
        update_board()
        if board.game_over:
            time.sleep(0.5)
            root.destroy()
            end = Tk()
            end.title("Конец игры")
            T = Text(end, height=5, width=52)
            T.pack()
            T.insert(END, f"Игра завершена.\nПобедил {'БЕЛЫЙ' if board.game_over == WHITE else 'ЧЕРНЫЙ'} игрок!")
            end.mainloop()

        row, col, row1, col1 = None, None, None, None




def update_board():
    for x in range(8):
        for y in range(8):
            Label(root, image=images[board.cell(x, y)], borderwidth=2, bg=["#bf6d24", "#ffe4cd"][(x + y) % 2], relief="solid").place(x=120 + 80 * y,
                                                                                          y=680 - 80 * x,
                                                                                          anchor="center")

board = Board()
root = Tk()
row, col, row1, col1 = None, None, None, None
root.title("Ход: "+ {WHITE: "белые", BLACK: "черные"}[board.color])
root.minsize(width=800, height=800)
root.bind('<Button-1>', click)
images = {x[:2]: ImageTk.PhotoImage(Image.open("assets/" + x).resize((80, 80))) for x in os.listdir("assets")}
images["  "] = ImageTk.PhotoImage(Image.new('RGBA', (80, 80), (255, 0, 0, 0)))
update_board()
root.mainloop()
