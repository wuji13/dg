# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate
import datetime,time
from datetime import timedelta
import random
import json
import requests

from qiniu import Auth
from qiniu import BucketManager
from collections import Iterable

# Create your views here.


#获取openid
def Get_openid(request):
    try:
        if request.method == 'GET':
            code = request.GET.get('code')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))

            if Verify(_ciphertext,_time):
                r = requests.get(
                    'https://api.weixin.qq.com/sns/jscode2session?appid=wx81714609760712b7&secret=2316ac3f1d412bcab1a67cc9174ab77b&js_code=' + code + '&grant_type=authorization_code')
                code = json.loads(r.text)
                print(code)
                lis = (100, code)
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


#创建用户id_wx
def Create_user(request):
    if request.method == 'POST':
        #req = json.loads(request.body)
        #_id_wx = req['id_wx']
        _id_wx = request.POST.get('id_wx')
        _ciphertext = int(request.POST.get('ciphertext'))
        _time = int(request.POST.get('text'))

        if Verify(_ciphertext,_time):
            if User.objects.filter(id_wx = _id_wx):
                return HttpResponse('102')
            else:
                _status = True
                _start_time = datetime.datetime.now()
                _end_time = _start_time + datetime.timedelta(days=30)
                _times = 0
                code = Generate_invite_code()
                while User.objects.filter(invite_code = code):
                    code = Generate_invite_code()
                _invite_code = code
                user = User(id_wx=_id_wx,status=_status,start_time=_start_time,end_time=_end_time,times=_times,invite_code=_invite_code,get_list=True)
                user.save()
                return HttpResponse('100')
        else:
            return HttpResponse('101')

    else:
        return HttpResponse('103')

#一个简单的认证函数,通过时间和秘钥加密和解密，这是一个解密的过程
def Verify(ciphertext,time):
    _developer = Developer.objects.get(pk=1)
    sum = 0
    for i in _developer.secret:
        num = ord(i)
        sum = sum + num
    if sum + time == ciphertext :
        return True
    else:
        return False


def Generate_invite_code():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))

    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    invite_code = ''.join(myslice)  # list to string
    return invite_code

#判断一个变量是否定义
def  Isset(v):
         try :
            type(eval(v))
         except :
            return False
         else :
           return True

#获取汇率
def Get_rate(request):
    try:
        rate = Rate.objects.all()
        data = serializers.serialize('json',rate)
        print('我的汇率是',data)
        return HttpResponse(data)
    except:
        return HttpResponse('104')





#添加或者修改，客户id_wx/name/phone/site
def Add_client(request):
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _name = request.POST.get('name')
            _phone = request.POST.get('phone')
            _site = request.POST.get('site')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            print('我的客户ID是',_id)
            if Verify(_ciphertext, _time):
                #修改客户_id有定义 有定义则就有id就是修改属性
                if Isset(_id):
                    client = Client.objects.get(pk=_id)
                    client.name = _name
                    client.phone = _phone
                    client.site = _site
                    client.save()
                    return HttpResponse('100')
                #新增客户
                else:
                    if Client.objects.filter(name=_name):
                        return HttpResponse('102')
                    else:
                        client = Client(name=_name,phone=_phone,site=_site,user=_user)
                        client.save()
                        return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#删除客户id_wx/id
def Delete_client(request):
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

