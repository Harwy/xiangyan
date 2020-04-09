import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

def itemBuyAction(pid:str):
    """商品出售操作函数
    Input：
    -pid
    Output：
    -null
    """
    k.type_string(pid)  # 输入商品pid码
    # 完成交易
    time.sleep(2)  # 每个操作保证时延

if if __name__ == "__main__":
    pass