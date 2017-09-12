#!/usr/bin/env python
# encoding:utf8

####################################
## specify the table name of caching
## TODO
tablename = "cache_name_develoop"

####################################
## specify the web api for data
## TODO
## support: GET/POST, no schema just netloc
#data_api = "192.168.0.136:11004"
data_api = "127.0.0.1:9001"

####################################
redis_config = dict(host="127.0.0.1", port=6379, db=0)

####################################
log_path = "./log/run.log"

