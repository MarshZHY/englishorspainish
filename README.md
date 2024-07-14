# englishorspainish
# Motion Detection Tinder Bot

This project integrates motion detection using OpenCV with automated actions on Tinder using Selenium and Chrome WebDriver. When motion is detected, it sends commands to like or unlike profiles on Tinder.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Chrome browser installed.
- ChromeDriver compatible with your Chrome version installed.
- Necessary Python packages installed.

## Installation

1. **Clone the repository**

    ```sh
    git clone https://github.com/yourusername/motion-detection-tinder-bot.git
    cd motion-detection-tinder-bot
    ```

2. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

3. **Download ChromeDriver**

    - Download ChromeDriver from [ChromeDriver - WebDriver for Chrome](https://sites.google.com/chromium.org/driver/downloads).
    - Make sure the ChromeDriver version matches your Chrome browser version.
    - Place the ChromeDriver executable in your system's PATH or specify its path in the code.

4. **Start Chrome with remote debugging**

    Open a terminal and run:

    ```sh
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9999
    ```

## Usage

1. **Run the main script**

    ```sh
    python index.py
    ```

    This script will:

    - Start a separate process to handle Tinder commands.
    - Initialize Pygame for audio playback.
    - Open your webcam using OpenCV and start detecting motion.
    - When motion is detected, it will trigger Tinder actions.

2. **Tinder Automation**

    The Tinder automation part is handled in `modules/tinder.py`. The script connects to the running Chrome instance and performs actions like "like" and "unlike" based on detected motion.

## Project Structure

