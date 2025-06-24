# Heve AI

**Intelligent real-time speech-to-text for people who hate typing (like me).**

Hold **Right Option (⌥)** and speak to instantly dictate text into any app.

## How it works

1. Hold down the **Right Option (⌥)** key - to the right of spacebar
2. Speak naturally 
3. Release **Right Option** key
4. Text appears in your active app

## Features

- **Privacy-first**: All processing happens locally on your device
- **Universal**: Works in any application
- **Fast**: Real-time speech recognition with Whisper
- **Simple**: Just hold Right Option and speak
- **Ultra-fast typing**: 50x faster text injection
- **Auto-start**: Runs automatically when you login

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Auto-Start Setup

To have Heve AI automatically start when you login:

```bash
# Copy service file to LaunchAgents (already done during installation)
cp com.heveai.dictation.plist ~/Library/LaunchAgents/

# Load the service (starts immediately and on every login)
launchctl load ~/Library/LaunchAgents/com.heveai.dictation.plist
```

## Service Management

Use the included service control script:

```bash
# Check if service is running
./service_control.sh status

# Start the service
./service_control.sh start

# Stop the service
./service_control.sh stop

# Restart the service
./service_control.sh restart

# View recent logs
./service_control.sh logs

# Disable auto-start completely
./service_control.sh disable
```

## Usage

Run the app and hold **Right Option (⌥)** while speaking. Text will be typed wherever your cursor is.

**Important**: If text doesn't appear, you need to grant accessibility permissions:
- **System Settings** → **Privacy & Security** → **Accessibility** 
- Add **Terminal** and enable it

Once the service is running, just **hold Right Option (⌥) and speak** - it's always ready!

Press **Ctrl+C** to quit (if running manually).

## Need Help?

If you need help setting up Heve AI, email avram {at} beesumbodi.com. 