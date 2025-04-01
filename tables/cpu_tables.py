import os
import sys
import customtkinter as ctk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import cpu  # assumes get_cpu_data() is defined in monitor/cpu.py

class LiveCPUTable(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)

        self.configure(fg_color="#1e1e1e")  # Dark background

        # Title label
        self.title = ctk.CTkLabel(self, text="CPU Usage Monitor", font=ctk.CTkFont("Segoe UI", 20, "bold"))
        self.title.pack(pady=(15, 10))

        # Container for CPU rows
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b", corner_radius=8)
        self.scroll_frame.pack(padx=15, pady=10, fill="both", expand=True)

        self.labels = []

        # Start polling
        self.poll_interval_ms = 1000
        self.poll_cpu()

    def poll_cpu(self):
        data = cpu.get_cpu_data()
        self.update_table(data)
        self.after(self.poll_interval_ms, self.poll_cpu)

    def update_table(self, data):
        # Clear existing labels
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Per-core usage
        for i, usage in enumerate(data["usage_per_core"]):
            row = ctk.CTkLabel(self.scroll_frame, text=f"Core {i:<2}  |  {usage:.1f}%", 
                               font=ctk.CTkFont("Consolas", 14), text_color="cyan")
            row.pack(anchor="w", padx=10, pady=2)

        # Total usage
        total_label = ctk.CTkLabel(self.scroll_frame, text=f"Total     |  {data['total_usage']:.1f}%", 
                                   font=ctk.CTkFont("Consolas", 14, "bold"), text_color="magenta")
        total_label.pack(anchor="w", padx=10, pady=(8, 2))

        # Frequency
        freq_label = ctk.CTkLabel(self.scroll_frame, text=f"Freq      |  {data['freq']['current']:.1f} MHz", 
                                  font=ctk.CTkFont("Consolas", 14), text_color="magenta")
        freq_label.pack(anchor="w", padx=10, pady=(0, 10))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # "light" or "dark"
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("System Monitor Tool")
    app.geometry("400x650")

    cpu_widget = LiveCPUTable(app)
    cpu_widget.pack(fill="both", expand=True, padx=10, pady=10)

    app.mainloop()
