#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "wyd"
# Date: 2017/10/17

from web.table_config import server_config
from web.baseclass.severbase import Baseclass
from repository import models
from utils.page import Pagination
from django.http import JsonResponse
import json
from django.shortcuts import HttpResponse
class ServerService(Baseclass):
    def __init__(self,request):
        self.search_config=server_config.search_config
        self.table_config=server_config.table_config
        self.request=request
    def fetch(self):
        current_page = int(self.request.GET.get('pageNum', 1))

        total_item_count = models.Server.objects.filter(self.contions()).count()

        page_obj = Pagination(current_page, total_item_count, per_page_count=2)

        server_data = models.Server.objects.filter(self.contions()).values(*self.value())[page_obj.start:page_obj.end]
        response = {
            'search_config': self.search_config,
            'data_list': list(server_data),
            'table_config': self.table_config,
            'global_choices_dict': {
                'status_choices': models.Server.server_status_choices
            },
            'page_html': page_obj.page_html_js()
        }
        return JsonResponse(response)

    def delete(self):
        id_list = json.loads(self.request.body.decode('utf-8'))
        response = {'status': True, 'msg': None}
        try:
            c = models.Server.objects.filter(id__in=id_list)
        except Exception as e:
            response['status'] = False
            response['msg'] = str(e)
        return HttpResponse(json.dumps(response))

    def save(self):
        c = json.loads(self.request.body.decode('utf-8'))
        # {'nid': '5', 'hostname': 'c1.com1'}, {'nid': '6', 'hostname': 'c2.com1'}]
        response = {'status': True, 'msg': None}
        try:
            for i in c:
                models.Server.objects.filter(id=i['id']).update(**i)
        except Exception as e:
            response['status'] = False
            response['msg'] = e
        return HttpResponse(json.dumps(response))
