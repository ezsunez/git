from selenium import webdriver
import requests
from lxml import etree
import pymssql,xlwt,time,sys,xlrd
from xlutils.copy import copy


print ('start')
startdate=input ('输入对账日期 例如：2021-01-29\n')
year_s, mon_s, day_s = startdate.strip(' ').split('-')
enddate=year_s+'-'+mon_s+'-'+str(int(day_s)+1)
log=startdate.strip(' ')+'报表\n'
timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
# with open(f'{startdate}-报表-{timestamp}.csv', 'w', encoding='utf8') as f:
#     f.write('\ufeff' + '\n')
style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'
font.height = 20*17
style.font = font
wbk=xlwt.Workbook(encoding='utf-8')
wbk.add_sheet(u'sheet1')
wbk.add_sheet(u'sheet2')
wbk.save(startdate+'report-'+timestamp+'.xls')

server = '.'
user = 'sa'
password = ''
# str_unicom='[unicom].'
str_unicom=''
lst_yys=[['联通','AccountUnicom2Netcom','unicomKM','联通卡密'],['移动','Account13800','mobileKM','13800卡密'],\
         ['移动10086','Account13800','mobile10086KM','13800卡密'],['电信','AccountUnicom2TelCom','telcom','电信卡密']]
lst_zjtype=['自家','自家卡密']
lst_sls=[['移动','0',['30','50','100']],['联通','1',['20','30','50','100']],['电信','2',['20','30','50','100']]]
lst_cards=[['移动','mobileKM',['30','50','100']],['移动10086','mobile10086KM',['30','50','100']],['联通','unicomKM',['20','30','50','100']],['电信','telcom',['20','30','50','100']]]

#检查过滤口导给自家的卡是否都已被导入卡库
def dbcompare(a=[],b=''):  #a:运营商列表  b:导自家种类列表
    global str_unicom
    str_sql='''select outtime,count(0) from  
                 (
                 select * from [dbo].[{}] 
                 where [to]='{}' and 
                 outtime between '{}' and '{}'
                 ) a  where not exists (select * from {}[dbo].[{}] b where a.sn=b.sn ) group by outtime'''.format(a[2],b,startdate.strip(' '),enddate,str_unicom,a[1].strip(' '))
    print (str_sql)
    with pymssql.connect(server, user, password, "ezuse") as conn:
    # with pymssql.connect(server, user, password, "newstock2020") as conn:
        with conn.cursor() as cursor:
            cursor.execute(str_sql)
            lst_mb = cursor.fetchall()
            global log
            if lst_mb:
                oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
                lastrow = oldexcel.sheets()[1].nrows
                newexcel = copy(oldexcel)
                sheet1 = newexcel.get_sheet(1)
                sheet1.write(lastrow+1, 0, '!!!!!!以下过滤口导出给{}的{}卡未入自家库!!!!!!!!'.format(b,a[0]),style)
                sheet1.write(lastrow + 2, 1, 'outtime',style)
                sheet1.write(lastrow + 2, 2, 'count',style)
                log+="!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                log+='以下过滤口导出给{}的{}卡未入自家库\nouttime,count\n'.format(b,a[0])
                tmpline=1
                for i in lst_mb:
                    log+="'"+str(i[0])+','+str(i[1])+'\n'
                    sheet1.write(lastrow + 2+tmpline, 1, str(i[0]),style)
                    sheet1.write(lastrow + 2+tmpline, 2, str(i[1]),style)
                    tmpline+=1
                # print(str(lst_mb[0][0]),lst_mb[0][1])
                sheet1.write(lastrow + 2 + tmpline, 0, '可用查询语句：',style)
                sheet1.write(lastrow + 2 + tmpline, 7,str_sql.replace('outtime,count(0)', '*').replace('group by outtime', ''))
                newexcel.save(startdate + 'report-' + timestamp + '.xls')
                log+='可用查询语句：\n'+str_sql.replace('outtime,count(0)','*').replace('group by outtime','')+'\n'
                log += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            else:
                oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
                lastrow = oldexcel.sheets()[1].nrows
                newexcel = copy(oldexcel)
                sheet1 = newexcel.get_sheet(1)
                sheet1.write(lastrow + 1, 0, '此日过滤口导出给{}的{}卡已全部入库'.format(b,a[0]),style)
                newexcel.save(startdate + 'report-' + timestamp + '.xls')
                log+='此日过滤口导出给{}的{}卡已全部入库\n'.format(b,a[0])
    # print(log)

