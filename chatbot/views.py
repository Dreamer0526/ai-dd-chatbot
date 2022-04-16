import time
import hashlib

from django.http import HttpResponse


def check_token(request):
    phrase = "186548"
    nonce = request.GET["nonce"]
    echostr = request.GET["echostr"]
    timestamp = request.GET["timestamp"]

    auth_list = [phrase, timestamp, nonce]
    auth_list.sort()
    auth_str = "".join(auth_list).encode("utf-8")
    hash_result = hashlib.sha1(auth_str).hexdigest()

    if hash_result == echostr:
        return HttpResponse(echostr)
    else:
        return HttpResponse("error")


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


def index(request):
    if request.method == "GET":
        return check_token(request)

    if request.method == "POST":
        response = gen_response(request.POST["openid"], "gh_74ccc0ad896d", "content")
        return HttpResponse(response, content_type="application/xml")
