import json
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from repository import models
from .plugins import PluginManger

@csrf_exempt
def server(request):
    # 客户端提交的最新资产数据
    server_dict = json.loads(request.body.decode('utf-8'))

    # 检查server表中是否有当前资产信息【主机名是唯一标识】
    if not server_dict['basic']['status']:
        return HttpResponse('臣妾做不到')

    manager = PluginManger()
    response = manager.exec(server_dict)

    return HttpResponse(json.dumps(response))








