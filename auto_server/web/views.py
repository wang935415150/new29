from django.shortcuts import render,HttpResponse
from repository import models
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'index.html')
def index_ajax(request):
    table_config=[
        {
            'q':None,
            'display': True,
         'title':'选择',
         'text':{
           'tpl':'<input type="checkbox" value="{nid}"/>','kwargs':{'nid':'@id'}},
         },
        {
          'q':'id',
            'display': False,
           'title':'id',
            'text':{
                'tpl':'{a1}','kwargs':{'a1':'@id'}}
        },
        {
            'q':'hostname',
            'display': True,
         'title':'主机名',
         'text':{
             'tpl':'{a1}','kwargs':{'a1':'@hostname'}},
         },
        {
            'q': 'sn',
            'display': True,
         'title': 'sn号',
         'text':{'tpl':'{a1}','kwargs':{'a1':'@sn'}},
        },
        {
            'q': 'server_status_id',
            'display': True,
            'title': '当前状态',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
        },
        {
            'q': 'os_platform',
            'display': True,
         'title': '系统',
         'text':{'tpl':'{a1}','kwargs':{'a1':'@os_platform'}},
         },
        {
            'q':None,
            'display': True,
         'title':'编辑',
         'text':{'tpl':'<a herf="/web/{nid1}">编辑</a>|<a herf="/web/{nid2}">删除</a>','kwargs':{'nid1':'@id','nid2':'@id'}},
        },
    ]
    values=[]
    for item in table_config:
        if item['q']:

            values.append(item['q'])
    server_list = models.Server.objects.values(*values)
    response={
        'data_list':list(server_list),
        'table_config':table_config,
        'global_choices_dict':{
            'status_choices':models.Server.server_status_choices
        }
    }
    return JsonResponse(response)


def disk(request):
    return render(request,'disk.html')
def disk_ajax(request):
    table_config=[
        {
            'q':None,
         'title':'选择',
         'text':{'tpl':'<input type="checkbox" value="{nid}"/>','kwargs':{'nid':'@id'}},
        },
        {
            'q':'id',
         'title':'id',
         'text':{'tpl':"{a1}",'kwargs':{'a1':'@id'}},
         },
        {
            'q':'slot',
            'title':'槽位',
            'text':{'tpl':'槽位{a1}','kwargs':{'a1':'@slot'}},
        },
        {
          'q':'pd_type',
            'title':'硬盘类型',
            'text':{'tpl':'{a1}','kwargs':{'a1':'@pd_type'}},
        },
        {
            'q':None,
            'title':'编辑',
            'text':{'tpl':'<a herf="/web/disk/{nid1}">编辑</a>|<a herf="/web/disk/{nid2}">删除</a>','kwargs':{'nid1':'@id','nid2':'@id'}},
        },
    ]
    values=[]
    for item in table_config:
        if item['q']:
            values.append(item['q'])
    server_list=models.Disk.objects.values(*values)
    data_list=list(server_list)
    response={
        "data_list":data_list,
        'table_config':table_config
    }
    return JsonResponse(response)

def nic(request):
    return render(request,'nic.html')

def nic_ajax(request):
    table_config=[
        {'q':None,
         'display':True,
         'title':'选择',
         'text':{'tpl':'<input type="checkbox" id="{a1}">','kwargs':{'a1':'@id'}},},
        {
            'q':'id',
            'display': False,
            'title':'id',
            'text':{'tpl':'{a1}','kwargs':{'a1':'@id'}},},
        {
            'q':'name',
            'display': True,
            'title':'网卡名称',
            'text':{"tpl":'{a1}','kwargs':{'a1':'@name'}},},
        {
            'q':'ipaddrs',
            'display': True,
            'title':'IP地址',
            'text':{'tpl':'{a1}','kwargs':{'a1':'@ipaddrs'}},},
        {
          'q':None,
            'display': True,
            'title':'编辑',
            'text':{'tpl':'<a href="web/nic/{a1}">编辑</a>|<a href="web/nic/{a2}">删除</a>','kwargs':{'a1':'@id','a2':'@id'}}
        },
    ]
    value=[]
    for i in table_config:
        if i['q']:
            value.append(i['q'])
    data_list = models.NIC.objects.values(*value)
    response={
        'table_config':table_config,
        'data_list':list(data_list),
    }

    return JsonResponse(response)


def test(request):
    data = models.Server.objects.values('hostname','server_status_id')
    def yeildd(server_list):
        for row in server_list:
            for item in models.Server.server_status_choices:
                if item[0]==row['server_status_id']:
                    row['server_status_choices_name']=item[1]
                    break
            yield row

    return render(request,'test.html',{'server_list':yeildd(data)})
