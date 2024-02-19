### 1
# while True:
#     try:
#         S = input()
#         L = input()
#         lenS = len(S)
#         lenL = len(L)
#         indexS = 0
#         indexL = 0
#
#         for i in range(lenL):
#             if S[indexS] == L[i]:
#                 indexS += 1
#                 indexL = i
#             if indexS == lenS:
#                 print(indexL)
#                 break
#
#         if indexS != lenS:
#             print('-1')
#     except:
#         break


### 2
# while True:
#     try:
#         s = list(map(int, input().split(',')))
#         num = 0
#
#         for i in range(len(s)):
#             if i == 0 and s[i] > s[i+1]:
#                 num += 1
#             elif i == len(s) - 1 and s[i] > s[i-1]:
#                 num += 1
#             elif s[i] > s[i-1] and s[i] > s[i+1]:
#                 num += 1
#         print(num)
#
#     except:
#         break


### 4
# s = int(input())
#
# count = 1
#
# sum_list = [[str(s)]]
#
# for i in range(1, s):
#     sum = 0
#     s_list = []
#     for j in range(i, s):
#         sum += j
#         s_list.append(str(j))
#         if sum == s:
#             sum_list.append(s_list)
#             break
#
#
# sum_list = sorted(sum_list,key=lambda x:len(x))
#
# for k in sum_list:
#     print(str(s) + '=' + '+'.join(k))
# print('result:'+ str(len(sum_list)))


### 5
# a:3,b:5,c:2@a:1,b:2
# a:2,b:3,c:2

# a:3,b:5,c:2@
# a:2,b:3,c:2@

# a:3,b:5,c:2@d:1,e:2
# a:3,b:5,c:2

# s = 'a:3,b:5,c:2@a:1,b:2'.split('@')
#
# all_s = {}
# all_u = {}
#
# if len(s[1]) == 0:
#     print(s[0] + '@')
# else:
#     s1 = s[1].split(',')
#     s0 = s[0].split(',')
#
#     for i in s0:
#         all_s[i.split(':')[0]] = int(i.split(':')[1])
#
#     for j in s1:
#         all_u[j.split(':')[0]] = int(j.split(':')[1])
#
#     for k in all_u.keys():
#         if k in all_s.keys():
#             all_s[k] -= all_u[k]
#
#     ss = []
#     for p in all_s:
#         if all_s[p] != 0:
#             s2 = p + ':' + str(all_s[p])
#             ss.append(s2)
#     print(','.join(ss))


### 6
# Aa1#<Bb2$<Cc3%<
# ABC<c89%000<

# s = input()
#
# res = ''
#
# for i in s:
#     if i == '<':
#         res = res[:-1]
#     else:
#         res += i
#
# is_num = False
# is_up = False
# is_lower = False
# is_s = False
#
# for j in res:
#     if j.isdigit():
#         is_num = True
#     elif j.isupper():
#         is_up = True
#     elif j.islower():
#         is_lower = True
#     else:
#         is_s = True
#
# if len(res) >= 8 and is_num and is_up and is_lower and is_s:
#     print(res + ',true')
# else:
#     print(res + ',false')


### 8
# 输入
# 0
# asdbuiodevauufgh
# 输出
# 3

# 2
# aeueo

# 3
# asdbuiodevauufgh


# n = 3
# s = 'asdbuiodevauufgh'
#
# y = 'aeiouAEIOU'
#
# ly = []
# ll = []
# count = 0
#
# for i in range(len(s)):
#     if s[i] in y:
#         ly.append(i)
#
# left, right = 0, 0
# while right < len(ly):
#     lc = ly[right] - ly[left] - (right-left)
#     if lc > n:
#         left += 1
#     else:
#         if lc == n:
#             ll.append(ly[right] - ly[left] + 1)
#         right += 1
# if not ll:
#     print('0')
# else:
#     print(max(ll))


### 9
# 输入
# 3 1 1 2
# 3 1 2 3
# 2
# 输出
# 4

# 输入
# 3 1 1 2
# 3 4 5 6
# 2
# 输出
# 10

# 输入
# 4 1 1 1 1
# 4 2 3 4 5
# 4
# 输出
# 12


# s1 = list(map(int, '3 1 1 2'.split()[1:]))
# s2 = list(map(int, '3 4 5 6'.split()[1:]))
# n = int('2')
#
# s = []
# for i in s1:
#     for j in s2:
#         s.append(i + j)
#
# s.sort()
#
# print(sum(s[:n]))


### 10
# 输入
# 5
# 1 90
# 2 91
# 3 95
# 4 96
# 5 100
# 输出
# 1 2
# 3 4

# 输入
# 5
# 1 90
# 2 91
# 3 92
# 4 85
# 5 86
# 输出
# 1 2
# 2 3
# 4 5

# n = int('5')

# s = []
# for i in range(n):
#     s.append(list(map(int,input().split())))

