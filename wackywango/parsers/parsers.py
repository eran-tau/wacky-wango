from .image_parser import parse_snapshot
import pika
from ..proto import cortex_pb2
import uuid

def parse():
    return 1



def run_parser(parser_type,url):
    def callback(channel, method, properties, body):
        upload_snapshot = cortex_pb2.UploadSnapshot()
        upload_snapshot.ParseFromString(body)
        if parser_type == 'color-image':
            result = parse_snapshot(upload_snapshot.snapshot)
            filename = save_result(result)
            upload_result = cortex_pb2.UploadParserResult()
            upload_result.user.CopyFrom(upload_snapshot.user)
            upload_result.parser_type = cortex_pb2.ParserType.TypeColorImage
            upload_result.data = filename.encode()
            publish_result(url,upload_result)

    params = pika.URLParameters(url)
    # params = pika.ConnectionParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_consume(
        queue='hello',
        auto_ack=True,
        on_message_callback=callback,
    )

    channel.start_consuming()


def publish_result(url,result):
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='color-image')
    channel.basic_publish(
        exchange='',
        routing_key='color-image',
        body=result.SerializeToString(),
    )
    print("published!")


def save_result(result):
    unique_filename = "pics/" + str(uuid.uuid4()) + ".jpg"
    result.save(unique_filename)
    return unique_filename


