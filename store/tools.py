import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webEX.settings")  # 添加环境变量，webEX是项目名称
django.setup()
from store.models import Area, ComdyClass


def writeArea():
    provinceList = ('全国', '北京', '天津',  '上海', '重庆', '河北', '山西', '辽宁',
                    '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
                    '山东', '河南',  '湖北', '湖南', '广东', '海南', '四川',
                    '贵州', '云南',  '陕西', '甘肃', '青海', '台湾', '内蒙古',
                    '广西', '西藏','宁夏', '新疆', '香港', '澳门')
    for p in provinceList:
        if not Area.objects.filter(Name=p).exists():
            Area.objects.create(Name=p)


def writeComdyClass():
    classList = ("游戏本", "轻薄本", "商务本", "台式机")
    StatementList = (u"轻薄笔记本在重量、厚度上比较有优势，易于携带。屏幕大多采用窄边框，颜值比较高。",
                     u"游戏笔记本大多采用标准电压处理器+独立显卡的配置，游戏性能突出，基本可以流畅运行大型单机/网络游戏，办公、学习更不在话下。",
                     u"商务笔记本的安全性较高。商务笔记本大多经过了高低温、湿度、灰尘、高海拔等多重测试，具备更高的可靠性。",
                     u"台式机耐用，以及价格实惠，和本本相比，相同价格前提下配置较好，散热性较好，配件若损坏更换价格相对便宜，缺点就是：笨重，耗电量大。")
    LogInfo = []
    for i in range(len(classList)):
        p = classList[i]
        s = StatementList[i]
        if not ComdyClass.objects.filter(CName=p).exists():
            LogInfo.append(p)
            ComdyClass.objects.create(CName=p, CStatement=s)
    print("已添加", LogInfo)



if __name__ == "__main__":
    pass
    # writeArea()
    # writeComdyClass()