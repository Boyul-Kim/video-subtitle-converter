import subtitles
import srt

srt_converter = srt.Srt("lecture.m4v.mp4")
srt_file = srt_converter.run()
subtitle_converter = subtitles.Subtitles("lecture.m4v.mp4", srt_file)
subtitle_converter.generate_subtitles("output")