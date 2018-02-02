from django.db import models

# Create your models here.
#用户表
class User(models.Model):
    id_wx = models.CharField(max_length=50)
    status = models.BooleanField()
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False)
    recently_time = models.DateTimeField(auto_now=True)
    times = models.IntegerField()
    invite_code = models.CharField(max_length=12)
    profit = models.FloatField(default=0)#总的利润
    saleroom = models.FloatField(default=0) #销售额
    get_list = models.BooleanField(default=True)  #这个字段记录是否需要重新获取最新代购明细的通过判断是否新增代购列表或者代购商品是否变化



    def __str__(self):  # __unicode__ on Python 2
        return self.id_wx


#商品表
class Good(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0,null=True,blank=True)              #售价
    specificati = models.CharField(max_length=80,null=True,blank=True)
    photo = models.CharField(max_length=300,null=True,blank=True)
    time = models.DateTimeField(auto_now=True)            #修改时间
    user = models.ForeignKey(User)
    purchase_price = models.FloatField(default=0,null=True,blank=True)     #采购价
    purchase_currency = models.IntegerField(default=0)             #采购币种，0：HKD  1:CNY  2:KRW  3:AUD  4:JPY  5:GBP  6:USD


    def __str__(self):  # __unicode__ on Python 2
        return self.name


#客户表
class Client(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, null=True,blank=True)
    site = models.CharField(max_length=200,null=True,blank=True)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)


    def __str__(self):  # __unicode__ on Python 2
        return self.name


#代购表对应buy页面
class Buy(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    cost = models.FloatField(null=True,blank=True)     #实际代购成本
    postcost = models.FloatField(null=True,blank=True)  #实际邮费成本
    gathering = models.FloatField(max_length=20,default=0)         #收款


    def __str__(self):  # __unicode__ on Python 2
        return self.name


#代购列表
class Buy_list(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    pay = models.BooleanField(default=False)
    client = models.ForeignKey(Client)
    buy = models.ForeignKey(Buy)
    gathering = models.FloatField(max_length=20, default=0)  # 已收款额
    total = models.FloatField(default=0)  #总待收款
    postage = models.FloatField(default=0) #邮费

    def __str__(self):  # __unicode__ on Python 2
        return self.client.name


#代购商品表
class Buy_good(models.Model):
    time = models.DateTimeField(auto_now=True)
    count = models.IntegerField()  #需购数量
    good = models.ForeignKey(Good)
    buy_list = models.ForeignKey(Buy_list)
    quantity = models.IntegerField(default=0)   #已购数量
    cost = models.FloatField(null=True,blank=True) #实际成本
    price = models.FloatField(null=True,blank=True) #实际售价

    def __str__(self):  # __unicode__ on Python 2
        return self.good.name


#开发者列表
class Developer(models.Model):
    name = models.CharField(max_length=40)
    secret = models.CharField(max_length=40)


    def __str__(self):  # __unicode__ on Python 2
        return self.name

#汇率表
class Rate(models.Model):
    HKD = models.FloatField()
    CNY = models.FloatField()
    KRW = models.FloatField()
    AUD = models.FloatField()
    USD = models.FloatField()
    JPY = models.FloatField()
    GBP = models.FloatField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.pk

