#!/usr/bin/env python
# encoding:utf8

class IDB(object):  # interface
    def __init__(self, config):
        raise NotImplementedError()
    def get(self, id):
        raise NotImplementedError()
    def insert(self, id, data_dict):
        raise NotImplementedError()
    def delete(self, id):
        raise NotImplementedError()


class DjangoORMDB(IDB):
    def __init__(self, cache_table):
        self.cache_table = cache_table
    def get(self, id):
        obj = self.cache_table.objects.get(id=id)
        return obj.data
    def insert(self, id, data_dict):
        self.cache_table.objects.update_or_create(id=id, defaults=data_dict)
    def delete(self, id):
        obj = self.cache_table.objects.get(id=id)
        obj.delete()