#查询客户get请求带id_wx
def Query_client(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _clients = b.client_set.all()
                data = serializers.serialize('json',_clients)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

#模糊查询客户
def DimQuery_client(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            _keyword = request.GET.get('keyword')
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _clients = b.client_set.all().filter(name__icontains=_keyword)
                data = serializers.serialize('json',_clients)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')




#添加商品post     ####################################

#添加或者修改，商品id_wx/name/phone/site
def Add_good(request):
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _name = request.POST.get('name')
            _price = request.POST.get('price')
            _specificati = request.POST.get('specificati')
            _photo = request.POST.get('photo')
            _purchase_price = request.POST.get('purchase_price')
            _purchase_currency = request.POST.get('purchase_currency')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            print('我的id是',_id)
            print('我的售价是', _price)
            if Verify(_ciphertext, _time):
                #修改客户_id有定义
                if Isset(_id):
                    good = Good.objects.get(pk=_id)
                    good.name = _name
                    good.price = _price
                    good.specificati = _specificati
                    good.photo = _photo
                    good.purchase_price = _purchase_price
                    good.purchase_currency = _purchase_currency
                    good.save()
                    return HttpResponse('100')
                #新增客户
                else:

                    good = Good(name=_name,price = _price,specificati = _specificati,photo = _photo,purchase_price = _purchase_price,purchase_currency = _purchase_currency,user=_user)
                    print('我的规格是', _specificati)
                    good.save()
                    return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#删除商品id_wx/name
def Delete_good(request):
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            print('要删除的ID是',_id)
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _good = b.good_set.get(pk=_id)
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

#查询商品get请求带id_wx
def Query_good(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _goods = b.good_set.all()
                data = serializers.serialize('json',_goods)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

# 模糊查询商品get请求带id_wx
def DimQuery_good(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _keyword = request.GET.get('keyword')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext, _time):
                b = User.objects.get(id_wx=_id_wx)
                _goods = b.good_set.all().filter(name__icontains=_keyword)
                data = serializers.serialize('json', _goods)
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#删除七牛空间图片
def delete_photo(key):
    try:
        access_key = 'FSHNpScDIuaUNAtBj0YTJQ6gZIbRYd4IoNtjaR8X'
        secret_key = '7wAnU6wXLwle-17E3mlz4nh9L4hqYH2OJoLhEIU3'
        # 初始化Auth状态
        q = Auth(access_key, secret_key)
        # 初始化BucketManager
        bucket = BucketManager(q)
        # 你要测试的空间， 并且这个key在你空间中存在
        bucket_name = 'good'
        _key = key
        # 删除bucket_name 中的文件 key
        ret, info = bucket.delete(bucket_name, _key)
        print(info)
        assert ret == {}
        return '100'
    except:
        return '104'




#生产七牛云的uptoken
def Uptoken(requset):
    try:
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'FSHNpScDIuaUNAtBj0YTJQ6gZIbRYd4IoNtjaR8X'
        secret_key = '7wAnU6wXLwle-17E3mlz4nh9L4hqYH2OJoLhEIU3'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'good'
        # 上传到七牛后保存的文件名
        t = str(int(time.time()*1000000))
        key = None
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        policy = {
            # 'callbackUrl':'https://requestb.in/1c7q2d31',
            # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
            # 'persistentOps':'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600, policy)
        data = {}
        data["uptoken"]=token
        js = json.dumps(data)

        return HttpResponse(js)
    except:
        return HttpResponse('104')

        #############################################################################################
#添加代购id_wx/name/
def Add_dg(request):
    try:
        print('收到创建代购请求')
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
                print('101')
                lis1 = (101)
                json_str = json.dumps(lis1)
                return HttpResponse(json_str)

        else:
            lis2 = (103)
            json_str = json.dumps(lis2)
            return HttpResponse(json_str)

    except:
        lis3 = (104)
        json_str = json.dumps(lis3)
        return HttpResponse(json_str)

#保存实际成本
def Save_cost(request):
    try:
        if request.method == 'POST':
            _id = request.POST.get('id')
            _cost = requests.POST.get('cost')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):
                buy=Buy.objects.filter(pk=_id)
                buy.cost = _cost
                buy.save()
                return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')



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
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#############################################################################################
#添加代购id_wx/name/
def Add_dglist(request):
    try:
        if request.method == 'POST':

            _id_client = request.POST.get('id_client')
            _id_buy = request.POST.get('id_buy')
            _id_wx = request.POST.get('id_wx')
            print('qwer',_id_client)
            print('111',_id_buy)

            _client = Client.objects.get(pk=_id_client)
            _buy = Buy.objects.get(pk=_id_buy)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))

            print(_client)
            print(_buy)
            if Verify(_ciphertext, _time):
                if Buy_list.objects.filter(buy=_buy).filter(client=_client):
                    lis2 = (102,300)
                    json_str = json.dumps(lis2)
                    print('6，相同客户')
                    return HttpResponse(json_str)
                else:
                    buy_list = Buy_list(client=_client,buy=_buy)
                    buy_list.save()
                    id_buy_list = buy_list.pk

                    user = User.objects.get(id_wx = _id_wx)
                    user.get_list = True
                    user.save()

                    print(id_buy_list)
                    lis = (100,id_buy_list)
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



#保存是否付款
def Save_pay(request):
    try:
        if request.method == 'POST':
            _id = request.POST.get('id')
            _gathering = float(request.POST.get('gathering'))
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            print(_id)
            print(_gathering)
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
                return HttpResponse(data)
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')

#输入币种数字代码返回汇率
def BZ(bz):
    _rate = Rate.objects.all()[0]
    if(bz == 0):
        return _rate.HKD
    elif(bz == 1):
        return _rate.CNY
    elif(bz == 2):
        return _rate.KRW
    elif(bz == 3):
        return _rate.AUD
    elif(bz == 4):
        return _rate.JPY
    elif(bz == 5):
        return _rate.GBP
    elif(bz == 6):
        return _rate.USD



#添加代购商品
def Add_dggood(request):
    rate = {'0':'HKD','1':'CNY','2':'KRW','3':'AUD','4':'JPY','5':'GBP','6':'USD'}
    try:
        if request.method == 'POST':

            _id_good = request.POST.get('id_good')
            _id_buy_list = request.POST.get('id_buy_list')
            _count = int(request.POST.get('count'))
            _id_wx = request.POST.get('id_wx')

            _good = Good.objects.get(pk=_id_good)
            _buy_list = Buy_list.objects.get(pk=_id_buy_list)

            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))

            if Verify(_ciphertext, _time):

                if Buy_good.objects.filter(buy_list=_buy_list).filter(good=_good) :
                    lis2 = (102,300)
                    json_str = json.dumps(lis2)
                    return HttpResponse(json_str)
                else:
                   
                    _price = round(_good.price,2)
                    bz = _good.purchase_currency
                    _cost =  round(_good.purchase_price * BZ(bz),2)
                    buy_good = Buy_good(count=_count,good=_good,buy_list=_buy_list,cost=_cost,price=_price)
                    buy_good.save()
                    user = User.objects.get(id_wx = _id_wx)
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
        lis4 = (104,300)
        print('7，xitong baob')
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)



