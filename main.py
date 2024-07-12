# from openai import OpenAI
# client = OpenAI()

# audio_file = open('lecture.m4v.mp4', "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="srt"
# )

# print(transcript)

# with open("lecture.srt", "w") as file:
#     file.write(transcript)

import time
import math
import ffmpeg

from faster_whisper import WhisperModel

video = "lecture.m4v.mp4"
video_title = video.replace(".mp4", "")

def video_to_audio():
    audio = f"audio-{video_title}.wav"
    stream = ffmpeg.input(video)
    stream = ffmpeg.output(stream, audio)
    ffmpeg.run(stream, overwrite_output=True)
    return audio

def transcribe(audio):
    model = WhisperModel("small")
    segments, info = model.transcribe(audio)
    language = info[0]
    # print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_srt(language, segments):

    subtitle_file = f"sub-{video_title}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file

def run():
    extracted_audio = video_to_audio()
    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_srt(
        language=language,
        segments=segments
    )
    
run()