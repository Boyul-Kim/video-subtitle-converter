from fastapi import FastAPI
import subtitles
import srt
import video_queue

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/videos/convert")
def convert_video():
    srt_converter = srt.Srt("lecture.m4v.mp4")
    srt_file = srt_converter.run()
    subtitle_converter = subtitles.Subtitles("lecture.m4v.mp4", srt_file)
    subtitle_converter.generate_subtitles("output")
    return {"result": "complete"}

@app.post("videos/convert/all")
def convert_all_videos():
    vid_queue = video_queue.VideoQueue("lecture.m4v.mp4")
    vid_queue.video_enqueue("/path")
    vid_queue.start_worker()
    return {"results", "converting"}

#implement routes for: rabbitMQ