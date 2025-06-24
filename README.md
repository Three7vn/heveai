# Heve AI

Hold **Right Option (⌥)** and speak to instantly dictate text into any app.

## How it works

1. Hold down the **Right Option (⌥)** key - to the right of spacebar
2. Speak naturally 
3. Release **Right Option** key
4. Text appears in your active app

## Why Right Option instead of Fn?

The **Fn key** on Mac is handled at hardware level and cannot be reliably detected by software. **Right Option (⌥)** is right next to the spacebar and works perfectly for hold-to-talk functionality.

## Features

- **Privacy-first**: All processing happens locally on your device
- **Universal**: Works in any application
- **Fast**: Real-time speech recognition with Vosk
- **Simple**: Just hold Right Option and speak

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download speech model (~40MB)
python install_model.py

# Run the app
python main.py
```

## Usage

Run the app and hold **Right Option (⌥)** while speaking. Text will be typed wherever your cursor is.

**Important**: If text doesn't appear, you need to grant accessibility permissions:
- **System Settings** → **Privacy & Security** → **Accessibility** 
- Add **Terminal** and enable it

Press **Ctrl+C** to quit. 