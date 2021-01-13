
import os
path= input('input your path \n')
keyword=input('input your keywords \n')

print('**********')

for root, dirs, files in os.walk(path, topdown=True):
    for name in dirs:
        if (keyword in name):
            print(os.path.join(root, name))
    for name in files:
        if (keyword in name):
            print(os.path.join(root, name))
        else:
            try:
                with open(os.path.join(root,name)) as f:
                    for l in f :
                        if (keyword in l):
                            print(os.path.join(root, name))
                            break

            except:
                continue