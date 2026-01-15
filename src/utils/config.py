"""Configuration file management"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any
from .constants import (
    DEFAULT_WAIT_MINUTES,
    DEFAULT_WARNING_SECONDS,
    DEFAULT_GAMES,
    DEFAULT_THEME,
    DEFAULT_SHOW_NOTIFICATIONS
)


class Config:
    """Handles loading and saving configuration"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {self.config_path}, using defaults")
                return self._get_default_config()
        else:
            # Create default config file
            config = self._get_default_config()
            self.save_config(config)
            return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "timer": {
                "wait_minutes": DEFAULT_WAIT_MINUTES,
                "warning_seconds": DEFAULT_WARNING_SECONDS
            },
            "games": DEFAULT_GAMES,
            "selected_game": DEFAULT_GAMES[0]["name"],
            "ui": {
                "theme": DEFAULT_THEME,
                "show_notifications": DEFAULT_SHOW_NOTIFICATIONS
            }
        }
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config_data
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        self.config_data = config
    
    # Timer settings
    def get_wait_minutes(self) -> int:
        """Get wait time in minutes"""
        return self.config_data.get("timer", {}).get("wait_minutes", DEFAULT_WAIT_MINUTES)
    
    def set_wait_minutes(self, minutes: int):
        """Set wait time in minutes"""
        if "timer" not in self.config_data:
            self.config_data["timer"] = {}
        self.config_data["timer"]["wait_minutes"] = minutes
        self.save_config()
    
    def get_warning_seconds(self) -> int:
        """Get warning countdown in seconds"""
        return self.config_data.get("timer", {}).get("warning_seconds", DEFAULT_WARNING_SECONDS)
    
    def set_warning_seconds(self, seconds: int):
        """Set warning countdown in seconds"""
        if "timer" not in self.config_data:
            self.config_data["timer"] = {}
        self.config_data["timer"]["warning_seconds"] = seconds
        self.save_config()
    
    # Games management
    def get_games(self) -> List[Dict[str, str]]:
        """Get list of games"""
        return self.config_data.get("games", DEFAULT_GAMES)
    
    def add_game(self, name: str, process_name: str):
        """Add a new game to the list"""
        if "games" not in self.config_data:
            self.config_data["games"] = []
        
        # Check if game already exists
        for game in self.config_data["games"]:
            if game["name"] == name or game["process_name"] == process_name:
                return False
        
        self.config_data["games"].append({
            "name": name,
            "process_name": process_name
        })
        self.save_config()
        return True
    
    def remove_game(self, name: str):
        """Remove a game from the list"""
        if "games" not in self.config_data:
            return False
        
        self.config_data["games"] = [
            game for game in self.config_data["games"] 
            if game["name"] != name
        ]
        self.save_config()
        return True
    
    def get_selected_game(self) -> str:
        """Get currently selected game name"""
        return self.config_data.get("selected_game", DEFAULT_GAMES[0]["name"])
    
    def set_selected_game(self, game_name: str):
        """Set currently selected game"""
        self.config_data["selected_game"] = game_name
        self.save_config()
    
    def get_selected_game_process(self) -> str:
        """Get process name for selected game"""
        selected = self.get_selected_game()
        for game in self.get_games():
            if game["name"] == selected:
                return game["process_name"]
        return DEFAULT_GAMES[0]["process_name"]
    
    # UI settings
    def get_theme(self) -> str:
        """Get UI theme"""
        return self.config_data.get("ui", {}).get("theme", DEFAULT_THEME)
    
    def set_theme(self, theme: str):
        """Set UI theme"""
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["theme"] = theme
        self.save_config()
    
    def get_show_notifications(self) -> bool:
        """Get whether to show notifications"""
        return self.config_data.get("ui", {}).get("show_notifications", DEFAULT_SHOW_NOTIFICATIONS)
    
    def set_show_notifications(self, show: bool):
        """Set whether to show notifications"""
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["show_notifications"] = show
        self.save_config()
