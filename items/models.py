from django.db import models

# Create your models here.
class Item(models.Model):
    """商品类"""
    uid = models.CharField(max_length=25, verbose_name='排序编码', unique=True)  # 排序依据
    name = models.CharField(max_length=20, verbose_name='商品名称')  # 商品品名
    pid = models.CharField(max_length=10, verbose_name='商品编码', unique=True)  # 商品编码
    number = models.IntegerField(default=0, verbose_name='库存数量')  # 商品库存
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间
    edited_time = models.DateTimeField(auto_now=True, verbose_name='编辑时间')  # 编辑时间
    
    def __str__(self):
        return "<Item: %s>" % self.name

    class Meta:
        # 排序规则
        ordering = ['uid']
        verbose_name = '商品库'
        verbose_name_plural = verbose_name


class NowItem(models.Model):
    """当前提交任务数量"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='iteming')
    num = models.IntegerField(default=0, verbose_name='任务数量')

    def __str__(self):
        return "<NowItem: %s>" % self.item.name

    class Meta:
        # 排序规则
        ordering = ['item__uid']
        verbose_name = '任务库'
        verbose_name_plural = verbose_name