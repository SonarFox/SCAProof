# YouTube SCA Pronunciation Counter

This Python script searches YouTube for videos related to "Software Composition Analysis," downloads the audio, transcribes it, and counts the occurrences of different pronunciations of "SCA" (S-C-A, Software Composition Analysis, and one-syllable variations).

## Prerequisites

Before running the script, ensure you have the following installed:

1.  **Python 3:** Python 3 is required to run the script. You can download it from [python.org](https://www.python.org/downloads/).
2.  **pip:** pip is Python's package installer. It is usually included with Python installations.
3.  **yt-dlp:** This tool is used to download audio from YouTube videos.

    * **macOS (Homebrew):**
        ```bash
        /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
        brew install yt-dlp
        ```
    * **macOS (pip):**
        ```bash
        pip3 install yt-dlp
        ```
4.  **Whisper:** This is the speech-to-text tool used for transcription.

    * Install it using pip:
        ```bash
        pip install whisper
        ```
    * **Note:** Whisper requires `ffmpeg` to be installed. If you do not have it, you can install it using brew on MacOS: `brew install ffmpeg`

5.  **Python Libraries:** Install the necessary Python libraries using pip:

    ```bash
    pip install requests beautifulsoup4 youtube-search-python
    ```

## Installation and Setup

1.  **Clone the Repository (Optional):** If you have the script in a Git repository, clone it:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a `downloads` Directory:** The script downloads audio files to a directory named `downloads`. Create this directory in the same location as your script:

    ```bash
    mkdir downloads
    ```

## Running the Script

1.  **Navigate to the Script Directory:** Open a terminal or command prompt and navigate to the directory where the script is located.

2.  **Run the Script:** Execute the Python script:

    ```bash
    python main.py
    ```

    The script will search YouTube for "Software Composition Analysis," download the audio from the top 10 videos, transcribe them, and display the counts of different SCA pronunciations.

## Script Functionality

* **YouTube Search:** The script uses the `youtube-search-python` library to search YouTube for videos related to "Software Composition Analysis."
* **Audio Download:** The `yt-dlp` tool is used to download the audio from the YouTube videos.
* **Transcription:** The Whisper speech-to-text tool is used to transcribe the downloaded audio.
* **Pronunciation Counting:** The script uses regular expressions to count the occurrences of "S-C-A," "Software Composition Analysis," and one-syllable variations of "SCA" in the transcribed text.
* **Output:** The script prints the transcription, individual video counts, running totals, and a final report with the overall counts.

## Troubleshooting

* **`yt-dlp` or Whisper not found:** Ensure that `yt-dlp` and Whisper are installed and in your system's PATH.
* **Transcription timed out:** If you encounter timeout errors, try increasing the timeout value in the `transcribe_audio` function or using a smaller Whisper model.
* **Incorrect counts:** The regular expressions used for counting pronunciations might need adjustments depending on the variations in the transcribed text. Inspect the transcriptions to identify any patterns.
* **Multiple audio files downloaded:** The script now only uses the first .wav file found in the downloads directory.
* **NameError: name 'search_youtube_and_process' is not defined:** Ensure the function is defined before it is called.

## Dependencies

* `requests`
* `beautifulsoup4`
* `youtube-search-python`
* `yt-dlp`
* `whisper`

## Notes

* This script requires an internet connection to search YouTube and download audio.
* The accuracy of the pronunciation counts depends on the accuracy of the Whisper speech-to-text engine.
* The script downloads audio files to the `downloads` directory. Ensure that this directory exists and has write permissions.
