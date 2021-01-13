list_attributes=[]    #第一行
list_students=[]    #剩余行

def totalscore(l):  #处理分数 l为分数的list
    sum=0
    for i in range(len(l)):
        sum+=int(l[i])          #累计总分
        if (int(l[i])<60):
            l[i]='不及格'        #判断不及格
    return l+[str(sum),str(format(sum/len(l),'.1f'))+'\n']          #返回处理好的分数list

try:
    with open('report.txt', encoding='utf8') as f:
        list_attributes = ['名次'] + f.read().splitlines()[0].split(' ') + ['总分', '平均分\n']  # 获得第一行
        # print(list_attributes,'\n',type(list_attributes))
        f.seek(0)
        list_students = str(f.read().splitlines()[1:])[1:-1].replace("'", '').split(', ')  # 获得剩余行list，并处理多余符号
        for i in range(len(list_students)):
            list_students[i] = list_students[i].split(' ')  # 转为list嵌套list
            list_students[i] = list_students[i][0:1] + totalscore(list_students[i][1:])  # 获得处理好的分数
except Exception as e:
    print('Error:',e)

list_students=sorted(list_students,key=lambda x:-int(x[-2]))                #按总分从高到低排序生成新list
#print(list_students, '\n', type(list_students[1]))
try:
    with open('result.txt', 'w', encoding='utf8') as f:                     # 写文件
        f.write(' '.join(list_attributes))
        for i in range(len(list_students)):
            f.writelines(' '.join([str(i+1)]+list_students[i]))            #加入排名
except Exception as e:
    print('Error:',e)
finally:
    print('DONE')


