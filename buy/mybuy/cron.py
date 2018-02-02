# -*- coding: utf-8 -*-

from mybuy.models import Rate
import requests
#获取汇率存在数据库
def Save_rate():
    try:
        r = requests.get("https://api.fixer.io/latest?base=CNY&symbols=HKD,KRW,AUD,USD,JPY,GBP,CNY")
        print(r.text)
        a=r.text
        rate = eval(r.text)
        print(rate['rates']['HKD'])
        print(type(rate['rates']['HKD']))
        ra = Rate.objects.all()

        if(len(ra)==0):
            rara = Rate(HKD=rate['rates']['HKD'], KRW=rate['rates']['KRW'], AUD=rate['rates']['AUD'], USD=rate['rates']['USD'],
                    JPY=rate['rates']['JPY'], GBP=rate['rates']['GBP'] ,CNY=1)
            rara.save()
            print('100.1')
        else:
            rara = ra[0]
            rara.HKD = rate['rates']['HKD']
            rara.KRW = rate['rates']['KRW']
            rara.AUD = rate['rates']['AUD']
            rara.USD = rate['rates']['USD']
            rara.JPY = rate['rates']['JPY']
            rara.GBP = rate['rates']['GBP']
            rara.save()
            print('100.2')
    except:
        print('104')






