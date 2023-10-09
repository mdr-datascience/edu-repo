# Check that Tkinter is installed
# If no error is returned, all is good
import tkinter
import _tkinter

# Run test routine
#tkinter._test()

# Import tkinter module
from tkinter import *
from tkinter import ttk

# Create top-level window
root = Tk()

# Create first button
button = ttk.Button(root, text = 'Click Me')

# To insert a button we need to call the placement method
button.pack()
