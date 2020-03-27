from flask import Flask
from flask import request
import sqlalchemy as db


def run_api_server(host,port,database):
    server.start(host,port,database)


class Server:
    def start(self, host, port, database):
        app.run(host, port)


server = Server()
app = Flask(__name__)

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

@app.route('/users/', methods=['GET'])
def get_users():
    query = db.select([users.columns.id,users.columns.username])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(ResultSet)
    return repr(ResultSet)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return "TODO"


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_snapshots_for_user(user_id):
    return "TODO:"


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def get_snapshot_for_user(user_id,snapshot_id):
    return "TODO"

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>,<result_name>', methods=['GET'])
def get_snapshot_data_for_user(user_id,snapshot_id,result_name):
    return "TODO"

