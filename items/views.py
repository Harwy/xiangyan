from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import Item

# Create your views here.
def index(request):
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


def itemBuy(request):
    """商品入库表"""
    context = {}
    items = Item.objects.all()
    context['items'] = items
    return render(request, 'itemBuy.html', context)

def itemCreateTXT(request):
    pass


def itemSellList(request):
    """商品出库表"""
    context = {}
    items = Item.objects.all()
    context['items'] = items
    return render(request, 'itemSellList.html', context)
