from django.test import TestCase

from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate,Good_specification,Inform,Confirm_inform
import requests
import json

from mybuy.views import Isset
# Create your tests here.

def Test(request):
    print('Test')
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _inform = Inform.objects.all().last()
            if _user.confirm_inform_set.all().filter(inform=_inform):
                print('3')
                lis = (102, 300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                print('4', type(_inform), type(_user))
                coninform = Confirm_inform(inform=_inform,user=_user)
                print('5')
                coninform.save()
                da = {'content': _inform.content, 'id_inform': _inform.pk}
                print('6', da)
                lis = (100, da)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis3 = (103, 300)
            json_str = json.dumps(lis3)
            return HttpResponse(json_str)
    except:
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)

