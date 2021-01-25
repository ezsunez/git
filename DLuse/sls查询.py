import gevent
from gevent import monkey

import requests
from lxml import etree
import pymssql
import time
import re
from selenium import webdriver


monkey.patch_all()
print('start')
driver = webdriver.Chrome()
driver.get('http://www1.slswd.com/Static/0001/Index5.htm')
time.sleep(3)
driver.find_element_by_id("UserName").send_keys("")
driver.find_element_by_id("Password").send_keys("")
driver.find_element_by_id("A1").click()
c = driver.get_cookies()
driver.close()
cookie = [item["name"] + "=" + item["value"] for item in c]
cookie_str = '; '.join(item for item in cookie)


# cookie_str = r'slnt-ex-iUser=1; .xf=4AD8AB80BD59DE1E962826875BAB23A109B4F2D1A5D0F2576D993F6820F9B4DB60409F5EF52A7F9A14EC8B07D80F0B3FFC7523DF36820B2C611DCC723F0CB8AC8610F2B39F3AF46A64CE789150F7FC5085E8FB84E25586A9C5D2039708B0850FBC9B03FA3CB85DC56F9082DED3EDAED92EC3FC95384AB5E4D4F91975E1D610EA852D4FAF90CB2280787ACC8DE81C045999404B54270BB3B894F2DDC1141111C52BD4D34A151E43E487DCF2CE53AEC328A5F444B5A11D352F213CF6314DF1F559F6941029869FCF5A28DAC5BA3A0982036D72C0E29F630DD9E039739978C880327379BF9AD4F6EA7824D8EE3DAB2B5E5AFAB84E32D14A6595B730FC975E5102CBEE715C9550046529D8019F0C8E3CC734FB339640951478B1E10B1766BCF22EF26E247F72F2A64428E7DCB95EA6061F58DDB3DC25BD603B4A29CC5E9F2006CB052191BEBA2A964FD546E20B2DD7582A8993628442273D5035A7DF471C8409DFC7F895D41C0FB6950B2821ACBCDC169DAFA3549C42F55B7A445E28926C56E37F834C829C4515F1C3EFFE5EBE8D51CD36FFB8DE739B68D4A90724675AC5C310B61EF1423A45DB3CF60B9986952D6AF33DCFCC4DC8FF; Hm_lpvt_b82ebe24a82ff4d8775ffed071afe2bb=1611572291; Hm_lvt_b82ebe24a82ff4d8775ffed071afe2bb=1611572291; userName=u_name=13941178777&u_cook=3f5bdffa-cf23-4f2a-ae11-35c0e90d75b2; ASP.NET_SessionId=4y1oim55zoa54zybr4i1fo45'

str_date = '2021-01-23'
cookies = dict([l.split("=", 1) for l in cookie_str.split("; ")])
data = {
    '__VIEWSTATE': '',
    '__EVENTTARGET': 'PageInf',
    '__EVENTARGUMENT': '1',
    # 'txtCardNo': sn,
    # 'drpISP': '',
    'ddState': '1',
    'txtStartTime': str_date,
    'txtEndTime': str_date,
    # 'txtPCNumber': '',
    # 'ddVerifyState': '',
    # 'txtCardAmount': '',
    # 'btnQuery': '查询',
    'PageInf_input': '1'
}
r = requests.post('http://www1.slswd.com/ClientNew/CardNoKaKuList.aspx', cookies=cookies, data=data)
root = etree.HTML(r.text)
lst1 = root.xpath('//input[@name="__VIEWSTATE"]/attribute::value')
viewstate = lst1[0]
lst1 = re.findall('(?<=<b>1/)\d*?(?=</b>)', r.text)
page_num = lst1[0]  # 总页数
lstsn = []
logs = ''


def func(page):
    data = {
        '__VIEWSTATE': viewstate,
        '__EVENTTARGET': 'PageInf',
        '__EVENTARGUMENT': page,
        'ddState': '1',
        'txtStartTime': str_date,
        'txtEndTime': str_date,
        'PageInf_input': '1'
    }
    global lstsn, logs
    try:
        rsn = requests.post('http://www1.slswd.com/ClientNew/CardNoKaKuList.aspx', cookies=cookies, data=data)

        ls = re.findall('当前第[\s\S]*?</b>页', rsn.text)
        # ls1 = re.findall('(\d{5,}?(?=<br />))|(?<=<td>\s{5,})(电信|联通|移动)', rsn.text)
        ls1 = re.findall('\d{5,}?(?=<br />)', rsn.text)
        lstsn += ls1
        logs += '**************\n' + ls[0] + '成功' + '\n**************\n'
        print('**************\n', ls[0])
    except Exception as e:
        logs += '!!!!!!!!!!!!!\n' + page + '失败--' + e + '\n'
        # print(page,'失败',e)


def async_func():
    """
    协程运行函数
    """
    print('async:\tON')
    # gevent.joinall([gevent.spawn(func, u) for u in range(1, 5)])
    gevent.joinall([gevent.spawn(func, u) for u in range(1, int(page_num) + 1)])


async_func()
timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
# func(200)
with open(f'{timestamp}-logs.txt','w',encoding='utf8') as f:
    f.write(logs)
# print(logs)
with open(f'{timestamp}-sn.txt','w',encoding='utf8') as f:
    f.write('\n'.join(lstsn))
# print(lstsn)

lst_dx = [x for x in lstsn if len(x) == 19]
lst_lt = [x for x in lstsn if len(x) == 15]
lst_yd = [x for x in lstsn if len(x) == 17]
server = '.'
user = 'sa'
password = ''
lst_sql = []
lst_sql.append(
    "update telcom set issold='{}' where isnull(issold,'') ='' and sn in ('{}') ".format('手拉手成功-' + timestamp + '|',
                                                                                         "','".join(lst_dx)))
lst_sql.append(
    "update mobileKM set issold='{}' where isnull(issold,'') ='' and sn in ('{}') ".format('手拉手成功-' + timestamp + '|',
                                                                                         "','".join(lst_yd)))
lst_sql.append(
    "update unicomKM set issold='{}' where isnull(issold,'') ='' and sn in ('{}') ".format('手拉手成功-' + timestamp + '|',
                                                                                         "','".join(lst_lt)))

try:
    with pymssql.connect(server, user, password, "ezuse") as conn:
        with conn.cursor() as cursor:
            for i in lst_sql:
                try:
                    cursor.execute(i)
                    conn.commit()
                    with open(f'{timestamp}-logs.txt', 'a', encoding='utf8') as f:
                        f.write('成功 '+i+'\n')
                except Exception as e:
                    with open(f'{timestamp}-logs.txt', 'a', encoding='utf8') as f:
                        f.write('!!!!失败-' + i + '--' + str(e)+'\n')
except Exception as e:
    with open(f'{timestamp}-logs.txt', 'a', encoding='utf8') as f:
        f.write('!!!!失败--'+str(e)+'\n')
finally:
    print('done')