#删除代购商品
def Delete_buy_good(request):
    try:
        if request.method == 'GET':
            _id_buy_good = request.GET.get('id_buy_good')
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            if Verify(_ciphertext,_time):
                _buy_good = Buy_good.objects.get(pk=_id_buy_good)
                _buy_good.delete()

                user = User.objects.get(id_wx=_id_wx)
                user.get_list = True
                user.save()
                lis = (100,300)
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



#查询代购客户列表get请求带id_wx
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
                clients = []
                print('通过')
                for i in b:
                    id_client = i.client_id
                    _client = Client.objects.get(pk=id_client)
                    c={'pay':i.pay,'id_buy_list':i.pk,'name_client':_client.name,'total':i.total,'gathering':i.gathering,'postage':i.postage}
                    clients.append(c)
                lis = (100,clients)
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


#查询代购客户的代购商品列表
def Query_buy_list(request):
    try:

        if request.method == 'GET':
            _id_buy_list = request.GET.get('id_buy_list')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))

            if Verify(_ciphertext,_time):
                b = Buy_list.objects.get(pk=_id_buy_list)
                id_client = b.client_id
                c = Client.objects.get(pk=id_client)
                all = b.buy_good_set.all()
                goods = []
                for i in all:
                    g = {}
                    _good = Good.objects.get(pk=i.good_id)
                    g = {'name': _good.name, 'specificati': _good.specificati,'photo': _good.photo}
                    goods.append(g)
                data = serializers.serialize('json', all, fields=('count', 'quantity','price','cost'))
                data_sz = json.loads(data)
                client_good = {'name': c.name, 'phone': c.phone, 'site': c.site, 'item': data_sz, 'goods': goods}
                lis = (100, client_good)
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


