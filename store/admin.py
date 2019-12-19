from django.contrib import admin
from .models import Area, UserMessage, ComdyClass, CommodityInfo, \
    SalesRecord, BasketMessage, Log
# Register your models here.


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name',)
    ordering = ('ID',)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('admin_name', 'Unickname', 'admin_email','USex', 'UPhone', 'admin_img')


@admin.register(ComdyClass)
class ComdyClassAdmin(admin.ModelAdmin):
    list_display = ('Cid', 'CName',)
    ordering = ('Cid',)


@admin.register(CommodityInfo)
class CommodityInfoAdmin(admin.ModelAdmin):
    ordering = ('Cid',)
    list_display = ('Cid', 'CName', 'admin_img', 'CCount', 'CPurchasesCount', 'price_str', 'colored_status')
    list_display_links = ('Cid', 'CName')

    # 筛选器
    list_filter = ('CName', 'CArea', )  # 过滤器
    search_fields = ('CName', 'CArea')  # 搜索字段



@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('Sid', 'SComdyId', 'Uname_str', 'colored_status', 'SCount', 'colored_TotalAmount', 'STime')
    ordering = ('Sid',)

    # 筛选器
    list_filter = ('SComdyId',)  # 过滤器
    search_fields = ('SComdyId',)  # 搜索字段

@admin.register(BasketMessage)
class BasketMessageAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'ComdyId', 'UsersId', 'MarkTime', 'count')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'comdy_str', 'UsersId', 'Statement','Time')



admin.site.site_header = '商城后台管理系统'
admin.site.site_title = '商城后台'
