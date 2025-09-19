# Heve AI

**Intelligent, privacy-first real-time speech-to-text for people who hate typing (like me).**

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
- **Ultra-fast typing**: Sub-second text injection
- **Real-time Grammar Correction**: Automatic grammar enhancement using Gramformer (for short phrases)
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
# 1. Create your custom plist file from template
cp com.heveai.dictation.plist.template com.heveai.dictation.plist

# 2. Edit the file and replace "/path/to/your/heveai" with your actual path
# 3. Copy service file to LaunchAgents
cp com.heveai.dictation.plist ~/Library/LaunchAgents/

# 4. Load the service (starts immediately and on every login)
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
- Add **Terminal** and **Python** and enable it

Once the service is running, just **hold Right Option (⌥) and speak** - it's always ready!

Press **Ctrl+C** to quit (if running manually).

## Supervised Fine-Tuning

Heve AI automatically collects training data for model improvement:

- **Data Collection**: Audio and transcriptions saved to `training/data/`
- **Manual Correction**: Edit `training/data/transcriptions.csv` to add corrected transcriptions
- **Methodology**: LoRA fine-tuning with 4-bit quantization for efficiency
- **Benefits**: Better accuracy for your voice, vocabulary, and speaking patterns

Recommended to have 100+ corrected samples to start training.

## Grammar Correction

Includes real-time grammar correction using Gramformer:

- **Automatic Enhancement**: Grammar, punctuation, and capitalization improvements
- **Processing**: Only applied to short phrases (≤50 words) to prevent text truncation (current flaw)
- **Preserves Meaning**: Conservative corrections that maintain your original intent
- **Dual Logging**: Both original and corrected transcriptions saved for training data

**Future Enhancement**: The next step is implementing a local language model for real-time grammar correction instead of Gramformer, providing better accuracy and handling longer text.

## Need Help?

If you need help setting up Heve AI, email avram {at} beesumbodi.me.