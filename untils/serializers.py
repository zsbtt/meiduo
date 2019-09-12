from rest_framework import serializers
from meid import models

class CateModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Cate
        fields = '__all__'

# 添加分类反序列化类
class CateSerializer(serializers.Serializer):
    name = serializers.CharField()  # 分类的名称
    pid = serializers.IntegerField()  # 上级分类
    type = serializers.IntegerField()  # 分类的级别
    pic = serializers.CharField(default='')
    top_id = serializers.IntegerField()  # 顶级分类，当前分类 所属的类
    is_recommend = serializers.IntegerField()  # 是否推荐首页显示 ，1显示，0 不显示
    #添加数据
    def create(self, data):
        cate = models.Cate.objects.create(**data)
        return cate
    #更新数据
    def update(self,instance,data):
        instance.name = data.get('name')
        instance.pid = data.get('pid')
        instance.type = data.get('type')
        instance.top_id = data.get('top_id')
        instance.pic = data.get('pic')
        instance.is_recommend = data.get('is_recommend')
        instance.save()
        return instance


#添加新闻反序列化
class NewsSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField(default='')
    is_recommend = serializers.IntegerField()
    # 添加数据
    def create(self,data):
        news = models.News.objects.create(**data)
        return news
    def update(self, instance, data):
        instance.title = data.get('title')
        instance.content = data.get('content')
        instance.is_recommend = data.get('is_recommend')
        instance.save()
        return instance
# 新闻序列化
class NewsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'


# 添加商品反序列化
class GoodSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=7,decimal_places=2)
    store = serializers.IntegerField()  # 库存
    lock_store = serializers.IntegerField()  # 锁定库存
    pic = serializers.CharField()
    descrip = serializers.CharField()  # 描述
    t_comment = serializers.IntegerField()  # 总评价数
    cid_id = serializers.IntegerField()  # 关联分类外键
    tagid_id = serializers.IntegerField()  # 关联标签外键
    top_id = serializers.IntegerField()  # 顶级分类
    sales = serializers.IntegerField()
    def create(self,data):
        goods = models.Goods.objects.create(**data)
        return goods
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.price = data.get('price')
        instance.store = data.get('store')
        instance.lock_store = data.get('lock_store')
        instance.pic = data.get('pic')
        instance.descrip = data.get('descrip')
        instance.t_comment = data.get('t_comment')
        instance.cid_id = data.get('cid_id')
        instance.tagid_id = data.get('tagid_id')
        instance.top_id = data.get('top_id')
        instance.sales = data.get('sales')
        instance.save()
        return instance

#商品数据的序列化
class GoodsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = '__all__'

#标签的反序列化
class TagsSerializer(serializers.Serializer):
    name = serializers.CharField()  # 分类的名称
    cid_id = serializers.IntegerField(default=1)  # 上级分类
    is_recommend = serializers.IntegerField()
    def create(self, data):
        tags = models.Tags.objects.create(**data)
        return tags
    # 更新数据
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.cid_id = data.get('cid_id')
        instance.is_recommend = data.get('is_recommend')
        instance.save()
        return instance
# 标签数据序列化
class TagsModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = '__all__'


# 焦点图的反序列化
class BannerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pic = serializers.CharField()
    is_show = serializers.IntegerField()  # 是否显示 1显示 0不显示
    sort = serializers.IntegerField()  # 显示的顺序
    type = serializers.IntegerField()  # 1焦点图 2 广告图
    # 添加焦点图数据
    def create(self, data):
        banner = models.Banner.objects.create(**data)
        return banner
    # 更新焦点图数据
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.type = data.get('type')
        instance.sort = data.get('sort')
        instance.is_show = data.get('is_show')
        instance.save()
        return instance
# 序列化焦点图数据
class BannerModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = "__all__"



#权限管理
#资源表反序列化
class ResourceSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()  # 跳转到的网址
    satus = serializers.IntegerField(default=0)  # 是否可用 1 可用 0 不可用
    def create(self, data):
        resource = models.Resource.objects.create(**data)
        return resource
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.url = data.get('url')
        instance.satus = data.get('satus')
        instance.save()
        return instance

