from threading import Thread
from datetime import datetime,date
import time
import logging
from random import randint
from control import itemBuyAction

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Item, NowItem, ItemSetting, ItemLog

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
@register_job(scheduler, "interval", seconds=setting.per_time+pertime)  # 每20分钟提交一次打卡任务
def test_job():
    global pertime
    missions = NowItem.objects.all()
    itemsetting = ItemSetting.objects.all()[0]
    get = missionControl(missions, itemsetting)
    get.start()
    get.join()
    logging.warning("waitting:{} min ".format(setting.per_time+pertime))
    pertime = randint(setting.min_time, setting.max_time)

register_events(scheduler)

scheduler.start()
print("Scheduler started!")
####################################################


class missionControl(Thread):
    """多线程分发任务"""
    def __init__(self, missions, itemsetting):  # 随机0~30分钟后执行一次打卡
        Thread.__init__(self)
        self.missions = missions
        #self.time = randint(itemsetting.min_time, itemsetting.max_time)*60
        self.min_hour = itemsetting.min_hour
        self.max_hour = itemsetting.max_hour

    def run(self) -> None:
        tnow = int(datetime.now().strftime('%H'))
        if tnow >= self.min_hour and tnow <=self.max_hour and self.missions.exists():
            #time.sleep(self.time)  # 休眠[t_min,t_max]内随机分钟数
            nitem = self.missions.order_by('?')[0] # 随机抽取
            logging.warning("solve item:{} store: {}".format(nitem.item.name, nitem.num))
            itemBuyAction(nitem.item.pid)
            nitem.num = nitem.num - 1
            nitem.save()
            if nitem.num == 0: # 任务完成，删除
                nitem.delete()


# Create your views here.
def index(request):
    """测试"""
    return HttpResponse("Hello, world. You're at the polls index.")


def itemCreate(request):
    context = {}
    """新商品录入"""
    if request.method == 'POST':
        pid = request.POST.get('pid', None)
        name = request.POST.get('name', None)
        uid = request.POST.get('uid', None)
        number = request.POST.get('number', None)
        if not Item.objects.filter(Q(pid=pid) | Q(uid=uid)):
            # 保存数据
            Item.objects.create(pid=pid, name=name, uid=uid, number=number)
            context['result'] = 1
        else:
            # 当前已存在
            context['result'] = 2
        return render(request, 'home.html', context)
    else:
        context['result'] = 0
    return render(request, 'itemCreate.html', context)


def txt_create(pids, nums):
    """生成txt文件"""
    now = datetime.now()
    strf = now.strftime('%Y-%m-%d')
    root = "txtbox/"
    name = "buyin-{}.txt".format(strf)
    path = root+name
    file = open(path, 'w')
    for i in range(len(pids)):
        file.write("{},{}\n".format(pids[i], nums[i]))
    file.close()
    return name


@csrf_exempt
def itemBuy(request):
    context = {}
    if request.method == 'POST':
        """AJAX提交返回下载链接"""
        pids = request.POST.getlist('pids')
        nums = request.POST.getlist('nums')
        path = txt_create(pids, nums)
        context['download'] = path
        return JsonResponse(context)
    else:
        """商品入库表"""
        items = Item.objects.all()
        context['items'] = items
        return render(request, 'itemBuy.html', context)


def download_file(request):
    """下载txt文件"""
    if request.method == 'GET':
        path = request.GET.get('download')
        root = "txtbox/"
        file = open(root+path, 'rb')
        response = FileResponse(file)
        response['Content-Type']='application/octet-stream'  
        response['Content-Disposition']='attachment;filename="{}"'.format(path)
        return response


def itemSellList(request):
    """商品出库表"""
    context = {}
    items = Item.objects.all()
    nowItems = NowItem.objects.all()
    context['items'] = items
    context['nowItems'] = nowItems
    return render(request, 'itemSellList.html', context)


@csrf_exempt
def itemNowAdd(request):
    """AJAX提交任务商品"""
    if request.method == 'POST':
        pids = request.POST.getlist('pids')
        nums = request.POST.getlist('nums')
        for i in range(len(pids)):
            item = Item.objects.get(pid=pids[i])
            nitem, created = NowItem.objects.get_or_create(item=item)
            if created is True:
                nitem.num = int(nums[i])
                nitem.save()
            else:
                nitem.num = int(nums[i]) + nitem.num
                nitem.save()
        context = {}
        context['result'] = 1
        # 提交异步任务
        ######弃用Thread方法，改用定时任务
        # missions = NowItem.objects.all()
        # get = missionControl(missions)
        # get.start()
        # get.join()
        context['status'] = "success"
        return JsonResponse(context)


def itemInsert(request):
    file = open('xiangyan-2020-04-15.txt', 'r', encoding='UTF-8')
    for i in file.readlines():
        s = i.strip().split(',')
        Item.objects.create(uid=s[0], name=s[1], pid=s[2], number=s[3])
    return render(request, 'home.html', {'result': 3})


def mission(request):
    """商品出库表"""
    context = {}
    nowItems = NowItem.objects.all()
    context['nowItems'] = nowItems
    return render(request, 'itemMission.html', context)

def loglist(request):
    context = {}
    logs = ItemLog.objects.all()
    context['logs'] = logs
    return render(request, 'logList.html', context)


def log(request, pk):
    context = {}
    try:
        log = ItemLog.objects.get(pk=pk)
        path = log.path
        f = open(path, 'r')
        context['result'] = 1
        context['name'] = log.name
        context['log'] = [i for i in f.readlines()]
        f.close()
    except:
        context['result'] = 0
    return render(request, 'logging.html', context)
