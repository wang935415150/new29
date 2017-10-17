#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "wyd"
# Date: 2017/10/17


import json
from django.db.models import Q
class Baseclass(object):
    def value(self):
        values = []
        for item in self.table_config:
            if item.get('q'):
                values.append(item['q'])
        return values

    def contions(self):
        condition = json.loads(self.request.GET.get('condition'))
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
            # print(k, 'aaaaa')
            if k == 'hostname':
                k = k + '__contains'
                # print(k)
            for item in v:
                temp.children.append((k, item))
            q.add(temp, 'AND')
        return q