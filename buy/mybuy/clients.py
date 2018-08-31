# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate,Client_site,Inform,Confirm_inform
import datetime,time
from datetime import timedelta
import random
import json
import requests
from mybuy.views import Verify,Isset

from qiniu import Auth
from qiniu import BucketManager
from collections import Iterable


#查询客户地址
def Query_site(request):
    print('Query_site')
    try:
        if request.method == 'GET':
            _id_client = request.GET.get('id_client')
            print(_id_client)
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                c = Client.objects.get(pk=_id_client)
                print(c)
                sites = c.client_site_set.all()
                data = serializers.serialize('json',sites)
                da = json.loads(data)
                print(da)
                lis = (100, da)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = (101, 300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = (103, 300)
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = (104, 300)
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#新增地址
def Add_site(request):
    print('Add_site')
    try:
        if request.method == 'POST':
            _id_client = request.POST.get('id_client')
            _datas = request.POST.get('datas')
            _da = json.loads(_datas)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                if Client_site.objects.filter(site=_da['name']):
                    lis = (102, 300)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    client = Client.objects.get(pk=_id_client)
                    site = Client_site(site=_da['name'], client=client)
                    site.save()
                    lis = (100, 300)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
            else:
                lis = (101, 300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = (103, 300)
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = (104, 300)
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#系统通知,xitong tongzhi 
def Get_inform(request):
    print('Get_inform')
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                _user = User.objects.get(id_wx=_id_wx)

                _inform = Inform.objects.all().last()

                if _user.confirm_inform_set.all().filter(inform=_inform):

                    lis = (102, 300)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    coninform = Confirm_inform(inform=_inform, user=_user)

                    coninform.save()
                    da = {'content': _inform.content, 'id_inform': _inform.pk}

                    lis = (100, da)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
            else:
                lis1 = (101, 300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis3 = (103, 300)
            json_str = json.dumps(lis3)
            return HttpResponse(json_str)
    except:
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)