#抓取手拉手上传的数量
def sls():
    dict_count = {}
    driver = webdriver.Chrome()
    driver.get('http://www1.slswd.com/Static/0001/Index5.htm')
    time.sleep(3)
    driver.find_element_by_id("UserName").send_keys("13941178777")
    driver.find_element_by_id("Password").send_keys("1234567890q")
    driver.find_element_by_id("A1").click()
    c = driver.get_cookies()
    driver.close()
    cookie = [item["name"] + "=" + item["value"] for item in c]
    cookie_str = '; '.join(item for item in cookie)
    cookies = dict([l.split("=", 1) for l in cookie_str.split("; ")])
    for types in lst_sls:
        dict_count[types[0]] = {}
        for amount in types[2]:
            data = {
                '__VIEWSTATE': '',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                # 'txtCardNo': sn,
                'drpISP': types[1],
                'ddState': '',
                'txtStartTime': startdate,
                'txtEndTime': startdate,
                # 'txtPCNumber': '',
                # 'ddVerifyState': '',
                'txtCardAmount': amount,
                'btnQuery': '查询',
                'PageInf_input': '1'
            }
            r = requests.post('http://www1.slswd.com/ClientNew/CardNoKaKuList.aspx', cookies=cookies, data=data)
            root = etree.HTML(r.text)
            lst1 = root.xpath('//div[@id="PageInf"]/descendant::b/text()')
            time.sleep(8)
            count = lst1[0]
            dict_count[types[0]][amount]=count
            print(count)
    return dict_count

#手拉手上传的数量与过滤口导出的数量对比
def glksls(dic_from_sls={}):
    str_insert=''
    global log
    for types in dic_from_sls.keys():
        for amount in dic_from_sls[types].keys():
            str_insert+=" select '{}','{}','{}' union".format(types,amount,dic_from_sls[types][amount])
    str_insert=str_insert.strip('union')
    str_tmp='''create table ##Tmp --创建临时表#Tmp
                (
                    cardtype   varchar(50),  
                    amount  varchar(50),   
                    countnum  varchar(50), 
                )
                '''
    str_tmp_insert = ''' insert ##Tmp
                       {a}
                       '''.format(a=str_insert)
    str_sql='''select 
                a.cardtype as N'手拉手种类',
                a.amount as N'手拉手面值',
                a.countnum as N'手拉手数量',
                isnull(b.[counts],0) as N'过滤口导出数量',
                a.countnum - isnull(b.[counts],0) as N'差额=手拉手上传数量-过滤口导出 负数为过滤口导出后未上传'
                from ##Tmp a 
                left join 
                (
                SELECT N'联通'as type, REPLACE(amount,'.00','') as amount,[to],count(0) as [counts] from [dbo].unicomKM 
                where outtime between '{b}' and '{c}'  and [to]='手拉手'
                group by amount,[to]
                union
                SELECT N'电信'as type, amount,[to],count(0) as [counts] from [dbo].telcom 
                where outtime between '{b}' and '{c}'  and [to]='手拉手'
                group by amount,[to]
                union
                SELECT N'移动'as type, amount,[to],count(0) as [counts] from [dbo].mobileKM 
                where outtime between '{b}' and '{c}'   and [to]='手拉手'
                group by amount,[to]
                ) b  on a.amount=b.amount and b.type=a.cardtype 
                where a.countnum<>0 or isnull(b.[counts],0) <>0
                order by a.cardtype ,a.amount
                '''.format(b=startdate,c=enddate)
    # print(str_tmp)
    # print(str_sql)
    with pymssql.connect(server, user, password, "ezuse") as conn:
    # with pymssql.connect(server, user, password, "newstock2020") as conn:
        with conn.cursor() as cursor:
            cursor.execute(str_tmp)
            cursor.execute(str_tmp_insert)
            conn.commit()
            cursor.execute(str_sql)
            lst_mb = cursor.fetchall()
            titles=cursor.description
            oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
            rows=oldexcel.sheets()[1].nrows
            newexcel = copy(oldexcel)
            sheet1 = newexcel.get_sheet(1)
            tmpcount=1
            if lst_mb:
                for t in titles:
                    sheet1.write(rows, tmpcount, t[0],style)
                    tmpcount+=1
                    log +=t[0]+','
                log+='\n'
                tmprows=1
                for i in lst_mb:
                    tmpcol=1
                    for j in i:
                        sheet1.write(rows+tmprows, tmpcol, str(j.encode('latin-1').decode('gbk')).strip(' ') if type(j)== type('a') else str(j).strip(' '),style)
                        log +=  str(j.encode('latin-1').decode('gbk')).strip(' ')  + ',' if type(j)== type('a') else str(j).strip(' ') +','
                        tmpcol+=1
                    log +='\n'
                    tmprows+=1
            else:
                writexls('此日手拉手未卖卡')
                log+='此日手拉手未卖卡\n'
            newexcel.save(startdate + 'report-' + timestamp + '.xls')
    # print(log)

