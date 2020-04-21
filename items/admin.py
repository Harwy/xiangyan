from django.contrib import admin
from .models import Item, NowItem, ItemSetting, ItemLog, ItemFile

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pid', 'number', 'edited_time')


@admin.register(NowItem)
class NowItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'num')

@admin.register(ItemSetting)
class ItemSettingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'max_time', 'min_time', 'per_time', 'min_hour', 'max_hour')

@admin.register(ItemLog)
class ItemLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'path', 'created_time')

@admin.register(ItemFile)
class ItemFileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'path', 'created_time')