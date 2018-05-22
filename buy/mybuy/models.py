from django.db import models

# Create your models here.
#用户表
class User(models.Model):
    id_wx = models.CharField(max_length=50)
    status = models.BooleanField()
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False)
    craete_time = models.DateTimeField(auto_now_add=True)
    recently_time = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(max_length=12)
    profit = models.FloatField(default=0)#总的利润
    saleroom = models.FloatField(default=0) #销售额
    get_list = models.BooleanField(default=True)  #这个字段记录是否需要重新获取最新代购明细的通过判断是否新增代购列表或者代购商品是否变化



    def __str__(self):  # __unicode__ on Python 2
        return self.id_wx

#商品标签表
class Category(models.Model):
    name = models.CharField(max_length=36) #10字
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # __unicode__ on Python 2
        return self.name


#商品表
class Good(models.Model):
    name = models.CharField(max_length=160) #50字
    photo = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)  # 修改时间
    create_time = models.DateTimeField(auto_now_add=True) #创建时间
    remark = models.CharField(max_length=740,null=True,blank=True) #备注  //240字
    label = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL)  #类别

    def __str__(self):  # __unicode__ on Python 2
        return self.name

#商品规格表
class Good_specification(models.Model):
    good = models.ForeignKey(Good)
    price = models.FloatField(default=0)              #售价
    specificati = models.CharField(max_length=64,null=True,blank=True)
    purchase_price = models.FloatField(default=0)     #采购价
    purchase_currency = models.IntegerField(default=0)             #采购币种，0：HKD  1:CNY  2:KRW  3:AUD  4:JPY  5:GBP  6:USD
    time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.specificati


#客户表
class Client(models.Model):
    name = models.CharField(max_length=36)
    phone = models.CharField(max_length=18, null=True,blank=True)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

#客户地址表
class Client_site(models.Model):
    site = models.CharField(max_length=210,null=True,blank=True) #60字
    client = models.ForeignKey(Client)
    time = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


#代购表对应buy页面
class Buy(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    create_time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    cost = models.FloatField(default=0)     #实际代购成本
    postcost = models.FloatField(default=0)  #实际邮费成本
    gathering = models.FloatField(default=0)         #收款

    def __str__(self):  # __unicode__ on Python 2
        return self.name


#代购列表
class Buy_list(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=36,null=True,blank=True)
    client_phone = models.CharField(max_length=18, null=True,blank=True)
    client_site = models.CharField(max_length=200,null=True,blank=True)
    buy = models.ForeignKey(Buy)
    gathering = models.FloatField(max_length=20, default=0)  # 已收款额
    total = models.FloatField(default=0)  #总待收款
    postage = models.FloatField(default=0) #邮费
    remarks = models.CharField(max_length=1024,null=True,blank=True)
    def __str__(self):  # __unicode__ on Python 2
        return self.client.name


#代购商品表
class Buy_good(models.Model):
    time = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)  #需购数量
    good = models.ForeignKey(Good,null=True,blank=True,on_delete=models.SET_NULL)
    spe = models.ForeignKey(Good_specification,null=True,blank=True,on_delete=models.SET_NULL)
    good_name = models.CharField(max_length=160,null=True,blank=True) #商品名称
    good_specification = models.CharField(max_length=128,null=True,blank=True) #40字
    good_photo = models.CharField(max_length=300, null=True, blank=True)
    buy_list = models.ForeignKey(Buy_list,null=True,blank=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)   #已购数量
    cost = models.FloatField(default=0) #实际成本
    price = models.FloatField(default=0) #实际售价

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


#系统通知
class Inform(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=600)
    createtime = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.title

#系统通知已读表
class Confirm_inform(models.Model):
    inform = models.ForeignKey(Inform)
    createtime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    confirm = models.BooleanField(default=False)
    def __str__(self):  # __unicode__ on Python 2
        return self.inform.title


