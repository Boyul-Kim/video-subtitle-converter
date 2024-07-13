import ffmpeg

class Subtitles:
    def __init__(self, video, srt):
        self.video = video
        self.audio = video.audio
        self.srt = srt

    def generate_subtitles(self, output_title):
        ffmpeg.concat(self.video.filter("subtitles", self.srt), self.audio, v=1, a=1).output(output_title + ".mp4").run()