import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models

def server(request):
    return render(request,'server.html')

def server_json(request):
    table_config = [
        {
            'q': None,
            "display": True,
            'title': '选择',
            'text': {'tpl':'<input type="checkbox" value="{nid}" />','kwargs':{'nid': '@id' }},

        },
        {
            'q': 'id',
            "display": False,
            'title': 'ID',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
        },
        {
            'q': 'hostname',
            "display": True,
            'title': '主机名',
            'text': {'tpl': '{a1}-{a2}','kwargs':{'a1': '@hostname','a2':'666'}},
        },
        {
            'q': 'sn',
            'title': '序列号',
            "display": True,
            'text': {'tpl': '{a1}','kwargs':{'a1': '@sn'}},
        },
        {
            'q': 'os_platform',
            'title': '系统',
            "display": True,
            'text': {'tpl': '{a1}','kwargs':{'a1': '@os_platform'}},
        },
        {
            'q': 'os_version',
            "display": True,
            'title': '系统版本',
            'text': {'tpl': '{a1}','kwargs':{'a1': '@os_version'}},
        },
        {
            'q': 'business_unit__name',
            "display": True,
            'title': '业务线',
            'text': {'tpl': '{a1}','kwargs':{'a1': '@business_unit__name'}},
        },
        {
            'q': 'server_status_id',
            "display": True,
            'title': '服务器状态',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
        },
        {
            'q': None,
            "display": True,
            'title': '操作',
            'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ', 'kwargs': {'nid': '@id','uid': '@id'}},
        },
    ]

    values = []
    for item in table_config:
        if item['q']:
            values.append(item['q'])
    server_list = models.Server.objects.values(*values)
    """
    [
        {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
    ]

    """
    response = {
        'data_list': list(server_list),
        'table_config': table_config,
        'global_choices_dict':{
            'status_choices': models.Server.server_status_choices
        }
    }

    return JsonResponse(response)



def disk(request):
    return render(request,'disk.html')

def disk_json(request):
    table_config = [
        {
            'q': None,
            'title': '选择',
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
        {
            'q': 'id',
            'title': 'ID',
            'text': {'tpl': '{nid}', 'kwargs': {'nid': '@id'}},
        },
        {
            'q': 'slot',
            'title': '槽位',
            'text': {'tpl': '{nid}', 'kwargs': {'nid': '@slot'}},
        },
    ]

    values = []
    for item in table_config:
        if item['q']:
            values.append(item['q'])
    server_list = models.Disk.objects.values(*values)
    response = {
        'data_list': list(server_list),
        'table_config': table_config
    }

    return JsonResponse(response)



def xxxxx(server_list):
    # [{},{}]
    for row in server_list:
        for item in models.Server.server_status_choices:
            if item[0] ==  row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
        yield row



def test(request):
    """
    赠送，模板语言显示choice
    :param request:
    :return:
    """
    # server_list = models.Server.objects.all()
    # for row in server_list:
    #     print(row.id,row.hostname,row.business_unit.name,"===",row.server_status_id,row.get_server_status_id_display() )

    # server_list = models.Server.objects.all().values('hostname','server_status_id')
    # for row in server_list:
    #     for item in models.Server.server_status_choices:
    #         if item[0] ==  row['server_status_id']:
    #             row['server_status_id_name'] = item[1]
    #             break

    data_list = models.Server.objects.all().values('hostname', 'server_status_id')

    return render(request,'test.html',{'server_list':xxxxx(data_list)})