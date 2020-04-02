import json
import sqlalchemy as db
from datetime import datetime as dt

class PostgresDriver:

    def __init__(self, url):
        url = url.replace("postgresql://", "postgresql://postgres:password@") + "/db"
        engine = db.create_engine(url)
        metadata = db.MetaData()
        self.users = db.Table('users', metadata,
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('username', db.String, nullable=False),
                        db.Column('birthday', db.DateTime, nullable=False),
                        )
        self.snapshots = db.Table('snapshots', metadata,
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('snapshot_timestamp', db.String, nullable=False),
                        db.Column('parser_type', db.String, nullable=False),
                        db.Column('data', db.String, nullable=False),
                        )

        metadata.create_all(engine)
        self.connection = engine.connect()

    def get_user(self, user_id):
        query = db.select([self.users]).where(self.users.columns.id == user_id)
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def create_user(self,user_id,username,birthday):
        insert = self.users.insert().values(id=user_id, username=username,birthday=dt.fromtimestamp(birthday))
        result = self.connection.execute(insert)
        return result.inserted_primary_key

    def add_snapshot(self,snapshot_timestamp,parser_type,data):
        insert = self.snapshots.insert().values(snapshot_timestamp=str(snapshot_timestamp),
                                                parser_type=parser_type,
                                                data=data)
        result = self.connection.execute(insert)
        return result.inserted_primary_key


