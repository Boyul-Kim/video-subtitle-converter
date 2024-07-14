import pika
import os
import srt
import subtitles

class VideoQueue:

    def __init__(self, video):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.queue_name = 'video_queue'
        self.video = video
        self.video_title = video.replace(".mp4", "")
        self.setup_queue()

    def setup_queue(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        print("Queue created")

    def video_enqueue(self, directory_path):
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        for filename in os.listdir(directory_path):
            if filename.endswith('.mp4'):
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue_name,
                    body=filename,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
                print(f"Enqueued: {filename}")

    def callback(self, ch, method, properties, body):
        srt_converter = srt.Srt(self.video)
        srt_file = srt_converter.run()
        subtitle_converter = subtitles.Subtitles(self.video, srt_file)
        subtitle_converter.generate_subtitles(self.video_title + "-" + "output")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #update so that it saves video in a specific directory so that it can be referred to
        print(f"Processed and acknowledged")

    def start_worker(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
        print("Connection closed")

    # def create_channel(channel_name):
    #     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    #     channel = connection.channel()
    #     channel.queue_declare(queue=channel_name, durable=True)
    #     return connection, channel

    # def send_to_channel(channel, body, routing_key):
    #     channel.basic_publish(exchange='',
    #                     routing_key=routing_key,
    #                     body=body,
    #                     properties=pika.BasicProperties(
    #                         delivery_mode = pika.DeliveryMode.Persistent
    #                     ))
    #     print(" [x] Sent 'Hello World!'")

    # def callback(ch, method, properties, body):
    #     print(f" [x] Received {body}")

    # connection, channel = create_channel("hello")
    # send_to_channel(channel, "hello world", "hello")
    # # connection.close()
    # channel.basic_qos(prefetch_count=1)
    # channel.basic_consume(queue='hello',
    #                     auto_ack=True,
    #                     on_message_callback=callback)

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

