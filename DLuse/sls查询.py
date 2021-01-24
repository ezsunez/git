import gevent
from gevent import monkey

import requests
from lxml import etree
import pymssql
import time
import re

monkey.patch_all()
print('start')

cookie_str = r'AASP.NET_SessionId=uhwwvrury3coegmvjqddasve; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lvt_b82ebe24a82ff4d8775ffed071afe2bb=1611080191,1611376194; slnt-ex-iUser=1; Hm_lpvt_b82ebe24a82ff4d8775ffed071afe2bb=1611468287; userName=u_name=13941178777&u_cook=dcf51470-f404-48ad-9efc-0c1eb559a33e; .xf=4294A10DE4248A2FDF9C080373030C5C3552381806FA7517DF34DDA037AA46DF8D797E1E6B7E2E77C9BEA5DAFB4DEAC0139843E0F38EB5CB6209AB60C867F31C0A02027FA220D24064DD73C308EB35C76EE01D9D8B51498ADB34EEFFE8C8BF3E7E626305B3110376867570A732B27766C31B99AB3A799100EA316A41C14787FCAF7757630252CA97A650DC32AE1F5FF54FF485EAA7D1B5391BC79D91CB5DB908A4608C1B17BF6F59337F0115C558E4DD5644AEDEA5A4BA073E11352B50376C5D3DF81C578A3FC7432DACD4EEB9DD412AC93E6FDEAA3188AE6076452ACD6C34E3339CA151330BE706226613208E769738C89D675BBBB0AE1483F59488B93326843D7E15BDE753D96E5368AB3E89D2F2EAC23FA2A5C01E40BADB45776EC6A0AB80360F5B4F683FC337A35A7E639B5826EAFBF19F416778F89FA32AA3A800D58742143DD4D12AD4C618A5F9D6268C5555EFAACBCC7FDE498DDD77F3C00048B467D0AF128D778188293C081F298330EE762C2FECB05D95E28CE8F1BDD0B9D4DA2F57EF3F0BDE05CB57E8A4B9ACEA27665065DE9C2DB276EDD28100DA649E5B7B7B2A01A9313BA0758727A2202411C410D9021CF733AA'

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