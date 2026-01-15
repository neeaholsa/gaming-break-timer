"""Gaming break timer logic"""
import time
import threading
from typing import Callable, Optional


class GamingTimer:
    """Manages the gaming break timer"""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.timer_thread: Optional[threading.Thread] = None
        self.remaining_seconds = 0
        self.total_seconds = 0
        
        # Callbacks
        self.on_timer_start: Optional[Callable] = None
        self.on_timer_warning: Optional[Callable] = None
        self.on_timer_complete: Optional[Callable] = None
        self.on_timer_tick: Optional[Callable[[int], None]] = None
    
    def start_timer(self, wait_minutes: int, warning_seconds: int, 
                   process_name: str):
        """
        Start the gaming timer
        
        Args:
            wait_minutes: How many minutes to wait before warning
            warning_seconds: How many seconds for the warning countdown
            process_name: Process name to close when timer completes
        """
        if self.is_running:
            return False
        
        self.is_running = True
        self.is_paused = False
        self.total_seconds = wait_minutes * 60
        self.remaining_seconds = self.total_seconds
        
        # Start timer in separate thread
        self.timer_thread = threading.Thread(
            target=self._timer_loop,
            args=(wait_minutes, warning_seconds, process_name),
            daemon=True
        )
        self.timer_thread.start()
        
        # Trigger start callback
        if self.on_timer_start:
            self.on_timer_start(wait_minutes)
        
        return True
    
    def _timer_loop(self, wait_minutes: int, warning_seconds: int, 
                   process_name: str):
        """Internal timer loop"""
        start_time = time.time()
        
        # Main countdown
        while self.is_running and self.remaining_seconds > 0:
            if not self.is_paused:
                elapsed = int(time.time() - start_time)
                self.remaining_seconds = self.total_seconds - elapsed
                
                # Update UI every second
                if self.on_timer_tick:
                    self.on_timer_tick(max(0, self.remaining_seconds))
            
            time.sleep(1)
        
        if not self.is_running:
            return
        
        # Trigger warning
        if self.on_timer_warning:
            self.on_timer_warning(warning_seconds)
        
        # Warning countdown
        time.sleep(warning_seconds)
        
        if not self.is_running:
            return
        
        # Timer complete
        if self.on_timer_complete:
            self.on_timer_complete(process_name)
        
        self.is_running = False
    
    def stop_timer(self):
        """Stop the timer"""
        self.is_running = False
        self.is_paused = False
        self.remaining_seconds = 0
    
    def pause_timer(self):
        """Pause the timer"""
        if self.is_running:
            self.is_paused = True
    
    def resume_timer(self):
        """Resume the timer"""
        if self.is_running:
            self.is_paused = False
    
    def get_remaining_time(self) -> tuple[int, int]:
        """
        Get remaining time
        
        Returns:
            Tuple of (minutes, seconds)
        """
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return minutes, seconds
    
    def get_status(self) -> str:
        """Get current timer status"""
        if not self.is_running:
            return "stopped"
        elif self.is_paused:
            return "paused"
        else:
            return "running"
