# xiangyan
 自动化录入和消化xiangyan
 > 因为家里小本经营经常需要人工录入和消耗操作，大量消耗人力物力。本人  
 > 不才，略学了点软件编程的皮毛，故借用软件的力量完成自动化的操作。  
 > `pyUserInput`模块来模拟键盘/鼠标操作  
 > `Django`框架做前后端完成交互  

## 2020/04/08日志
---
关于Django上的初步构想  
需要一个`商品类`，内含一下信息：
* uid:string 排序依据
* name:string
* pid:string 
* number:int 库存
* created_time:datetime
* edited_time:datetime

核心功能：  
1. 新商品录入
2. 商品入库
3. 商品出库

超级管理员：
admin
test123456

## 重大调整
因所配置电脑为XP系统，最高支持到python3.4.4，部分包版本需要调整

> Django==2.0.13  
> pyHook==1.5.1  
> pytz==2019.3  
> PyUserInput==0.1.11  
> pywin32==221  

## 2020/04/14日志
更新入库功能  
更新出库功能

## v1.0版本
在实际部署中发现目标主机竟然是 `XP SP3 32位` 震惊之余还是根据实际情况更新了所有的安装包和python版本。

### 使用的工具和库
依次安装的顺序如下：
> python3.4.4 32位  
> win32  
> virtualenv  
> pyhook-py34-win32  
> pip install pyuserinput  
> pip install django  

### 出库功能介绍
在页面提交 `出库商品` 后，在 `出库类` (外键连接 `商品类` ) 由后台随机挑选其一进行自动出库操作。问题的关键在于如何**自动提交任务**。

#### while循环
首先考虑到的是对自动提交任务while循环，但是这样会导致进程阻塞，使得页面无法继续访问。

#### Thread+while循环（v1.0使用）
python自带的多线程+while循环，这样可以使得提交后能够在后台静默运行而前台能够继续使用。

#### redis+celery
这是网络上对于分布式任务所共识的方法，可以完成任务的调度。但是我们这个项目仅用到定时任务一点，有点大材小用，，同时也考虑到搭载的主机难以适配，暂时不考虑。

#### django-crontab定时任务库
将定时任务直接装载在 `django` 框架内，尽量减少不必要的操作。  
`crontab` 最出彩的地方在于 `定时运行函数` 。可以定制非常精确的定时任务，期望在v2.0版本中更新。
>  Cron时间格式实例：  
>  (0-59/10 7-8 * * *)    ------>  7点到8点内的每十分钟  
>  引用：[Cron时间格式网站](https://crontab.guru/#13_*/1_*_*_*)

**更新！**  
django-crontab基于linux的crontab指令，因此在windows环境下无法执行！，故`v2.0版本`放弃该方法

#### django-APScheduler模块
尝试`django-APScheduler`，但是网上查到的方法没有正常使用起来，最后实在github上的官方readme下找到 ===》 [（传送门）](https://github.com/jarekwg/django-apscheduler)。  


> 1. pip install django-APScheduler  
> 2. 将`django-APScheduler`添加进mysite/settings.py---->install INSTALLED_APPS = [..., 'django-APScheduler', yourapp] ，要在自己建的app之前。  
> 3. settings.py添加 `APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"  # Default`  
> 4. python manage.py migrate  
> 5. 在views.py或者urls.py下使用，代码如下： 

```python
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=5)  # 每5s提交一次打卡任务
def test_job():
    print("执行一次定时任务")  # 可以将定时任务的函数放在这里

register_events(scheduler)

scheduler.start()
print("Scheduler started!")
```

