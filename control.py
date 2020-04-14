import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()
sleeptime = 2
bigSleeptime = 5

def itemBuyAction(pid:str):
    """商品出售操作函数
    Input：
    -pid
    Output：
    -null
    """
    k.type_string(pid)  # 输入商品pid码
    # 完成交易
    time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key(k.enter_key)
    time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key('c')
    time.sleep(sleeptime)
    k.tap_key(k.enter_key)
    time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key('c')
    time.sleep(sleeptime)
    k.tap_key(k.enter_key)


def itemBuyActionOne(pid:str):
    """商品出售操作函数
    Input：
    -pid
    Output：
    -null
    """
    for i in pid:
        k.tap_key(i)  # 输入商品pid码
        # 完成交易
        time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key(k.enter_key)
    time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key('c')
    time.sleep(sleeptime)
    k.tap_key(k.enter_key)
    time.sleep(sleeptime)  # 每个操作保证时延
    k.tap_key('c')
    time.sleep(sleeptime)
    k.tap_key(k.enter_key)

if __name__ == "__main__":
    time.sleep(bigSleeptime)
    itemBuyAction("093854")
