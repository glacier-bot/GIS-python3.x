import pyautogui
import time

print("开始")
time.sleep(3)
i=0
while True:
    # 先使用下面两行代码获取执行每个操作时鼠标的坐标
    # x,y=pyautogui.position()
    # print(x,y)

    time.sleep(3)

    # 将鼠标坐标填入下面函数的前两个参数中；第三个参数是鼠标移动到坐标需要的时间，不宜过短
    # 鼠标右键点击
    pyautogui.rightClick(206,789,duration=0.7)
    # 鼠标左键点击
    pyautogui.click(276,922,duration=0.7)
    pyautogui.click(1050,662,duration=0.7)

    i+=1
    print(i)
    # i是错误的数量，这里是2，可以根据实际情况修改，不宜过大，一般不超过20
    if i==2:
        break