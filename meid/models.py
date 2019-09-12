from django.db import models


class Base(object):
    creat_time = models.DateTimeField(auto_now_add=True) # 创建时的时间
    update_time = models.DateTimeField(auto_now=True)# 最新的更新的时间

    class Meta:
        abstract = True  #只作为一个基类表存在


#管理员表
class Sadmin(Base,models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.IntegerField(default=0) # 1 超级管理员

    class Meta:
        db_table = 'sadmin'

# 分类表 （多对多）
class Cate(Base,models.Model):
    name =  models.CharField(max_length=50,unique=True) #分类的名称
    pid = models.IntegerField(default=0) # 上级分类
    type = models.IntegerField(default=1) # 分类的级别
    pic = models.CharField(max_length=255,default='')
    top_id = models.IntegerField(default=0) #顶级分类，当前分类 所属的类
    is_recommend = models.IntegerField(default=1) # 是否推荐首页显示 ，1显示，0 不显示
    class Meta:
        db_table = 'cate'
#标签表
class Tags(Base,models.Model):
    name =  models.CharField(max_length=50,unique=True) #分类的名称
    cid = models.ForeignKey('Cate',to_field='id',on_delete=models.CASCADE) # 上级分类
    is_recommend = models.IntegerField(default=1) # 是否推荐首页显示 ，1显示，0 不显示
    class Meta:
        db_table = 'tags'
# 新闻快讯表
class News(Base,models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(default='')
    is_recommend = models.IntegerField(default=1)  # 是否推荐首页显示 ，1显示，0 不显示
    class Meta:
        db_table = "news"
#Banner表
class Banner(Base,models.Model):
    name = models.CharField(max_length=30,unique=True)
    pic = models.CharField(max_length=255, default='')
    is_show = models.IntegerField(default=1) # 是否显示 1显示 0不显示
    sort = models.IntegerField(default=1) # 显示的顺序
    type = models.IntegerField(default=1)# 1焦点图 2 广告图
    class Meta:
        db_table = "banner"
#商品表
class Goods(Base,models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=99999999.99)
    store = models.IntegerField(default=0)  #库存
    lock_store = models.IntegerField(default=0) #锁定库存
    pic = models.CharField(max_length=100)
    descrip = models.CharField(max_length=50) # 描述
    t_comment = models.IntegerField(default=0)  # 总评价数
    cid = models.ForeignKey('Cate', to_field='id', on_delete=models.CASCADE)  # 关联分类外键
    tagid = models.ForeignKey('Tags', to_field='id', on_delete=models.CASCADE)  # 关联标签外键
    top_id = models.IntegerField(default=0)  # 顶级分类
    sales = models.IntegerField(default=0)  # 销量
    com_num = models.IntegerField(default=0) # 当前商品的总评论数


    class Meta:
        db_table = 'goods'


from django.contrib.auth.models import AbstractUser
class User(Base, AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    signator = models.CharField(max_length=100)
    image = models.CharField(max_length=255, default='')
    is_active = models.IntegerField(default=0)  # 0未验证  1验证  2验证失败
    token = models.CharField(max_length=100)

    class Meta:
        db_table = 'user'







# 权限管理

#角色表
class Role(Base,models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=0) # 1启用 0停用
    resource = models.ManyToManyField('Resource')  # 多对多关联资源表
    class Meta:
        db_table = 'role'

# 资源表
class Resource(Base,models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=255)# 跳转到的网址
    satus = models.IntegerField(default=0) # 是否可用 1 可用 0 不可用
    class Meta:
        db_table = 'resource'



#用户表
class UserInfo(Base,models.Model):
    username = models.CharField(max_length=50,unique=True)
    passwd = models.CharField(max_length=255)
    role_id = models.ForeignKey('Role',on_delete=models.CASCADE) # 关联角色表外键
    is_admin = models.IntegerField() #是否是超级管理员 1是 0不是
    class Meta:
        db_table = 'userinfo'


class Cart(Base,models.Model):
    good_id = models.IntegerField()
    user_id = models.IntegerField()
    pic = models.CharField(max_length=255)
    goods_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    count = models.IntegerField()
    is_checked = models.IntegerField(default=0) #0 未加入订单  1 加入订单
    class Meta:
        db_table = 'cart'



#订单表
class Order(Base,models.Model):
    order_sn = models.CharField(max_length=100,unique=True) #订单号
    user = models.ForeignKey('User',on_delete=models.CASCADE) # 购买的用户
    address = models.CharField(max_length=255) # 购买地址
    tmony = models.DecimalField(max_digits=10,decimal_places=2)
    pay_type = models.IntegerField(default=1) #1货到付款 2支付宝  3微信  4 银行卡
    status = models.IntegerField(default=0) #状态 0未支付 1未评价 2 支付失败  3 已评价
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE)  # 关联地址
    code = models.CharField(max_length=100)  #流水号
    class Meta:
        db_table = 'order'
#订单详情表
class OrderDetail(Base,models.Model):
    order_sn = models.ForeignKey('Order',to_field='order_sn',on_delete=models.CASCADE)
    pic = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    name = models.CharField(max_length=50)
    good_id = models.ForeignKey('Goods',on_delete=models.CASCADE)
    count = models.IntegerField(default=0) #购买的数量
    user_id = models.IntegerField() #订单所属用户
    is_say = models.IntegerField(default=0) #0没有评价 1 已经评价
    class Meta:
        db_table = 'orderdetail'

#评价表
class Comment(models.Model):
    good_id = models.IntegerField() #和商品ID相关联的id
    user_id = models.IntegerField() # 和用户关联的id
    content = models.CharField(max_length=255)
    store = models.IntegerField() #评论分数
    class Meta:
        db_table = 'comment'



#地址表
class Adress(models.Model):
    receiver = models.CharField(max_length=30) #关联用户
    province = models.CharField(max_length=10)  # 城市
    city = models.CharField(max_length=10)  # 乡镇
    district = models.CharField(max_length=20) # 区
    place = models.CharField(max_length=30) # 详细地址
    mobile = models.CharField(max_length=11) #手机号
    tel = models.CharField(max_length=8) #固定电话
    email = models.CharField(max_length=30) #电子邮箱
    is_mo = models.IntegerField(default=0)  # 0不是默认地址  1 是默认地址
    is_se = models.IntegerField(default=0) #0 不是确认地址  1 是确认收货地址
    user_id = models.IntegerField() # 关联用户id

    class Meta:
        db_table = 'adress'

#省市区的表
class City(models.Model):
    pid = models.IntegerField(default=0) #上级id
    name = models.CharField(max_length=30)
    type = models.IntegerField()
    class Meta:
        db_table = 'city'


