#过滤口导自家与卡库入卡对比
def detail_to_zijia(tlist=[]):
    global log, str_unicom
    str_10086_sql='and len(account)=22' if tlist[0]=='移动10086' else 'and len(account)<22'
    str_10086_sql='' if '移动' not in tlist[0] else str_10086_sql
    str_sql = f'''
                    select '{tlist[0]}' as [种类],* from (
                    select 
                    case when a.[amount] is null then b.[amount] else a.[amount] end as [过滤口面值] ,
                    case when a.[to] is null then b.[to] else a.[to] end as [导给] ,
                    isnull(a.[过滤口数量],0)as [过滤口数量],
                    --case when b.[amount] is null then a.[amount] else b.[amount] end as [卡库面值] ,
                    --case when b.[to] is null then a.[to] else isnull(b.[to],'') end as [自家to] ,
                    isnull(b.[自家卡库数量],0)as [自家卡库数量] ,
                    isnull(b.[自家卡库数量],0)-isnull(a.[过滤口数量],0)  as [差额=自家卡库-过滤口导出 负数为过滤口导出后未进自家卡库]
                    from (
                    SELECT REPLACE(RTRIM(amount),'.00','') as amount,[to],count(0) as '过滤口数量' from [dbo].[{tlist[2]}] 
                    where outtime between '{startdate}' and '{enddate}'  and [to] in ('自家','自家卡密') 
                    group by amount,[to]
                    ) a 
                    full join
                    (SELECT amount,'自家'as [to],count(0)as '自家卡库数量' from {str_unicom}[dbo].[{tlist[1]}]
                    where Createtime between '{startdate}' and '{enddate}' 
                    {str_10086_sql}
                    group by amount
                    union
                    SELECT amount,'自家卡密'as [to],count(0)as '自家卡库数量' from {str_unicom}[dbo].[AccountPswOnline]
                    where Createtime between '{startdate}' and '{enddate}'  and Classname='{tlist[3]}' {str_10086_sql}
                    group by amount
                    ) b 
                    on a.[to]=b.[to] and a.amount=b.amount
                    ) f
                    order by cast([过滤口面值] as int)
'''.format()
    print(str_sql)
    with pymssql.connect(server, user, password, "ezuse") as conn:
    # with pymssql.connect(server, user, password, "newstock2020") as conn:
        with conn.cursor() as cursor:
            cursor.execute(str_sql)
            lst_mb = cursor.fetchall()
            titles = cursor.description
            oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
            rows=oldexcel.sheets()[1].nrows
            newexcel = copy(oldexcel)
            sheet1 = newexcel.get_sheet(1)
            if lst_mb:
                tmpcount=1
                for t in titles:
                    sheet1.write(rows, tmpcount, t[0],style)
                    sheet1.col(tmpcount).width = 256 * (len((t[0]).encode('utf8')) + 7)
                    tmpcount+=1
                    log += t[0] + ','
                log += '\n'
                tmprow=1
                for i in lst_mb:
                    tmpcol=1
                    for j in i:
                        sheet1.write(rows+tmprow, tmpcol, str(j.encode('latin-1').decode('gbk')).strip(' ')  if type(j) == type('a') else \
                            str(j).strip(' ') ,style)
                        tmpcol+=1
                        log += str(j.encode('latin-1').decode('gbk')).strip(' ') + ',' if type(j) == type('a') else \
                            str(j).strip(' ')  + ','
                    log += '\n'
                    tmprow+=1
            else:
                writexls(f'此日{tlist[0]}未向自家导卡')
                log += f'此日{tlist[0]}未向自家导卡\n'
            newexcel.save(startdate + 'report-' + timestamp + '.xls')
    # print(log)

