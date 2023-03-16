# PDF2MP3_TelegramBot

This is a Telegram bot that allows users to convert PDF documents into MP3 audio files. It is particularly useful for people who want to listen to long documents but don't have the time or ability to read them.

The bot is built using Python and the [**pyTelegramBotAPI**](https://pypi.org/project/pyTelegramBotAPI/) library. It uses [**gtts**](https://pypi.org/project/gTTS/) library for text-to-speech conversion and [**pdfplumber**](https://pypi.org/project/pdfplumber/) library for PDF parsing.

## Features

+ Convert PDF documents into MP3 audio files
+ Ability to split large PDF files into smaller MP3 files
+ Language selection for voiceover
+ Easy to use and navigate

## Usage

1. Add the bot to your Telegram contacts by searching for "@PDF2MP3_bot".
2. Send a PDF document to the bot.
3. Select the language for the voiceover.
4. The bot will convert the PDF document into an MP3 audio file.
5. If the PDF document is too large, the bot will ask you if you want to split it into smaller MP3 files.
6. Download the MP3 file(s) and enjoy!

## Installation

1. Clone the repository to your local machine.
2. Create a new virtual environment and activate it.
3. Install the required libraries using '**pip install -r requirements.txt**'.
4. Create '**.env**' file in bot directory and put there your bot token.
5. Run '**python main.py**' to start the bot.

## Contributing

Contributions to this project are always welcome. If you find a bug or have an idea for a new feature, please open an issue on the GitHub repository or create a pull request.

License
This project is licensed under the MIT License - see the **LICENSE** file for details.
