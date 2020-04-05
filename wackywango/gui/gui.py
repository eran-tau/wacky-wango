from flask import Flask
from flask import render_template




def run_server(host, port, api_host, api_port):
    server.start(host, port, api_host, api_port)


class Server:
    def start(self, host, port, api_host, api_port):
        app.config['api_host'] = api_host
        app.config['api_port'] = api_port
        app.run(host, port)


server = Server()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('index.html', api_url=api_url)


@app.route('/users/', methods=['GET'])
def users():
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('users.html', api_url=api_url,title="Users")

@app.route('/users/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('user.html', api_url=api_url, user_id=user_id)

@app.route('/users/<int:user_id>/snapshots/', methods=['GET'])
def user_snapshots(user_id):
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('snapshots.html', api_url=api_url, user_id=user_id)


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/', methods=['GET'])
def user_snapshot(user_id,snapshot_id):
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('snapshot.html', api_url=api_url, user_id=user_id,snapshot_id=snapshot_id)

@app.route('/analytics/', methods=['GET'])
def analytics():
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('users.html', api_url=api_url,title="Analyitcs")

@app.route('/analytics/<int:user_id>/', methods=['GET'])
def get_user_analytics(user_id):
    api_url = "http://"+app.config['api_host']+":"+app.config['api_port']
    return render_template('analytics.html', api_url=api_url, user_id=user_id)
