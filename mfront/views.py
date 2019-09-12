from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from untils.response_code import RET,error_map
from untils.serializers import *
import re
from django.contrib.auth.hashers import make_password,check_password
from untils.captcha.captcha import captcha
from django.http import HttpResponse
from django.core.mail import EmailMessage
from meiduo import settings
from django.db import  transaction


class getCateGoods(APIView):
    def get(self,request):
        #获取所有的一级分类
        cates = models.Cate.objects.filter(pid=0).all()
        catelist = []
        print(11111111111111111111111111111111111111)
        for i in cates:
            cdict = {}
            cdict['id'] = i.id
            cdict['name'] = i.name
            cdict['pic'] = i.pic
            #获取二级分类
            cate2 = models.Cate.objects.filter(pid=i.id).all()
            c2 = CateModelSerializers(cate2,many=True)
            cdict['erji'] = c2.data
            #获取一级分类下的标签
            tags = models.Tags.objects.filter(cid=i.id).all()
            ta = TagsModelserializer(tags,many=True)
            cdict['tags'] = ta.data
            #获取一级分类下的商品

            goods = models.Goods.objects.filter(top_id=i.id).all()
            go = GoodsModelSerializers(goods,many=True)
            cdict['goodlist'] = go.data
            catelist.append(cdict)
        mes={}
        mes['code'] = RET.OK
        mes['catelist'] = catelist
        return Response(mes)

