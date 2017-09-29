import json
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from repository import models
from .plugins import PluginManger
from django.db.models import Q
from datetime import date
import hashlib
import time
from django.conf import settings

@csrf_exempt
def server(request):
    if request.method == "POST":
        # 客户端提交的最新资产数据
        server_dict = json.loads(request.body.decode('utf-8'))

        # 检查server表中是否有当前资产信息【主机名是唯一标识】
        if not server_dict['basic']['status']:
            errorlog = models.ErrorLog.objects.create(server_obj_name=server_dict['basic']['data'],
                                                      title='%s服务器获取失败' % (server_dict['basic']['data']),
                                                      content=server_dict['basic']['msg'])
            return HttpResponse('臣妾做不到')
        manager = PluginManger()
        response = manager.exec(server_dict)
        return HttpResponse(json.dumps(response))


def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()
visited_keys = {
    # "841770f74ef3b7867d90be37c5b4adfc":时间,  10
}

def api_auth(func):
    '''
    认证装饰器签名服务
    '''
    def inner(request,*args,**kwargs):
        '''
        认证函数
        '''
        server_float_ctime = time.time()
        auth_header_val = request.META.get('HTTP_AUTH_API')#获取到用户发来的签名进行认证
        client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)#通过|拆解获取时间和签名md5
        client_float_ctime = float(client_ctime)
        if (client_float_ctime + 20) < server_float_ctime:#根据当前的系统时间判断用户的签名是否小于规定的20秒如果小于通过
            return HttpResponse('1.签名超时')
        server_md5_str = md5("%s|%s" % (settings.LASSENCE_KEY, client_ctime,))#判断用户的md5值是否正确通过获取到的时间和本地密钥如果正确通过
        if server_md5_str != client_md5_str:
            return HttpResponse('2.签名错误')
        if visited_keys.get(client_md5_str):#判断该密钥是否在列表内，建议这一层放在MD5运算之前面，不需要运算，加密，仅仅取一下缓存器就可以
            return HttpResponse('3.签名已使用')
        visited_keys[client_md5_str] = client_float_ctime#如果上面的都通过加入缓存器
        return func(request,*args,**kwargs)
    return inner
@api_auth
def test(request):
    '''
    获取未采集的API
    '''
    if request.method == "GET":
        current_date = date.today()
        # 获取今日未采集的主机列表
        host_list = models.Server.objects.filter(
            Q(Q(latest_date=None)|Q(latest_date__date__lt=current_date)) & Q(server_status_id=2)
        ).values('hostname')#筛选时间在今天以前的，并且没有latest时间的列表
        host_list = list(host_list)
        return HttpResponse(json.dumps(host_list))
    return HttpResponse('呵呵')







