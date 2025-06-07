import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import ctypes
from ctypes import wintypes

# --- GDI effect using a transparent layered window (Windows only) ---
# This will create a transparent window that draws a moving circle

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
WS_EX_TOPMOST = 0x8
LWA_ALPHA = 0x2

class GDIEffectWindow:
    def __init__(self):
        self.hInstance = user32.GetModuleHandleW(None)
        self.className = "GDIOverlayWindow"

        wndClass = wintypes.WNDCLASS()
        wndClass.style = 0
        wndClass.lpfnWndProc = self.wndProc
        wndClass.cbClsExtra = wndClass.cbWndExtra = 0
        wndClass.hInstance = self.hInstance
        wndClass.hIcon = user32.LoadIconW(None, wintypes.LPCWSTR(32512)) # IDI_APPLICATION
        wndClass.hCursor = user32.LoadCursorW(None, wintypes.LPCWSTR(32512)) # IDC_ARROW
        wndClass.hbrBackground = 0
        wndClass.lpszMenuName = None
        wndClass.lpszClassName = self.className

        self.atom = user32.RegisterClassW(ctypes.byref(wndClass))
        if not self.atom:
            raise ctypes.WinError()

        # Create layered window (transparent)
        self.hwnd = user32.CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST,
            self.className,
            "GDI Effect",
            0x80000000 | 0x10000000,  # WS_POPUP | WS_VISIBLE
            100, 100, 300, 300,
            None, None, self.hInstance, None
        )
        if not self.hwnd:
            raise ctypes.WinError()

        # Set layered window attributes (opacity 200 out of 255)
        user32.SetLayeredWindowAttributes(self.hwnd, 0, 200, LWA_ALPHA)

        self.dc = user32.GetDC(self.hwnd)
        self.running = False
        self.radius = 30
        self.x = 50
        self.y = 150
        self.dx = 5

    def wndProc(self, hwnd, msg, wParam, lParam):
        if msg == 2:  # WM_DESTROY
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, msg, wParam, lParam)

    def start(self):
        self.running = True
        threading.Thread(target=self.animate, daemon=True).start()

    def animate(self):
        while self.running:
            # Clear background (transparent)
            brush = gdi32.CreateSolidBrush(0x000000)
            rect = wintypes.RECT(0, 0, 300, 300)
            gdi32.FillRect(self.dc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)

            # Draw a red circle that moves horizontally
            pen = gdi32.CreatePen(0, 3, 0x0000FF)  # Blue pen
            old_pen = gdi32.SelectObject(self.dc, pen)
            brush_red = gdi32.CreateSolidBrush(0x0000FF)  # Blue brush
            old_brush = gdi32.SelectObject(self.dc, brush_red)

            gdi32.Ellipse(self.dc, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)

            gdi32.SelectObject(self.dc, old_pen)
            gdi32.SelectObject(self.dc, old_brush)
            gdi32.DeleteObject(pen)
            gdi32.DeleteObject(brush_red)

            self.x += self.dx
            if self.x > 250 or self.x < 50:
                self.dx = -self.dx

            time.sleep(0.05)

    def stop(self):
        self.running = False
        user32.DestroyWindow(self.hwnd)

# --- GUI Setup ---
class ScriptExecutorApp:
    def __init__(self, root):
        self.root = root
        root.title("Roblox Script Executor (Fake)")

        self.text_area = tk.Text(root, height=15, width=60)
        self.text_area.pack(padx=10, pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        self.open_button = tk.Button(frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(frame, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.execute_button = tk.Button(frame, text="Execute", command=self.start_gdi_effect)
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.inject_button = tk.Button(frame, text="Inject", command=self.start_gdi_effect)
        self.inject_button.pack(side=tk.LEFT, padx=5)

        self.gdi_effect = None

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

    def start_gdi_effect(self):
        if self.gdi_effect is None:
            try:
                self.gdi_effect = GDIEffectWindow()
                self.gdi_effect.start()
                messagebox.showinfo("GDI Effect", "GDI effect started! Close the program to stop.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start GDI effect: {e}")
        else:
            messagebox.showinfo("GDI Effect", "GDI effect already running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptExecutorApp(root)
    root.mainloop()
