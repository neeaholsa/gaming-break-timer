# 🎮 Gaming Break Timer

A desktop application to manage gaming time and enforce breaks by automatically closing games after a set duration.

## 📖 About This Project

This project was created to solve a personal need - having a reliable way to enforce gaming time limits. As someone who wanted a tool that would automatically close games after a certain time period with a fair warning, I decided to build it myself.

This is also a learning project where I'm practicing and testing coding with GitHub Copilot, exploring how AI-assisted development can help bring ideas to life quickly.

## ✨ Features

- ⏱️ **Customizable Timer**: Set your gaming session length (in minutes)
- ⚠️ **Warning Countdown**: Get a configurable warning (in seconds) before your game closes
- 🎯 **Game Management**: Add and manage multiple games with their process names
- 🎨 **Modern UI**: Built with CustomTkinter for a sleek dark theme interface
- 💾 **Persistent Settings**: All your preferences are saved automatically
- 🔔 **Visual Notifications**: Clear on-screen notifications when timer starts and when time's up

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Windows 10/11 (tested on Windows)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/gaming-break-timer.git
   cd gaming-break-timer
   ```

2. **Install dependencies:**

   ```bash
   py -m pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   py main.py
   ```

### Building an Executable (Optional)

To create a standalone `.exe` file:

```bash
py -m pip install pyinstaller
pyinstaller --onefile --name "GamingBreakTimer" main.py
```

The executable will be in the `dist` folder.

## 📝 Usage

1. **Select a game** from the dropdown (or add your own in Settings)
2. **Set gaming time** (minutes) and **warning time** (seconds)
3. **Click "Start Timer"** before you start playing
4. The timer runs in the background
5. When time's up, you'll see a countdown warning
6. After the countdown, the game closes automatically

### Adding New Games

1. Click the **Settings** button
2. Enter the game name and process name (e.g., `game.exe`)
3. Click **Add Game**
4. Find process names in Task Manager → Details tab

## 🛠️ Tech Stack

- **Python 3.14**
- **CustomTkinter** - Modern UI framework
- **psutil** - Process management
- **tkinter** - Notification overlays

## 📂 Project Structure

```
gaming_break/
├── main.py                 # Entry point
├── config.json            # User settings
├── requirements.txt       # Dependencies
├── src/
│   ├── core/             # Timer and process logic
│   ├── gui/              # UI components
│   └── utils/            # Configuration management
└── assets/               # Icons and resources
```

## ⚙️ Configuration

Settings are stored in `config.json` and include:

- Timer duration (minutes)
- Warning countdown (seconds)
- Game list with process names
- UI theme preferences
- Notification settings

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

MIT License - feel free to use and modify for your own needs.

## 🙏 Acknowledgments

Built with assistance from GitHub Copilot as a practical exercise in AI-assisted development.
