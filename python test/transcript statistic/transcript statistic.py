list_attributes=[]    #第一行
list_students=[]    #剩余行
sum_all_class =0      #累计所有学生所有课程的总分

def totalscore(l,lines):  #处理分数 l为分数的list lines为参数判断传入的是第几行学生
    sum_student=0
    global sum_all_class
    for i in range(len(l)):
        list_class_average[i]+=int(l[i])                #累计平均行的各科目总分
        if(lines==len(list_students)-1):                 #判断l是否为最后一个学生的成绩
            sum_all_class+=list_class_average[i]        #累加所有学生所有课程的总分以算平均行的总分及平均分
            list_class_average[i]=format(list_class_average[i]/len(list_students),'.1f')   #将平均行中的值转换为各科目全体学生的平均分
            if (float(list_class_average[i]) < 60):
                list_class_average[i] = '不及格'  # 判断不及格
        sum_student += int(l[i])  # 累计学生的总分
        if (int(l[i]) < 60):
            l[i] = '不及格'  # 判断不及格
    return l+[str(sum_student),str(format(sum_student/len(l),'.1f'))+'\n']          #返回处理好的学生分数list

try:
    with open('report.txt', encoding='utf8') as f:
        list_attributes = ['名次'] + f.read().splitlines()[0].split(' ') + ['总分', '平均分\n']  # 获得第一行
        list_class_average=[0]*len(list_attributes[2:-2])                               #定义list存储平均行数据 长度为科目的数量
        # print(list_attributes,'\n',type(list_attributes))
        f.seek(0)
        list_students = str(f.read().splitlines()[1:])[1:-1].replace("'", '').split(', ')  # 获得剩余行list，并处理多余符号
        for i in range(len(list_students)):
            list_students[i] = list_students[i].split(' ')  # 转为list嵌套list
            list_students[i] = list_students[i][0:1] + totalscore(list_students[i][1:],i)  # 获得处理好的分数
except Exception as e:
    print('Error:',e)
list_average=['平均']+list_class_average+\
             [format(sum_all_class/len(list_students),'.1f')]+\
             [format((sum_all_class/len(list_students))/len(list_attributes[2:-2]),'.1f')+'\n']
#整理平均行的数据  平均行总分=所有学生的总分/学生人数   平均行平均分=所有学生总分/学生人数/科目数量
list_students=sorted(list_students,key=lambda x:-int(x[-2]))                #按总分从高到低排序生成新list
list_students.insert(0,list_average)                                        #插入平均行
#print(list_students, '\n', type(list_students[1]))
try:
    with open('result.txt', 'w', encoding='utf8') as f:                     # 写文件
        f.write(' '.join(list_attributes))
        for i in range(len(list_students)):
            f.writelines(' '.join([str(i)]+list_students[i]))            #加入排名
except Exception as e:
    print('Error:',e)
finally:
    print('DONE')


