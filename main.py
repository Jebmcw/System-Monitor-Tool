import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from tables import cpu_tables

class SystemMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor Tool")
        self.geometry("600x800")
        self.configure(bg='#1e1e1e')

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="System Monitor", font=("Segoe UI", 16))
        title.pack(pady=10)

        chart_frame = cpu_tables.LiveCPUChart(self)
        chart_frame.pack(pady=10)

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()