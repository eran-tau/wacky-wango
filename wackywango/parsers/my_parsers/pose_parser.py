from google.protobuf.json_format import MessageToJson
import json


def parse_pose(context, snap):
    return json.loads(MessageToJson(snap.pose))


parse_pose.parser_type = 'pose'
