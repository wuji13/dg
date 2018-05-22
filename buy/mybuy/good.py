# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate,Client_site,Category,Good_specification
import datetime,time
from datetime import timedelta
import random
import json
import requests

from mybuy.views import Verify,Isset,delete_photo

#添加商品分类
def Add_category(request):
    print('Add_category')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _datas = request.POST.get('datas')
            _da = json.loads(_datas)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                if Category.objects.filter(user=_user).filter(name=_da['name']):
                    return HttpResponse('102')
                else:
                    client = Category(name=_da['name'],user=_user)
                    client.save()
                    return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#删除客户id_wx/id
def Delete_category(request):
    print('Delete_category')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                print(_id)
                _client = b.client_set.get(pk=_id)
                print(_client)
                _client.delete()
                return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

#查询类别

def Query_category(request):
    print('Query_category')
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _category = b.category_set.all()
                data = serializers.serialize('json',_category)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

#存储商品规格
def add_good_specificati(good,datas,purchase_currency,nub):
    print('add_good_specificati', nub)
    sit = ['0','1','2','3','4','5','6','7','no']
    n = int(nub)
    j = 0
    for i in sit:
        if j < n:
            specificati = Good_specification(good=good, purchase_currency=purchase_currency)
            if datas.get('specificati'+i,False):
                specificati.specificati=datas.get('specificati'+i)
            if datas.get('price'+i,False):
                specificati.price=datas.get('price'+i)
            if datas.get('purchase_price'+i,False):
                specificati.purchase_price = datas.get('purchase_price' + i)
            if datas.get('specificati'+i,False) or datas.get('price'+i,False) or datas.get('purchase_price'+i,False):
                specificati.save()
            j=j+1
        else:
            break



# 修改商品规格
def fix_good_specificati(good, datas, purchase_currency, nub):
    print('fix_good_specificati', nub)
    sit = ['0', '1', '2', '3', '4', '5', '6', '7', 'no']
    n = int(nub)
    j = 0
    good_specificati=Good_specification.objects.filter(good=good)
    for i in good_specificati:
        i.delete()
    for i in sit:
        if j < n:
            specificati = Good_specification(good=good, purchase_currency=purchase_currency)
            if datas.get('specificati' + i, False):
                specificati.specificati = datas.get('specificati' + i)
            if datas.get('price' + i, False):
                specificati.price = datas.get('price' + i)
            if datas.get('purchase_price' + i, False):
                specificati.purchase_price = datas.get('purchase_price' + i)
            if datas.get('specificati' + i, False) or datas.get('price' + i, False) or datas.get(
                            'purchase_price' + i, False):
                specificati.save()
            j = j + 1
        else:
            break

#添加或者修改，商品id_wx/name/phone/site
def Add_good(request):
    print('Add_good')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _photo = request.POST.get('photo')
            _purchase_currency = request.POST.get('purchase_currency')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            _categoryid = request.POST.get('categoryid')
            _speNub = request.POST.get('speNub')

            _datas = request.POST.get('datas')
            _da = json.loads(_datas)

            if Verify(_ciphertext, _time):
                #修改_id有定义
                if Isset(_id):
                    _good = Good.objects.get(pk=_id)
                    if Isset(_categoryid):
                        _categ = Category.objects.get(pk=_categoryid)
                        _good.label = _categ
                        _good.name = _da.get('name')
                        _good.photo = _photo
                        _good.remark = _da.get('remark')
                        _good.save()
                        fix_good_specificati(_good, _da, _purchase_currency, _speNub)
                    else:
                        _good.name = _da.get('name')
                        _good.photo = _photo
                        _good.remark = _da.get('remark')
                        _good.save()
                        fix_good_specificati(_good, _da, _purchase_currency, _speNub)

                    return HttpResponse('100')
                #新增
                else:
                    if Isset(_categoryid):
                        _categ = Category.objects.get(pk=_categoryid)
                    else:
                        _categ = None
                    good = Good(name=_da.get('name'),photo=_photo,user=_user,remark=_da.get('remark'),label=_categ)
                    good.save()
                    add_good_specificati(good,_da,_purchase_currency,_speNub)
                    return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')



# 筛选商品
def Query_category_good(request):
    print('Query_category_good')
    try:
        if request.method == 'GET':
            _id_category = request.GET.get('id_category')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                print('Query',_id_category)
                c = Category.objects.get(pk=_id_category)
                goods = c.good_set.all()
                data = serializers.serialize('json', goods)
                da = json.loads(data)
                print('今天真惨',data)
                lis = (100,da)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis0 = (101, 300)
                json_str0 = json.dumps(lis0)
                return HttpResponse(json_str0)
        else:
            lis1 = (103, 300)
            json_str1 = json.dumps(lis1)
            return HttpResponse(json_str1)
    except:
        lis2 = (104, 300)
        json_str2 = json.dumps(lis2)
        return HttpResponse(json_str2)

#删除商品name
def Delete_good(request):
    try:
        if request.method == 'POST':
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            print('要删除的ID是',_id,_ciphertext,_time)
            if Verify(_ciphertext,_time):
                print('我要删除',)
                _good = Good.objects.get(pk=_id)
                _photo_url = _good.photo
                print('我要删除的图片的名字',_photo_url)
                #删除七牛图片
                re = delete_photo(_photo_url)
                print(re)
                _good.delete()
                return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

def Select_good(request):
    print('Select_good')
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                b = User.objects.get(id_wx=_id_wx)
                _goods = b.good_set.all()
                data = serializers.serialize('json',_goods)
                print(data)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#查询商品详情
def Query_good_detail(request):
    print('Query_good_detail')
    try:
        if request.method == 'GET':
            _id_good = request.GET.get('id_good')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                print('Query',_id_good)
                g = Good.objects.get(pk=_id_good)
                goodspe = g.good_specification_set.all()
                data = serializers.serialize('json', goodspe)
                da = json.loads(data)
                print(g.label)
                if g.label is None:
                    print('no', g.photo)
                    da = {'name': g.name, 'photo': g.photo, 'remark': g.remark, 'category': '无', 'categoryid': '',
                          'spe': da}
                else:
                    print('ok', g.photo)
                    da = {'name': g.name, 'photo': g.photo, 'remark': g.remark, 'category': g.label.name,
                          'categoryid': g.label_id, 'spe': da}

                lis = (100,da)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis0 = (101, 300)
                json_str0 = json.dumps(lis0)
                return HttpResponse(json_str0)
        else:
            lis1 = (103, 300)
            json_str1 = json.dumps(lis1)
            return HttpResponse(json_str1)
    except:
        lis2 = (104, 300)
        json_str2 = json.dumps(lis2)
        return HttpResponse(json_str2)

def Alter_remark(request):
    print('Alter_remark')
    try:
        if request.method == 'POST':
            _id_buy_list = request.POST.get('id_buy_list')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _remark = request.POST.get('remark')
            if Verify(_ciphertext, _time):
                buy_list = Buy_list.objects.get(pk=_id_buy_list)
                buy_list.remarks = _remark
                buy_list.save()
                lis = (100,300)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis0 = (101, 300)
                json_str0 = json.dumps(lis0)
                return HttpResponse(json_str0)
        else:
            lis1 = (103, 300)
            json_str1 = json.dumps(lis1)
            return HttpResponse(json_str1)
    except:
        lis2 = (104, 300)
        json_str2 = json.dumps(lis2)
        return HttpResponse(json_str2)