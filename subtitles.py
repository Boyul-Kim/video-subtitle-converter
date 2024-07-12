import ffmpeg

video = ffmpeg.input("lecture.m4v.mp4")
audio = video.audio
ffmpeg.concat(video.filter("subtitles", "sub-lecture.m4v.en.srt"), audio, v=1, a=1).output("output.mp4").run()