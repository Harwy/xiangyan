import os
from threading import Thread
from datetime import datetime,date
import time
import logging
from random import randint
from control import itemBuyAction

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse, Http404
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Item, ItemSetting, ItemLog, ItemFile

# ====log setting======
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter('%(asctime)s - %(message)s')
path = 'log/{}.log'.format(date.today().isoformat())

# logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
console = logging.FileHandler(filename=path, encoding='utf-8')
console.setLevel(logging.WARNING)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

ItemLog.objects.get_or_create(name=date.today().isoformat(), path=path)

##################"""定时任务模块"""#################
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

setting = ItemSetting.objects.all()
if not setting.exists():
    setting = ItemSetting.objects.create()
else:
    setting = setting[0]
pertime = randint(setting.min_time, setting.max_time)
@register_job(scheduler, "interval", seconds=setting.per_time*60 + pertime*60)  # 每20分钟提交一次打卡任务
def test_job():
    global pertime
    q = ItemSetting.objects.all()[0]
    tnow = int(datetime.now().strftime('%H'))
    if tnow >= q.min_hour and tnow <= q.max_hour:
        missions = Item.objects.filter(mission__gt=0)
        if missions.exists():
            mission = missions.order_by('?')[0] # 随机抽取
            get = missionControl(mission)
            get.start()
            get.join()
            logging.warning("Working! waitting:{} min".format(q.per_time+pertime))
        else:
            logging.warning("no mission! Please add!")
        pertime = randint(q.min_time, q.max_time)
    else:
        logging.warning("time not in range({},{})".format(q.min_hour, q.max_hour))

register_events(scheduler)

scheduler.start()
# print("Scheduler started!")
####################################################


class missionControl(Thread):
    """多线程分发任务"""
    def __init__(self, mission):  # 随机0~30分钟后执行一次打卡
        Thread.__init__(self)
        self.mission = mission

    def run(self) -> None:
        logging.warning("销售品名:{} /当前任务库存: {}".format(self.mission.name, self.mission.mission))
        itemBuyAction(self.mission.uid)
        self.mission.mission = self.mission.mission - 1
        self.mission.save()


class fileExpress(Thread):
    """多线程导入数据"""
    def __init__(self, file_name, file_type):
        Thread.__init__(self)
        self.file = file_name
        self.file_type = file_type
        self.status = True
        logging.warning("开始导入===>{}".format(file_name))

    def run(self) -> None:
        import xlrd
        book = xlrd.open_workbook(self.file)
        sheet = book.sheets()[0]
        nrows = sheet.nrows
        file_type = "进货" if self.file_type == '1' else "库存"
        txt_name = "{}-{}-{}.txt".format("pcin", file_type, datetime.now().strftime('%Y-%m-%d'))
        path = "txtbox/" + txt_name
        f = open(path, 'w')
        if self.file_type == '1':  # 每周进货入库
            for i in range(nrows):
                if sheet.cell(i,0).value.isdigit():
                    uid = sheet.cell(i,1).value
                    # pid = sheet.cell(i,2).value
                    name = sheet.cell(i,3).value
                    num = sheet.cell(i,5).value
                    if name.isdigit(): 
                        logging.warning("您操作的是进货入库，但是上传的是'库存单'")
                        self.status = False
                        break
                    item, created = Item.objects.get_or_create(uid=uid, name=name)
                    # item, created = Item.objects.get_or_create(pid=pid, uid=uid, name=name)
                    item.number = item.number + num
                    item.save()
                    f.write("{},{}\n".format(uid, int(num)))
        else:  # 库存
            for i in range(nrows): 
                if sheet.cell(i,0).value.isdigit():
                    uid = sheet.cell(i,0).value
                    # pid = sheet.cell(i,1).value
                    name = sheet.cell(i,2).value
                    num = sheet.cell(i,4).value
                    if name.isdigit(): 
                        logging.warning("您操作的是库存入库，但是上传的是'进货单'")
                        self.status = False
                        break
                    item, created = Item.objects.get_or_create(uid=uid, name=name)
                    # item, created = Item.objects.get_or_create(pid=pid, uid=uid, name=name)
                    item.number = item.number + num
                    item.save()
                    f.write("{},{}\n".format(uid, int(num)))
        f.close()
        logging.warning("=====导入完成=====")
        if self.status is True:
            ItemFile.objects.create(name=self.file,path=txt_name)  # 数据库保存导入文件路径


