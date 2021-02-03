def compareVersion( version1: str, version2: str):
    def get_chunk(str,p,n):
        if p>n-1:
            return 0,p
        p_end=p
        while p_end<n and str[p_end]!='.':
            p_end+=1
        i= str[p:p_end] if p_end<n-1 else str[p:]
        p=p_end+1
        return  int(i),p
    l1,l2=len(version1),len(version2)
    p1,p2=0,0
    while p1<l1 or p2 < l2:
        v1,p1=get_chunk(version1,p1,l1)
        v2,p2=get_chunk(version2,p2,l2)
        if v1!=v2:
            return 1 if v1>v2 else -1
    return 0



a=compareVersion(version1 = "1.20", version2 = "1.")

print(a)



