import time
import hashlib
import xmltodict

from django.http import HttpResponse


def check_signature(request):
    phrase = "186548"
    nonce = request.GET["nonce"]
    echostr = request.GET["echostr"]
    timestamp = request.GET["timestamp"]
    signature = request.GET["signature"]

    auth_list = [phrase, timestamp, nonce]
    auth_list.sort()
    auth_str = "".join(auth_list).encode("utf-8")
    hashcode = hashlib.sha1(auth_str).hexdigest()

    if signature == hashcode:
        return HttpResponse(echostr)
    else:
        return HttpResponse("token error")


def gen_response(to_user_open_id, from_user_open_id, content):
    response_dict = dict()
    response_dict["ToUserName"] = to_user_open_id
    response_dict["FromUserName"] = from_user_open_id
    response_dict["CreateTime"] = int(time.time())
    response_dict["Content"] = content

    xml_template = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
    return xml_template.format(**response_dict)


def parse_msg_recv(request):
    request_body = xmltodict.parse(request.body)
    xml_dict = dict(request_body)["xml"]
    user_input = dict(xml_dict)["Content"]
    return user_input


def index(request):
    if request.method == "GET":
        return check_signature(request)

    if request.method == "POST":
        user_input = parse_msg_recv(request)
        response = gen_response(
            to_user_open_id=request.GET["openid"],
            from_user_open_id="gh_74ccc0ad896d",
            content=user_input,
        )
        return HttpResponse(response, content_type="application/xml")
