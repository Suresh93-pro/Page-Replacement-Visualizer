import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from algorithms import simulate
from visualizer import PageReplacementApp

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementApp(root)
    root.mainloop()
