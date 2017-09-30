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
            #{'status': True, 'data': {'eth0': {'up': True, 'hwaddr': '00:1c:42:a5:57:7a', 'ipaddrs': '10.211.55.4', 'netmask': '255.255.255.0'}}, 'msg': None}
            print(new_nic_info_dict)
            old_nic_info_dict=self.server_obj.nic.all()
            print(old_nic_info_dict)
            new_nic_slot_set=set(new_nic_info_dict.keys())
            old_nic_slot_set={obj.name for obj in new_nic_info_dict}
            add_slot_list=new_nic_slot_set.difference(old_nic_slot_set)
            del_slot_list=old_nic_slot_set.difference(new_nic_slot_set)
            update_slot_list=old_nic_slot_set.intersection(new_nic_slot_set)
            add_record_list=[]
            for eth in add_slot_list:
                value=new_nic_info_dict[eth]
                tmp='添加网卡'
                add_record_list.append(tmp)
                value['server_obj']=self.server_obj
                models.NIC.objects.create(**value)

            models.NIC.objects.filter(server_obj=self.server_obj,name__in=del_slot_list).delete()

            for eth in update_slot_list:
                value=new_nic_info_dict[eth]
                obj = models.NIC.objects.filter(server_obj=self.server_obj,name=eth).first()
                for k,new_val in value.items():
                    old_val = getattr(obj,k)
                    if old_val!=new_val:
                        setattr(obj,k,new_val)
                obj.save()