# Create your views here.
def itemCreate(request):
    context = {}
    """新商品录入"""
    if request.method == 'POST':
        # pid = request.POST.get('pid', None)
        name = request.POST.get('name', None)
        uid = request.POST.get('uid', None)
        number = request.POST.get('number', None)
        if not Item.objects.filter(uid=uid):
            # 保存数据
            Item.objects.create(name=name, uid=uid, number=number)
            # Item.objects.create(pid=pid, name=name, uid=uid, number=number)
            context['result'] = 1
        else:
            # 当前已存在
            context['result'] = 2
        return render(request, 'home.html', context)
    else:
        context['result'] = 0
    return render(request, 'itemCreate.html', context)


def txt_create(uids, nums, ty="buyin"):
    """生成txt文件"""
    strf = datetime.now().strftime('%Y-%m-%d')
    root = "txtbox/"
    name = "{}-{}.txt".format(ty, strf)
    path = root+name
    f = open(path, 'w')
    for i in range(len(uids)):
        f.write("{},{}\n".format(uids[i], nums[i]))
    f.close()
    return name


@csrf_exempt
def itemBuy(request):
    context = {}
    if request.method == 'POST':
        """AJAX提交返回下载链接"""
        uids = request.POST.getlist('uids')
        nums = request.POST.getlist('nums')
        path = txt_create(uids, nums)
        context['download'] = path
        return JsonResponse(context)
    else:
        """商品入库表"""
        items = Item.objects.all()
        context['items'] = items
        return render(request, 'itemBuy.html', context)


def downloadList(request):
    """下载文件列表"""
    ifiles = ItemFile.objects.all()
    context = {}
    context['files'] = ifiles
    return render(request, 'itemFile.html', context)


def downloadFile(request, pk):
    """下载txt文件"""
    if request.method == 'GET':
        try:
            ifile = ItemFile.objects.get(pk=pk)
            root = 'txtbox/'
            f = open(root+ifile.path, 'rb')
            response = FileResponse(f)
            response['Content-Type']='application/octet-stream'  
            # response['Content-Disposition']='attachment;filename="{}"'.format(ifile.path)
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(ifile.path))  # 解决下载文件中文命名问题
            return response
        except Exception as e:
            raise Http404
        


def itemSellList(request):
    """商品出库表"""
    context = {}
    items = Item.objects.all()
    context['items'] = items
    return render(request, 'itemSellList.html', context)


@csrf_exempt
def itemNowAdd(request):
    """AJAX提交任务商品"""
    if request.method == 'POST':
        types = request.POST.get('type')
        if types == '1':
            uids = request.POST.getlist('uids')
            nums = request.POST.getlist('nums')
            for i in range(len(uids)):
                item = Item.objects.get(uid=uids[i])
                item.mission = int(nums[i]) + item.mission if int(nums[i]) + item.mission > 0 else 0
                item.number = item.number - int(nums[i]) if int(nums[i]) + item.mission > 0 else item.number
                item.save()
        else:
            items = Item.objects.all()
            for item in items:
                item.mission = item.number + item.mission
                item.number = 0
                item.save()
        context = {}
        context['result'] = 1
        context['status'] = "success"
        return JsonResponse(context)


def mission(request):
    """商品任务表"""
    context = {}
    items = Item.objects.filter(mission__gt=0)
    context['items'] = items
    return render(request, 'itemMission.html', context)

def loglist(request):
    """log列表"""
    context = {}
    logs = ItemLog.objects.all()
    context['logs'] = logs
    return render(request, 'logList.html', context)


def log(request, pk):
    """pk页log展示"""
    context = {}
    try:
        log = ItemLog.objects.get(pk=pk)
        path = log.path
        f = open(path, 'r', encoding='utf-8')
        context['result'] = 1
        context['name'] = log.name
        context['log'] = [i for i in f.readlines()[::-1]]
        f.close()
    except:
        context['result'] = 0
    return render(request, 'logging.html', context)


def fileUpload(request):
    """入库文件上传"""
    context = {}
    if request.method == 'POST':
        file_type = request.POST.get('file_type')
        file_obj = request.FILES.get('file_obj')
        file_name = "upload/" + datetime.now().strftime('%Y-%m-%d') + '.xlsx'
        with open(file_name, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        get = fileExpress(file_name, file_type)
        get.start()
        get.join()
        context['result'] = '1'
    return JsonResponse(context)

@csrf_exempt
def missionDelete(request):
    context = {}
    if request.method == 'POST':
        uid = request.POST.get('uid')
        item = Item.objects.get(uid=uid)
        item.number = item.mission + item.number
        item.mission = 0
        item.save()
        context['result'] = '1'
    return JsonResponse(context)
