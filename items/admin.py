from django.contrib import admin
from .models import Item

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pid', 'number', 'edited_time')