# s = [[1, 91], [2, 90], [3, 92], [4, 85], [5, 86]]
# s = sorted(s, key=lambda x: x[1])
#
# sc = []
# for j in range(n - 1):
#     if s[j][0] < s[j + 1][0]:
#         sc.append([s[j][0], s[j + 1][0], s[j + 1][1] - s[j][1]])
#     else:
#         sc.append([s[j + 1][0], s[j][0], s[j + 1][1] - s[j][1]])
#
# sc = sorted(sc, key=lambda x: (x[2], x[0]))
#
# print(sc)
# ss = []
# for k in sc:
#     if k[2] == sc[0][2]:
#         ss.append(k[:2])
#
# for p in ss:
#     print(*p)


### 11

# 输入
# looxdolx
# 输出
# 7

# 输入
# bcbcbc
# 输出
# 6

# s = 'looxdolx'
#
# o_count = 0
# length = len(s)
#
# for i in s:
#     if i == 'o':
#         o_count += 1
#
# if o_count % 2 == 0:
#     print(length)
# else:
#     print(length - 1)


### 12
# 输入
# 10001
# 输出
# 1

# 输入
# 0101
# 输出
# 0

# 输入
# 111000
# 输出
# 1

# 输入
# 1001
# 输出
# 0

# s = '1000001001'
#
# num = 0
#
# for i in range(len(s)):
#     if s[i] == '0' and (i == 0 or s[i-1] == '0') and (i == len(s) - 1 or s[i+1] == '0'):
#         num += 1
#         s = s[:i] + '1' + s[i+1:]
#
# print(num)

### 13

# 输入
# 3 15 6 14
# 输出
# 3 21 9 17

# s = list(map(int, ('3 15 6 14').split()))
# s1 = s * 2
# s2 = []
# for i in range(len(s)):
#     for j in range(i + 1, len(s1)):
#         if s1[j] < s[i]:
#             s2.append(s[i] + s1[j])
#             break
#         if j == len(s1) - 1:
#             s2.append(s[i])
# print(*s2)


### 14

# 输入
# 2
# 100 95
# 输出
# 0 0

# 输入
# 8
# 123 124 125 121 119 122 126 123
# 输出
# 1 2 6 5 5 6 0 0

# n = int('8')
# s = list(map(int, '123 124 125 121 119 122 126 123'.split()))
#
# ss = []
#
# for i in range(n-1):
#     for j in range(i+1,n):
#         if s[i] < s[j]:
#             ss.append(j)
#             break
#         if j == n-1:
#             ss.append(0)
#
# ss.append(0)
# print(*ss)


### 15

# 输入
# 2 3 4 5
# 4
# 输出
# 5

# 输入
# 2 3 4 5
# 3
# 输出
# 0

# 输入
# 30 11 23 4 20
# 6
# 输出
# 23

# 输入
# 30 11 23 4 20
# 11
# 输出
# 10

# 输入
# 30 11 23 4 20
# 30
# 输出
# 4

# N = list(map(int, '30 11 23 4 20'.split()))
# H = int('5')
#
# N.sort(reverse=True)
#
# nl = len(N)
#
# if H >= nl:
#     i = H // nl
#     j = H % nl
#     s = sum(N)
#     if i == 1:
#         if N[j] % i != 0:
#             print(int(N[j] / i) + 1)
#         else:
#             print(int(N[j] / i))
#     else:
#         sp = s / H
#         NN = []
#         count = 0
#         for k in N:
#             if k / i > sp:
#                 NN.append(k)
#             else:
#                 if k / sp != 0:
#                     count += int(k / sp) + 1
#                 else:
#                     count += int(k / sp)
#
#         NNl = len(NN)
#         ii = (H - count) // NNl
#         jj = (H - count) % NNl
#         if NN[jj] % ii != 0:
#             print(int(NN[jj] / ii) + 1)
#         else:
#             print(int(NN[jj] / ii))
#
# else:
#     print(0)


### 16

# 输入
# 1 2 3 4 5 6 7 8 9 10
# 输出
# 1

# import sys
# res = sys.maxsize
#
# def dfs(nums, idx, count, currentSum):
#     global res, totalSum, targetSum
#
#     if count == 5:
#         otherTeamSum = totalSum - currentSum
#         res = min(res, abs(currentSum - otherTeamSum))
#         return
#
#     if idx == 10:
#         return
#
#     dfs(nums, idx + 1, count + 1, currentSum + nums[idx])
#
#     dfs(nums, idx + 1, count, currentSum)
#
#
# nums = list(map(int, input().split()))
# totalSum = sum(nums)
# targetSum = totalSum // 2
# dfs(nums, 0, 0, 0)
# print(res)


### 17

# 输入
# abC124Acb
# 输出
# 4

# 输入
# a5
# 输出
# 2

# 输入
# abC1
# 输出
# 2

# 输入
# abCdef
# 输出
# -1

# 输入
# abcd1234abcd12345abcd1234
# 输出
# 5

