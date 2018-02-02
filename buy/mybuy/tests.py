from django.test import TestCase

from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate
import requests
import json

# Create your tests here.

def Test(request):
    pass
    '''
    print('收到请求')
    try:
        if request.method == 'GET':
            code = request.GET.get('code')
            print(code)
            r = requests.get(
                'https://api.weixin.qq.com/sns/jscode2session?appid=wx81714609760712b7&secret=2316ac3f1d412bcab1a67cc9174ab77b&js_code=' + code + '&grant_type=authorization_code')
            print(r.text)
            code = json.loads(r.text)
            print(code)
            print(type(r.text))
            lis = (100, code)
            json_str = json.dumps(lis)
            return HttpResponse(json_str)

        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')
    '''