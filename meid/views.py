

from django.shortcuts import render
from django.http import HttpResponse
from meid import models
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from untils.response_code import RET,error_map
from rest_framework.views import APIView
from rest_framework.response import Response
from untils.serializers import *





def login(request):
    return  render(request,'admin/login.html')

# def addsadmin(request):
#     pwd = make_password('123')
#     one_sadmin = models.Sadmin(username='haha',password=pwd,is_admin=1)
#     one_sadmin.save()
#     return HttpResponse('ok')

import json
class SubLogin(View):
    def post(self,request):
        mes = {}
        #如果使用的是 vue 那么用body 或者data 取值
        # data = json.loads(request.body.decode())
        # print(11111111111111111111111111111111111111)
        # print(data)
        # return HttpResponse('ok')
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        print(11111111111111111111111111111111111111)
        print(name,pwd)
        if not all([name,pwd]):
            mes['code'] = RET.DATAERR
            mes['message'] = error_map[RET.DATAERR]
        one_user = models.Sadmin.objects.filter(username=name).first()
        if one_user:
            if check_password(pwd,one_user.password):
                # 登录成功
                request.session['one_user_id'] = one_user.id
                mes['code'] = RET.OK
                mes['message'] =error_map[RET.OK]
            else:
                mes['code'] = RET.PWDERR
                mes['message'] = error_map[RET.PWDERR]
        else:
            mes['code'] = RET.USERERR
            mes['message'] = error_map[RET.USERERR ]
        print(mes)
        return HttpResponse(json.dumps(mes))


