"""Overlay windows for notifications and warnings"""
import tkinter as tk
import threading


def show_start_notification(wait_minutes: int):
    """Display a notification that the timer has started"""
    root = tk.Tk()
    root.withdraw()
    
    notification = tk.Toplevel(root)
    notification.title("Gaming Break Timer Started")
    notification.withdraw()  # Hide until positioned
    notification.attributes('-topmost', True)
    notification.configure(bg='#007b2d')
    
    # Calculate center position
    window_width = 400
    window_height = 150
    screen_width = notification.winfo_screenwidth()
    screen_height = notification.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    notification.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Set dark title bar (Windows 10/11)
    try:
        notification.update_idletasks()
        import ctypes
        hwnd = ctypes.windll.user32.GetParent(notification.winfo_id())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except:
        pass  # If it fails, just use default title bar
    
    label = tk.Label(
        notification,
        text=f"✅ Gaming Break Timer Started\n\nYou have {wait_minutes} minutes of gaming time!",
        font=("Arial", 14, "bold"),
        bg='#007b2d',
        fg='white',
        pady=20
    )
    label.pack()
    
    # Show window after everything is set up
    notification.deiconify()
    
    # Auto-close after 5 seconds
    notification.after(5000, notification.destroy)
    notification.mainloop()


def show_warning_overlay(warning_seconds: int = 30):
    """Display a topmost warning window that overlays all other windows"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create a topmost window
    warning = tk.Toplevel(root)
    warning.title("Gaming Break Warning")
    warning.withdraw()  # Hide until positioned
    warning.attributes('-topmost', True)
    warning.configure(bg='#8f0000')
    
    # Calculate center position
    window_width = 400
    window_height = 200
    screen_width = warning.winfo_screenwidth()
    screen_height = warning.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    warning.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Set dark title bar (Windows 10/11)
    try:
        warning.update_idletasks()
        import ctypes
        hwnd = ctypes.windll.user32.GetParent(warning.winfo_id())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except:
        pass  # If it fails, just use default title bar
    
    label = tk.Label(
        warning,
        text="⚠️ GAMING BREAK ⚠️\n\nYour game will close in:",
        font=("Arial", 16, "bold"),
        bg='#8f0000',
        fg='white',
        pady=10
    )
    label.pack()
    
    # Countdown label
    countdown_label = tk.Label(
        warning,
        text=str(warning_seconds),
        font=("Arial", 48, "bold"),
        bg='#8f0000',
        fg='white'
    )
    countdown_label.pack()
    
    # Countdown function
    def update_countdown(seconds):
        if seconds >= 0:
            countdown_label.config(text=str(seconds))
            warning.after(1000, update_countdown, seconds - 1)
        else:
            warning.destroy()
    
    # Show window after everything is set up
    warning.deiconify()
    
    # Start countdown
    update_countdown(warning_seconds)
    
    warning.mainloop()


def show_start_notification_threaded(wait_minutes: int):
    """Show start notification in a separate thread"""
    thread = threading.Thread(target=show_start_notification, args=(wait_minutes,))
    thread.start()


def show_warning_overlay_threaded(warning_seconds: int = 30):
    """Show warning overlay in a separate thread"""
    thread = threading.Thread(target=show_warning_overlay, args=(warning_seconds,))
    thread.start()
