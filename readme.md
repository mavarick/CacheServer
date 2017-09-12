CacheServer
----------

  use this Cache middleware to accelerate your web api for some relative stable data


USAGE
========

  the server will replace original request netloc 

  0. Set Target Server in config.py: `data_api = "127.0.0.1:9001"`
     
    the server will replace original request netloc with data_api automatically,
    1) ordered url parameters and get redis key: get_hash_id(url)
    2) get value:data in redis, if exists, then return value; if not, then request 
       data_api to get fresh value, save in redis by key and return

  1. modify the `config.py`
  
    1. use mysql as cache middleware: set mysql info in `cacheserver::setting.py`.
    2. use redis as cache middleware: change redis server host:port in `config.py`

  2. start server by `run.sh`


DEPENDENT ON
=========

  1. MYSQL == 5.6
  2. DJANGO==1.8.3
  3. requests=2.8.1


