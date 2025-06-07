import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import ctypes
import win32gui
import win32con
import random
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# The key to unlock the app
VALID_KEY = "JJSploitV.MadeByPopcat21senior.DLL"

# GDI Effect Function
def gdi_effect():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    for _ in range(1000):
        win32gui.DrawIcon(
            hdc,
            random.randint(0, w),
            random.randint(0, h),
            win32gui.LoadIcon(None, win32con.IDI_ERROR),
        )
        time.sleep(0.01)

# (All other functions like open_injection_log, open_admin_panel, open_c00lgui, open_tubers93_gui, open_script_hub, make_draggable remain unchanged)
# For brevity, I’ll omit those here, but you should keep the same functions from the last full code.

# Insert the previous helper functions here: open_injection_log(), open_admin_panel(), etc.

def open_injection_log():
    # ... same as before ...

    log_window = ctk.CTkToplevel()
    log_window.title("Xeno Injection Log")
    log_window.geometry("500x300")
    log_window.configure(fg_color="black")

    log_text = ctk.CTkTextbox(log_window, fg_color="black", text_color="lime", font=("Consolas", 10))
    log_text.pack(fill=tk.BOTH, expand=True)

    fake_logs = [
        "[Xeno] Initializing injection engine...",
        "[Xeno] Scanning Roblox process...",
        "[Xeno] Process ID found: 9824",
        "[Xeno] Injecting payload...",
        "[Xeno] Bypassing AC...",
        "[Xeno] Injection successful.",
        "[Xeno] Ready for execution.",
    ]

    def write_logs():
        for line in fake_logs:
            log_text.insert(tk.END, line + "\n")
            log_text.see(tk.END)
            log_window.update()
            time.sleep(0.5)

    threading.Thread(target=write_logs, daemon=True).start()

def open_admin_panel():
    admin = ctk.CTkToplevel()
    admin.title("Admin Panel")
    admin.geometry("300x300")

    actions = ["Fly", "Noclip", "CTRL + CLICK TP", "Speed", "ESP", "Infinite Jump", "Godmode"]

    for action in actions:
        btn = ctk.CTkButton(admin, text=action, width=150,
                            command=lambda: threading.Thread(target=gdi_effect, daemon=True).start())
        btn.pack(pady=5)

def open_c00lgui():
    win = ctk.CTkToplevel()
    win.title("c00lgui")
    win.geometry("400x450")
    win.configure(fg_color="#2d2d2d")

    header = ctk.CTkLabel(win, text="c00lgui", font=("Comic Sans MS", 22, "bold"), text_color="lime")
    header.pack(pady=10)

    script_frame = ctk.CTkFrame(win)
    script_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    actions = [
        "Spin Bot",
        "Invisible",
        "Clone",
        "Fire Trail",
        "Regen Health",
        "Spam Chat",
        "Headless",
        "R6 to R15",
        "Creeper Mode"
    ]

    for action in actions:
        btn = ctk.CTkButton(script_frame, text=action, width=200,
                            fg_color="black", text_color="lime",
                            font=("Comic Sans MS", 10),
                            command=lambda: threading.Thread(target=gdi_effect, daemon=True).start())
        btn.pack(pady=4)

def open_tubers93_gui():
    win = ctk.CTkToplevel()
    win.title("Tubers93 GUI")
    win.geometry("300x250")
    win.configure(fg_color="red")

    header = ctk.CTkLabel(win, text="TUBERS93", font=("Impact", 20), text_color="white", fg_color="red")
    header.pack(pady=10)

    actions = ["Kick All", "Explode Map", "Spam GUIs", "Loop Kill"]
    for action in actions:
        btn = ctk.CTkButton(win, text=action, width=200,
                            fg_color="white", text_color="red",
                            command=lambda: threading.Thread(target=gdi_effect, daemon=True).start())
        btn.pack(pady=5)

def open_script_hub(textbox):
    hub = ctk.CTkToplevel()
    hub.title("Script Hub")
    hub.geometry("400x400")

    categories = {
        "Combat": {
            "Aimbot.lua": "-- Aimbot script\nwhile true do\n   AimAtEnemy()\nend",
            "KillAura.lua": "-- KillAura\nfor _,v in pairs(enemies) do\n   v:Destroy()\nend"
        },
        "Movement": {
            "Fly.lua": "-- Fly script\nplayer.Character.Humanoid:ChangeState(11)",
            "Speed.lua": "-- Speed hack\nplayer.Character.Humanoid.WalkSpeed = 150"
        },
        "Fun": {
            "Dance.lua": "-- Make character dance\nplayer:PlayAnimation('Dance')",
            "Fart.lua": "-- Fart FX\nworkspace:EmitFartParticle()"
        }
    }

    category_var = ctk.StringVar(hub)
    category_var.set("Combat")

    search_var = ctk.StringVar()

    script_listbox = tk.Listbox(hub)
    script_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

    def update_list():
        script_listbox.delete(0, tk.END)
        for name in categories[category_var.get()]:
            if search_var.get().lower() in name.lower():
                script_listbox.insert(tk.END, name)

    def load_script():
        category = category_var.get()
        selection = script_listbox.curselection()
        if selection:
            name = script_listbox.get(selection[0])
            script = categories[category][name]
            textbox.delete("1.0", tk.END)
            textbox.insert("1.0", script)

    option_menu = ctk.CTkOptionMenu(hub, variable=category_var, values=list(categories.keys()),
                                   command=lambda _: update_list())
    option_menu.pack(pady=5)

    search_entry = ctk.CTkEntry(hub, textvariable=search_var)
    search_entry.pack(pady=5)

    search_var.trace_add("write", lambda *args: update_list())

    load_btn = ctk.CTkButton(hub, text="Load Script", command=load_script)
    load_btn.pack(pady=5)

    update_list()

