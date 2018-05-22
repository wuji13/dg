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
                    'https://api.weixin.qq.com/sns/jscode2session?appid=wx8e2f68ed92592476&secret=891afae4860dd6b0cc862df32e814d0b&js_code=' + code + '&grant_type=authorization_code')
                code = json.loads(r.text)
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
                code = Generate_invite_code()
                while User.objects.filter(invite_code = code):
                    code = Generate_invite_code()
                _invite_code = code
                user = User(id_wx=_id_wx,status=_status,start_time=_start_time,end_time=_end_time,invite_code=_invite_code,get_list=True)
                user.save()
                return HttpResponse('100')
        else:
            return HttpResponse('101')
    else:
        return HttpResponse('103')

#一个简单的认证函数,通过时间和秘钥加密和解密，这是一个解密的过程
def Verify(ciphertext,ti):
    t = time.time()*1000
    if ti - t > -10000:
        _developer = Developer.objects.get(pk=1)
        sum = 0
        for i in _developer.secret:
            num = ord(i)
            sum = sum + num
        if sum + ti == ciphertext :
            return True
        else:
            return False
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
        return HttpResponse(data)
    except:
        return HttpResponse('104')


#存用户地址
def Save_site(client,datas):
    sit = ['site0','site1','site2','site3','site4','no']
    for i in sit:
        if datas.get(i,False):
            site = Client_site(site=datas.get(i),client=client)
            site.save()
        else:
            continue

#修改用户地址
def Fix_site(client,datas):
    print('Fix_site',datas)
    sit = ['site0', 'site1', 'site2', 'site3', 'site4', 'no']
    site = Client_site.objects.filter(client = client)
    for i in site:
            i.delete()
    for i in sit:
        if datas.get(i, False):
            site = Client_site(site=datas.get(i), client=client)
            site.save()
        else:
            continue

#添加或者修改，客户id_wx/name/phone/site
def Add_client(request):
    print('Add_client')
    try:
        if request.method == 'POST':
            _id_wx = request.POST.get('id_wx')
            _user = User.objects.get(id_wx=_id_wx)
            _datas = request.POST.get('datas')

            _da = json.loads(_datas)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            if Verify(_ciphertext, _time):
                #修改客户_id有定义 有定义则就有id就是修改属性
                if Isset(_id):
                    print('fix')
                    client = Client.objects.get(pk=_id)
                    client.name = _da['name']
                    client.phone = _da['phone']
                    client.save()
                    Fix_site(client,_da)
                    return HttpResponse('100')
                #新增客户
                else:
                    if Client.objects.filter(name=_da['name']):
                        return HttpResponse('102')
                    else:
                        client = Client(name=_da['name'],phone=_da['phone'],user=_user)
                        client.save()
                        Save_site(client,_da)
                        return HttpResponse('100')
            else:
                return HttpResponse('101')
        else:
            return HttpResponse('103')
    except:
        return HttpResponse('104')


#删除客户id_wx/id
def Delete_client(request):
    print('Delete_client')
    try:
        if request.method == 'POST':
            _id = request.POST.get('id')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('text'))
            _id = request.POST.get('id')
            if Verify(_ciphertext,_time):
                _client = Client.objects.get(pk=_id)
                _client.delete()
                lis = (100, 300)
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

#查询客户get请求带id_wx

def Query_client(request):
    print('Query_client')
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

# 查询客户单个详情get请求带id_wx
def Query_client_detail(request):
    print('Query_client_detail')
    try:
        if request.method == 'GET':
            _id_client = request.GET.get('id_client')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            print('今天真惨shoudao',_id_client)
            if Verify(_ciphertext, _time):
                c = Client.objects.get(pk=_id_client)
                sites = c.client_site_set.all()
                data = serializers.serialize('json', sites)
                ddaa = json.loads(data)
                print('今天真惨',data)
                da = {'name':c.name,'phone':c.phone,'site':ddaa}
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






#查询商品get请求带id_wx
def Query_good(request):
    print('Query_good')
    try:
        if request.method == 'GET':
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            arry = []
            if Verify(_ciphertext,_time):
                b = User.objects.get(id_wx=_id_wx)
                _goods = b.good_set.all()
                for i in _goods:
                    good_spe = Good_specification.objects.filter(good = i)
                    Dgood_spe = serializers.serialize('json', good_spe)
                    bs = {'name':i.name,'photo':i.photo,'pk':i.pk,'spe':Dgood_spe}
                    arry.append(bs)
                data = json.dumps(arry)
                print(data)
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







#查询最新次代购需代购的所有商品
def Query_buy_good_list(request):
    print("Query_buy_good_list")
    try:
        if request.method == 'GET':
            print('00000')
            _id_wx = request.GET.get('id_wx')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('text'))
            sz = int(request.GET.get('datasnull'))  #判断是否为空，来查是否需要再次请求数据
            print('11111',_id_wx,sz)
            if sz==0:
                datasnull=False
            else:
                datasnull=True
            if Verify(_ciphertext,_time):
                user = User.objects.get(id_wx=_id_wx)
                print('22222',user)
                if user.get_list or datasnull:
                    print('33333', user)
                    user.get_list = False
                    user.save()
                    print('44444', user.get_list)
                    u = User.objects.get(id_wx=_id_wx)

                    # 找到最近添加的buy记录
                    _buy = u.buy_set.all().last()
                    # 找到关联buy记录的所有buy_list的记录
                    print('44444', _buy)
                    # 找到关联buy记录的所有buy_list的记录
                    b_list = _buy.buy_list_set.all()
                    goods = []
                    print('44444',b_list)
                    for i in b_list:
                        # 找到关联buy_list记录中每条记录中的的所有buy_good的记录

                        buy_good = i.buy_good_set.all()
                        print('55555',buy_good)
                        for j in buy_good:
                            print('66666')
                            m = True
                            for x in goods:
                                print('77777', type(x))
                                print('88888', x)
                                print('99999',x['good_id'])
                                if j.good_id == x['good_id']:
                                    print('44446666')
                                    x['count_good'] = x['count_good'] + j.count
                                    print('fasdf',j.count)
                                    x['quantity'] = x['quantity'] + j.quantity
                                    x['id_buy_good'].append(j.pk)
                                    m = False
                                    break
                            if m:
                                good = {'id_buy': _buy.id, 'id_buy_good': [j.pk], 'count_good': j.count,'good_id':j.good_id,
                                         'name': j.good_name, 'specificati': j.good_specification,
                                        'price': j.price, 'photo': j.good_photo, 'quantity':j.quantity}
                                goods.append(good)
                                print('9090',good,goods)
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
        print('final')
        lis4 = (104, 300)
        json_str = json.dumps(lis4)
        return HttpResponse(json_str)



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




