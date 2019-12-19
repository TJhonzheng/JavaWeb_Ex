from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q, F
from django.contrib.auth.models import User
from .forms import RegisterForm, MessageForm
import json
from django.contrib import auth
from django.db import models
from django.forms.models import model_to_dict
from .models import Area, UserMessage, ComdyClass, CommodityInfo, SalesRecord, BasketMessage, Log
from django.core.files.base import ContentFile
from PIL import Image
from webEX.settings import URL_MEDIA
# 引入发送邮件的模块
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives

import datetime,pytz, os
from webEX import settings

tz = pytz.timezone('Asia/Shanghai')

# Create your views here.



def index(request):
    request.META["CSRF_COOKIE_USED"] = True
    return render(request, 'index.html')

# 注册
@require_http_methods(["POST"])
def register(request):
    response = {}
    form = RegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        User.objects.create_user(username=username, email=email, password=password)

        response["message"] = 'success'
        response["status"] = 0
        response["content"] = ['1', '2']
        user = User.objects.get(username=username)

        user.usermessage.Unickname = username # 默认昵称
        print(user.usermessage.img)
        user.save()
        print(Model_To_Dict(user.usermessage, fields=["Unickname", "UBirthday", "USex", "UStatement"]))

    else:
        if 'email' in form.get_errors().keys():
            response["message"] = form.errors["email"][0]
        elif 'username' in form.get_errors().keys():
            response["message"] = form.errors["username"][0]
        else:
            response["message"] = "注册失败！未知错误。"
        response["status"] = 1


    return JsonResponse(response)

# 登录函数
@require_http_methods(["POST"])
def login(request):
    response = {}
    user = request.POST.get('username')
    pwd = request.POST.get('password')
    user_name = auth.authenticate(username=user, password=pwd)  # 自动校验user表 用户账号校验
    try:
        userEmail = User.objects.get(email=user)
    except:
        userEmail = None

    if user_name is not None:  # 登陆成功
        response1 = Model_To_Dict(user_name)
        response2 = Model_To_Dict(user_name.usermessage)
        response = {**response1, **response2}

        response['img'] = str(URL_MEDIA + str(response['img']))

        user_name.last_login = datetime.datetime.now()# + datetime.timedelta(hours=8)
        user_name.save()
        response["status"] = 0

    elif userEmail is not None:
        user_email = auth.authenticate(username=userEmail, password=pwd)  # 自动校验user表 用户邮箱校验
        if user_email is not None:
            response1 = Model_To_Dict(user_email)
            response2 = Model_To_Dict(user_email.usermessage)
            response = {**response1, **response2}
            response['img'] = str(URL_MEDIA + str(response['img']))
            user_email.last_login = datetime.datetime.now() + datetime.timedelta(hours=8)
            user_email.save()
            response["status"] = 0
        else:
            response["status"] = 1
    else:
        response["status"] = 1

    return JsonResponse(response)

# 获取用户信息
@require_http_methods(["POST"])
def getMessage(request):
    response = {}
    id = request.POST.get("id")
    user = User.objects.get(pk=id)
    if user is not None:  # 查询成功
        response = Model_To_Dict(user.usermessage, fields=["Unickname", "UBirthday", "USex", "UStatement", 'img'])
        response['img'] = str(URL_MEDIA + str(response['img']))
        print(response['img'])
        if response['UBirthday'] is not None:
            response["UBirthday"] = response["UBirthday"].strftime("%Y-%m-%d")
        else:
            response['UBirthday'] = 0
        response["status"] = 0
    else:
        response["status"] = 1

    return JsonResponse(response)

# 修改用户信息
@require_http_methods(["POST"])
def alterMessage(request):
    response = {}
    id = request.POST.get("id")
    user = User.objects.get(pk=id)
    if user is not None:  # 查询成功
        dateStr = request.POST.get("birthday")[:10] # 截取时间字符串
        dateTime = datetime.datetime.strptime(dateStr, '%Y-%m-%d') + datetime.timedelta(hours=24)
        print(dateTime)
        # 修改POST内容
        data = request.POST.copy()
        data['birthday'] = dateTime
        form = MessageForm(data)
        if form.is_valid():
            user.usermessage.UBirthday = form.cleaned_data.get('birthday')
            user.usermessage.Unickname = form.cleaned_data.get('nickname')
            user.usermessage.USex = form.cleaned_data.get('sex')
            user.usermessage.UStatement = form.cleaned_data.get('statement')
            user.usermessage.save()
            # print(model_to_dict(user.usermessage))
            response["status"] = 0
        else:
            if 'nickname' in form.errors.keys():
                response["message"] = form.errors["nickname"][0]
            elif 'statement' in form.errors.keys():
                response["message"] = form.errors["statement"][0]
            else:
                print(form.errors)
                response["message"] = "信息修改失败！未知错误。"
                response["status"] = 1
    else:
        response["status"] = 1

    return JsonResponse(response)

