from django.conf.urls import url
from . import views,tests

urlpatterns = [
    url(r'^test', tests.Test, name='test'),

    url(r'^createuser',views.Create_user,name='create_user'),
    url(r'^addclient',views.Add_client,name='add_client'),
    url(r'^deleteclient',views.Delete_client,name='delete_client'),
    url(r'^queryclient',views.Query_client,name='query_client'),
    url(r'^getrate',views.Get_rate,name='get_rate'),
    url(r'^uptoken',views.Uptoken,name='uptoken'),
    url(r'^addgood',views.Add_good,name='addgood'),
    url(r'^deletegood',views.Delete_good,name='deletegood'),
    url(r'^querygood',views.Query_good,name='querygood'),

    url(r'^adddg',views.Add_dg,name='adddg'),
    url(r'^savecost',views.Save_cost,name='savecost'),
    url(r'^querydg',views.Query_dg,name='querydg'),

    url(r'^addlist', views.Add_dglist, name='adddglist'),
    url(r'^savepay', views.Save_pay, name='savepay'),
    url(r'^querydglist', views.Query_buylist, name='querydglist'),

    url(r'^dggood', views.Add_dggood, name='adddggood'),

    url(r'^querybuyclient', views.Query_buy_client, name='querybuyclient'),

    url(r'^querybuylist', views.Query_buy_list, name='querybuylist'),

    url(r'^querybuygoodlist', views.Query_buy_good_list, name='querybuygoodlist'),

    url(r'^alterquantity', views.Alter_quantity, name='querybuygoodlist'),

    url(r'^alterbuygood', views.Alter_buy_good, name='alterbuygood'),

    url(r'^alterpostage', views.Alter_postage, name='alterpostage'),

    url(r'^deletebuygood', views.Delete_buy_good, name='deletebuygood'),
    url(r'^altercost', views.Alter_cost, name='altercost'),

    url(r'^deletebuylist', views.Delete_buy_list, name='deletebuylist'),

    url(r'^getprofit', views.Get_profit, name='getprofit'),

    url(r'^dimqueryclient', views.DimQuery_client, name='dimqueryclient'),
    url(r'^dimquery_good', views.DimQuery_good, name='dimquery_good'),

    url(r'^getopenid', views.Get_openid, name='getopenid'),



]