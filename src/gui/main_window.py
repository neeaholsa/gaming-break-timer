"""Main application window"""
import customtkinter as ctk
from tkinter import messagebox
from ..core.timer import GamingTimer
from ..core.process_manager import close_process
from ..utils.config import Config
from .overlays import show_start_notification_threaded, show_warning_overlay_threaded


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration
        self.config = Config()
        
        # Timer
        self.timer = GamingTimer()
        self.timer.on_timer_start = self._on_timer_start
        self.timer.on_timer_warning = self._on_timer_warning
        self.timer.on_timer_complete = self._on_timer_complete
        self.timer.on_timer_tick = self._on_timer_tick
        
        # Window setup
        self.title("Gaming Break Timer")
        
        # Center window on screen
        window_width = 500
        window_height = 450
        self.geometry(f"{window_width}x{window_height}")
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set theme
        ctk.set_appearance_mode(self.config.get_theme())
        
        self._create_widgets()
        self._update_ui()
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="🎮 Gaming Break Timer",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
        # Game selection
        self.game_frame = ctk.CTkFrame(self)
        self.game_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            self.game_frame,
            text="Select Game:",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        
        game_names = [game["name"] for game in self.config.get_games()]
        self.game_dropdown = ctk.CTkComboBox(
            self.game_frame,
            values=game_names,
            command=self._on_game_changed,
            width=250
        )
        self.game_dropdown.set(self.config.get_selected_game())
        self.game_dropdown.pack(side="left", padx=10)
        
        # Timer settings frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=10, padx=20, fill="x")
        
        # Gaming time
        ctk.CTkLabel(
            self.settings_frame,
            text="Gaming Time (minutes):",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.gaming_time_var = ctk.StringVar(value=str(self.config.get_wait_minutes()))
        self.gaming_time_entry = ctk.CTkEntry(
            self.settings_frame,
            textvariable=self.gaming_time_var,
            width=100
        )
        self.gaming_time_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Warning time
        ctk.CTkLabel(
            self.settings_frame,
            text="Warning Time (seconds):",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.warning_time_var = ctk.StringVar(value=str(self.config.get_warning_seconds()))
        self.warning_time_entry = ctk.CTkEntry(
            self.settings_frame,
            textvariable=self.warning_time_var,
            width=100
        )
        self.warning_time_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Time remaining display
        self.time_display = ctk.CTkLabel(
            self,
            text="00:00",
            font=("Arial", 48, "bold")
        )
        self.time_display.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready to start",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)
        
        # Control buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Timer",
            command=self._start_timer,
            width=120,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4b00ab"
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="Stop Timer",
            command=self._stop_timer,
            width=120,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4b00ab",
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=10)
        
        self.settings_button = ctk.CTkButton(
            self.button_frame,
            text="Settings",
            command=self._open_settings,
            width=120,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4b00ab"
        )
        self.settings_button.grid(row=0, column=2, padx=10)
    
    def _on_game_changed(self, choice):
        """Handle game selection change"""
        self.config.set_selected_game(choice)
    
    def _start_timer(self):
        """Start the timer"""
        try:
            wait_minutes = int(self.gaming_time_var.get())
            warning_seconds = int(self.warning_time_var.get())
            
            if wait_minutes <= 0 or warning_seconds <= 0:
                messagebox.showerror("Invalid Input", "Times must be positive numbers")
                return
            
            # Save settings
            self.config.set_wait_minutes(wait_minutes)
            self.config.set_warning_seconds(warning_seconds)
            
            # Get selected game process
            process_name = self.config.get_selected_game_process()
            
            # Start timer
            if self.timer.start_timer(wait_minutes, warning_seconds, process_name):
                self.start_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                self.game_dropdown.configure(state="disabled")
                self.gaming_time_entry.configure(state="disabled")
                self.warning_time_entry.configure(state="disabled")
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")
    
    def _stop_timer(self):
        """Stop the timer"""
        self.timer.stop_timer()
        self._update_ui()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.game_dropdown.configure(state="normal")
        self.gaming_time_entry.configure(state="normal")
        self.warning_time_entry.configure(state="normal")
        self.status_label.configure(text="Timer stopped")
        self.time_display.configure(text="00:00")
    
    def _open_settings(self):
        """Open settings window"""
        from .settings_window import SettingsWindow
        settings = SettingsWindow(self)
        settings.grab_set()  # Make modal
    
    def _on_timer_start(self, wait_minutes: int):
        """Called when timer starts"""
        if self.config.get_show_notifications():
            show_start_notification_threaded(wait_minutes)
    
    def _on_timer_warning(self, warning_seconds: int):
        """Called when warning is shown"""
        if self.config.get_show_notifications():
            show_warning_overlay_threaded(warning_seconds)
    
    def _on_timer_complete(self, process_name: str):
        """Called when timer completes"""
        if close_process(process_name):
            print(f"Closed {process_name}")
        else:
            print(f"Could not find process: {process_name}")
        
        self._stop_timer()
    
    def _on_timer_tick(self, remaining_seconds: int):
        """Called every second to update UI - schedules update on main thread"""
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        # Schedule UI update on main thread to avoid threading issues
        self.after(0, lambda: self.time_display.configure(text=f"{minutes:02d}:{seconds:02d}"))
        self.after(0, lambda: self.status_label.configure(text=f"Timer running..."))
    
    def _update_ui(self):
        """Update UI based on timer status"""
        status = self.timer.get_status()
        
        if status == "running":
            self.status_label.configure(text="Timer running...")
        elif status == "paused":
            self.status_label.configure(text="Timer paused")
        else:
            self.status_label.configure(text="Ready to start")