# 根据分类获取商品信息
@require_http_methods(["POST"])
def getComdyInfoByClassId(request):
    response = {}
    comdy = []
    classId = int(request.POST.get("classId"))
    comdyInfo = CommodityInfo.objects.filter(CCid=classId)
    if comdyInfo is not None:
        for info in comdyInfo:
            info_temp = Model_To_Dict(info, fields=['Cid', 'CName', 'CPrice'])
            info_temp_img = Model_To_Dict(info, fields=['img'])
            print(info_temp)
            info_temp['CImg'] = str(URL_MEDIA + str(info_temp_img['img']))
            comdy.append(info_temp)
        response['comdyInfo'] = comdy
        response['status'] = 0
        response['message'] = '商品信息返回成功'
    else:
        response['status'] = 1
        response['message'] = '商品信息返回失败，请重试！'
    return JsonResponse(response)

# 根据id获取商品信息
@require_http_methods(["POST"])
def getComdyInfoById(request):
    response = {}
    comdyId = int(request.POST.get("comdyId"))
    try:
        comdy = CommodityInfo.objects.get(Cid=comdyId)
        info_temp = Model_To_Dict(comdy, fields=['Cid', 'CName', 'CPrice','CCount', 'CState', 'CPurchasesCount', 'CStatement'])
        info_temp_img = Model_To_Dict(comdy, fields=['img'])
        print(info_temp)
        info_temp['CImg'] = str(URL_MEDIA + str(info_temp_img['img']))
        info_temp['Area'] = comdy.CArea.Name

        response['comdyInfo'] = info_temp
        response['status'] = 0
        response['message'] = '商品信息返回成功'
    except:
        response['status'] = 1
        response['message'] = '商品信息返回失败，请重试！'
    return JsonResponse(response)

# 添加进购物篮
@require_http_methods(["POST"])
def addBasket(request):
    response = {}
    comdyId = int(request.POST.get('comdyId'))
    userId = int(request.POST.get('userId'))
    try:
        compRecord = CommodityInfo.objects.get(Cid=comdyId)
        user = User.objects.get(pk=userId).usermessage
        # 判断传入用户、帖子数据是否存在数据库中
        try :
            ifMark = BasketMessage.objects.get(ComdyId=compRecord, UsersId=user, )
            response['status'] = 2
            response['message'] = '您已添加了，请勿重复操作。'
        except:
                BasketMessage.objects.create(ComdyId=compRecord, UsersId=user)
                response['status'] = 0
                response['message'] = '添加成功！'
    except:
        response['status'] = 1
        response['message'] = '添加失败，请稍后重试！'
    return JsonResponse(response)

# 取消购物篮记录
@require_http_methods(["POST"])
def DeleteBasketMessage(request):
    response = {}
    comdyId = int(request.POST.get('comdyId'))
    userId = int(request.POST.get('userId'))
    try:
        compRecord = CommodityInfo.objects.get(Cid=comdyId)
        user = User.objects.get(pk=userId).usermessage
        BasketMessage.objects.get(ComdyId=compRecord, UsersId=user).delete()
        response['status'] = 0
        response['message'] = '成功取消收藏！'
    except:
        response['status'] = 1
        response['message'] = '取消收藏失败，请刷新后重试！'
    return JsonResponse(response)

# 获取购物篮消息
@require_http_methods(["POST"])
def getBasketMessage(request):
    response = {}
    userId = int(request.POST.get('userId'))
    try:
        user = User.objects.get(pk=userId).usermessage
        marklist = BasketMessage.objects.filter(UsersId=user)
        markMessages = []
        for message in marklist:
            comdyInfoId = message.ComdyId.Cid
            comdyP = message.ComdyId.CPrice
            comdyC = message.count
            comdyN = message.ComdyId.CName
            markMessages.append(
                {"comdyInfoId": comdyInfoId,
                 "price" : comdyP,
                 "name" : comdyN,
                 "count" : comdyC},
            )
        response['basketMessages'] = markMessages
        response['basketMessagesCount'] = len(markMessages)
        response['status'] = 0
        response['message'] = '查询成功'
    except:
        response['status'] = 1
        response['message'] = '查询失败，请稍后重试！'
    return JsonResponse(response)


