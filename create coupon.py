import random
import string
#123
print (random.choice(string.ascii_lowercase + string.ascii_uppercase))
#1111
a=lambda : ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(8))
dic ={}
'''
1

 '''
for _ in range(200):
    random_str=a()
    while random_str in dic:
        random_str = a()
    dic[random_str]=1
str='\n'.join(list(dic))

print(str)