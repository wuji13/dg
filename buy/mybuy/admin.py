from django.contrib import admin
from mybuy.models import User,Buy_list,Buy,Buy_good,Good,Client,Developer,Rate
# Register your models here.

admin.site.register(User)
admin.site.register(Buy_list)
admin.site.register(Buy)
admin.site.register(Buy_good)
admin.site.register(Good)
admin.site.register(Client)
admin.site.register(Developer)
admin.site.register(Rate)