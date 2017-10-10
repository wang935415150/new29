import requests
import time
import hashlib
import json
from lib.config import settings
def md5(arg):
    '''
    一个md5制作函数
    :param arg: 获取到的new_key
    :return: 加密后的数据
    '''
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()
def lesscen():
    '''
    进行签名加密并且进行上传，如果成功返回ssh需要查看的列表
    :return:[{'hostname': 'c1.com'}]
    '''
    key = "asdfuasodijfoausfnasdf"
    ctime = str(time.time())
    new_key = "%s|%s" %(key,ctime,)
    md5_str = md5(new_key)
    auth_header_val = "%s|%s" %(md5_str,ctime,)
    response = requests.get(settings.GET_API,headers={'auth-api':auth_header_val})
    response=json.loads(response.text)
    return response