import pika

def create_channel(channel_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=channel_name)
    return connection, channel

def send_to_channel(channel, body, routing_key):
    channel.basic_publish(exchange='',
                      routing_key=routing_key,
                      body=body)
    print(" [x] Sent 'Hello World!'")

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

connection, channel = create_channel("hello")
send_to_channel(channel, "hello world", "hello")
# connection.close()

channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

