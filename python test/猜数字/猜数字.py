import os
import re
import requests

dict_records={}

class file:
    def initial(self):    #处理record文件
        if (os.path.exists('record.txt')):
            f = open('record.txt', 'r', encoding='utf8')
            global dict_records  #字典储存用户数据 dictionary<list>
            lst_records = f.read().splitlines()
            lst_name = []
            lst_value = []
            for i in range(len(lst_records)):
                lst_name.append(lst_records[i].split(' ')[0])   #取出名字作为 key
                lst_value.append([i] + lst_records[i].split(' '))   # 行号+人名+成绩行程list作为 value
            dict_records = dict(zip(lst_name, lst_value))
            f.close()
        else:
            open('record.txt', 'w', encoding='utf8')   #如文件不存在则新建
    def write(self,name): # 文本写入
        file().initial()  #得到最新的记录
        if (name in dict_records):  #判断是否有过记录
            with open('record.txt', 'r', encoding='utf8') as f:
                lineNo = dict_records[name][0]  #得到旧记录行号
                str = ''
                l = f.readlines()
                for i in range(len(l)):
                    if (i != lineNo):
                        str += l[i]
            with open('record.txt', 'w', encoding='utf8') as f:
                f.write(str + player.creat_record())    #重写文本 除去旧记录添加新记录
        else:
            with open('record.txt', 'a', encoding='utf8') as f:
                n='\n'
                if(len(dict_records)==0):
                    n=''
                f.write(n + player.creat_record())  #如没有旧记录则直接添加

class user:   #用户成绩的操作类
    def __init__(self,lst_infor):
        self.name=lst_infor[0]
        self.games=int(lst_infor[1])
        self.best=int(lst_infor[2])
        self.avg=float(lst_infor[3])
    def __str__(self):
        return f'{self.name}，你已经玩了{self.games}次，最少{self.best}轮猜出答案，平均{self.avg}轮猜出答案。'
    def compute_score(self,rounds):  #计算分数
        self.best=rounds if self.best ==0 or rounds<self.best else self.best
        self.avg=round((self.avg*self.games+rounds)/(self.games+1),1)
        self.games += 1
    def creat_record(self):   #生成记录
        return f'{self.name} {self.games} {self.best} {self.avg}'

file().initial()
#print(dict_records)
while True:
    name = input('请输入用户名，用户名不可包含空格')
    if  re.match('\S*\s+\S*', name) or name=='':
        print('错误：检测到不合规用户名，请尝试其他')
    else:
        break
if(name in dict_records):  #如果曾有记录
    player=user(dict_records[name][1:])
    print(player)  #输出以往成绩
else:
    player=user([name,'0','0','0'])
    print(player)
while True:
    if (input('输入y开始游戏，其他退出')!='y'):
        print('退出游戏，欢迎再来')
        break
    r = requests.get('https://python666.cn/cls/number/guess/')
    answer=int(r.text)
    print (answer)
    rounds=0  #游戏轮数
    while True:
        while True:
            guess = input('猜一个1-100的数字，请输入')
            if re.match('.*\D', guess) or guess=='':
                print('错误：只能输入数字')
            else:
                guess=int(guess)
                break
        rounds+=1
        if (guess < answer):
            print('太小了，再猜一次')
        elif (guess > answer):
            print('太大了，再猜一次')
        else:
            player.compute_score(rounds)  #计算成绩
            print('正确,你一共猜了%s轮' %rounds)
            print(player)  #显示成绩
            file().write(name)  #写入文件
            break






