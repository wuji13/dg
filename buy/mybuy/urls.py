from django.conf.urls import url
from . import views,tests,good,dgs,clients

urlpatterns = [
    url(r'^test', tests.Test, name='test'),

    url(r'^createuser',views.Create_user,name='create_user'),
    url(r'^addclient',views.Add_client,name='add_client'),
    url(r'^deleteclient',views.Delete_client,name='delete_client'),
    url(r'^queryclient',views.Query_client,name='query_client'),
    url(r'^getrate',views.Get_rate,name='get_rate'),
    url(r'^uptoken',views.Uptoken,name='uptoken'),
    url(r'^addgood',good.Add_good,name='addgood'),
    url(r'^deletegood',good.Delete_good,name='deletegood'),
    url(r'^querygood',views.Query_good,name='querygood'),
    url(r'^selectgood',good.Select_good,name='selectgood'),

    url(r'^adddg',dgs.Add_dg,name='adddg'),
    url(r'^querydg',dgs.Query_dg,name='querydg'),

    url(r'^addlist', dgs.Add_dglist, name='adddglist'),
    url(r'^savepay', dgs.Save_pay, name='savepay'),
    url(r'^querydglist', dgs.Query_buylist, name='querydglist'),

    url(r'^adggood', dgs.Add_dggood, name='adggood'),
    url(r'^ddggood', dgs.Delete_dg_good, name='ddggood'),

    url(r'^querybuyclient', dgs.Query_buy_client, name='querybuyclient'),

    url(r'^querybuylist', dgs.Query_buy_list, name='querybuylist'),

    url(r'^querybuygoodlist', views.Query_buy_good_list, name='querybuygoodlist'),

    url(r'^alterquantity', views.Alter_quantity, name='querybuygoodlist'),

    url(r'^alterbuygood', dgs.Alter_buy_good, name='alterbuygood'),

    url(r'^alterpostage', dgs.Alter_postage, name='alterpostage'),



    url(r'^altercost', dgs.Alter_cost, name='altercost'),

    url(r'^deletebuylist', dgs.Delete_buy_list, name='deletebuylist'),

    url(r'^getprofit', views.Get_profit, name='getprofit'),

    url(r'^dimqueryclient', views.DimQuery_client, name='dimqueryclient'),
    url(r'^dimquery_good', views.DimQuery_good, name='dimquery_good'),

    url(r'^getopenid', views.Get_openid, name='getopenid'),

    url(r'^querycldetail', views.Query_client_detail, name='querycldetail'),

    url(r'^addcategory', good.Add_category, name='addcategory'),
    url(r'^querycategory', good.Query_category, name='querycategory'),

    url(r'^querycggood', good.Query_category_good, name='querycategorygood'),

    url(r'^qgooddetail', good.Query_good_detail, name='qgooddetail'),

    url(r'^qsite', clients.Query_site, name='qsite'),
    url(r'^asite', clients.Add_site, name='asite'),

    url(r'^fdgsite', dgs.Fix_dgsite, name='fdgsite'),

    url(r'^qspecification', dgs.Query_good_specification, name='qspecification'),

    url(r'^getinform', clients.Get_inform, name='getinform'),
    url(r'^alterremark', good.Alter_remark, name='alterremark'),


]