# pure-Tk spinner – works with Apple’s Tk 8.5 and inside --windowed executables
import tkinter as tk
from itertools import cycle

frames = cycle('|/-\\')           # ASCII spinner frames

root = tk.Tk()
root.geometry('+600+300')         # put it somewhere visible
root.overrideredirect(True)       # no title-bar
root.attributes('-topmost', True) # stay on top

lbl = tk.Label(root, font=('Courier', 28), padx=20, pady=20)
lbl.pack()

def spin():
    lbl.config(text=next(frames))
    root.after(120, spin)         # ~8 fps
spin()

root.mainloop()
