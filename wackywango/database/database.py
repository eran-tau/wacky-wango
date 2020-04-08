from .postgres import PostgresDriver


class Database:
    def __init__(self, url):
        self._driver = find_driver(url)

    def get_user(self, user_id):
        return self._driver.get_user(user_id)

    def get_all_users(self):
        return self._driver.get_all_users()

    def get_snapshots(self, user_id):
        return self._driver.get_snapshots(user_id)

    def get_snapshot(self, user_id, snapshot_id):
        return self._driver.get_snapshot(user_id, snapshot_id)

    def get_snapshot_data(self, user_id, snapshot_id, result_name):
        return self._driver.get_snapshot_data(user_id,
                                              snapshot_id,
                                              result_name)

    def create_user(self, user_id, username, birthday):
        return self._driver.create_user(user_id,
                                        username,
                                        birthday)

    def add_snapshot(self, user_id, snapshot_timestamp, parser_type, data):
        return self._driver.add_snapshot(user_id,
                                         snapshot_timestamp,
                                         parser_type, data)


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url!r}')


drivers = {'postgresql://': PostgresDriver}
