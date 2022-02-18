from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pyautogui as gui
from ctypes import *  # 获取屏幕上某个坐标的颜色



def get_color(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)  # 获取颜色值
    pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r,g,b]



def lo():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=option)
    driver.get('https://sz.jd.com/sz/view/index/login.html')       #打开网页
    driver.find_element_by_xpath("//a[@class='login-btn btn']").click()   # 点登陆
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginDialogBody")))  # 等弹窗
    tgt_f=driver.find_element_by_xpath("//div[@class='ui-dialog-content']").location  #获得弹窗相对坐标
    print (tgt_f)
    driver.switch_to.frame('dialogIframe')      #切换到iframe里
    driver.find_element_by_xpath("//div[@class='login-tab login-tab-r']").click()   #点账号密码登陆
    driver.find_element_by_id("loginname").send_keys("13644117176")         #账号
    driver.find_element_by_id("nloginpwd").send_keys("13644117176")         #密码
    driver.find_element_by_xpath("//div[@class='login-btn']").click()       # 登陆
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "JDJRV-wrap-loginsubmit"))) #等验证码弹窗
    tgt=driver.find_element_by_xpath("//div[@class='JDJRV-smallimg']").location    # 验证码拖拽框相对坐标
    print (tgt)
    mw=driver.get_window_position()     #浏览器对于屏幕的绝对坐标
    print (mw)
    abs_tgt_x=mw['x']+7+tgt_f['x']+10+tgt['x']+1        #算出拖拽框最左侧的屏幕绝对x坐标， 数字需要量一下
    abs_tgt_y = mw['y'] + 120 + tgt_f['y'] + tgt['y']   # 拖拽框最左侧的大致的屏幕绝对y坐标
    print (abs_tgt_x,abs_tgt_y)
    #接下来找准确的y坐标
    credit_y=0
    for _ in range(50):
        abs_tgt_y+=1
        clr = get_color(abs_tgt_x, abs_tgt_y)
        if clr==[120,120,120]:     # 最左边的边框会有5个连续的像素rgb都=120
            credit += 1
            if credit == 5:
                break
        else:
            credit = 0

    chk_x=abs_tgt_x+38+20               #从此x坐标向右找目的地  38是拖拽框宽度  20是拖拽框右侧到目的地最短的距离
    chk_y=abs_tgt_y-2           #-2 是把y值取到相对中间的位置

    #找目的地
    credit=0
    for _ in range(200):
        chk_x+=1
        clr=get_color(chk_x,chk_y)
        if clr[0]<100 and clr[1]<100 and clr[2]<100:    #目的地会有10个连续rgb<100的像素
            credit+=1
            if credit==10:
                break
        else:
            credit=0

    #print (credit,chk_x,chk_y)
    #print (clr)
    #print (chk_x-10-abs_tgt_x)
    start=[abs_tgt_x,abs_tgt_y]       #起始坐标
    destination=[chk_x-10,abs_tgt_y]    #结束坐标
    #print (destination)
    gui.moveTo(start[0],start[1],1)   #鼠标移动到起始
    gui.dragTo(destination[0], destination[1]+3, 2, gui.easeInOutQuad)  # 拖



lo()


