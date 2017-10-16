
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models
from utils.page import Pagination
from django.db.models import Q
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class Server_json(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Server_json, self).dispatch(request, *args, **kwargs)

    def get(self,request):
        search_config = [
            {
                'name': 'hostname', 'title': '主机名', 'type': 'input'
            },
            {
                'name': 'cabint_num', 'title': '机柜号',
                'type': 'input'
            },
            {
                'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'
            }
        ]
        table_config = [
            {
                'q': None,
                'title': '选择',
                'display': True,
                'text': {'tpl': '<input type="checkbox" class="checkbox"  value="{nid}" />', 'kwargs': {'nid': '@id'}},
                'attr': {'class': 'c1', 'nid': '@id', },
            },
            {
                'q': 'id',
                'title': 'id',
                'display': False,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}, },
                'attr': {},
            },
            {
                'q': 'hostname',
                'title': '主机名',
                'display': True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@hostname'}},
                'attr': {'class': 'hostname', 'nid': '@id','edit':'true', 'type': 'input', 'origin': '@hostname','name':'hostname'},

            },
            {
                'q': 'sn',
                'title': '序号',
                'display': True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}},
                'attr': {'class': 'sn', 'nid': '@id', 'edit':'true','type': 'input', 'origin': '@sn','name':'sn'},
            },
            {
                'q': 'os_platform',
                'title': '系统',
                'display': True,
                'text': {'tpl': '{a1}', 'kwargs': {"a1": '@os_platform'}},
                'attr': {'class': 'os_platform', 'edit':'true','nid': '@id', 'type': 'input', 'origin': '@os_platform','name':'os_platform'},
            },
            {
                'q': 'server_status_id',
                'display': True,
                'title': '服务器状态',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
                'attr': {'class': 'server_status_id', 'nid': '@id', 'edit-type': 'select','edit':'true','choice-key':'status_choices', 'origin': "@server_status_id",'name':'server_status_id'},
            },
            {
                'q': None,
                'display': True,
                'title': "编辑",
                'text': {'tpl': '<a href="#{a1}">编辑</a>|<a href="#{a2}">删除</a>', 'kwargs': {'a1': '@id', 'a2': '@id'}},
                'attr': {'class': 'c1', 'nid': '@id'},
            },
        ]
        values = []
        for item in table_config:
            if item.get('q'):
                values.append(item['q'])

        condition = json.loads(request.GET.get('condition'))
        """
          {
              server_status_id: [1,2],
              hostname: ['c1.com','c2.com']
          }
          """
        q = Q()
        for k, v in condition.items():
            temp = Q()
            temp.connector = 'OR'
            print(k, 'aaaaa')
            if k == 'hostname':
                k = k + '__contains'
                print(k)
            for item in v:
                temp.children.append((k, item))
            q.add(temp, 'AND')
        current_page = int(request.GET.get('pageNum', 1))

        total_item_count = models.Server.objects.filter(q).count()

        page_obj = Pagination(current_page, total_item_count, per_page_count=2)

        server_data = models.Server.objects.filter(q).values(*values)[page_obj.start:page_obj.end]

        response = {
            'search_config': search_config,
            'data_list': list(server_data),
            'table_config': table_config,
            'global_choices_dict': {
                'status_choices': models.Server.server_status_choices
            },
            'page_html': page_obj.page_html_js()
        }
        return JsonResponse(response)

    def delete(self, request):
        id_list=json.loads(request.body.decode('utf-8'))
        response={'status':True,'msg':None}
        try:
            c=models.Server.objects.filter(id__in=id_list)
            print(c)
        except Exception as e:
            response['status']=False
            response['msg']=str(e)
        return HttpResponse(json.dumps(response))

    def put(self,request):
        c=json.loads(request.body.decode('utf-8'))
        # {'nid': '5', 'hostname': 'c1.com1'}, {'nid': '6', 'hostname': 'c2.com1'}]
        response = {'status': True, 'msg': None}
        try:
            for i in c:
                    models.Server.objects.filter(id=i['id']).update(**i)
        except Exception as e:
            response['status']=False
            response['msg']=e
        return HttpResponse(json.dumps(response))
def server(request):
    return render(request,'server.html')

