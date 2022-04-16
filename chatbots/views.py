import time

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    try:
        echostr = request.GET["echostr"]
        return HttpResponse(echostr)
    except MultiValueDictKeyError:
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