#过滤口卖给别家的卡明细
def detail_to_others():
    global log
    str_sql=f'''
                select '联通'as [种类],REPLACE(amount,'.00','') as [面值],[to],count(0) as counts from [dbo].[unicomKM] where outtime between '{startdate}' and '{enddate}'
                and [to] not in ('手拉手','自家','自家卡密')
                group by [to],amount
                union 
                select '移动'as [种类],[to],amount,count(0) as counts from [dbo].mobileKM where outtime between '{startdate}' and '{enddate}'
                and [to] not in ('手拉手','自家','自家卡密')
                group by [to],amount
                union
                select '联通'as [种类],[to],amount,count(0) as counts from [dbo].telcom where outtime between '{startdate}' and '{enddate}'
                and [to] not in ('手拉手','自家','自家卡密')
                group by [to],amount
                union
                select '移动10086'as [种类],[to],amount,count(0) as counts from [dbo].mobile10086KM where outtime between '{startdate}' and '{enddate}'
                and [to] not in ('手拉手','自家','自家卡密')
                group by [to],amount
    '''
    with pymssql.connect(server, user, password, "ezuse") as conn:
    # with pymssql.connect(server, user, password, "newstock2020") as conn:
        with conn.cursor() as cursor:
            cursor.execute(str_sql)
            lst_mb=cursor.fetchall()
            titles = cursor.description
            oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
            rows=oldexcel.sheets()[1].nrows
            newexcel = copy(oldexcel)
            sheet1 = newexcel.get_sheet(1)
            if lst_mb:
                tmpcount=1
                for t in titles:
                    sheet1.write(rows, tmpcount, t[0],style)
                    tmpcount+=1
                    log += t[0] + ','
                log += '\n'
                tmprows=1
                for i in lst_mb:
                    tmpcol=1
                    for j in i:
                        sheet1.write(rows+tmprows, tmpcol, str(j.encode('latin-1').decode('gbk')).strip(' ') if type(j) == type('a') else \
                            str(j).strip(' '),style)
                        tmpcol+=1
                        log += str(j.encode('latin-1').decode('gbk')).strip(' ') + ',' if type(j) == type('a') else \
                            str(j).strip(' ') + ','
                    log += '\n'
                    tmprows+=1
            else:
                writexls(f'此日未对外卖卡')
                log += f'此日未对外卖卡\n'
            newexcel.save(startdate + 'report-' + timestamp + '.xls')

