# 
from tkinter import *
root = Tk()

def key_press(event):
    print(f"x coord:{event.x}")
    print(f"y coord:{event.y}")

canvas = Canvas(root)
canvas.pack()
canvas.bind('<ButtonPress>', key_press)
root.mainloop()