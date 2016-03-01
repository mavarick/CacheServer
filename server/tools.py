#!/usr/bin/env python
# encoding:utf8

import datetime
import hashlib

def get_hash_id(s):
    return hashlib.md5(s).hexdigest()

def dt_format(dt, format="%Y-%m-%d %H:%M:%S"):
    if not dt: return dt
    return dt.strftime(format)


def test_dt_format():
    now = datetime.datetime.now()
    print dt_format(now)


# 获得请求的request相关信息
def get_request_info(req):
    meta = req.META
    client_ip = meta.get("REMOTE_ADDR", "U")
    data = dict(client_ip=client_ip)
    return data


def _get_field(request, field_name, method='POST', must=False, default=None):
    ''' get field value from request dict,

    :param request: request.
    :param field_name: field name.
    :param method: POST, GET, REQUEST
    :param must: if true, must be not None.
    :param default: if missing, then should be this value
    :return: field value
    '''
    request_dict = getattr(request, method)
    if must:
        field_value = request_dict[field_name]
    else:
        field_value = request_dict.get(field_name, default)
    return field_value

def get_post_field(request, field_name, must=False, default=None):
    return _get_field(request, field_name, method='POST', must=False, default=None)

def get_get_field(request, field_name, must=False, default=None):
    return _get_field(request, field_name, method='GET', must=False, default=None)

# METHOD IS NOT USED, TODO
def get_request_field(request, field_name, must=False, default=None, method="BOTH"):
    post_value = None
    if method=='post':
        post_value = get_post_field(request, field_name)
    get_value = None
    if method == "get":
        get_value = get_get_field(request, field_name)
    if method=='both':
        post_value = get_post_field(request, field_name)
        get_value = get_get_field(request, field_name)
    if must:
        value = post_value or get_value # only None will be ignored
        if value is None:
            raise Exception("no field [%s] in GET or POST"%field_name)
        return value
    else:
        return post_value or get_value


def unicode_to_utf8(s):
    return s.encode("utf8")


if __name__ == "__main__":
    test_dt_format()

