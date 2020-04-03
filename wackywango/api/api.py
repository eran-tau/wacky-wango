from flask import Flask
from flask import current_app
from ..database import Database
from flask import jsonify

def run_api_server(host,port,database):
    server.start(host,port,database)


class Server:
    def start(self, host, port, database):
        app.config['database'] = Database(database)
        app.run(host, port)


server = Server()
app = Flask(__name__)


@app.route('/users/', methods=['GET'])
def get_users():
    db = current_app.config['database']

    return repr(db.get_all_users())


@app.route('/users/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    db = current_app.config['database']
    user = db.get_user(user_id)
    return jsonify({'result': dict(user[0])})



@app.route('/users/<int:user_id>/snapshots/', methods=['GET'])
def get_snapshots_for_user(user_id):
    db = current_app.config['database']
    snapshots = db.get_snapshots(user_id)
    return jsonify({'result': [dict(row) for row in snapshots]})


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/', methods=['GET'])
def get_snapshot_for_user(user_id,snapshot_id):
    db = current_app.config['database']
    snapshots = db.get_snapshot(user_id,snapshot_id)
    result = {"snapshot_id":snapshots['snapshot']['id'],"snapshot_timestamp":snapshots['snapshot']['snapshot_timestamp'],"snapshot_types":[dict(row) for row in snapshots['snapshot_data']]}
    return jsonify({'result': result})

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/', methods=['GET'])
def get_snapshot_data_for_user(user_id,snapshot_id,result_name):
    db = current_app.config['database']
    snapshots = db.get_snapshot_data(user_id,snapshot_id,result_name)
    return jsonify({'result': dict(snapshots[0])})

