class missionControl(Thread):
    """多线程分发任务"""
    def __init__(self, missions, t_min=0, t_max=30):
        Thread.__init__(self)
        self.missions = missions
        self.time = randint(t_min, t_max)*60

    def run(self) -> None:
        time.sleep(self.time)  # 休眠[t_min,t_max]内随机分钟数
        if self.missions.exists():
            nitem = self.missions.order_by('?')[0] # 随机抽取
            itemBuyAction(nitem.item.pid)
            nitem.num = nitem.num - 1
            nitem.save()
            if nitem.num == 0: # 任务完成，删除
                nitem.delete()


def timeable():
    """定时任务"""
    from threading import Thread
    import time
    from random import randint
    from control import itemBuyAction

    from .models import NowItem
    missions = NowItem.objects.all()
    get = missionControl(missions)
    get.start()
    get.join()


def test():
    import time
    time = randint(0, 30)
    print(time)