import os
def cl (path):
    num_comm,num_space,num_code=0,0,0
    startcomment=False   # 多行缩进标识
    with open(path,'r',encoding='utf8') as f:
        lst_l= f.read().splitlines()
        for a in lst_l:
            if (a.startswith('#')):
                num_comm+=1
            elif(startcomment==True ):
                num_comm+=1
                if (a.strip().endswith("'''")):
                    startcomment=False
            elif(a.startswith("'''") and startcomment==False):
                num_comm+=1
                startcomment = True
                if (len(a.strip())>3 and a.strip().endswith("'''")):
                    startcomment=False
            elif (a.strip()==''):
                num_space+=1
            else:
                num_code+=1
    return  f'{path}\n注释：{num_comm}，空白:{num_space}，有效:{num_code}'
for root, dirs, files in os.walk(r'C:\Users\ezsun\Desktop\git', topdown=True):
    for i in files:
        if i.endswith('.py'):
            print(cl(os.path.join(root,i)))


# 2 1 12