#查询最新次代购需代购的所有商品
def Query_buy_good_list(request):
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            sz = int(request.GET.get('datasnull'))
            if sz==0:
                datasnull=False
            else:
                datasnull=True
            print(datasnull)
            if Verify(_ciphertext,_time):
                user = User.objects.get(id_wx=_id_wx)
                if user.get_list or datasnull:

                    user.get_list = False
                    user.save()
                    b = User.objects.get(id_wx=_id_wx)
                    # 找到最近添加的buy记录
                    _buy = b.buy_set.all().last()
                    # 找到关联buy记录的所有buy_list的记录

                    # 找到关联buy记录的所有buy_list的记录
                    b = _buy.buy_list_set.all()
                    goods = []
                    for i in b:

                        # 找到关联buy_list记录中每条记录中的的所有buy_good的记录
                        buy_good = i.buy_good_set.all()
                        m = True
                        for j in buy_good:

                            m = True
                            for x in goods:
                                if j.good_id == x['id_good']:
                                    x['count_good'] = x['count_good'] + j.count
                                    x['quantity'] = x['quantity'] + j.quantity
                                    x['id_buy_good'].append(j.pk)
                                    m = False
                                    break
                            if m:
                                _good = Good.objects.get(pk=j.good_id)

                                good = {'id_buy': _buy.id, 'id_buy_good': [j.pk], 'count_good': j.count,
                                        'id_good': j.good_id, 'name': _good.name, 'specificati': _good.specificati,
                                        'price': _good.price, 'photo': _good.photo, 'quantity':j.quantity}
                                goods.append(good)

                    lis = (100, goods)

                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    lis0 = (105, 300)
                    json_str = json.dumps(lis0)
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

# 设置代购列表中某人的待收款额
def Set_total(buy_list_id):
    _buy_list = Buy_list.objects.get(pk=buy_list_id)
    _buy_list_good = Buy_good.objects.filter(buy_list=_buy_list)
    sum = 0
    for x in _buy_list_good:
        su = x.quantity * x.price
        sum = sum + su
    _buy_list.total = sum
    _buy_list.save()


#修改采购数量
def Alter_quantity(request):
    try:
        if request.method == 'POST':
            _quantity = int(request.POST.get('quantity'))
            id_buygood = request.POST.get('id_buy_good')
            id_buy_good = id_buygood.split(',')
            _finalcount = int(request.POST.get('finalcount'))
            _id_wx = request.POST.get('id_wx')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            if Verify(_ciphertext, _time):

                if _finalcount == _quantity:

                    for i in id_buy_good:
                        _buy_good = Buy_good.objects.get(pk=i)
                        _buy_good.quantity = _buy_good.count
                        _buy_good.save()
                else:
                    u = _quantity

                    for i in id_buy_good:
                        _buy_good = Buy_good.objects.get(pk=i)
                        if _buy_good.count<=u:
                            _buy_good.quantity = _buy_good.count
                            _buy_good.save()
                            u = u - _buy_good.count
                        else:
                            _buy_good.quantity = u
                            _buy_good.save()
                            u = 0
                for i in id_buy_good:
                    _buy_good = Buy_good.objects.get(pk=i)
                    Set_total(_buy_good.buy_list_id)

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


#修改代购商品的数量价格
def Alter_buy_good(request):

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
                print(buy_list.postage)
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


#获取个人利润
def Get_profit(request):
    try:
        if request.method == 'GET':

            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))

            if Verify(_ciphertext, _time):
                #print('请求接收')
                user = User.objects.get(id_wx=_id_wx)
                print(user)
                _buys = user.buy_set.all()
                #print('请求接收')
                sumcost = 0
                sumtotal = 0
                for i in _buys:
                    print(i.cost,i.postcost,i.gathering)
                    if(i.cost==None):
                        cost = 0
                    else:
                        cost = i.cost
                    if(i.postcost==None):
                        postcost = 0
                    else:
                        postcost = i.postcost

                    if (i.gathering == None):
                        gathering = 0
                    else:
                        gathering = i.gathering

                    print(cost, postcost, gathering)
                    sumcost = sumcost+cost+postcost
                    sumtotal = sumtotal + gathering
                    print(sumtotal)
                js = {'sumcost':sumcost,'sumtotal':sumtotal}
                lis = (100, js)
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