def index(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        one_user = models.Sadmin.objects.filter(id=admin_id).first()
    return render(request,'admin/index.html',locals())



from django.core.paginator import Paginator
#查出分类表中数据  在untils文件夹中创建序列化配置文件
class CateList(APIView):
    def get(self,request):
        try:
            p = request.GET.get('p')
        except:
            p = 1
        cate = models.Cate.objects.all()
        #将数据实例化paginator 规定每页1条数据
        page = Paginator(cate,2)
        #获取当前页的数据
        catelist =page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        currentPage = p
        #将查出来的数据进行序列化
        catelist = CateModelSerializers(catelist,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['catelist'] = catelist.data
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        return Response(mes)

#展示分类页面
def showcate(request):
    return render(request, 'admin/showcate.html')


#添加分类数据
def addcate(request):
    #获取所有的分类顶级数据
    newid = request.GET.get('newid')
    cates = models.Cate.objects.filter(pid=0).all()
    return render(request,'admin/add_cate.html',locals())

import os
from meiduo.settings import UPLOAD_FILE
# from datetime import datetime
#上传图片的方法
def image(pic):
    if pic:
        pic_url = os.path.join(UPLOAD_FILE,pic.name)
        # time = datetime.strftime('%Y%m%D%H%M%S')
        # print(time)
        with open(pic_url,'wb') as f:
            for chunk in pic.chunks():
                f.write(chunk)
        return 'http://127.0.0.1:8000/static/upload/'+pic.name
    else:
        return ''

#添加分类的接口
class Submit_addcate(APIView):
    def post(self,request):
        data = request.data
        # 上传图图片
        pic = request.FILES.get('pic')
        # 将图片的路径实例化
        path = image(pic)
        data['pic'] = path
        try:
            pid = int(data['pid'])
        except:
            pid=0
        if pid==0:
            type = 1
            top_id = 0
        else:
            cates = models.Cate.objects.get(id=pid)
            type = cates.type+1
            if cates.top_id==0:
                top_id = cates.id
            else:
                top_id = cates.top_id
        data['type'] = type
        data['top_id'] = top_id
        try:
            newid = int(data['newid'])
        except:
            newid = 0
        if newid > 0:
            #修改
            new_cate = models.Cate.objects.get(id=newid)
            cate = CateSerializer(new_cate,data=data)
        else:
            cate = CateSerializer(data=data)
        mes={}
        if cate.is_valid():
            try:
                cate.save()
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)

# 删除分类数据
def deletecate(request):
    delid = request.GET.get('delid')
    one_cate = models.Cate.objects.get(id=delid)
    one_cate.delete()
    return render(request, 'admin/shownews1.html')

#添加新闻
def addnews(request):
    newid = request.GET.get('newid')
    return render(request, 'admin/addnews.html',locals())
# 添加新闻接口
class Submit_addnews(APIView):
    def post(self,request):
        data = request.data.copy()
        print(data)
        pic = request.FILES.get('pic')
        path = image(pic)
        data['pic'] = path
        try:
            newid = int(data['newid'])
        except:
            newid=0
        if newid>0:
            nn = models.News.objects.get(id=newid)
            news = NewsSerializer(nn,data=data)
        else:
            news = NewsSerializer(data = data)
        mes = {}
        if news.is_valid():
            try:
             news.save()
             mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR

        return Response(mes)
#富文本框里面上传图片
def upload_image(request):
    pic = request.FILES.get('file')
    mes = {}
    mes['path'] =  image(pic)
    mes['error'] = False
    return HttpResponse(json.dumps(mes,ensure_ascii=False))

# 展示新闻
def show_news(request):
    return render(request,'admin/shownews1.html')
# 展示新闻接口
class NewsList(APIView):
    def get(self,request):
        news = models.News.objects.all()
        try:
            p = request.GET.get('p')
        except:
            p =1
        currentPage = p
        page = Paginator(news,2)
        newslist1 = page.get_page(p)
        newslist = NewsModelSerializers(newslist1,many=True)
        totalPage = page.num_pages
        mes = {}
        mes['code'] = RET.OK
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        mes['newslist'] = newslist.data
        return Response(mes)
#删除新闻
def deletenews(request):
    delid = request.GET.get('delid')
    one_news = models.News.objects.get(id = delid)
    one_news.delete()
    return render(request,'admin/shownews1.html')


# 展示商品
def showgood(request):
    return render(request,'admin/showgood.html')
#展示商品接口
class  GoodList(APIView):
    def get(self,request):
        try:
            p = request.GET.get('p')
        except:
            p =1
        goods = models.Goods.objects.all()
        page = Paginator(goods,2)
        good = page.get_page(p)
        currentPage=p
        totalPage = page.num_pages
        go = GoodsModelSerializers(good,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['goodlist'] =go.data
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        return Response(mes)

def addgood(request):
    cates = models.Cate.objects.filter(type=2).all()
    newid = request.GET.get('newid')
    return render(request,'admin/add_good.html',locals())


#添加商品关联标签接口
class GettagList(APIView):
    def post(self,request):
        cid_id = request.POST.get('cid_id')
        one_cate = models.Cate.objects.get(id=cid_id)
        tags = models.Tags.objects.filter(cid=one_cate.top_id).all()
        tagslist = TagsModelserializer(tags,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['taglist'] = tagslist.data
        return Response(mes)


#添加商品接口
class Submit_addgood(APIView):
    def post(self,request):
        data = request.data
        pic = request.FILES.get('pic')
        path = image(pic)
        data['pic'] = path
        data['t_comment']=0
        data['lock_store']=0
        mes={}
        try:
            cid_id = int(data['cid_id'])
            one_cate = models.Cate.objects.get(id=cid_id)
            data['top_id']=one_cate.top_id
            try:
                newid = int(data['newid'])
            except:
                newid = 0
            if newid>0:
                gg = models.Goods.objects.get(id=newid)
                goods = GoodSerializer(gg,data=data)
            else:
                goods = GoodSerializer(data=data)
            if goods.is_valid():
                try:
                    goods.save()
                    mes['code'] = RET.OK
                except:
                    mes['code'] = RET.DATAERR
        except:
            mes['code'] = RET.DATAERR
        return Response(mes)

#标签表展示
def showtags(request):
    return render(request,'admin/showtags.html')
# 展示标签表接口
class TagsList(APIView):
    def get(self,request):
        tags = models.Tags.objects.all()
        try:
            p = request.GET.get('p')
        except:
            p=1
        #实例化tags分页对象
        page = Paginator(tags,3)
        # 获取总页数
        totalPage = page.num_pages
        # 获取当前页数据
        tagslist1 = page.get_page(p)
        # 获取当前页
        currentPage = p
        # 序列化 当前页面的数据
        tagslist = TagsModelserializer(tagslist1,many=True)
        mes= {}
        mes['code'] = RET.OK
        mes['totalPage'] = totalPage
        mes['currentPage'] = currentPage
        mes['tagslist'] = tagslist.data
        return Response(mes)

# 添加标签
def addtags(request):
    cates = models.Cate.objects.all()
    newid = request.GET.get('newid')
    return render(request,'admin/add_tags.html',locals())
# 添加标签接口
class Submit_addtags(APIView):
    def post(self,request):
        data = request.data
        try:
            newid = int(data['newid'])
        except:
            newid =0
        if newid>0:
            #修改数据查询
            one_tags = models.Tags.objects.get(id=newid)
            tags = TagsSerializer(one_tags,data=data)
        else:
            tags = TagsSerializer(data=data)
        mes = {}
        if tags.is_valid():
            try:
                tags.save()
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)
#删除焦点
def deletetags(request):
    delid = request.GET.get('delid')
    one_tags = models.Tags.objects.get(id=delid)
    one_tags.delete()
    return render(request,'admin/showtags.html')

#焦点图展示
def showbanner(request):
    return render(request,'admin/showbanner.html',locals())
#焦点图展示接口
class BannerList(APIView):
    def get(self,request):
        try:
            p = request.GET.get('p')
        except:
            p=1
        banners = models.Banner.objects.all()
        page = Paginator(banners,1)
        # 获取总页数
        totalPage = page.num_pages
        # 获取当前页数
        currentPage = p
        # 获取当前页数据
        banner = page.get_page(p)
        bannerlist = BannerModelserializer(banner,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        mes['bannerlist'] = bannerlist.data
        return Response(mes)

#添加焦点图
def addbanner(request):
    cates = models.Cate.objects.all()
    newid = request.GET.get('newid')
    return render(request,'admin/add_banner.html',locals())
# 添加焦点图 接口
class Submit_addbanner(APIView):
    def post(self,request):
        data = request.data
        pic = request.FILES.get('pic')
        path = image(pic)
        data['pic'] = path
        try:
            newid = int(data['newid'])
        except:
            newid =0
        if newid>0:
            # 修改
            bb = models.Banner.objects.get(id=newid)
            banner = BannerSerializer(bb,data=data)
        else:
            banner = BannerSerializer(data=data)
        mes = {}
        if banner.is_valid():
            try:
                banner.save()
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)

# 删除焦点图
def deletebanner(request):
    delid = request.GET.get('delid')
    one_ban = models.Banner.objects.get(id=delid)
    one_ban.delete()
    return render(request,'admin/showbanner.html')


# 权限管理
#显示资源
def show_resource(request):
    return render(request,'admin/showresource.html')
#显示资源接口
class Resourcelist(APIView):
    def get(self,request):
        resourcelist1 = models.Resource.objects.all()
        try:
            p = request.GET.get('p')
        except:
            p = 1
        page = Paginator(resourcelist1,2)
        currentPage = p
        rr = page.get_page(p)
        resourcelist = ResourceModelserializer(rr,many=True)
        totalPage = page.num_pages
        mes ={}
        mes['code'] = RET.OK
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        mes['resourcelist'] =resourcelist.data
        return Response(mes)


# 添加资源
def addresource(request):
    newid = request.GET.get('newid')
    return render(request,'admin/addresource.html',locals())
#添加资源接口
class Submit_addresource(APIView):
    def post(self,request):
        data = request.data
        try:
            newid = int(data['newid'])
        except:
            newid = 0
        if newid>0:
            rr = models.Resource.objects.get(id=newid)
            resource = ResourceModelserializer(rr,data=data)
        else:
            resource = ResourceSerializer(data=data)
        mes = {}
        if resource.is_valid():
            try:
                resource.save()
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)
#删除资源
def deleteres(request):
    delid = request.GET.get('delid')
    one_reso = models.Resource.objects.get(id=delid)
    one_reso.delete()
    return render(request,'admin/showresource.html')


#显示角色权限
def showrole(request):
    return render(request,'admin/showrole.html')

#删除角色权限
def deleterole(request):
    delid = request.GET.get('delid')
    print(1111111111111111111111111111111111)
    print(delid)
    one_role = models.Role.objects.get(id=delid)
    one_role.resource.clear()
    one_role.delete()
    return render(request,'admin/showrole.html')
#角色展示接口
class Rolelist(APIView):
    def get(self,request):
        roles = models.Role.objects.all()
        # list = []
        # for i in roles:
        #     rdict={}
        #     rdict['id'] = i.id
        #     rdict['name'] = i.name
        #     rdict['status'] = i.status
        #     one_role = models.Role.objects.get(id=i.id)
        #     resource = one_role.resource
        #     r = ResourceModelserializer(r,many=True)
        #     rdict['resourcelist'] = r.data
        #     list.append(rdict)

        try:
            p = request.GET.get('p')
        except:
            p = 1
        page = Paginator(roles,2)
        ro = page.get_page(p)
        role = RoleModelserializer(ro,many=True)
        currentPage = p
        totalPage = page.num_pages

        mes = {}
        mes['code'] = RET.OK
        mes['rolelist'] = role.data
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        return Response(mes)
# 添加角色数据
def addrole(request):
    reslist = models.Resource.objects.all()
    return render(request,'admin/addrole.html',locals())
#添加角色接口
class Submit_addrole(APIView):
    def post(self,request):
        data  = request.data
        names = request.POST.getlist('a')
        roles = RoleSerializer(data=data)
        mes={}
        if roles.is_valid():
            try:
                roles.save()
                role = models.Role.objects.filter(name=data['name']).first()
                resource = models.Resource.objects.filter(name__in=names).all()
                role.resource.add(*resource)
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)

