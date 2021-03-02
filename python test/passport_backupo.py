from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import winsound
import requests
import random

driver = webdriver.Chrome()
driver.get('https://ppt.mfa.gov.cn/appo/index.html')
time.sleep(3)
driver.find_element_by_id("continueReservation").click()
time.sleep(2)
driver.find_element_by_id("recordNumberHuifu").send_keys("202101200294740")
driver.find_element_by_id("answerHuifu").send_keys("YANG CHUNHUI")
s1 = Select(driver.find_element_by_id('questionIDHuifu'))
s1.select_by_index(1)
driver.find_element_by_xpath('//span[contains(text(),"提交")]').click()
time.sleep(3)
driver.find_element_by_id("myButton").click()
time.sleep(2)
timesleep=20
while True:
    driver.find_element_by_xpath('//span[contains(text(),"确认")]').click()
    time.sleep(2)
    for _ in range(3):
        driver.find_element_by_xpath("//span[@class='ui-icon ui-icon-circle-triangle-e']").click()
    s1 = Select(driver.find_element_by_id('address'))
    if s1:
        s1.select_by_index(2)
        time.sleep(2)
    else:
        time.sleep(20)
        continue
    current_window = driver.current_window_handle
    lst_date=driver.find_elements_by_xpath("//span[@class='fc-event-title']")
    lst_date=[x for x in lst_date if x.text.split('/')[0]<=x.text.split('/')[1]][-1::-1]
    for i in lst_date:
        i.click()
        time.sleep(1)
        all_windows = driver.window_handles  # 获取所有窗口handle name
        # 切换window，如果window不是当前window，则切换到该window
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
        # title=driver.title
        # driver.execute_script(f"document.title='5-1-{title}'")
        # lst_btn=driver.find_elements_by_xpath('''//input[contains(@onclick,"'/appo','undefined','undefined','undefined','undefined','undefined'")]''') #no limit
        lst_btn = driver.find_elements_by_xpath('''//input[contains(@onclick,"180','undefined','0','597','29','0','0','0','1'")]''') # 210 or 180

        if len(lst_btn)==0:
            driver.close()
            timesleep = 2
            driver.switch_to.window(current_window)
            continue
        ele_btn=lst_btn[0]
        a=ele_btn.get_attribute('disabled')
        if not ele_btn or a =='true':
            driver.close()
            driver.switch_to.window(current_window)
            timesleep=2
            winsound.Beep(300, 100)
            continue
        subwndow_1=driver.current_window_handle
        ele_btn.click()
        # while True:
        #     winsound.Beep(300, 100)
        time.sleep(1)
        for window in driver.window_handles:
            if window != current_window and window!=subwndow_1:
                driver.switch_to.window(window)
        # while True:
        #     for _ in range(5):
        #         ele_img=driver.find_element_by_xpath("//img[@class='yidun_bg-img']").get_attribute('src')
        #         print(ele_img)
        #         if ele_img!=None:
        #             break
        #         time.sleep(2)
        #     r = requests.get(ele_img)
        #     timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        #     with open(f'./img/{timestamp}.jpg', 'wb') as f:
        #         f.write(r.content)
        #     # interval=random.randint(2,6)
        #     time.sleep(1)
        #     driver.refresh()
        #     # interval = random.randint(8, 20)
        #     time.sleep(2)
        #     # print(driver.page_source)
    time.sleep(timesleep)
    driver.get('https://ppt.mfa.gov.cn/appo/page/reservation.html')
    time.sleep(2)









# all_windows = driver.window_handles  # 获取所有窗口handle name
# # 切换window，如果window不是当前window，则切换到该window
# for window in all_windows:
#     if window != current_window:
#         driver.switch_to.window(window)
# print(driver.page_source)

# input('123')
# driver.get('https://ppt.mfa.gov.cn/appo/page/reservation.html')
# time.sleep(3)