lst_allcard=[]
def detail_all(all_cards=[]):
    global lst_allcard
    str_tmp='''create table ##Col (cols nvarchar(50))'''
    str_tmp_insert=f''' insert ##Col 
                        select [to] from [dbo].[mobileKM]  where outtime between '{startdate}' and '{enddate}'
                        group by [to]
                        union
                        select [to] from [dbo].[mobile10086KM]  where outtime between '{startdate}' and '{enddate}'
                        group by [to]
                        union
                        select [to] from [dbo].[telcom]  where outtime between '{startdate}' and '{enddate}'
                        group by [to]
                        union
                        select [to] from [dbo].[unicomKM]  where outtime between '{startdate}' and '{enddate}'
                        group by [to]
    '''
    str_getcols='select * from ##Col order by cols desc'
    with pymssql.connect(server, user, password, "ezuse") as conn:
    # with pymssql.connect(server, user, password, "newstock2020") as conn:
        with conn.cursor() as cursor:
            cursor.execute(str_tmp)
            cursor.execute(str_tmp_insert)
            conn.commit()
            cursor.execute(str_getcols)
            cols = cursor.fetchall()
            oldexcel = xlrd.open_workbook(startdate+'report-'+timestamp+'.xls',formatting_info=True)
            newexcel = copy(oldexcel)
            sheet1=newexcel.get_sheet(0)
            sheet1.write(0, 0, startdate + '报表', style)
            sheet1.write(1, 0, '昨日过滤口剩余', style)
            sheet1.write(2, 0, '昨日实卡剩余', style)
            sheet1.write(3, 0, '今日8-30', style)
            for i in range(len(cols)):
                sheet1.write(i + 4,0,cols[i][0].strip(' '),style)
            sheet1.write(len(cols) + 4, 0, '今日过滤口剩余', style)
            sheet1.write(len(cols) + 5, 0, '今日实卡剩余', style)
            sheet1.write(len(cols) + 6, 0, '今日理论剩卡', style)
            sheet1.write(len(cols) + 7, 0, '差额', style)
            sheet1.write(len(cols) + 8, 0, '实际-理论', style)
            sheet1.write(len(cols) + 9, 0, '负数是少卡', style)
            startcol=1
            for i in all_cards:
                for j in i[2]:
                    str_sql = f'''
                                    select isnull(counts,0) as counts from 
                                    ##Col a left join 
                                    (select [to], count(0)as counts from [{i[1]}] where outtime between '{startdate}' and '{enddate}'  and REPLACE(amount,'.00','')='{j}'
                                    group by [to])b on a.[cols]=b.[to]    order by a.cols desc      
                            '''
                    cursor.execute(str_sql)
                    results=cursor.fetchall()
                    sheet1.col(startcol).width = 256 * (len((i[0]+'-'+j).encode('utf8'))+7)
                    sheet1.write(0, startcol, i[0]+'-'+j,style)
                    for k in range(len(results)):
                        sheet1.write(k + 4, startcol, results[k][0],style)
                    str_index = 'ABCDEFGHIJGLMNOPQRSTUVWXYZ'
                    endline=4+len(results)
                    str_formula = 'sum({a}2:{a}4)-sum({a}5:{a}{b})'.format(a=str_index[startcol],b=endline)
                    sheet1.write(len(results) + 6, startcol, xlwt.Formula(str_formula), style)
                    str_formula='sum({a}{b}:{a}{c})-{a}{d})'.format(a=str_index[startcol],b=endline+1,c=endline+2,d=endline+3)
                    sheet1.write(len(results) + 7, startcol, xlwt.Formula(str_formula), style)
                    startcol+=1
            sheet1.col(0).width = 256 * (len('昨日过滤口剩余'.encode('utf8'))+3)
            newexcel.save(startdate + 'report-' + timestamp + '.xls')



def writexls(a):
    oldexcel = xlrd.open_workbook(startdate + 'report-' + timestamp + '.xls',formatting_info=True)
    rows = oldexcel.sheets()[1].nrows
    newexcel = copy(oldexcel)
    sheet1 = newexcel.get_sheet(1)
    sheet1.write(rows, 0, a,style)
    newexcel.save(startdate + 'report-' + timestamp + '.xls')





for types in lst_zjtype:
    for yys in lst_yys:
        dbcompare(yys,types)
writexls('*********************************************')
log+='*********************************************\n'
for yys in lst_yys:
    detail_to_zijia(yys)
    writexls('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    log += '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
writexls('*********************************************')
log+='*********************************************\n'
detail_to_others()
writexls('*********************************************')
log+='*********************************************\n'
# dict_sls_count=sls()
dict_sls_count={'移动': {'30': '200', '50': '0', '100': '0'}, '联通': {'20': '0', '30': '500', '50': '0', '100': '10'}, '电信': {'20': '100', '30': '0', '50': '0', '100': '0'}}
glksls(dict_sls_count)
writexls('*********************************************')
log+='*********************************************\n'
detail_all(lst_cards)

print('done')
# with open(f'{startdate}-报表-{timestamp}.csv','a',encoding='utf8') as f:
#     f.write(log)
while True:
    pass