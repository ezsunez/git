import random
import string

a=lambda : ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(8))
dic ={}
for _ in range(200):
    random_str=a()
    while random_str in dic:
        random_str = a()
    dic[random_str]=1
str='\n'.join(list(dic))
print(str)