import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request
import os
import subprocess
import time
from youtube_search import YoutubeSearch

def search_youtube_and_process(search_term, num_results=10):
    results = YoutubeSearch(search_term, max_results=num_results).to_dict()
    total_sca_count = 0
    total_long_form_count = 0
    total_one_syllable_count = 0
    video_count = 0

    for result in results:
        url = "https://www.youtube.com" + result['url_suffix']
        video_title = result['title']
        video_count += 1
        sca, long, one = process_url(url, video_title)
        total_sca_count += sca
        total_long_form_count += long
        total_one_syllable_count += one

        print(f"\n--- Processed {video_count} videos ---")
        print(f"Running Totals: S-C-A: {total_sca_count}, Long Form: {total_long_form_count}, One Syllable: {total_one_syllable_count}")

    print("\n--- Final Report ---")
    print(f"Total S-C-A pronunciations: {total_sca_count}")
    print(f"Total \"Software Composition Analysis\" mentions: {total_long_form_count}")
    print(f"Total one-syllable (approximate) pronunciations: {total_one_syllable_count}")

def download_audio_video(url, output_dir="downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if "youtube.com" in url:
        try:
            command = ["yt-dlp", "-x", "--audio-format", "wav", "-o", f"{output_dir}/%(title)s.%(ext)s", url]
            subprocess.run(command, check=True)
            print(f"Downloaded audio from YouTube: {url}")
        except FileNotFoundError:
            print("yt-dlp not found. Ensure it is installed and in your PATH.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading from YouTube: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            audio_tags = soup.find_all("audio")
            video_tags = soup.find_all("video")

            for tag in audio_tags + video_tags:
                src = tag.get("src")
                if src:
                    if not src.startswith("http"):
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
    try:
        command = ["whisper", audio_file, "--model", "base.en"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, timeout=600)  # 10 minute timeout
        return process.stdout
    except subprocess.TimeoutExpired:
        return "Transcription timed out."
    except FileNotFoundError:
        return "Whisper not found. Ensure it is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error during transcription: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def count_sca_pronunciations(text):
    sca_count = len(re.findall(r"s[\s-]*c[\s-]*a", text, re.IGNORECASE))
    long_form_count = len(re.findall(r"\bsoftware composition analysis\b", text, re.IGNORECASE))
    one_syllable_count = len(re.findall(r"(ska|scah|skuh|sko|skaw|skee|scas|scas'|scaz|scaze|skas|skase|skaze|skaz'|scase|scaz)", text, re.IGNORECASE))
    return sca_count, long_form_count, one_syllable_count


def process_url(url, video_title):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print(f"\nProcessing video: {video_title}")

    download_audio_video(url)

    audio_files = [f for f in os.listdir("downloads") if f.lower().endswith((".wav"))] #only process wav files.

    total_sca_count = 0
    total_long_form_count = 0
    total_one_syllable_count = 0

    if audio_files: #only process if there are wav files.
        audio_file = audio_files[0] #only process the first wav file.
        audio_path = os.path.join("downloads", audio_file)
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
        print(f"File size: {file_size:.2f} MB")
        transcription = transcribe_audio(audio_path)
        print(f"Transcription of {audio_file}:\n{transcription}")

        sca_count, long_form_count, one_syllable_count = count_sca_pronunciations(transcription)
        total_sca_count += sca_count
        total_long_form_count += long_form_count
        total_one_syllable_count += one_syllable_count

        print(f"S-C-A: {total_sca_count}, Long Form: {total_long_form_count}, One Syllable: {total_one_syllable_count}")

    return total_sca_count, total_long_form_count, total_one_syllable_count

search_youtube_and_process("Software Composition Analysis", num_results=10)