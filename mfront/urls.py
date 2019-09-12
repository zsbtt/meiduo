"""meiduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path
from mfront import views
from rest_framework_jwt.views import obtain_jwt_token
from mfront import pay


app_name = 'mfront'
urlpatterns = [
    path('getcategoods/', views.getCateGoods.as_view()),
    path('getgoodlist/', views.GetGoodlist.as_view()),
    path('getcateslist/', views.Getcateslist.as_view()),
    path('getbannerlist/', views.GetBannerlist.as_view()),
    path('getnewslist/', views.GetNewslist.as_view()),
    path('getcartlist/', views.GetCartlist.as_view()),
    path('cartlist/', views.Cartlist.as_view()),
    path('getgoods/', views.GetGoods.as_view()),
    path('getorderlists/', views.Getorderlists.as_view()),
    path('regoodlist/', views.GetRegoodlist.as_view()),
    path('getcitylist/<id>/', views.GetCitylist.as_view()),

    path('addadress/', views.Addadress.as_view()),
    path('addping/', views.Addping.as_view()),
    path('addresses1/', views.Addresses1.as_view()),
    path('addresses2/', views.Addresses2.as_view()),
    path('alladdress/', views.Alladdress.as_view()),
    path('deleteaddress/', views.Deleteaddress.as_view()),

    path('addcount/', views.Addcount.as_view()),
    path('addorder/', views.Addorder.as_view()),
    path('createorder/', views.Createorder.as_view()),
    path('page1/', pay.page1),
    #注册接口
    path('register/', views.Register.as_view()),
    path('addcart/', views.AddCart.as_view()),
    path('valid_email/', views.Valid_email),
    #注册接口
    # path('login/', views.LoginApiviews.as_view()),
    # 验证码生成
    path('getimgcapcth/', views.GetimgCapcth),
    path('logout/', views.logout),
    re_path(r'login/', obtain_jwt_token, name='login'),


]