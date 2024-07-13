import time
import math
import ffmpeg
from faster_whisper import WhisperModel

class Srt:
    def __init__(self, video):
        self.video = video
        self.video_title = video.replace(".mp4", "")

    # video = "lecture.m4v.mp4"
    # video_title = video.replace(".mp4", "")

    def video_to_audio(self):
        audio = f"audio-{self.video_title}.wav"
        stream = ffmpeg.input(self.video)
        stream = ffmpeg.output(stream, audio)
        ffmpeg.run(stream, overwrite_output=True)
        return audio

    def transcribe(self, audio):
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

    def format_time(self, seconds):
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

        return formatted_time

    def generate_srt(self, language, segments):

        subtitle_file = f"sub-{self.video_title}.{language}.srt"
        text = ""
        for index, segment in enumerate(segments):
            segment_start = self.format_time(segment.start)
            segment_end = self.format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{segment.text} \n"
            text += "\n"
            
        f = open(subtitle_file, "w")
        f.write(text)
        f.close()

        return subtitle_file

    def run(self):
        extracted_audio = self.video_to_audio()
        language, segments = self.transcribe(audio=extracted_audio)
        subtitle_file = self.generate_srt(
            language=language,
            segments=segments
        )
        return subtitle_file