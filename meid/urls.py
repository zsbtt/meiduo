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

from django.urls import path
from meid import views

urlpatterns = [
    path('login/', views.login),
    path('', views.index),
    path('deletecate/', views.deletecate),
    path('deletebanner/', views.deletebanner),
    path('deletenews/', views.deletenews),
    path('deleteres/', views.deleteres),
    path('deleterole/', views.deleterole),

    path('addcate/', views.addcate),
    path('addtags/', views.addtags),
    path('upload_image/', views.upload_image),
    path('addgood/', views.addgood),
    path('addrole/', views.addrole),
    path('addresource/', views.addresource),
    path('addnews/', views.addnews),
    path('addbanner/', views.addbanner),
    path('adduserinfo/', views.adduserinfo),

    path('show_news/', views.show_news),
    path('showgood/', views.showgood),
    path('showtags/', views.showtags),
    path('showcate/', views.showcate),
    path('showrole/', views.showrole),
    path('showbanner/', views.showbanner),
    path('showresource/', views.show_resource),
    path('showuserinfo/', views.showuserinfo),
    # path('addsadmin/', views.addsadmin),

    path('sublogin/', views.SubLogin.as_view()),
    path('submit_addcate/', views.Submit_addcate.as_view()),
    path('submit_addnews/', views.Submit_addnews.as_view()),
    path('submit_addgood/', views.Submit_addgood.as_view()),
    path('submit_addtags/', views.Submit_addtags.as_view()),
    path('submit_addbanner/', views.Submit_addbanner.as_view()),
    path('submit_addresource/', views.Submit_addresource.as_view()),
    path('submit_addrole/', views.Submit_addrole.as_view()),
    path('submit_adduserinfo/', views.Submit_adduserinfo.as_view()),

    path('bannerlist/', views.BannerList.as_view()),
    path('catelist/', views.CateList.as_view()),
    path('tagslist/', views.TagsList.as_view()),
    path('gettaglist/', views.GettagList.as_view()),
    path('newslist/', views.NewsList.as_view()),
    path('resourcelist/', views.Resourcelist.as_view()),
    path('goodlist/', views.GoodList.as_view()),
    path('rolelist/', views.Rolelist.as_view()),
    path('userinfolist/', views.Userinfolist.as_view()),


    path('finish_order/<name>', views.finish_order),
    path('send/', views.send),


]