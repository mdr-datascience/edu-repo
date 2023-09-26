from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):

        # Main window title and properties
        self.master = master
        master.title('Weather Statistics')
        master.resizable(True, True)
        master.state('zoomed')
        
        self.label = Label(master, text="Welcome to my first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("HELLO!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()