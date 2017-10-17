#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "wyd"
# Date: 2017/10/17

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
