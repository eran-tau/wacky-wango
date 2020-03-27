import pika
from ..proto import cortex_pb2
import uuid
import sqlalchemy as db
from datetime import datetime as dt

class Saver:
    def __init__(self, database_url):
        self.db = database_url


def save_once():
    return 1

def run_saver(database_url, queue_url):
    def callback(channel, method, properties, body):
        print("consumed")
        upload_snapshot = cortex_pb2.UploadParserResult()
        upload_snapshot.ParseFromString(body)
        # if channel == 'color-image':
        save_result(upload_snapshot)

    params = pika.URLParameters(queue_url)
    # params = pika.ConnectionParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='color-image')

    channel.basic_consume(
        queue='color-image',
        auto_ack=True,
        on_message_callback=callback,
    )
    print("hello")

    channel.start_consuming()


def save_result(result):
    print(result)
    engine = db.create_engine('postgresql://postgres:password@localhost/db')
    metadata = db.MetaData()
    users = db.Table('users', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('username', db.String, nullable=False),
        db.Column('birthday', db.DateTime, nullable=False),
    )
    snapshots = db.Table('snapshots', metadata,
         db.Column('id', db.Integer, primary_key=True),
         db.Column('parser_type', db.String, nullable=False),
         db.Column('data', db.String, nullable=False),
     )


    metadata.create_all(engine)
    connection = engine.connect()
    query = db.select([users]).where(users.columns.id == result.user.user_id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    if not ResultSet:
        insert = users.insert().values(id=result.user.user_id, username=result.user.username,birthday=dt.fromtimestamp(result.user.birthday))
        result2 = connection.execute(insert)
        result2.inserted_primary_key
        print("adding user")

    if (result.parser_type == cortex_pb2.ParserType.TypeColorImage):
        insert2 = snapshots.insert().values(parser_type=result.parser_type,
                                       data=result.data.decode())
        result3 = connection.execute(insert2)
        result3.inserted_primary_key
        print("adding snapshot")





