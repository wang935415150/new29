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
         'title':'选择',
         'text':{
           'tpl':'<input type="checkbox" value="{nid}"/>','kwargs':{'nid':'@id'}},
         },
        {
          'q':'id',
           'title':'id',
            'text':{
                'tpl':'{a1}','kwargs':{'a1':'@id'}}
        },
        {
            'q':'hostname',
         'title':'主机名',
         'text':{
             'tpl':'{a1}','kwargs':{'a1':'@hostname'}},
         },
        {
            'q': 'sn',
         'title': 'sn号',
         'text':{'tpl':'{a1}','kwargs':{'a1':'@sn'}},
        },
        {
            'q': 'os_platform',
         'title': '系统',
         'text':{'tpl':'{a1}','kwargs':{'a1':'@os_platform'}},
         },
        {
            'q':None,
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
        'table_config':table_config
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