# 提交报表记录
@require_http_methods(["POST"])
def addSalesRecord(request):
    response = {}
    userId = int(request.POST.get('userId'))
    comdyId = int(request.POST.get('comdyId'))
    try:
        user = User.objects.get(pk=userId).usermessage
        comdy = CommodityInfo.objects.get(pk=comdyId)
        comdy.CPurchasesCount += 1  # 已购数量加一
        comdy.CCount -= 1 # 库存减一
        comdy.save()
        count = request.POST.get('count')
        totalAmount = request.POST.get('totalAmount')
        SalesRecord.objects.create(SUsersId=user, SComdyId=comdy, SCount=count, STotalAmount=totalAmount)
        response['status'] = 0
        response['message'] = '记录成功'
    except:
        response['status'] = 1
        response['message'] = '记录失败，请稍后重试！'
    return JsonResponse(response)


# 日志记录
@require_http_methods(["POST"])
def addLog(request):
    response = {}
    userId = int(request.POST.get('userId'))
    comdyId = int(request.POST.get('comdyId'))
    try:
        user = User.objects.get(pk=userId).usermessage
        comdy = CommodityInfo.objects.get(pk=comdyId)
        Statement = request.POST.get('Statement')
        Log.objects.create(UsersId=user, ComdyId=comdy, Statement=Statement)
        response['status'] = 0
        response['message'] = '记录成功'
    except:
        response['status'] = 1
        response['message'] = '记录失败，请稍后重试！'
    return JsonResponse(response)

# 发送邮件
@require_http_methods(["POST"])
def send_email(request):
    response = {}
    userId = int(request.POST.get('userId'))
    comdyId = int(request.POST.get('comdyId'))
    try:
        user = User.objects.get(pk=userId).usermessage
        comdy = CommodityInfo.objects.get(pk=comdyId)
        userName = user.Unickname
        comdyName = comdy.CName
        totalAmount = request.POST.get('totalAmount')
        email = User.objects.get(pk=userId).email
        # 值1：  邮件标题   值2： 邮件主体
        # 值3： 发件人      值4： 收件人
        res = send_mail('下单成功通知',
                        '尊敬的用户 '+userName+":\n"+"\t您在商城下单的商品+【"+comdyName+"】，总金额："+totalAmount+'元，已成功发货。\n祝您生活幸福。',
                        'zjh_scutcs@163.com',
                        [email])
        if res == 1:
            response['status'] = 0
            response['message'] = '邮件发送成功'
        else:
            response['status'] = 1
            response['message'] = '邮件发送失败'
    except:
        response['status'] = 1
        response['message'] = '邮件发送失败，请稍后重试'
    return JsonResponse(response)

# 上传图像
@require_http_methods(["POST"])
def upLoadImage(request):
    response = {}
    userId = int(request.POST.get('userId'))
    try:
        User.objects.get(pk=userId).usermessage.img = request.FILES['img']
        file_content = ContentFile(request.FILES['img'].read())
        suffix = os.path.splitext(str(request.FILES['img']))[1]

        if suffix.lower() == '.jpg':
            User.objects.get(pk=userId).usermessage.img.save(
                str(userId)+'_'+datetime.datetime.now().strftime("%Y%m%d%H%M")+'.jpg', file_content)
        elif suffix.lower() == '.png':
            User.objects.get(pk=userId).usermessage.img.save(
                str(userId) + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M") + '.png', file_content)
        else:
            raise ()
        response['status'] = 0
        response['message'] = '上传成功！'
        response['img'] = URL_MEDIA + str(User.objects.get(pk=userId).usermessage.img)
    except:
        response['status'] = 1
        response['message'] = '上传失败！请稍后再试。'
    return JsonResponse(response)


# 辅助函数：
def Model_To_Dict(model, fields=None, exclude=None):
    dic = model_to_dict(model, fields, exclude)
    for key in dic:
        if isinstance(dic[key], datetime.datetime):
           dic[key] = dic[key].strftime("%Y-%m-%d %H:%M")

    return dic