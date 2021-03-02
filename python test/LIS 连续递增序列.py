
#  Longest increasing subsequence

def lee(A):
    W = len(A[0])
    dp= [1 for _ in range(len(A[0]))]
    for i in range(W-2,-1,-1):
        for j in range(i+1,W):
            if all(r[i]<r[j] for r in A):
                dp[i]=max(dp[i],1+dp[j])
    return W-max(dp)


print (lee(["ghi","def","abc"]))