# s = input()
#
# maxlen = -1
#
# p = len(s)
#
# for index, value in enumerate(s):
#     if value.isalpha():
#         p = index
#     if value.isdigit():
#         maxlen = max(maxlen, index - p + 1)
#
# if maxlen:
#     print(maxlen)
# else:
#     print(-1)


### 18

# 输入
# XXYYXY
# 输出
# 2

# s = input()
# ans = 0
# count = 0
# for i in s:
#     if i == 'X':
#         count += 1
#     else:
#         count -= 1
#     if count == 0:
#         ans += 1
# print(ans)


### 19

# 输入
# 30 12 25 8 19
# 输出
# 15

# 输入
# 10 12 25 8 19 8 6 4 17 19 20 30
# 输出
# -1

# import math
#
#
# def min_energy(bricks, hours):
#     if len(bricks) > 8:
#         return -1
#     left, right = 1, max(bricks)
#
#     while left < right:
#         middle = (left + right) // 2
#         total_time = sum(math.ceil(i / middle) for i in bricks)
#         if total_time > hours:
#             left = middle + 1
#         else:
#             right = middle
#
#     if sum(math.ceil(i / left) for i in bricks) > hours:
#         return -1
#     return left
#
#
# nums = list(map(int, '30 12 25 8 19'.split()))
#
# print(min_energy(nums, 8))


### 20

# 输入
# 5
# 输出
# 4

# 输入
# 17
# 输出
# 15

# 输入
# 100
# 输出
# 81

# s = input()
# c = 0
#
# for i in s:
#     d = int(i)
#     if d > 4:
#         d -= 1
#     c = c * 9 + d
# print(c)


### 21

# 输入
# 4
# 100 200 300 500
# 1 2
# 1 3
# 2 4
# 输出
# 700


# N = int(input())
# w = list(map(int, input().split()))
# fw = w.copy()
# maxw = 0
#
# for i in range(N - 1):
#     N1, N2 = map(int, input().split())
#     fw[N1 - 1] += w[N2 - 1]
# maxw = max(fw)
# print(w)
# print(fw)
# print(maxw)


### 22

# 输入
# 5
# 5 6 6 1 2
# camila 13 88 46 26 169
# grace 64 38 87 23 103
# lucas 91 79 98 154 79
# leo 29 27 36 43 178
# ava 29 27 36 43 178
# 输出
# lucas
# grace
# camila
# ava
# leo

# N = int('5')
# w = list(map(int, '5 6 6 1 2'.split()))
#
# H = [['camila', '13', '88', '46', '26', '169'], ['grace', '64', '38', '87', '23', '103'],
#      ['lucas', '91', '79', '98', '154', '79'], ['leo', '29', '27', '36', '43', '178'],
#      ['ava', '29', '27', '36', '43', '178']]
# # H = []
# # for i in range(N):
# #     H.append(input().split())
#
# for i in range(N):
#     H[i].append(
#         w[0] * int(H[i][1]) + w[1] * int(H[i][2]) + w[2] * int(H[i][3]) + w[3] * int(H[i][4]) + w[4] * int(H[i][5]))
#
#
# H = sorted(H, key=lambda x: (-x[6], x[0].lower()))
#
# for j in H:
#     print(j[0])


### 23
# 输入
# 2
# present
# present absent present present leaveearly present absent
# 输出
# true
# false


# def check(records):
#     absent = 0
#     for i in range(len(records)):
#         if records[i] == 'absent':
#             absent += 1
#             if absent > 1:
#                 return False
#
#         elif records[i] == 'late' or records[i] == 'leaveearly':
#             if i > 0 and (records[i-1] == 'late' or records[i-1] == 'leaveearly'):
#                 return False
#
#         if i >= 6:
#             count = 0
#             for j in range(i-6, i+1):
#                 if records[j] != 'present':
#                     count += 1
#             if count > 3:
#                 return False
#     return True
#
#
# n = int('2')
# # for k in range(n):
# #     r = input().split()
# #     print('true' if check(r) else 'false')
#
# s = 'present absent present present leaveearly present absent'.split()
#
# if check(s):
#     print('true')
# else:
#     print('false')


### 24

# 输入
# 100 10
# 95 96 97 98 99 101 102 103 104 105
# 输出
# 99 101 98 102 97 103 96 104 95 105


# s1 = '100 10'.split()
# h = int(s1[0])
#
#
# s2 = list(map(int, '105 96 97 98 99 101 102 103 104 95'.split()))
#
# s2 = sorted(s2,key=lambda x:(abs(x-h),x))
# print(*s2)
# print(' '.join(list(map(str, s2))))

# s3 = [i for i in range(int(s1[1]))]
# d = dict(zip(s3, s2))
# for k in d.keys():
#     d[k] = [d[k], abs(d[k] - h)]
# d = dict(sorted(d.items(), key=lambda x: (x[1][1], x[1][0])))
# s = []
# for j in d.keys():
#     s.append(d[j][0])
# print(*s)
