from repository import models
class Nic(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.nic_dict = info
        self.hostname=server_obj.hostname
    def process(self):
        print('nic process')
        if not self.nic_dict['status']:
            errorlog=models.ErrorLog.objects.create(server_obj=self.server_obj,title='%s网卡获取失败'%(self.hostname),content=self.nic_dict['msg'])
        else:
            new_nic_info_dict=self.nic_dict['data']
            print(new_nic_info_dict)
            old_nic_info_dict=self.server_obj.nic.all()
            print(old_nic_info_dict)
            new_nic_name_set=set(new_nic_info_dict.keys())
            old_nic_name_set={obj.name for obj in new_nic_info_dict}
            add_name_list=new_nic_name_set.difference(old_nic_name_set)
            del_name_list=old_nic_name_set.difference(new_nic_name_set)
            update_name_list=old_nic_name_set.intersection(new_nic_name_set)
            add_record_list=[]
            for eth in add_name_list:
                value=new_nic_info_dict[eth]
                tmp="[%s]添加网卡[%s]"(self.server_obj.hostname,eth,)
                add_record_list.append(tmp)
                value['server_obj']=self.server_obj
                models.NIC.objects.create(**value)
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(add_record_list))
            delete_record_list = '[%s]删除了网卡[%s]' % (self.server_obj.hostname, ';'.join(del_name_list))
            models.NIC.objects.filter(server_obj=self.server_obj,name__in=del_name_list).delete()
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(delete_record_list))
            update_record_list = []
            for eth in update_name_list:
                value=new_nic_info_dict[eth]
                obj = models.NIC.objects.filter(server_obj=self.server_obj,name=eth).first()
                for k,new_val in value.items():
                    old_val = getattr(obj,k)
                    if old_val!=new_val:
                        tmp = '%s更新了硬盘%s的%s从%s更新到%s' % (self.hostname, eth, k, old_val, new_val)
                        update_record_list.append(tmp)
                        setattr(obj,k,new_val)
                obj.save()
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(update_record_list))

