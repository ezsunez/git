import re
import requests
import threading
def sw(city):
    req = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=%s' %city )
    dic_city = req.json()

    city_data = dic_city.get('data')  # 没有’data‘的话返回 []
    print(city_data.get('city'))

    if city_data:
        city_forecast = city_data['forecast'][0]  # 下面的都可以换成'get'方法
        print(city_forecast.get('date'))
        print(city_forecast.get('high'))
        print(city_forecast.get('low'))
        print(city_forecast.get('type'))
    else:
        print('未获得')
thread=[]
citys=['北京', '南京', '上海', '深圳', '广州', '杭州', '苏州', '天津', '西安', '成都']
#citys=['北京']
for i in range(len(citys)):
    t = threading.Thread(target=sw,args=(citys[i],))
    thread.append(t)
for i in thread:
    i.start()
for i in thread:
    i.join()
print('111111111111111')