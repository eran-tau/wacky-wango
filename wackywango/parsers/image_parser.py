from PIL import Image
import pika
from ..proto import cortex_pb2


def parse_snapshot(snap,name):
    image = Image.frombytes('RGB', (snap.color_image.width, snap.color_image.height), snap.color_image.data)
    image.save("pics/" + name)

i = 0
def callback(channel, method, properties, body):
    global i
    i += 1
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(body)
    parse_snapshot(upload_snapshot.snapshot, "test" + str(i) + ".jpg")

params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello')


channel.basic_consume(
    queue='hello',
    auto_ack=True,
    on_message_callback=callback,
)

channel.start_consuming()
