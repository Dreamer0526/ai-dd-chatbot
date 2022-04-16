import time
import hashlib


from django.http import HttpResponse


def index(request):
    if request.method == "GET":
        phrase = "186548"
        nonce = request.GET["nonce"]
        echostr = request.GET["echostr"]
        timestamp = request.GET["timestamp"]

        auth_list = [phrase, timestamp, nonce]
        auth_list.sort()
        hash_result = hashlib.sha1("".join(auth_list)).encode("utf-8").hexdigest()

        if hash_result == echostr:
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")

    if request.method == "POST":
        response_dict = dict()
        response_dict["ToUserName"] = request.POST["openid"]
        response_dict["FromUserName"] = "gh_74ccc0ad896d"
        response_dict["CreateTime"] = int(time.time())
        response_dict["Content"] = "content"

        XmlForm = """
                <xml>
                    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                    <CreateTime>{CreateTime}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{Content}]]></Content>
                </xml>
                """
        response = XmlForm.format(**response_dict)

        return HttpResponse(response, content_type="application/xml")