# 点击标签时 商品的变化
class GetGoodlist(APIView):
    def get(self,request):
        tid = request.GET.get('tid')
        print(11111111111111111111111111)
        print(tid)
        cid = request.GET.get('cid')
        goodlist = models.Goods.objects.filter(top_id=cid,tagid=tid).all()
        go = GoodsModelSerializers(goodlist,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['goodlist'] = go.data
        return Response(mes)

#获取一级分类接口
class Getcateslist(APIView):
    def get(self,request):
        cate1 = models.Cate.objects.filter(pid=0).all()
        c = CateModelSerializers(cate1,many=True)
        # news = models.Banner.objects.all()
        # n = NewsModelSerializers(news, many=True)
        # banner = models.Banner.objects.all()
        # b = BannerModelserializer(banner,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['cateslist'] = c.data
        # mes['bannerlist']=b.data
        # mes['newslist'] = n.data
        return Response(mes)
# 获取焦点图接口
class GetBannerlist(APIView):
    def get(self,request):
        banner = models.Banner.objects.all()
        b = BannerModelserializer(banner,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['bannerlist'] = b.data
        return Response(mes)

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 获取新闻的接口
class GetNewslist(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request):
        news = models.News.objects.all()[0:4]
        n = NewsModelSerializers(news,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['newslist'] = n.data
        return Response(mes)




# 获取详情页goods接口
class GetGoods(APIView):
    def get(self,request):
        gid = request.GET.get('gid')
        one_goods = models.Goods.objects.get(id=gid)
        g = GoodsModelSerializers(one_goods)
        mes={}
        mes['code'] = RET.OK
        mes['goods'] = g.data
        return Response(mes)
#获取热销排行接口
class GetRegoodlist(APIView):
    def get(self,request):
        regoodlist = models.Goods.objects.all().order_by('-sales')[:2]
        rr = GoodsModelSerializers(regoodlist,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['regoodlist'] = rr.data
        return Response(mes)




import os
from meiduo.settings import UPLOAD_FILE
def upload_img(img):
    if img:
        img_url = os.path.join(UPLOAD_FILE,img.name)
        with open(img_url,'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        return 'http://127.0.0.1:8000/'+img.name
    else:
        return ''

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
#反序列化user表数据
class Userseralizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.CharField() # 0未验证  1验证  2验证失败
    token = serializers.CharField()
    def create(self, data):
        data['password'] = make_password(data['password'])
        user=models.User.objects.create(**data)
        return user


import uuid
#注册接口
class Register(APIView):
    def post(self,request):
        mes = {}
        #获取用户输入
        data = request.data.copy()
        username = data['username']
        password = data['password']
        pwd2 = data['pwd2']
        email = data['email']
        sms_code = data['sms_code']
        allow = data['allow']
        mobile = data['mobile']
        #判断输入的数据是否完整
        if not all([username,password,pwd2,email,sms_code,mobile]):
            mes['code'] = RET.DATAERR
            mes['mess'] = '参数不完整'
        # 验证码是否一致
        text = (request.session.get('text')).lower()
        print(data['sms_code'])
        if data['sms_code'] != text:
            mes['code'] = RET.DATAERR
            mes['mess'] = '验证码输入不正确，请重新输入'
        if len(data['password'])<8 or len(data['password'])>20:
            mes['code'] = RET.PARAMERR
            mes['mess'] = '密码的长度至少要8位'
        if data['password'] != data['pwd2'] :
            mes['code'] = RET.PARAMERR
            mes['mess'] = '两次输入的密码不一致'
        if not re.match(r'[0-9a-zA-Z]+@qq.com',data['email']):
            mes['code'] = RET.DATAERR
            mes['mess'] = '邮箱请使用qq邮箱'
        if not data['allow']:
            mes['code'] = RET.DATAERR
            mes['mess'] = '请勾选同意'
        #生成token串
        token = str(uuid.uuid1())
        data['token'] = token
        one_user = Userseralizer(data=data)
        if one_user.is_valid():
            #加入数据库
            try:
                one_user.save()
                #发送邮件
                title = '欢迎注册本网站'
                hrefs = "点击此链接<a href='http://localhost:8000/valid_email?code="+token+"'>点此</a>链接进行用户激活"
                set_email = settings.DEFAULT_FROM_EMAIL
                # 发送给哪个邮箱
                send_email = [data['email']]
                send_m = EmailMessage(title,hrefs,set_email,send_email)
                send_m.content_subtype = 'html'
                send_m.send()
                mes['code'] = RET.OK
                mes['mess']='注册成功'
            except:
                mes['code'] = RET.DATAERR
                mes['mess'] = '添加数据库失败'
        else:
            mes['code'] = RET.DATAERR
            mes['mess'] = '添加数据库失败'
        return Response(mes)

#激活验证码接口
def Valid_email(request):
    token = request.GET.get('code')
    one_user = models.User.objects.filter(token=token).first()
    one_user.is_active = 1
    one_user.save()
    return redirect(reversed('mfront:login'))



#验证码接口
def  GetimgCapcth(request):
    name,text,image = captcha.generate_captcha()
    request.session['text'] = text
    return HttpResponse(image,'image/jpg')

#验证登录接口
# class LoginApiviews(APIView):
#     def post(self,request):
#         mes ={}
#         data=request.data
#         username = data['username']
#         password = data['password']
#         remember = data['remember']
#         if not all([username,password,remember]):
#             mes['code'] = RET.OK
#             mes['mess'] = '参数不全的哟'
#         user = models.User.objects.filter(username=username).first()
#         if not check_password(password,user.password):
#             mes['code'] = RET.DATAERR
#             mes['mess'] ='密码不正确'
#         #生成能token值
#         user.set_password(data.get('password'))
#         user.save()
#         # 补充生成记录登录状态的token
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         user.token = token
#         return Response(mes)



#退出接口
def logout(request):
    username = request.GET.get('username')
    request.session.pop(username)
    return redirect(reversed('mfront:login'))


#添加商品接口
class AddCart(APIView):
    def post(self,request):
        mes={}
        data = request.data.copy()
        good_id = data['good_id']
        user_id = data['user_id']
        #根据传过来的id 判断是否有这个购物车数据
        carts = models.Cart.objects.filter(user_id=int(user_id),good_id=int(good_id)).first()
        #有的话就 增加 count
        if carts:
            carts.count = int(data['count'])+carts.count
            carts.save()
            mes['code'] = RET.OK
        else:
            one_good = models.Goods.objects.get(id=good_id)
            data['goods_name'] = one_good.name
            data['price'] = one_good.price
            data['pic'] = one_good.pic
            carts = CartSerializer(data=data)
            if carts.is_valid():
                carts.save()
                mes['code'] = RET.OK
            else:
                mes['code'] = RET.DATAERR
        return Response(mes)

#获取购物车表的数据
class GetCartlist(APIView):
    def get(self,request):
        user_id = request.GET.get('user_id')
        carts = models.Cart.objects.filter(user_id=user_id).all()
        # 将购物车中的数据序列化
        cart = CartlstModelSerializer(carts,many=True)
        mes={}
        mes['code'] = RET.OK
        mes['cart'] = cart.data
        return Response(mes)


#购物车 加减数据时 count变化
class Addcount(APIView):
    def get(self,request):
        mes = {}
        try:
            id = request.GET.get('id')
            count = request.GET.get('count')
            cart = models.Cart.objects.get(id=id)
            one_good = models.Goods.objects.get(id=cart.good_id)
            if count<one_good.lock_store:
                cart.count = count
                cart.save()
                mes['code'] = 200
            else:
                mes['code'] = 809
                mes['message']='库存不足，不能再添加了'
        except:
            mes['code'] = 608
        return Response(mes)

#去结算调用这个接口
class Addorder(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        mes = {}
        # 获取数据
        data = request.data.copy()
        ids =data['ids'].split(',')
        user_id = request.POST.get('user_id')
        print(222222222222222222)
        print(user_id,ids)
        try:
            #根据得到的ids 将状态全部修改为 未加入订单状态
            cart = models.Cart.objects.filter(user_id=user_id).update(is_checked=0)
        except:
            mes['code'] = 606
            mes['message'] = '更新数据失败1'
        try:
            # 查询数据库
            carts = models.Cart.objects.filter(user_id=user_id,id__in=ids).update(is_checked=1)
            sss = models.Cart.objects.filter(is_checked=1).first()
            print(sss)

            mes['code'] = 200
            mes['message'] = '更新状态成功'
        except:
            mes['code'] = 607
            mes['message'] = '更新数据失败222'

        return Response(mes)


#获取is_checked 为1 的所有商品
class Cartlist(APIView):
    def get(self,request):
        cart = models.Cart.objects.filter(is_checked=1).all()
        cc = CartlstModelSerializer(cart,many=True)
        mes={}
        mes['code'] = 200
        mes['cartlist'] = cc.data
        mes['freight'] = 0
        return Response(mes)


import uuid
#点击提交订单 的时候调用这个接口 生成订单保存入库
class Createorder(APIView):
    # 加入事务的时候要用装饰器
    @transaction.atomic
    def post(self,request):
        mes = {}
        data = request.data.copy()
        user_id = data['user_id']
        pay_type = data['pay_type']
        sid1 = transaction.savepoint()
        #生成订单
        address = models.Adress.objects.filter(is_se=1).first()
        adress = models.Adress.objects.filter(is_mo=1).first()
        user = models.User.objects.get(id=user_id)
        order_sn = str(uuid.uuid1())
        order = models.Order(order_sn=order_sn,user=user,adress=adress,address=address.receiver,tmony=0,pay_type=pay_type,status=0,code='aa')
        order.save()

        #查出要进行交易的cart数据
        cart = models.Cart.objects.filter(user_id=user_id,is_checked=1).all()
        # 判断库存是否充足
        tmony = 0
        for i in cart:
            #根据购物车获取商品  得出库存
            one_goods = models.Goods.objects.filter(id=i.good_id).first()

            # 生成悲观锁
            # one_goods = models.Goods.objects.select_for_update().filter(id=i.good_id).first()

            # 商品详情页
            order_sn = order_sn
            good_id = i.good_id
            pic = one_goods.pic
            price = one_goods.price
            name = one_goods.name
            count = i.count
            user_id = user_id
            # 实例化订单详情
            order_detail = models.OrderDetail(order_sn=order, pic=pic, price=price, name=name, count=count,
                                              user_id=user_id, good_id_id=good_id)

            ###############乐观锁
            locks = one_goods.lock_store
            if i.count>one_goods.lock_store:
                transaction.savepoint_rollback(sid1)
                mes['code'] = 609
                mes['message'] = '抱歉，库存不足，不能购买'
            else:
                # 库存充足 就计算出总的价格
                tmony += i.count*i.price
                # 判断 库存是否有被篡改
                res = models.Goods.objects.filter(id=i.good_id,lock_store=locks).first()
                if res == 0:
                    transaction.savepoint_rollback(sid1)
                    mes['code'] = 809
                    mes['message'] = '订单失败'
                else:
                    #更新lock_store
                    one_goods.lock_store -=i.count
                    # 将订单详情页保存
                    order_detail.save()
                    print(order_detail)
                    one_goods.save()
                    i.delete()
        order.tmony = tmony
        order.save()
        transaction.savepoint_commit(sid1)
        mes['code'] = 200
        mes['message'] = '添加订单成功'

        return Response(mes)








#获取全国城市镇的数据接口
class GetCitylist(APIView):
    def get(self,request,id):
        try:
            pid = int(id)
        except:
            pid=1
        city = models.City.objects.filter(pid=pid).all()
        er_ji = models.City.objects.filter(type=2).all()
        san_ji = models.City.objects.filter(type=3).all()
        cc = CityModelserializer(city,many=True)
        er = CityModelserializer(er_ji,many=True)
        sa = CityModelserializer(san_ji,many=True)
        mes={}
        mes['code'] = 200
        mes['citylist'] = cc.data
        mes['er_ji'] = er.data
        mes['san_ji'] = sa.data
        return Response(mes)


#添加 地址的接口
class Addadress(APIView):
    def post(self,request):
        mes = {}
        data = request.data.copy()
        one_province = models.City.objects.get(id=int(data['province']))
        one_city = models.City.objects.get(id=int(data['city']))
        one_district = models.City.objects.get(id=int(data['district']))
        data['province'] = one_province.name
        data['city'] = one_city.name
        data['district'] = one_district.name
        data['is_mo'] = 0
        data['is_se'] = 0
        try:
            id = int(request.GET.get('id'))
        except:
            id=0
        if id>0:
            one_ad = models.Adress.objects.get(id=id)
            adress = Adressserializer(one_ad,data=data)
            mes['code'] = 200
            mes['message'] = '添加成功'
        else:
            adress = Adressserializer(data=data)
        if adress.is_valid():
            adress.save()
            mes['code'] = 200
            mes['message'] = '添加成功'
        else:
            mes['code'] = 606
            mes['message'] = '添加失败了'
        return Response(mes)
    def put(self,request):
        mes={}

        mes['code'] = 200
        return Response(mes)



#获取当前用户下的而所有地址 ..............address 页面
class Alladdress(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request):
        mes={}
        user_id = request.GET.get('user_id')
        addresses = models.Adress.objects.filter(user_id=user_id).all()
        aa = AdressModelserializer(addresses,many=True)
        mes['code'] = 200
        mes['addresses'] = aa.data
        return Response(mes)

#删除当前用户创建的地址接口
class Deleteaddress(APIView):
    def get(self,request):
        address_id = request.GET.get('address_id')
        one_address = models.Adress.objects.get(id=address_id)
        one_address.delete()
        mes={}
        mes['code'] = 200
        return Response(mes)

#获取用户选择的收货地址
class Addresses1(APIView):
    def get(self,request):
        user_id = request.GET.get('user_id')
        addresses = models.Adress.objects.filter(user_id=user_id,is_se=1).first()
        aa = AdressModelserializer(addresses)
        mes={}
        mes['code'] = 200
        mes['addresses'] = aa.data
        return Response(mes)


#设置默认地址接口
class Addresses2(APIView):
    def get(self,request):
        mes = {}
        user_id = int(request.GET.get('user_id'))
        add_id = int(request.GET.get('add_id'))
        one_adress = models.Adress.objects.get(user_id=user_id,id=add_id)
        on = models.Adress.objects.filter(user_id=user_id,is_mo=1).first()
        if on:
            on.is_mo = 0
            on.save()
            one_adress.is_mo=1
            one_adress.save()
            mes['code'] = 201
            mes['message'] = '更新成功'

        else:
            one_adress.is_mo = 1
            one_adress.save()
            mes['code'] = 200
            mes['message'] = '添加成功'

        return Response(mes)



from django.core.paginator import Paginator
# 获取全部订单的接口
class Getorderlists(APIView):

    permission_classes = [IsAuthenticated,]
    authentication_classes = [JSONWebTokenAuthentication,]

    def get(self,request):
        mes={}
        user_id = request.GET.get('user_id')
        orderlist = models.Order.objects.filter(user_id=user_id).all()
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        page = Paginator(orderlist,2)
        corder = page.get_page(p)
        currentPage = p
        totalPage = page.num_pages
        list=[]
        for o in corder:
            odict={}
            odict['tmony'] = o.tmony
            odict['pay_type'] = o.pay_type
            odict['order_sn'] = o.order_sn
            odict['status'] = o.status
            orderdetails = models.OrderDetail.objects.filter(order_sn=o).all()
            oor = OrderdetailModelserializer(orderdetails,many=True)
            odict['orderdetails'] = oor.data
            list.append(odict)
        mes['code'] = 200
        mes['orderlist'] = list
        mes['currentPage'] = currentPage
        mes['totalPage'] = totalPage
        return Response(mes)


class Addping(APIView):
    def post(self,request):
        mes={}
        data = request.data
        print(111111111111111111111111111)
        print(data)
        cc = Commentserializer(data=data)
        if cc.is_valid():
            cc.save()
            good_id = int(data['good_id'])
            one_good = models.Goods.objects.get(id=good_id)
            one_good.com_num +=1
            mes['code'] = 200
            mes['message'] = '评论成功了哟'
        else:
            mes['code'] = 609
            mes['message'] = '评论失败了哟'

        return Response(mes)



