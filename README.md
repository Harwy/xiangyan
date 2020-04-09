# xiangyan
 自动化录入和消化xiangyan
 > 因为家里小本经营经常需要人工录入和消耗操作，大量消耗人力物力。本人  
 > 不才，略学了点软件编程的皮毛，故借用软件的力量完成自动化的操作。  
 > `pyUserInput`模块来模拟键盘/鼠标操作  
 > `Django`框架做前后端完成交互  

## 2020/04/08
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
