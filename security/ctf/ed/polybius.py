import itertools

s="abcdefghijklmnopqrstuvwxy"
sumResult=[]
numSumResult=[]
ciper="1432145551541131233313542541343435232145215423541254443122112521452323"
for i in itertools.permutations(s,25):#找出所有全排列
    key = "".join(i)
    keyMap = [key[0:5], key[5:10], key[10:15], key[15:20], key[20:25]]
    result = ''
    for i in range(0, (len(ciper)-2), 2):
        alpha = keyMap[int(ciper[i])][int(ciper[i + 1])]
        print(alpha)
        result = result + alpha
    print(result)

# for i in sumResult:
#     temp=""
#     for j in ciper:
#         temp+=str(i.index(j)+1)
#     numSumResult.append(temp)
# for i in numSumResult:
#     ans_=""
#     for j in range(0, len(i),2):
#         xx=(int(i[j])-1)*5+int(i[j+1])+96
#         if xx>ord('i'):
#             xx+=1
#         ans_+=chr(xx)
#     print(ans_)
