from django.db import models

# Create your models here.
class Item(models.Model):
    """商品类"""
    uid = models.CharField(max_length=25, verbose_name='条形码')  # 排序依据 条形码
    name = models.CharField(max_length=20, verbose_name='商品名称')  # 商品品名
    # pid = models.CharField(max_length=10, verbose_name='商品编码')  # 商品编码
    number = models.IntegerField(default=0, verbose_name='库存数量')  # 商品库存
    mission = models.IntegerField(default=0, verbose_name='任务数量')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间
    edited_time = models.DateTimeField(auto_now=True, verbose_name='编辑时间')  # 编辑时间
    
    def __str__(self):
        return "<Item: %s>" % self.name

    class Meta:
        # 排序规则
        ordering = ['uid']
        verbose_name = '商品库'
        verbose_name_plural = verbose_name


class ItemSetting(models.Model):
    max_time = models.IntegerField(default=30, verbose_name='最大随机时间')
    min_time = models.IntegerField(default=0, verbose_name='最小随机时间')
    per_time = models.IntegerField(default=20, verbose_name='任务间隔时间')
    min_hour = models.IntegerField(default=7, verbose_name='最早时间')
    max_hour = models.IntegerField(default=22, verbose_name='最晚时间')

    def __str__(self):
        return "配置"

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name

class ItemLog(models.Model):
    name = models.CharField(max_length=20, verbose_name='日志日期')
    path = models.CharField(max_length=50, verbose_name='日志路径')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间

    def __str__(self):
        return "日志"

    class Meta:
        # 排序规则
        ordering = ['-created_time']
        verbose_name = '日志'
        verbose_name_plural = verbose_name

class ItemFile(models.Model):
    name = models.CharField(max_length=20, verbose_name='文件名')
    path = models.CharField(max_length=50, verbose_name='文件路径')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return "<文件: %s>" % self.name

    class Meta:
        # 排序规则
        ordering = ['-created_time']
        verbose_name = '文件'
        verbose_name_plural = verbose_name

