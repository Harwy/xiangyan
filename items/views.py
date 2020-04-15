from threading import Thread
from datetime import datetime
from control import itemBuyAction

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Item, NowItem


class missionControl(Thread):
    """多线程分发任务"""
    def __init__(self, missions, tstart='07', tend='22'):
        Thread.__init__(self)
        self.missions = missions
        self.tstart = tstart
        self.tend = tend

    def run(self) -> None:
        while(self.missions.exists()):
            tnow = datetime.now().strftime('%H')
            print("===== %s ======" % tnow)
            if tnow >= self.tstart and tnow <=self.tend:
                nitem = self.missions.order_by('?')[0] # 随机抽取
                itemBuyAction(nitem.item.pid)
                nitem.num = nitem.num - 1
                nitem.save()
                if nitem.num == 0: # 任务完成，删除
                    nitem.delete()
            else: break;




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
        missions = NowItem.objects.all()
        get = missionControl(missions)
        get.start()
        get.join()
        context['status'] = "success"
        return JsonResponse(context)


