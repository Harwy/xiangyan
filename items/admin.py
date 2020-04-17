from django.contrib import admin
from .models import Item, NowItem, ItemSetting

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pid', 'number', 'edited_time')


@admin.register(NowItem)
class NowItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'num')

@admin.register(ItemSetting)
class ItemSettingAdmin(admin.ModelAdmin):
    list_display = ('max_time', 'min_time', 'per_time', 'min_hour', 'max_hour')