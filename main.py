from pytube import YouTube
from pytube.contrib.search import Search
from youtube_transcript_api import YouTubeTranscriptApi
import re
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

def analyze_sca_pronunciation(query="Software Composition Analysis", num_videos=10):
    try:
        s = Search(query)
        s.results #this line forces the search to happen.
        video_ids = [result.video_id for result in s.results[:num_videos]] # get video id's
        sca_count_sca = 0
        sca_count_skaw = 0

        for video_id in video_ids:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_transcript = " ".join([item['text'] for item in transcript])

                sca_count_sca += len(re.findall(r"\bS\s*[-.]?\s*C\s*[-.]?\s*A\b", full_transcript, re.IGNORECASE))
                sca_count_skaw += len(re.findall(r"\bskaw\b", full_transcript, re.IGNORECASE))

            except Exception as transcript_error:
                print(f"Error processing transcript for video {video_id}: {transcript_error}")

        return sca_count_sca, sca_count_skaw

    except Exception as search_error:
        print(f"Error during search or overall processing: {search_error}")
        return None

if __name__ == "__main__":
    counts = analyze_sca_pronunciation()
    if counts:
        sca_count, skaw_count = counts
        print(f"Count of 'S-C-A': {sca_count}")
        print(f"Count of 'skaw': {skaw_count}")