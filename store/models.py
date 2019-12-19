from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Area(models.Model):
    ID   = models.AutoField(primary_key=True, verbose_name=u"地区编号")
    Name = models.CharField(max_length=5, default=u"北京", verbose_name=u"地区名字")

    class Meta:
        db_table = "Area"
        verbose_name = '地区'
        verbose_name_plural = '地区列表'

    def __str__(self):
        return self.Name


class UserMessage(models.Model):
    """
    表中列名	        数据类型	    可否为空	        说明
    Uid	            Int	        not null(主键)	用户编号
    UName	        char	    not null	    用户名
    UPassword 	    char	    not null	    用户密码
    UEmail	        char	    not null	    用户Email
    UBirthday	    datetime	null	        用户生日
    USex	        char	    null	        用户性别
    UStatement	    varchar	    null	        用户个人说明
    URegDate 	    datetime	not null	    用户注册时间
    ULastOnlineDate	datetime	not null	    用户最后上线时间
    UIfAdmin	    bool	    Not null	    是否管理员
    Unickname       varchar     not null        昵称
    """
    UserBase = models.OneToOneField(User, on_delete=models.CASCADE)
    # 个人资料
    UPhone = models.CharField(u'手机号', max_length=11, default='none', null=True, blank=True)
    UBirthday  = models.DateField(u'用户生日', null=True, blank=True)
    USex       = models.CharField(u'用户性别', max_length=2, default='X', null=True, blank=True)
    UStatement = models.CharField(u'用户个人说明', max_length=150, default='none', null=True, blank=True)
    Unickname   = models.CharField(u'用户昵称', max_length=10, default='', blank=True)
    UImg       = models.ImageField(u'用户头像', upload_to='HeadPortrait', name='img', default='HeadPortrait\\defult.png')

    class Meta:
        db_table = "Users"
        verbose_name = '用户信息'
        verbose_name_plural = '用户列表'

    def __str__(self):
        return self.UserBase.username

    def admin_img(self):
        return mark_safe('<img src="/media/%s" height="50" width="50" />' % (self.img))

    def admin_name(self):
        return format_html(
            '<span>{}</span>',
            self.UserBase.username,
        )
    def admin_email(self):
        return format_html(
            '<span>{}</span>',
            self.UserBase.email,
        )

    admin_img.short_description = '头像'
    admin_img.allow_tags = True
    admin_name.short_description = '用户名'
    admin_email.short_description = '邮箱'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        a = UserMessage.objects.create(UserBase=instance)
        #a.save()

@receiver(post_save, sender=User)
def save_user_userMessage(sender, instance, **kwargs):
    instance.usermessage.save()


class ComdyClass(models.Model):
    Cid = models.AutoField(primary_key=True, verbose_name=u"商品类别编号")
    CName = models.CharField(max_length=10, default="未设置", verbose_name=u"类别名称")
    CStatement = models.CharField(max_length=200, null=True, verbose_name=u"类别说明")

    class Meta:
        db_table = "ComdyClass"
        verbose_name = '商品类别'
        verbose_name_plural = '商品类别列表'

    def __str__(self):
        return self.CName


class CommodityInfo(models.Model):
    # 主键
    Cid = models.AutoField(primary_key=True, verbose_name=u"商品编号")
    # 外键
    CName = models.CharField(max_length=50,  default="", verbose_name=u"商品名称")
    CCid = models.ForeignKey(ComdyClass, on_delete=models.CASCADE, verbose_name=u"类别")
    CArea = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name=u"发货地区")

    CCount = models.PositiveIntegerField(default=0,  verbose_name=u"库存数量")
    CState = models.CharField(max_length=20, default='售卖中', verbose_name=u"状态")
    CPurchasesCount = models.PositiveIntegerField(default=0, verbose_name=u"已购买量")
    CPrice = models.FloatField(default=0,  verbose_name=u"价格")
    CStatement = models.TextField(default="（空）", verbose_name="商品介绍")
    CImg = models.ImageField(u'商品图片', upload_to='CommodityImg', name='img', default='CommodityImg\\defult.png')

    class Meta:
        db_table = "ComdyInfo"
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息列表'

    def __str__(self):
        return self.CName

    def colored_status(self):
        if self.CState == '停售':
            color_code = 'red'
        else:
            color_code = 'green'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.CState,
        )
    def price_str(self):
        return format_html(
            '<span>{} 元</span>',
            self.CPrice,
        )
    def admin_img(self):
        return mark_safe('<img src="/media/%s" height="40" width="40" />' % (self.img))

    admin_img.short_description = '图片'
    admin_img.allow_tags = True
    colored_status.short_description = u"状态"
    price_str.short_description = '价格'


class SalesRecord(models.Model):
    # 主键
    Sid = models.AutoField(primary_key=True, verbose_name=u"记录编号")
    # 外键
    SComdyId = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE, verbose_name="商品名称")
    SUsersId = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name="用户编号")

    STime = models.DateTimeField(auto_now_add=True, verbose_name="交易时间")
    SCount = models.PositiveIntegerField(default=1,  verbose_name=u"成交商品数量")
    STotalAmount = models.FloatField(default=0,  verbose_name=u"成交总额")
    SState = models.CharField(max_length=10,  default="已付款", verbose_name=u"交易状态")
    SRemark = models.TextField(default="", verbose_name="买家备注")

    class Meta:
        db_table = "SalesRecord"
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录列表'

    def Cname_str(self):
        return format_html(
            '<span>{}</span>',
            self.SComdyId.CName[:22]+'...',
        )
    def Uname_str(self):
        return format_html(
            '<span>{}</span>',
            self.SUsersId.UserBase.username
        )
    def colored_status(self):
        if self.SState == '已付款':
            color_code = 'green'
        else:
            color_code = 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.SState,
        )
    def colored_TotalAmount(self):
        return format_html(
            '<span style="color: {}; font-weight:700;">￥ {}</span>',
            'red',
            self.STotalAmount,
        )
    Cname_str.short_description = '商品名称'
    Uname_str.short_description = '下单用户'
    colored_status.short_description = '交易状态'
    colored_TotalAmount.short_description = '成交总额'


class BasketMessage(models.Model):
    """
        表中列名	        数据类型	    可否为空	        说明
        CompRecordId	Int	        not null	    记录编号
        UsersId     	Int	        not null	    用户编号
        MarkTime        datetime    not null        添加时间
    """
    ComdyId      = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE, verbose_name="商品编号")
    UsersId      = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name="用户名")
    MarkTime     = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="加入购物篮时间")
    count        = models.PositiveIntegerField(default=1,  verbose_name=u"添加的数量")

    class Meta:
        db_table = "BasketMessage"
        verbose_name = '购物篮记录'
        verbose_name_plural = '购物篮记录列表'

    def id_str(self):
        return format_html(
            '<span>{}</span>',
            self.pk,
        )
    id_str.short_description = '编号'


class Log(models.Model):
    ComdyId = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE, verbose_name="商品编号")
    UsersId = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name="用户编号")
    Time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="日志记录时间")
    Statement = models.CharField(max_length=100,  default="", verbose_name=u"日志内容")

    class Meta:
        db_table = "Log"
        verbose_name = '日志记录'
        verbose_name_plural = '日志记录列表'

    def id_str(self):
        return format_html(
            '<span>{}</span>',
            self.pk,
        )
    def comdy_str(self):
        return format_html(
            '<span>{}</span>',
            self.ComdyId.CName[:20],
        )
    id_str.short_description = '编号'
    comdy_str.short_description = '商品名称'


