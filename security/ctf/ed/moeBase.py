s = '1wX/yRrA4RfR2wj72Qv52x3L5qa='
# 1wX/ yRrA 4RfR 2wj7 2Qv5 2x3L 5qa=
base64Char = 'abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ'

temp0 = 0
temp1 = 0
temp2 = 0
temp3 = 0

i = 0
j = 0

v2 = 0
v3 = 0

result = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(len(result))

for i in range(0,len(s),4):
    # print(j)
    # print(i)
    temp0 = 0
    temp1 = 0
    temp2 = 0
    temp3 = 0

    for k in range(0,64):
        if base64Char[k] == s[i]:
            # print(s[i])
            temp0 = k
    for k in range(0, 64):
        if base64Char[k] == s[i+1]:
            temp1 = k
    for k in range(0, 64):
        if base64Char[k] == s[i+2]:
            temp2 = k
    for k in range(0, 64):
        if base64Char[k] == s[i+3]:
            # print(s[i+3])
            temp3 = k
    # v2 = j
    # j += 1

    result[j] = (temp1 >> 4) & 3 | (4*temp0)
    j+=1

    if s[i+2] == '=':
        break
    # v3 = j
    # j += 1
    result[j] = ((temp2 >> 2) & 0xf | (16*temp1)) % 128
    j+=1


    if s[i+3] == '=':
        break
    result[j] = (temp3 & 0x3f | (temp2 << 6)) % 128
    j+=1

    for haha in range(0,len(result)):
        print(chr(result[haha]), end='')
    print()

print(i)
print(j)
print(ord('ů'))
