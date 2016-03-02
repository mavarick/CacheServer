#!/usr/bin/env python
# encoding:utf8

import redis

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

class RedisDB(IDB):
    def __init__(self, config):
        self.config = config
        self.host = config['host']
        self.port = config['port']
        self.db = config.get("db", 0)
        self.connect()

    def connect(self):
        self.conn = redis.StrictRedis(self.host, self.port, self.db)

    def get(self, id):
        obj = self.conn.hgetall(id)
        if obj:
            return obj['data']
        else:
            raise Exception("Redis no data")

    def insert(self, id, data_dict):
        self.conn.hmset(id, data_dict)

    def delete(self, id):
        self.conn.delete(id)

def test_RedisDB():
    config = dict(host="192.168.0.136", port=6379, db=0)
    r = RedisDB(config)
    id = "xaggasdfg"
    data = dict(id="abcd", data=u"data 世界", info="asdfgas{}")
    r.insert(id, data)
    print r.get(id)

if __name__ == "__main__":
    test_RedisDB()