#-*- coding: UTF-8 -*-
import urllib
from urllib import request, error, parse
import hashlib
import time
import base64
import json

app_key = 'msD6WmxJhP0ynRbJ'
app_id = '1106905332'
# url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_bizlicenseocr'
url_preffix='https://api.ai.qq.com/fcgi-bin/'

def setParams(array, key, value):
    array[key] = value

def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.request.quote(str(parser[key]), safe = ''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()

class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}

    def invoke(self, params):
        self.url_data = parse.urlencode(params).encode('utf-8')
        req = request.Request(self.url, self.url_data, method='POST')
        try:
            rsp = request.urlopen(req)
            str_rsp = rsp.read()
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except error.URLError as e:
            dict_error = {}
            if hasattr(e, "code"):
                dict_error = {}
                dict_error['ret'] = -1
                dict_error['httpcode'] = e.code
                dict_error['msg'] = "sdk http post err"
                return dict_error
            if hasattr(e,"reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error
        # else:
        #     dict_error = {}
        #     dict_error['ret'] = -1
        #     dict_error['httpcode'] = -1
        #     dict_error['msg'] = "system error"
        #     return dict_error


    def busi_lic_check(self, image):
        self.url = url_preffix + 'ocr/ocr_bizlicenseocr'
        setParams(self.data, 'app_id', self.app_id)
        setParams(self.data, 'app_key', self.app_key)
        setParams(self.data, 'time_stamp', int(time.time()))
        setParams(self.data, 'nonce_str', int(time.time()))
        image_data = str(base64.b64encode(image), 'utf-8')
        setParams(self.data, 'image', image_data)
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)
        # self.data.pop('app_key')
        return self.invoke(self.data)

# if __name__ == '__main__':
#     with open('./data/0001003.jpg', 'rb') as bin_data:
#         image = bin_data.read()
#
#     ai_obj = AiPlat(app_id, app_key)
#
#     print('----------------------SEND REQ----------------------')
#     rsp = ai_obj.busi_lic_check(image)
#
#     if rsp['ret'] == 0:
#         for i in rsp['data']['item_list']:
#             print(i['itemstring'])
#         print('----------------------API SUCC----------------------')
#     else:
#         print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
#         print('----------------------API FAIL----------------------')