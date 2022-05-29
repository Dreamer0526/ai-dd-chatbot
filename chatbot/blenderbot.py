import json
from websocket import create_connection
from django.http import HttpResponse

import chatbot.utils.wechat_integration as wi
from chatbot.utils.logger import logger

socket_register = [
    {
        "id": x,
        "open_id": None,
        "socket": create_connection("ws://localhost:8888/websocket"),
    }
    for x in range(50)
]


def initiate_chat():
    for socket_obj in socket_register:
        ws = socket_obj["socket"]

        invoke_message = json.dumps(
            {"recipient": {"id": socket_obj["id"]}, "text": "invoke chat"}
        )
        ws.send(invoke_message)
        result = ws.recv()

        begin_message = json.dumps(
            {"recipient": {"id": socket_obj["id"]}, "text": "begin"}
        )
        ws.send(begin_message)
        result = ws.recv()

        logger.info(f"Socket # {socket_obj['id']} ready to use")


initiate_chat()


def find_socket(user_open_id):
    for socket_obj in socket_register:
        if user_open_id == socket_obj["open_id"]:
            return socket_obj

    for socket_obj in socket_register:
        if socket_obj["open_id"] is None:
            socket_obj["open_id"] = user_open_id
            return socket_obj

    return None


def index(request):
    if request.method == "GET":
        return wi.check_signature(request)

    if request.method == "POST":
        # parse user info and message received
        user_open_id = request.GET["openid"]
        msg_recv = wi.parse_msg_recv(request)
        logger.info(f"Message received from user {user_open_id}: {msg_recv}")

        # find docket
        socket_dict = find_socket(user_open_id)
        logger.info(f"Socket {socket_dict['id']} used for user {user_open_id}")

        # prepare answer
        ws = socket_dict["socket"]
        message = json.dumps({"recipient": {"id": user_open_id}, "text": msg_recv})
        ws.send(message)
        ws_response = ws.recv()
        answer = json.loads(ws_response)["text"]
        logger.info(f"Answer selected for user {user_open_id}: {answer}")

        # return answer to user
        response = wi.gen_response(
            to_user_open_id=user_open_id,
            from_user_open_id="gh_c9fbe359883f",  # PMXbot003
            content=answer,
        )
        return HttpResponse(response, content_type="application/xml")
