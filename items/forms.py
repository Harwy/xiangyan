from django import forms

class createItemForm(forms.Form):
    uid = forms.CharField(max_length=25, label='排序编码')  # 排序依据
    name = forms.CharField(max_length=20, label='商品名称')  # 商品品名
    pid = forms.CharField(max_length=10, label='商品编码')  # 商品编码
    number = forms.IntegerField(label='库存数量')  # 商品库存