from math import sqrt


def judge(num):
    if num<2:
        return False
    if num==2 or num==3:
        return True
    if num%6 != 1 and num%6 !=5:
        return False
    temp = int(sqrt(num))
    for i in range(5, temp, 6):
        if num%i == 0 or num%(i+2) == 0:
            return False
    return True

if __name__ == '__main__':
    n = int(input())
    t = int(n/2)
    for i in range(173999999, t, 6):
        if judge(i) and judge(n-i):
            print(i)
            print(n-i)