def make_draggable(widget):
    def start_move(event):
        widget.x = event.x
        widget.y = event.y

    def do_move(event):
        x = event.x_root - widget.x
        y = event.y_root - widget.y
        widget.geometry(f"+{x}+{y}")

    widget.bind("<Button-1>", start_move)
    widget.bind("<B1-Motion>", do_move)

def create_main_ui():
    root = ctk.CTk()
    root.title("JJSPLOIT - Totally Real Executor")
    root.geometry("600x520")
    root.resizable(False, False)

    # Always on top
    root.attributes("-topmost", True)

    # Remove default window decorations for custom title bar
    root.overrideredirect(True)

    # Custom title bar
    title_bar = ctk.CTkFrame(root, height=30, fg_color="#222222")
    title_bar.pack(fill=tk.X)

    title_label = ctk.CTkLabel(title_bar, text="JJSPLOIT - Totally Real Executor", fg_color="#222222", text_color="white")
    title_label.pack(side=tk.LEFT, padx=10)

    # Close button
    def close_app():
        root.destroy()

    close_btn = ctk.CTkButton(title_bar, text="X", width=30, fg_color="#aa2222", hover_color="#ff4444",
                              command=close_app)
    close_btn.pack(side=tk.RIGHT, padx=5, pady=2)

    # Minimize button
    def minimize_app():
        root.iconify()

    minimize_btn = ctk.CTkButton(title_bar, text="_", width=30, fg_color="#444444", hover_color="#666666",
                                 command=minimize_app)
    minimize_btn.pack(side=tk.RIGHT, pady=2)

    make_draggable(root)

    # Buttons frame under title bar
    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(pady=10)

    btn_admin = ctk.CTkButton(buttons_frame, text="Admin Panel", width=110, command=open_admin_panel)
    btn_admin.grid(row=0, column=0, padx=5)

    btn_hub = ctk.CTkButton(buttons_frame, text="Script Hub", width=110, command=lambda: open_script_hub(textbox))
    btn_hub.grid(row=0, column=1, padx=5)

    btn_cool = ctk.CTkButton(buttons_frame, text="c00lgui", width=110, command=open_c00lgui)
    btn_cool.grid(row=0, column=2, padx=5)

    btn_tubers = ctk.CTkButton(buttons_frame, text="Tubers93", width=110, command=open_tubers93_gui)
    btn_tubers.grid(row=0, column=3, padx=5)

    # Textbox
    textbox = ctk.CTkTextbox(root, width=580, height=240)
    textbox.pack(pady=10)

    # Bottom buttons frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack()

    btn_execute = ctk.CTkButton(bottom_frame, text="Execute", width=100,
                               command=lambda: threading.Thread(target=gdi_effect, daemon=True).start())
    btn_execute.grid(row=0, column=0, padx=5, pady=5)

    btn_inject = ctk.CTkButton(bottom_frame, text="Inject", width=100, command=open_injection_log)
    btn_inject.grid(row=0, column=1, padx=5, pady=5)

    btn_clear = ctk.CTkButton(bottom_frame, text="Clear", width=100,
                              command=lambda: textbox.delete("1.0", tk.END))
    btn_clear.grid(row=0, column=2, padx=5, pady=5)

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt;*.lua"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            textbox.delete("1.0", tk.END)
            textbox.insert("1.0", content)

    btn_open = ctk.CTkButton(bottom_frame, text="Open", width=100, command=open_file)
    btn_open.grid(row=0, column=3, padx=5, pady=5)

    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt;*.lua"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(textbox.get("1.0", tk.END))

    btn_save = ctk.CTkButton(bottom_frame, text="Save", width=100, command=save_file)
    btn_save.grid(row=0, column=4, padx=5, pady=5)

    root.mainloop()

def create_key_window():
    key_window = ctk.CTk()
    key_window.title("Enter Key")
    key_window.geometry("400x180")
    key_window.resizable(False, False)

    label = ctk.CTkLabel(key_window, text="Please enter your key to unlock JJSPLOIT:", font=("Arial", 14))
    label.pack(pady=20)

    key_var = ctk.StringVar()

    key_entry = ctk.CTkEntry(key_window, textvariable=key_var, width=300, font=("Arial", 14))
    key_entry.pack(pady=5)
    key_entry.focus()

    def try_key():
        entered_key = key_var.get()
        if entered_key == VALID_KEY:
            messagebox.showinfo("Access Granted", "Correct key! Launching JJSPLOIT...")
            key_window.destroy()
            create_main_ui()
        else:
            messagebox.showerror("Access Denied", "Invalid key. Please try again.")
            key_var.set("")
            key_entry.focus()

    btn_frame = ctk.CTkFrame(key_window)
    btn_frame.pack(pady=10)

    submit_btn = ctk.CTkButton(btn_frame, text="Submit", width=100, command=try_key)
    submit_btn.grid(row=0, column=0, padx=10)

    quit_btn = ctk.CTkButton(btn_frame, text="Quit", width=100, command=key_window.destroy)
    quit_btn.grid(row=0, column=1, padx=10)

    key_window.mainloop()

if __name__ == "__main__":
    create_key_window()
