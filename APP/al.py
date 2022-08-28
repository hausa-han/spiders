# def isReturn(inputStr):
#     start = 0
#     end = len(inputStr) - 1
#     while start <= end:
#         if inputStr[start] == inputStr[end]:
#             start += 1
#             end -= 1
#             continue
#         else:
#             return False
#     return True
#
#
# if __name__ == '__main__':
#     correctList = ['A', 'H', 'I', 'M', 'O', 'T', 'U', 'V', 'W', 'X', 'Y']
#     inputList = []
#
#     while True:
#         try:
#             inputStr = list(input().strip().split('\n'))[0]
#             yesFlag = False
#             afterReplaceStr = inputStr
#             for c in correctList:
#                 afterReplaceStr = afterReplaceStr.replace(c, '')
#                 if afterReplaceStr == '':
#                     yesFlag = True
#             if yesFlag:
#                 if isReturn(inputStr):
#                     print('YES')
#                     continue
#             print('NO')
#         except EOFError:
#             break


# 图，求包含所有节点且路径最短的那个算法。


if __name__ == '__main__':
    num = input().strip().split()
    u = input().strip().split()
    v = input().strip().split()
    w = input().strip().split()

    usedWay = []


