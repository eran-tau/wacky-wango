import requests
import json


class CLI:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def call_api(self, params):
        url = 'http://' + self.host + ':' + str(self.port) + '/'+params
        r = requests.get(url)
        if r.status_code == 200:
            data = json.loads(r.content)
            return data['result']
        else:
            return "Not Found"

    def get_users(self):
        return self.call_api("users")

    def get_user(self, user_id):
        return self.call_api("users/"+user_id)

    def get_snapshots(self, user_id):
        return self.call_api("users/" + user_id+"/snapshots")

    def get_snapshot(self, user_id, snapshot_id):
        return self.call_api("users/" + user_id+"/snapshots/"+snapshot_id)

    def get_result(self, user_id, snapshot_id, parser_type):
        return self.call_api("users/"+user_id+"/snapshots/" +
                             snapshot_id+'/'+parser_type)

    def get_result_and_save(self, user_id, snapshot_id, parser_type, path):
        data = self.get_result(user_id, snapshot_id, parser_type)
        file = open(path, 'w')
        file.write(data)
        file.close()
