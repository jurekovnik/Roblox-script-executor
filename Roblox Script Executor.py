import tkinter as tk
from tkinter import filedialog, messagebox, font
import threading
import ctypes
import random
import win32gui
import win32con
import time

# --- Your requested GDI effect for Execute ---
def gdi_random_icons():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    while True:
        win32gui.DrawIcon(
            hdc,
            random.randint(0, w),
            random.randint(0, h),
            win32gui.LoadIcon(None, win32con.IDI_ERROR),
        )

# --- Roblox Xeno Injection Log Window ---
class InjectionLogWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Roblox Xeno | Injection Log")
        self.geometry("600x300")
        self.configure(bg="#1e1e2f")
        self.resizable(False, False)

        self.log_text = tk.Text(self, bg="#1e1e2f", fg="#d4d4d4", insertbackground="#d4d4d4",
                                font=("Consolas", 11), state=tk.DISABLED)
        self.log_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.messages = [
            "[INFO] Initializing Roblox Xeno...",
            "[INFO] Checking Roblox process...",
            "[INFO] Roblox process found (PID 1234).",
            "[INFO] Preparing injection environment...",
            "[INFO] Injecting payload...",
            "[SUCCESS] Payload injected successfully.",
            "[INFO] Attaching to Roblox client...",
            "[SUCCESS] Attached successfully.",
            "[INFO] Starting executor...",
            "[SUCCESS] Executor ready.",
            "[INFO] Injection complete. Have fun!",
        ]
        self.current_line = 0
        self.after(500, self.show_next_line)

    def show_next_line(self):
        if self.current_line < len(self.messages):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, self.messages[self.current_line] + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.current_line += 1
            self.after(700, self.show_next_line)

    def on_close(self):
        self.destroy()

# --- GUI Setup ---
class ScriptExecutorApp:
    def __init__(self, root):
        self.root = root
        root.title("Roblox Script Executor (Took me an hour but works)")
        root.geometry("700x400")
        root.configure(bg="#2c2f33")

        # Fonts & colors
        self.btn_font = font.Font(family="Segoe UI", size=10, weight="bold")
        self.text_font = font.Font(family="Consolas", size=11)
        self.btn_bg = "#7289da"
        self.btn_fg = "white"
        self.text_bg = "#23272a"
        self.text_fg = "white"

        # Left panel: buttons stacked vertically
        self.left_frame = tk.Frame(root, bg="#2c2f33")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=20)

        self.open_button = tk.Button(self.left_frame, text="Open", font=self.btn_font, bg=self.btn_bg, fg=self.btn_fg, width=14, command=self.open_file)
        self.open_button.pack(pady=8)

        self.save_button = tk.Button(self.left_frame, text="Save", font=self.btn_font, bg=self.btn_bg, fg=self.btn_fg, width=14, command=self.save_file)
        self.save_button.pack(pady=8)

        self.clear_button = tk.Button(self.left_frame, text="Clear", font=self.btn_font, bg="#99aab5", fg=self.btn_fg, width=14, command=self.clear_text)
        self.clear_button.pack(pady=8)

        self.execute_button = tk.Button(self.left_frame, text="Execute", font=self.btn_font, bg="#43b581", fg=self.btn_fg, width=14, command=self.execute_gdi_effect)
        self.execute_button.pack(pady=8)

        self.inject_button = tk.Button(self.left_frame, text="Inject", font=self.btn_font, bg="#faa61a", fg=self.btn_fg, width=14, command=self.show_injection_log)
        self.inject_button.pack(pady=8)

        # Text area on right
        self.text_area = tk.Text(root, font=self.text_font, bg=self.text_bg, fg=self.text_fg, insertbackground="white")
        self.text_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=20)

        self.execute_thread = None

    def open_file(self):
        filename = filedialog.askopenfilename(title="Open Script", filetypes=[("Lua Scripts", "*.lua"), ("All files", "*.*")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                data = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, data)

    def save_file(self):
        filename = filedialog.asksaveasfilename(title="Save Script", defaultextension=".lua", filetypes=[("Lua Scripts", "*.lua"), ("All files", "*.*")])
        if filename:
            data = self.text_area.get(1.0, tk.END)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(data)
            messagebox.showinfo("Saved", f"Script saved to {filename}")

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)

    def execute_gdi_effect(self):
        if self.execute_thread and self.execute_thread.is_alive():
            messagebox.showinfo("Info", "Execute effect already running.")
            return
        self.execute_thread = threading.Thread(target=gdi_random_icons, daemon=True)
        self.execute_thread.start()
        messagebox.showinfo("GDI Effect", "Execute GDI effect started! Close program to stop.")

    def show_injection_log(self):
        InjectionLogWindow(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptExecutorApp(root)
    root.mainloop()
