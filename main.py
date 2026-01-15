"""
Gaming Break Timer
A desktop application to manage gaming time and enforce breaks
"""
from src.gui.main_window import MainWindow


def main():
    """Main entry point"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()