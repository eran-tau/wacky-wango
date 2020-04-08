import json
import sqlalchemy as db
from sqlalchemy.sql import and_
from datetime import datetime as dt


class PostgresDriver:

    def __init__(self, url):
        url = url.replace("postgresql://", "postgresql://postgres:password@") + "/postgres"
        engine = db.create_engine(url)
        metadata = db.MetaData()
        self.users = db.Table('users',
                              metadata,
                              db.Column('id', db.Integer, primary_key=True),
                              db.Column('username', db.String, nullable=False),
                              db.Column('birthday', db.DateTime, nullable=False)
                              )
        self.snapshots = db.Table('snapshots',
                                  metadata,
                                  db.Column('id', db.Integer, primary_key=True),
                                  db.Column('user_id', db.Integer, nullable=False),
                                  db.Column('snapshot_timestamp', db.String, nullable=False)
                                  )

        self.snapshots_data = db.Table('snapshots_data',
                                       metadata,
                                       db.Column('id', db.Integer, primary_key=True),
                                       db.Column('snapshot_id', db.Integer, nullable=False),
                                       db.Column('parser_type', db.String, nullable=False),
                                       db.Column('data', db.String, nullable=False)
                                       )
        metadata.create_all(engine)
        self.connection = engine.connect()

    def get_user(self, user_id):
        query = db.select([self.users]).where(self.users.columns.id == user_id)
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def get_all_users(self):
        query = db.select([self.users.columns.id, self.users.columns.username])
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def get_snapshots(self, user_id):
        query = db.select([self.snapshots.c.id, self.snapshots.c.snapshot_timestamp]).where(self.snapshots.columns.user_id == user_id)
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def get_snapshot(self, user_id, snapshot_id):
        # Get the snapshot
        query = db.select([self.snapshots.c.id,
                           self.snapshots.c.snapshot_timestamp]).where(and_(self.snapshots.columns.id == snapshot_id,
                                                                            self.snapshots.columns.user_id == user_id))
        ResultProxy = self.connection.execute(query)
        snapshot_ResultSet = ResultProxy.fetchall()

        # Get the snapshot data
        query = db.select([self.snapshots_data.c.parser_type]).where(self.snapshots_data.columns.snapshot_id == snapshot_id)
        ResultProxy = self.connection.execute(query)
        snapshot_data_ResultSet = ResultProxy.fetchall()
        return {"snapshot": snapshot_ResultSet[0], "snapshot_data": snapshot_data_ResultSet}

    def get_snapshot_data(self, user_id, snapshot_id, result_name):
        # Get the snapshot - For "security" reasons it might be worth adding
        # a validation here that the snapshot id matches the user_id
        # query = db.select([self.snapshots.c.id, self.snapshots.c.snapshot_timestamp]).where(and_(self.snapshots.columns.id == snapshot_id,self.snapshots.columns.user_id == user_id))
        # ResultProxy = self.connection.execute(query)
        # snapshot_ResultSet = ResultProxy.fetchall()

        # Get the snapshot data
        query = db.select([self.snapshots_data.c.data]).where(and_(self.snapshots_data.columns.snapshot_id == snapshot_id,
                                                                   self.snapshots_data.columns.parser_type == result_name))
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()

        return ResultSet

    def create_user(self, user_id, username, birthday):
        insert = self.users.insert().values(id=user_id,
                                            username=username,
                                            birthday=dt.fromtimestamp(birthday))
        result = self.connection.execute(insert)
        return result.inserted_primary_key

    def add_snapshot(self, user_id, snapshot_timestamp, parser_type, data):
        # Check if snapshoot already exists for user
        query = db.select([self.snapshots]).where(and_(self.snapshots.columns.user_id == user_id,
                                                       self.snapshots.columns.snapshot_timestamp == str(snapshot_timestamp)))
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        snapshot_id = 0
        if not ResultSet:
            # If snapshot doesn't exist - enter it
            insert = self.snapshots.insert().values(snapshot_timestamp=str(snapshot_timestamp),
                                                    user_id=user_id)
            result = self.connection.execute(insert)
            snapshot_id = result.inserted_primary_key[0]
        else:
            snapshot_id = ResultSet[0]['id']

        # Add snapshot data
        insert = self.snapshots_data.insert().values(snapshot_id=snapshot_id,
                                                     parser_type=parser_type,
                                                     data=json.dumps(data))
        result = self.connection.execute(insert)

        return result.inserted_primary_key
