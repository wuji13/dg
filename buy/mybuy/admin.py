from django.contrib import admin
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate,Good_specification,Confirm_inform,Inform,Client_site
# Register your models here.

admin.site.register(User)
admin.site.register(Buy_list)
admin.site.register(Buy)
admin.site.register(Buy_good)
admin.site.register(Good)
admin.site.register(Good_specification)
admin.site.register(Client)
admin.site.register(Developer)
admin.site.register(Rate)
admin.site.register(Inform)
admin.site.register(Confirm_inform)
admin.site.register(Client_site)