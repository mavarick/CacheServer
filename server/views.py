#encoding:utf8
import copy
import pdb
import json
import urllib
import urllib2
import requests
import urlparse
import traceback
from collections import OrderedDict

from django.shortcuts import render, HttpResponse

# Create your views here.
from models import CacheTable
from config import data_api
from tools import get_request_field, unicode_to_utf8, get_hash_id
from Logger import logger

return_data = dict(code=0, msg="", data=None)
DEFAULT_SCHEME = 'http'

def get(request):
    data = copy.copy(return_data)

    ##############################################################################
    # url parser
    url= request.get_full_path()
    logger.info("[REQUEST_URL]: {0}".format(url))
    url_tuple = urlparse.urlparse(url)
    # scheme='http', netloc='192.168.0.136:14001', path='/name_parser/', params='',
    # query='name=%E6%BD%98%E5%B0%91%E5%AE%81&birthday=1990-12-01&sex=1', fragment='
    (_scheme, _netloc, _path, _params, _query, _fragment) = (
        url_tuple.scheme, url_tuple.netloc, url_tuple.path, url_tuple.params,
        url_tuple.query, url_tuple.fragment)

    # 获得相关的参数，并生成id
    get_params_list = dict_to_order_list(request.GET)
    post_params_list = dict_to_order_list(request.POST)
    id_dict = dict(get=get_params_list, post=post_params_list, path=_path)
    id_json = json.dumps(id_dict)
    id = get_hash_id(id_json)

    ###############################################################################
    # 2, first check the mysql and return data if existed
    try:
        logger.info("[PARSE_ID]: {0}".format(id))
        obj = CacheTable.objects.get(id=id)
        obj_data = obj.data
        data['data'] = json.loads(obj_data)

        data = json.dumps(data)
        logger.info("get old data and return")
        return HttpResponse(data,  content_type="application/json")
    except :
        msg = traceback.format_exc()
        logger.error(msg)

    ################################################################################
    if not _scheme: _scheme = DEFAULT_SCHEME
    new_url = urlparse.urlunparse([_scheme, data_api, _path, _params, _query, _fragment])
    logger.info("[TRANSFER URL]: {0}".format(new_url))

    # 4, 根据或的url通过数据接口获得数据
    try:
        # resp = requests.post(new_url, data=request.POST), # TODO
        # '<html><title>405: Method Not Allowed</title><body>405: Method Not Allowed</body></html>'
        resp = urllib2.urlopen(new_url, data=urllib.urlencode(request.POST), timeout=1)
        result = extract_data(resp.read())
        data['data'] = result

        # save the data
        try:
            result = json.dumps(result)
            logger.info("insert new item [id: {0}]".format(id))
            created, obj = CacheTable.objects.update_or_create(id=id,
                    defaults=dict(id=id, path=_path, info=id_json, data=result))
        except:
            msg = traceback.format_exc()
            logger.error(msg)
    except Exception, ex:
        msg = traceback.format_exc()
        print msg
        data['code'] = -1
        data['msg'] = ex.message

    data = json.dumps(data)
    logger.info("Done")
    return HttpResponse(data,  content_type="application/json")


'''注意
1，django支持对params中的非英文字符的自动转义；
2，django对于params中重名的参数不支持，同名参数，选择最后一个;
'''
# dict to ordered sequence
def dict_to_order_list(d):
    return sorted(d.iteritems(), key=lambda x:x[0])

def list_to_params(params_list):
    # params_list: [(key, value), (key, value)]
    # use urllib.urlencode(params_dict)
    params = []
    for k, v in params_list:
        print k, v
        if isinstance(v, unicode):
            v = unicode_to_utf8(v)
        params.append("{0}={1}".format(urllib.quote(k), urllib.quote(v)))
    return '&'.join(params)

def extract_data(resp_content):
    content = json.loads(resp_content)
    code, msg, data = content['code'], content['msg'], content['data']
    if code != 0:
        raise Exception("Error happened! code: [{0}], msg: [{1}]".format(code, msg))
    return data



