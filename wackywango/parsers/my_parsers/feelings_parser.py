from google.protobuf.json_format import MessageToJson
import json


def parse_feelings(context, snap):
    return json.loads(MessageToJson(snap.feelings))


parse_feelings.parser_type = 'feelings'
