"""Settings window for managing games and preferences"""
import customtkinter as ctk
from tkinter import messagebox
from ..utils.config import Config
from ..utils.constants import COLOR_PRIMARY, COLOR_PRIMARY_HOVER


class SettingsWindow(ctk.CTkToplevel):
    """Settings window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.config = Config()
        self.parent = parent
        
        # Window setup
        self.title("Settings")
        
        # Center on parent window
        window_width = 500
        window_height = 500
        self.geometry(f"{window_width}x{window_height}")
        self.update_idletasks()
        
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make window modal
        self.transient(parent)
        self.focus()
        
        self._create_widgets()
        self._load_games()
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)
        
        # Games section
        games_frame = ctk.CTkFrame(self)
        games_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            games_frame,
            text="Manage Games",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Games list
        self.games_list = ctk.CTkTextbox(
            games_frame,
            width=400,
            height=200
        )
        self.games_list.pack(pady=10, padx=10)
        
        # Add game section
        add_frame = ctk.CTkFrame(games_frame)
        add_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(
            add_frame,
            text="Game Name:"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.game_name_entry = ctk.CTkEntry(add_frame, width=150)
        self.game_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(
            add_frame,
            text="Process Name:"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.process_name_entry = ctk.CTkEntry(add_frame, width=150)
        self.process_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        button_frame = ctk.CTkFrame(add_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Add Game",
            command=self._add_game,
            width=100,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Remove Selected",
            command=self._remove_game,
            width=120,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
        ).pack(side="left", padx=5)
        
        # UI Settings
        ui_frame = ctk.CTkFrame(self)
        ui_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            ui_frame,
            text="UI Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(ui_frame)
        theme_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:"
        ).pack(side="left", padx=10)
        
        self.theme_var = ctk.StringVar(value=self.config.get_theme())
        theme_dropdown = ctk.CTkComboBox(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self._change_theme,
            width=150
        )
        theme_dropdown.pack(side="left", padx=10)
        
        # Notifications toggle
        self.notifications_var = ctk.BooleanVar(value=self.config.get_show_notifications())
        notifications_check = ctk.CTkCheckBox(
            ui_frame,
            text="Show Notifications",
            variable=self.notifications_var,
            command=self._toggle_notifications
        )
        notifications_check.pack(pady=10)
        
        # Close button
        ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=120,
            fg_color=COLOR_PRIMARY
        ).pack(pady=20)
    
    def _load_games(self):
        """Load games list"""
        self.games_list.delete("1.0", "end")
        
        games = self.config.get_games()
        selected = self.config.get_selected_game()
        
        for game in games:
            prefix = "✅ " if game["name"] == selected else "   "
            self.games_list.insert("end", f"{prefix}{game['name']} - {game['process_name']}\n")
        
        self.games_list.configure(state="disabled")
    
    def _add_game(self):
        """Add a new game"""
        name = self.game_name_entry.get().strip()
        process = self.process_name_entry.get().strip()
        
        if not name or not process:
            messagebox.showerror("Invalid Input", "Please enter both game name and process name")
            return
        
        if not process.endswith(".exe"):
            process += ".exe"
        
        if self.config.add_game(name, process):
            messagebox.showinfo("Success", f"Added {name}")
            self.game_name_entry.delete(0, "end")
            self.process_name_entry.delete(0, "end")
            self._load_games()
            
            # Update parent dropdown
            if hasattr(self.parent, 'game_dropdown'):
                game_names = [game["name"] for game in self.config.get_games()]
                self.parent.game_dropdown.configure(values=game_names)
        else:
            messagebox.showerror("Error", "Game already exists")
    
    def _remove_game(self):
        """Remove selected game"""
        # Get selected text (this is a simple implementation)
        # In a real app, you'd want a proper list widget
        try:
            text = self.games_list.get("1.0", "end")
            lines = text.strip().split("\n")
            
            # Find game with checkmark
            for line in lines:
                if line.startswith("✅"):
                    game_name = line.replace("✅", "").strip().split(" - ")[0].strip()
                    
                    if len(self.config.get_games()) <= 1:
                        messagebox.showerror("Error", "Cannot remove the last game")
                        return
                    
                    confirm = messagebox.askyesno(
                        "Confirm Removal",
                        f"Remove {game_name}?"
                    )
                    
                    if confirm:
                        self.config.remove_game(game_name)
                        self._load_games()
                        
                        # Update parent dropdown
                        if hasattr(self.parent, 'game_dropdown'):
                            game_names = [game["name"] for game in self.config.get_games()]
                            self.parent.game_dropdown.configure(values=game_names)
                            self.parent.game_dropdown.set(game_names[0])
                            self.config.set_selected_game(game_names[0])
                    return
            
            messagebox.showinfo("Info", "Click on a game in the list to select it first")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not remove game: {e}")
    
    def _change_theme(self, choice):
        """Change UI theme"""
        self.config.set_theme(choice)
        ctk.set_appearance_mode(choice)
    
    def _toggle_notifications(self):
        """Toggle notifications on/off"""
        self.config.set_show_notifications(self.notifications_var.get())
