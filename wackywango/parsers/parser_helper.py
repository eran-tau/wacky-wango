from ..proto import cortex_pb2
from google.protobuf.json_format import MessageToJson

import uuid
import json
import importlib
import sys
import pathlib
from ..config import Config

config = Config()


class Parser:
    def __init__(self):
        self.parsers = []

    def load_parsers(self, root):
        root = pathlib.Path(root).absolute()
        sys.path.insert(0, str(root.parent))
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            importlib.import_module(f'{root.name}.{path.stem}',
                                    package=root.name)
            imported_parser = sys.modules[f'{root.name}.{path.stem}'].__dict__
            for potential_parser in imported_parser:
                if potential_parser.startswith('parse'):
                    self.parsers.append(imported_parser[potential_parser])
                if potential_parser.endswith('Parser'):
                    self.parsers.append(imported_parser[potential_parser].parse)

    def parse(self, parser_type, data):
        upload_snapshot = cortex_pb2.UploadSnapshot()
        upload_snapshot.ParseFromString(open(data, "rb").read())
        collect_results = []
        for parser in self.parsers:
            if parser.parser_type == parser_type:
                context = Context(parser.parser_type, upload_snapshot.user)
                result = parser(context, upload_snapshot.snapshot)
                collect_results.append(
                    context.prepare_result(result,
                                           upload_snapshot.snapshot.datetime))
        return collect_results


class Context:
    def __init__(self, parser_type, user_data):
        self.parser_type = parser_type
        self.user_data = user_data
        self.result = {}
        return

    def save(self, data):
        unique_filename = self.get_save_path()
        data.save(unique_filename)
        return unique_filename

    def get_save_path(self):
        return config.data['path'] + \
               "/pics/" + self.parser_type +\
               "/" + str(uuid.uuid4()) + ".jpg"

    def prepare_result(self, data, snapshot_timestamp):
        if not self.result:
            user_data = MessageToJson(self.user_data)
            user_data = json.loads(user_data)
            return {"snapshot_timestamp": snapshot_timestamp,
                    "parser_type": self.parser_type,
                    "snapshot_data": data,
                    "user_data": user_data}
        else:
            return self.result

    def set_result(self, result):
        self.result = result
