import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import os
import subprocess

def download_audio_video(url, output_dir="downloads"):
    """Downloads audio and video files from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find audio and video tags
        audio_tags = soup.find_all("audio")
        video_tags = soup.find_all("video")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for tag in audio_tags + video_tags:
            src = tag.get("src")
            if src:
                if not src.startswith("http"): #handle relative paths
                    src = urljoin(url, src)

                filename = os.path.join(output_dir, src.split("/")[-1])
                try:
                    urllib.request.urlretrieve(src, filename)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {src}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def transcribe_audio(audio_file):
    """Transcribes audio using a local speech-to-text tool (e.g., whisper)."""
    try:
        # Replace with your actual speech-to-text command
        # This example uses whisper. Ensure it's installed and in your PATH.
        command = ["whisper", audio_file, "--model", "base.en"] #or small, medium, large.en
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        return process.stdout
    except FileNotFoundError:
        return "Whisper not found. Ensure it is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error during transcription: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def count_sca_pronunciations(text):
    """Counts "S-C-A", "Software Composition Analysis", and one-syllable pronunciations in the transcribed text."""
    sca_count = len(re.findall(r"\bS-C-A\b|\bS\.C\.A\b|\bS C A\b", text, re.IGNORECASE))
    long_form_count = len(re.findall(r"\bSoftware Composition Analysis\b", text, re.IGNORECASE))

    # More comprehensive regex for one-syllable pronunciations
    # This tries to capture variations that sound like "ska", "scah", etc.
    # It's still challenging to be exhaustive without phonetic analysis.
    one_syllable_count = len(re.findall(r"\b(ska|scah|skuh|sko|skaw|skee)\b", text, re.IGNORECASE))

    return sca_count, long_form_count, one_syllable_count

def process_url(url):
    """Downloads audio/video, transcribes, and counts pronunciations for a URL."""
    download_audio_video(url)

    audio_files = [f for f in os.listdir("downloads") if f.lower().endswith((".mp3", ".wav", ".ogg", ".flac", ".m4a"))] #add other audio extensions as needed.
    total_sca_count = 0
    total_long_form_count = 0
    total_one_syllable_count = 0

    for audio_file in audio_files:
        audio_path = os.path.join("downloads", audio_file)
        transcription = transcribe_audio(audio_path)
        print(f"Transcription of {audio_file}:\n{transcription}")

        sca_count, long_form_count, one_syllable_count = count_sca_pronunciations(transcription)
        total_sca_count += sca_count
        total_long_form_count += long_form_count
        total_one_syllable_count += one_syllable_count

    print(f"\nTotal S-C-A pronunciations: {total_sca_count}")
    print(f"Total \"Software Composition Analysis\" mentions: {total_long_form_count}")
    print(f"Total one-syllable (approximate) pronunciations: {total_one_syllable_count}")

# Example usage:
# process_url("YOUR_URL_HERE") # Replace with the URL you want to process.

# Example of how to iterate through many urls.
urls = [
    "YOUR_URL_1_HERE",
    "YOUR_URL_2_HERE",
    # Add more URLs as needed
]
for url in urls:
    process_url(url)