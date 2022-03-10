# imports
from tkinter import *

# Parent Window
root = Tk()


# main
if __name__ == "__main__":
    # Allow resize
    root.resizable(True, True)
    # set title
    root.title("Mission Planner")
    # Set minimum size for root window
    root.geometry("650x400")
    # Main event loop of root window
    root.mainloop()