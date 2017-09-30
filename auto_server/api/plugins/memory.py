from repository import models
class Memory(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.memory_dict = info
        self.hostname=server_obj.hostname
    def process(self):
        if not self.memory_dict['status'] :
            errorlog=models.ErrorLog.objects.create(server_obj=self.server_obj,title='%s内存获取失败'%(self.hostname),content=self.memory_dict['msg'])
        else:
            new_memory_info_dict = self.memory_dict['data']
            new_memory_info_list = self.server_obj.memory.all()
            new_memory_slot_set = set(new_memory_info_dict.keys())
            old_memory_slot_set = {obj.slot for obj in new_memory_info_list}
            add_slot_list = new_memory_slot_set.difference(old_memory_slot_set)
            del_slot_list = old_memory_slot_set.difference(new_memory_slot_set)
            update_slot_list = old_memory_slot_set.intersection(new_memory_slot_set)
            add_record_list = []
            for slot in add_slot_list:
                value = new_memory_info_dict[slot]
                tmp = "[%s]添加内存[%s]"(self.server_obj.hostname,slot,)
                add_record_list.append(tmp)
                value['server_obj'] = self.server_obj
                models.Disk.objects.create(**value)
            models.ServerRecord.objects.create(server_obj=self.server_obj,content=';'.join(add_record_list))
            delete_record_list = '[%s]删除了内存[%s]'%(self.server_obj.hostname,';'.join(del_slot_list))
            models.Disk.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(delete_record_list))
            update_record_list=[]
            for slot in update_slot_list:
                value = new_memory_info_dict[
                    slot]
                obj = models.Disk.objects.filter(server_obj=self.server_obj, slot=slot).first()
                for k, new_val in value.items():
                    old_val = getattr(obj, k)
                    if old_val != new_val:
                        tmp='%s更新了内存%s的%s从%s更新到%s'%(self.hostname,slot,k,old_val,new_val)
                        update_record_list.append(tmp)
                        setattr(obj, k, new_val)
                obj.save()
                models.ServerRecord.objects.create(server_obj=self.server_obj,content=';'.join(update_record_list))