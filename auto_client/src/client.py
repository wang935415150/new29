import requests
from src.plugins import PluginManager
from lib.config import settings
from concurrent.futures import ThreadPoolExecutor
from lesscen import lesscen
class BaseClient(object):
    def __init__(self):
        self.api = settings.API
    def post_server_info(self,server_dict):
        # requests.post(self.api,data=server_dict) # 1. k=v&k=v,   2.  content-type:   application/x-www-form-urlencoded
        response = requests.post(self.api,json=server_dict) # 1. 字典序列化；2. 带请求头 content-type:   application/json
    def exec(self):
        raise NotImplementedError('必须实现exec方法')

class AgentClient(BaseClient):

    def exec(self):
        obj = PluginManager()
        server_dict = obj.exec_plugin()
        print('采集到的服务器信息：',server_dict)
        self.post_server_info(server_dict)



class SaltSshClient(BaseClient):
    '''
    salt和ssh认证新增加了签名
    '''
    def task(self,host):
        obj = PluginManager(host)
        server_dict = obj.exec_plugin()
        self.post_server_info(server_dict)

    def get_host_list(self):
        '''
        获取采集列表
        :return:[{'hostname': 'c1.com'}]
        '''
        response = lesscen()
        return response

    def exec(self):
        pool = ThreadPoolExecutor(10)

        host_list = self.get_host_list()
        for host in host_list:
            pool.submit(self.task,host['hostname'])