#显示用户
def showuserinfo(request):
    return render(request,'admin/showuserinfo.html')
#添加用户
def adduserinfo(request):
    roles = models.Role.objects.all()
    return render(request,'admin/adduserinfo.html',locals())
#用户数据序列化
class Userinfolist(APIView):
    def get(self,request):
        userinfolist = models.UserInfo.objects.all()
        u = UserinfolstSerializer(userinfolist,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['userinfolist'] = u.data
        return Response(mes)

#添加用户接口
class Submit_adduserinfo(APIView):
    def post(self,request):
        data = request.data.copy()
        pwd = make_password(data['passwd'] )
        data['passwd'] = pwd
        userinfo = UserinfoSerializer(data=data)
        mes = {}
        if userinfo.is_valid():
            try:
                userinfo.save()
                mes['code'] = RET.OK
            except:
                mes['code'] =RET.DATAERR
        else:
            mes['code'] = RET.DATAERR
        return Response(mes)








from dwebsocket.decorators import accept_websocket

#创建一个连接池
conn = {}

@accept_websocket
def finish_order(request,name):
    if request.is_websocket:
        #如果有连接的话 就将这个连接保存进连接池
        conn[name] = request.websocket
    # 检测连接是否在  必须写
    for message in request.websocket:
        pass


def send(request):
    #支付宝已经支付成功，回调接口
    # 给商户 发送提醒
    name = 'zs'
    mes =json.dumps({'title':'您有新的订单生成'},ensure_ascii=False).encode('utf-8')
    conn[name].send(mes)
    return HttpResponse('ok')





