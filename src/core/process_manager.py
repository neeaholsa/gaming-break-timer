"""Process management for closing games"""
import psutil


def close_process(process_name: str) -> bool:
    """
    Close the specified process
    
    Args:
        process_name: Name of the process to close (e.g., "game.exe")
    
    Returns:
        True if process was found and closed, False otherwise
    """
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                print(f"Closed {process_name}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def is_process_running(process_name: str) -> bool:
    """
    Check if a process is currently running
    
    Args:
        process_name: Name of the process to check
    
    Returns:
        True if process is running, False otherwise
    """
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False
