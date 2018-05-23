# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate,Client_site,Good_specification
import datetime,time
from datetime import timedelta
import random
import json
import requests
from mybuy.views import Verify,Isset,BZ,Set_total

from qiniu import Auth
from qiniu import BucketManager


#添加代购id_wx/name/
def Add_dg(request):
    print('Add_dg')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _name = request.POST.get('name')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                buy = Buy(name=_name,user=_user)
                buy.save()
                user = User.objects.get(id_wx=_id_wx)
                user.get_list = True
                user.save()
                id_buy = buy.id
                lis = (100,id_buy)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis1 = (101,300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis2 = (103.300)
            json_str = json.dumps(lis2)
            return HttpResponse(json_str)

    except:
        lis3 = (104,300)
        json_str = json.dumps(lis3)
        return HttpResponse(json_str)


#查询代购列表get请求带id_wx
def Query_dg(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _buys = b.buy_set.all()
                data = serializers.serialize('json',_buys)
                da = json.loads(data)
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


#############################################################################################
#添加代购人id_wx/name/
def Add_dglist(request):
    print("Add_dglist")
    try:
        if request.method == 'POST':

            _id_client = request.POST.get('id_client')
            _id_buy = request.POST.get('id_buy')
            _id_wx = request.POST.get('id_wx')
            client = Client.objects.get(pk=_id_client)
            print(client)

            _buy = Buy.objects.get(pk=_id_buy)
            print(_buy)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))


            if Verify(_ciphertext, _time):
                if Buy_list.objects.filter(buy=_buy).filter(client=client):
                    lis2 = (102,300)
                    json_str = json.dumps(lis2)
                    print('6，相同客户')
                    return HttpResponse(json_str)
                else:
                    try:
                        _site = client.client_site_set.all()[0:1].get()
                        buy_list = Buy_list(client=client, buy=_buy, client_name=client.name, client_phone=client.phone,
                                            client_site=_site.site)
                    except :
                        buy_list = Buy_list(client=client, buy=_buy, client_name=client.name, client_phone=client.phone,
                                            client_site='')
                    buy_list.save()

                    user = User.objects.get(id_wx = _id_wx)
                    user.get_list = True
                    user.save()
                    da = {'id_buylist':buy_list.pk,'clientid':buy_list.client_id, 'name':buy_list.client.name, 'phone':buy_list.client.phone,
                                            'site':buy_list.client_site}
                    lis = (100,da)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)

            else:
                lis1 = (101,300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis2 = (103,300)
            json_str = json.dumps(lis2)
            return HttpResponse(json_str)

    except:
        lis3 = (104,300)
        json_str = json.dumps(lis3)
        return HttpResponse(json_str)

#查询单次代购所以客户列表
def Query_buy_client(request):
    print('j接收到请求')
    try:
        if request.method == 'GET':
            _id_buy = request.GET.get('id_buy')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            print('j接收到请求')
            if Verify(_ciphertext,_time):
                b = Buy_list.objects.filter(buy=_id_buy)
                data = serializers.serialize('json', b)
                da = json.loads(data)
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

# 查询代购客户详情的代购商品列表
def Query_buy_list(request):
    print('Query_buy_list')
    try:
        if request.method == 'GET':
            _id_buy_list = request.GET.get('id_buy_list')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                print('Query_buy_l_id_buy_listist', _id_buy_list)
                b = Buy_list.objects.get(pk=_id_buy_list)
                all = b.buy_good_set.all()
                data = serializers.serialize('json', all, fields=('count', 'quantity', 'price', 'cost','good_name','good_specification','good_photo'))
                data_sz = json.loads(data)
                print('Query_buy_list',data_sz)
                lis = (100, data_sz)
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

# 添加代购商品
def Add_dggood(request):
    print('Add_dggood')
    rate = {'0': 'HKD', '1': 'CNY', '2': 'KRW', '3': 'AUD', '4': 'JPY', '5': 'GBP', '6': 'USD'}
    try:
        if request.method == 'POST':
            _id_good = request.POST.get('id_good')
            _id_buy_list = request.POST.get('id_buy_list')
            _count = int(request.POST.get('count'))
            _id_wx = request.POST.get('id_wx')
            _id_spe = request.POST.get('id_spe')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            print(_id_spe,_id_good,_id_buy_list)
            if Verify(_ciphertext, _time):
                _good = Good.objects.get(pk=_id_good)
                _buy_list = Buy_list.objects.get(pk=_id_buy_list)

                if _id_spe!='':
                    print('spespe',_id_spe)
                    _spe = Good_specification.objects.get(pk=_id_spe)
                    if Buy_good.objects.filter(buy_list=_buy_list).filter(spe=_spe):
                        lis2 = (102, 300)
                        json_str = json.dumps(lis2)
                        return HttpResponse(json_str)
                    else:
                        print(_buy_list)
                        _price = round(_spe.price, 2)
                        bz = _spe.purchase_currency
                        _cost = round(_spe.purchase_price * BZ(bz), 2)
                        buy_good = Buy_good(count=_count, good=_good, buy_list=_buy_list, cost=_cost, price=_price,good_name=_good.name,good_specification=_spe.specificati,good_photo=_good.photo,spe=_spe)
                        buy_good.save()
                        user = User.objects.get(id_wx=_id_wx)
                        user.get_list = True
                        user.save()
                        lis = (100, 300)
                        json_str = json.dumps(lis)
                        return HttpResponse(json_str)
                else:
                    print('buygood', _id_spe)
                    if Buy_good.objects.filter(buy_list=_buy_list).filter(good=_good):
                        lis2 = (102, 300)
                        json_str = json.dumps(lis2)
                        return HttpResponse(json_str)
                    else:
                        print(_buy_list)
                        buy_good = Buy_good(count=_count, good=_good, buy_list=_buy_list,
                                            good_name=_good.name,
                                            good_photo=_good.photo )
                        buy_good.save()
                        user = User.objects.get(id_wx=_id_wx)
                        user.get_list = True
                        user.save()
                        lis = (100, 300)
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

# 删除代购商品
def Delete_dg_good(request):
    try:
        if request.method == 'GET':
            _id_buy_good = request.GET.get('id_buy_good')
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                _buy_good = Buy_good.objects.get(pk=_id_buy_good)
                _buy_good.delete()
                user = User.objects.get(id_wx=_id_wx)
                user.get_list = True
                user.save()
                lis = (100, 300)
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


#查询代购列表get请求带id_wx
def Query_buylist(request):
    try:
        if request.method == 'GET':
            _id_buy = request.GET.get('id_buy')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                b = Buy.objects.get(pk=_id_buy)
                _buylists = b.buy_list.all()
                data = serializers.serialize('json',_buylists)
                da = json.loads(data)
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

#修改代购收货地址
def Fix_dgsite(request):
    print('Fix_dgsite')
    try:
        if request.method == 'POST':
            _id_buy_list = request.POST.get('id_buy_list')
            _site = request.POST.get('site')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                buy_list = Buy_list.objects.get(pk=_id_buy_list)
                buy_list.client_site = _site
                buy_list.save()
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


#查询商品规格
def Query_good_specification(request):
    print("Query_good_specification")
    try:
        if request.method == 'GET':
            _id_good = request.GET.get('id_good')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                g = Good.objects.get(pk=_id_good)
                spe = g.good_specification_set.all()
                data = serializers.serialize('json',spe,fields=('specificati'))
                da = json.loads(data)
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


#修改代购商品的数量价格
def Alter_buy_good(request):
    print('Alter_buy_good')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _price = float(request.POST.get('price'))
            _cost = float(request.POST.get('cost'))
            _count = int(request.POST.get('count'))
            _id_buy_good = request.POST.get('id_buy_good')
            _id_buy_list = request.POST.get('id_buy_list')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            print(_id_wx,_price,_cost,_count,_id_buy_good)
            if Verify(_ciphertext, _time):
                buy_good = Buy_good.objects.get(pk=_id_buy_good)
                print(buy_good.price)
                buy_good.price = round(_price,2)
                buy_good.cost = round(_cost,2)
                buy_good.count = _count
                buy_good.save()
                #修改商品的待收款额
                # 设置代购列表中某人的待收款额
                Set_total(_id_buy_list)
                user = User.objects.get(id_wx=_id_wx)
                user.get_list = True
                user.save()
                lis = (100,300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis1 = (101,300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis3 = (103,300)
            json_str = json.dumps(lis3)
            return HttpResponse(json_str)
    except:
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)




#修改客户邮价
def Alter_postage(request):
    try:
        if request.method == 'POST':
            _postage = float(request.POST.get('postage'))
            _id_buy_list = request.POST.get('id_buy_list')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                buy_list = Buy_list.objects.get(pk=_id_buy_list)
                buy_list.postage = round(_postage,2)
                buy_list.save()
                lis = (100,300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis1 = (101,300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis3 = (103,300)
            json_str = json.dumps(lis3)
            return HttpResponse(json_str)
    except:
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)

#保存是否付款多少
def Save_pay(request):
    print('Save_pay')
    try:
        if request.method == 'POST':
            _id = request.POST.get('id')
            _gathering = float(request.POST.get('gathering'))
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                buy_list=Buy_list.objects.get(pk=_id)
                s = buy_list.gathering
                buy_list.gathering = _gathering
                buy_list.save()
                _buy = Buy.objects.get(pk=buy_list.buy_id)
                x = _buy.gathering
                valpay = x - s + _gathering
                _buy.gathering = valpay
                _buy.save()
                lis = (100, 300)
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



#修改一次代购成本
def Alter_cost(request):
    try:
        if request.method == 'POST':
            _cost = float(request.POST.get('cost'))
            _id_buy = request.POST.get('id_buy')
            _postcost = float(request.POST.get('postcost'))
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
           # print('接收到请求',_id_buy)
            if Verify(_ciphertext, _time):
                buy = Buy.objects.get(pk=_id_buy)
                buy.cost = round(_cost,2)
                buy.postcost = round(_postcost, 2)
                buy.save()
                lis = (100,300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis1 = (101,300)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)
        else:
            lis3 = (103,300)
            json_str = json.dumps(lis3)
            return HttpResponse(json_str)
    except:
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)


#删除个人订单
def Delete_buy_list(request):
    try:
        if request.method == 'GET':

            _id_wx = request.GET.get('id_wx')
            _id_buy_list = request.GET.get('id_buy_list')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))

            print(_id_wx,_id_buy_list)
            if Verify(_ciphertext, _time):
                buy_list = Buy_list.objects.get(pk=_id_buy_list)
                buy_list.delete()

                user = User.objects.get(id_wx=_id_wx)
                user.get_list = True
                user.save()
                lis = (100, 300)
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