#序列化资源表
class ResourceModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = '__all__'

#角色反序列化数据
class RoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.IntegerField(default=0)  # 1启用 0停用
    def create(self, validated_data):
        return models.Role.objects.create(**validated_data)
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.status = data.get('status')
        instance.save()
        return instance
# 角色序列化数据
class RoleModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ('id','name','status','resource')
        depth = 1

#管理员反序列化
class UserinfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    passwd = serializers.CharField()
    role_id_id = serializers.IntegerField()  # 关联角色表外键
    is_admin = serializers.IntegerField()  # 是否是超级管理员 1是 0不是
    def create(self, data):
        userinfo = models.UserInfo.objects.create(**data)
        return userinfo

# 用户序列表
class UserinfolstSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'



# 购物车数据反序列化
class CartSerializer(serializers.Serializer):
    good_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    pic = serializers.CharField()
    goods_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    count = serializers.IntegerField()
    def create(self, data):
        cart = models.Cart.objects.create(**data)
        return cart
    def update(self, instance, data):
        instance.count = data.get('count')
        instance.good_id = data.get('good_id')
        instance.user_id = data.get('user_id')
        instance.pic = data.get('pic')
        instance.goods_name = data.get('goods_name')
        instance.price = data.get('price')
        instance.save()
        return instance
# 购物车序列化
class CartlstModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


#城镇表的序列化
class CityModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


#地址数据的序列化
class AdressModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adress
        fields = '__all__'
#地址数据的反序列化
class Adressserializer(serializers.Serializer):
    receiver = serializers.CharField()  # 关联用户
    province = serializers.CharField()  # 城市
    city = serializers.CharField()  # 乡镇
    district = serializers.CharField()  # 区
    place = serializers.CharField()  # 详细地址
    mobile = serializers.CharField()  # 手机号
    tel = serializers.CharField()  # 固定电话
    email = serializers.CharField()  # 电子邮箱
    is_mo = serializers.IntegerField()  # 0不是默认地址  1 是默认地址
    is_se = serializers.IntegerField()  # 0 不是确认地址  1 是确认收货地址
    user_id = serializers.IntegerField()  # 关联用户id
    def create(self, data):
        adress = models.Adress.objects.create(**data)
        return adress
    def update(self, instance, data):
        instance.user_id = data.get('user_id')
        instance.receiver = data.get('receiver')
        instance.province = data.get('province')
        instance.city = data.get('city')
        instance.district = data.get('district')
        instance.place = data.get('place')
        instance.mobile = data.get('mobile')
        instance.tel = data.get('tel')
        instance.email = data.get('email')
        instance.is_mo = data.get('is_mo')
        instance.is_se = data.get('is_se')
        instance.save()
        return instance

#订单数据反序列化
class Orderserializer(serializers.Serializer):
    order_sn = serializers.CharField()  # 订单号
    user_id = serializers.IntegerField()  # 购买的用户
    address = serializers.CharField()  # 购买地址
    tmony = serializers.DecimalField(max_digits=10,decimal_places=2)
    pay_type = serializers.IntegerField()  # 1货到付款 2支付宝  3微信  4 银行卡
    status = serializers.IntegerField()  # 状态 0未支付 1未评价 2 支付失败  3 已评价
    adress_id = serializers.IntegerField()  # 关联地址
    code = serializers.CharField()  # 流水号
    def create(self, data):
        order = models.Order.objects.create(**data)
        return order

#订单详情页序列化
class OrderdetailModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = '__all__'

#评价反序列化
class Commentserializer(serializers.Serializer):
    good_id = serializers.IntegerField()  # 和商品ID相关联的id
    user_id = serializers.IntegerField()  # 和用户关联的id
    content = serializers.CharField()
    store = serializers.IntegerField()  # 评论分数
    def create(self, data):
        comment = models.Comment.objects.create(**data)
        return comment