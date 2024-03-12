# 1
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
# import string
# import time
# import time
# from itertools import permutations
# import time

# 2
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


# 4
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


# 5
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


# 6
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


# 8
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


# 9
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


# 10
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


# 11

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


# 12
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

# 13

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


# 14

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


# 15

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


# 16

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


# 17

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


# 18

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


# 19

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


# 20

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


# 21

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


# 22

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


# 23
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


# 24

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


# 25

# 输入
# 3 3
# 1 2 1
# 3 1 3
# 1 1 1

# 输出
# 9

# m, n = map(int, '2 5'.split())
# s = [[1, 0, 0, 0, 1], [0, 1, 0, 1, 0]]
# # s = []
# # for i in range(m):
# #     s.append(list(map(int, input().split())))
#
# minpos = {}
# maxpos = {}
#
# for i in range(m):
#     for j in range(n):
#         num = s[i][j]
#         if num != 0:
#             if num not in minpos:
#                 minpos[num] = (i, j)
#                 maxpos[num] = (i, j)
#             else:
#                 minpos[num] = (min(minpos[num][0], i), min(minpos[num][1], j))
#                 maxpos[num] = (max(maxpos[num][0], i), max(maxpos[num][1], j))
#
# maxarea = 0
#
# for num in minpos:
#     area = (maxpos[num][0] - minpos[num][0] + 1) * (maxpos[num][1] - minpos[num][1] + 1)
#     maxarea = max(maxarea, area)
#
# print(maxarea)


# 26

# 输入
# 3
# 1 1 1
# 输出
# 0

# 输入
# 3
# 3 7 10
# 输出
# 1

# 输入
# 4
# 2 2 3 5
# 输出
# 2

# 输入
# 5
# 4 2 2 3 5
# 输出
# 2

# n = int('4')
# s = list(map(int, '2 2 3 5'.split()))
#
# s.sort(reverse=True)
#
# while len(s) > 2:
#     z = s[0]
#     y = s[1]
#     x = s[2]
#     s.pop(0)
#     s.pop(0)
#     s.pop(0)
#     if x == y and y != z:
#         s.append(z-y)
#     elif x != y and y == z:
#         s.append(y-x)
#     elif x != y and y != z:
#         c = abs((z-y)-(y-x))
#         if c:
#             s.append(c)
#     s.sort(reverse=True)
#
# if len(s):
#     print(max(s))
# else:
#     print(0)


# 26

# 输入
# 10
# 1 2 1 2 1 2 1 2 1 2
# 5
# 输出
# 2 1 2

# 输入
# 5
# 1 2 3 4 5
# 3
# 输出
# 0

# 输入
# 10
# 1 1 1 2 2 2 2 3 3 4
# 3
# 输出
# 2 2 1

# n = int('10')
# s = list(map(int, '1 1 1 2 2 2 2 3 3 4'.split()))
# y = int('3')
#
# sd = {}
#
# for i in set(s):
#     x = s.count(i)
#     if x >= y:
#         sd[i] = x
#
# sd = dict(sorted(sd.items(), key=lambda x: (-x[1], x[0])))
#
# if len(sd):
#     print(len(sd),*sd)
# else:
#     print(0)


# 27

# 输入
# bAaAcBb
# 输出
# a3b2b2c0

# s = 'bAaAdBbc'.lower()
# ss = []
# ds = []
#
# for i in s:
#     if 'a' <= i <= 'z':
#         ss.append(i)
#
# pre = ss[0]
# repeat = 1
#
# for j in range(1, len(ss)):
#     cur = ss[j]
#     if cur == pre:
#         repeat += 1
#     else:
#         ds.append(pre + str(repeat) if repeat > 1 else pre + str(ss[j:].count(pre)))
#         pre = cur
#         repeat = 1
#     if j == len(ss) - 1:
#         ds.append(pre + str(repeat) if repeat > 1 else pre + str('0'))
#
# ds.sort(key=lambda x: (-int(x[1:]), x[0]))
# print(''.join(ds))


# 29

# 输入
# 1,2,5,-21,22,11,55,-101,42,8,7,32
# 输出
# 1,-21,11,-101,2,22,42,32,5,55,7,8

# 输入
# 19,-31,10,57,61,27,11,28,-94
# 输出
# 10,-31,61,11,-94,57,27,28,19

# s = '19,-31,10,57,61,27,11,28,-94'.split(',')
#
# s.sort(key=lambda x: x[-1])
# print(','.join(s))


# 30

# 输入
# 1,3,3,3,2,4,4,4,5
# 输出
# 3,4,1,2,5

# s = '1,3,3,3,2,4,4,4,5'.split(',')
#
# ds = {}
#
# for i in s:
#     ds[i] = ds.get(i, 0) + 1
#
# ds = dict(sorted(ds.items(), key=lambda x: -x[1]))
# print(','.join(ds.keys()))


# 31

# 输入
# 3 2
# yuwen shuxue
# fangfang 95 90
# xiaohua 88 98
# minmin 100 82
# shuxue
# 输出
# xiaohua fangfang minmin

# 输入
# 3 2
# yuwen shuxue
# fangfang 95 90
# xiaohua 88 95
# minmin 90 95
# zongfen
# 输出
# fangfang minmin xiaohua

# n, m = map(int, '3 2'.split())
#
# kemu = 'yuwen shuxue'.split()
#
# # score = []
# # for i in range(n):
# #     score.append(input().split())
#
# score = [['fangfang', '95', '90'], ['xiaohua', '88', '95'], ['minmin', '90', '95']]
#
# t = 'zongfen'
#
# if t in kemu:
#     i = kemu.index(t)
#     score = sorted(score, key=lambda x: (-int(x[i + 1]), x[0]))
# else:
#     score = sorted(score, key=lambda x: (-(int(x[1]) + int(x[2])), x[0]))
#
# s = [j[0] for j in score]
# print(*s)

# 32

# 输入
# 4
# 100 100 120 130
# 40 30 60 50
# 输出
# 2 1 3 4

# n = int('4')
# h = list(map(int, '100 100 120 130'.split()))
# w = list(map(int, '40 30 60 50'.split()))
#
# s = []
# for i in range(n):
#     s.append([i + 1, h[i], w[i]])
#
# s.sort(key=lambda x: (x[1], x[2], x[0]))
#
# s = [j[0] for j in s]
# print(*s)


# 33

# 输入
# abcdef
# 输出
# abcdef

# 输入
# bcdefa
# 输出
# acdefb


# 34

# 输入
# 3
# 5
# 1 2 3 4 5
# 输出
# 6

# 输入
# 4
# 5
# 5 4 1 1 1
# 输出
# 5

# maxtasks = int('4')
# taskarrlen = int('5')
# taskarr = list(map(int, '5 4 1 1 1'.split()))
#
# currenttask = 0
# time = 0
# index = 0
#
# while currenttask != 0 or index != len(taskarr):
#     if index < len(taskarr):
#         currenttask += taskarr[index]
#         index += 1
#     currenttask -= maxtasks
#     if currenttask < 0:
#         currenttask = 0
#     time += 1
#
# print(time)


# 35

# 输入
# 5
# 95 88 83 64 100
# 2
# 输出
# 342

# 输入
# 5
# 3 2 3 4 2
# 2
# 输出
# -1


# m = int('5')
# s = sorted(list(map(int, set('5 5 5 5 5'.split()))))
# n = int('1')
# if n * 2 > len(s):
#     print(-1)
# else:
#     print(sum(s[:n]) + sum(s[-n:]))

# 36

# 输入
# 93,95,97,100,102,123,155
# 110
# 输出
# 6


# s = list(map(int, '93,95,97,100,102,123,155'.split(',')))
# c = int('93')
#
# left, right = 0, len(s)
#
# while left < right:
#     mid = (left + right) // 2
#     if s[mid] < c:
#         left = mid + 1
#     else:
#         right = mid
# print(left+1)


# 37

# 输入
# 4
# 3
# 1 2
# 1 3
# 1 4
# 1 5
# 输出
# 5

# 输入
# 4
# 3
# 1 2
# 1 3
# 1 4
# 3 5
# 输出
# 9

# 输入
# 4
# 3
# 1 2
# 2 3
# 3 4
# 3 5
# 输出
# 12

# n = int('4')
# t = int('3')
#
# # s = []
# # for i in range(n):
# #     s.append(list(map(int, input().split())))
#
# s = [[1, 40], [2, 20], [1, 30], [3, 12], [4, 15], [1, 50]]
# s.sort(key=lambda x: x[0])
# print(s)
# q = []
#
# for i in s:
#     if len(q) < i[0]:
#         q.append(i[1])
#         q.sort()
#     elif q and q[0] < i[1]:
#         q.pop(0)
#         q.append(i[1])
#         q.sort()
#     if len(q) > t:
#         q.pop(0)
# print(sum(q))


# 38

# 输入
# 9
# 6
# 1
# 3
# 1
# 8
# 9
# 3
# 2
# 4
# 15
# 输出
# 4

# n = int('9')
# s = [6, 1, 3, 1, 8, 9, 3, 2, 1]
#
# # s = []
# # for i in range(n):
# #     s.append(int(input()))
#
# z = int('15')
# ms = 0
# left, right = 0, 0
# tt = 0
# for i in range(len(s)):
#     tt += s[i]
#     right = i
#     while tt > z:
#         tt -= s[left]
#         left += 1
#     ms = max(ms, right - left + 1)
#
# print(ms)


# 39

# 输入
# 15
# 输出
# 3 5

# 输入
# 27
# 输出
# -1 -1


# def bool_ss(n):
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return False
#     return True
#
#
# m = int('589')
# s = []
#
# if not bool_ss(m):
#     for j in range(2, int(m ** 0.5) + 1):
#         if bool_ss(j) and m % j == 0 and bool_ss(m / j):
#             s.append(j)
#             s.append(int(m / j))
#             s.sort()
#             break
# if len(s):
#     print(*s)
# else:
#     print('-1 -1')


# 40

# 输入
# 4
# cat
# bt
# hat
# tree
# attach??
# 输出
# 3

# 输入
# 3
# hello
# world
# cloud
# whlldonehohneyr
# 输出
# 2

# 输入
# 3
# apple
# car
# window
# whlldoneapplec?
# 输出
# 2

# n = int('4')

# s = []
# for i in range(n):
#     s.append(input())

# words = ['cat', 'bt', 'hat', 'tree']
#
# chars = 'attach??'
#
# tc = {}
# for i in set(chars):
#     tc[i] = chars.count(i)
#
# count = 0
# for j in words:
#     tcc = tc.copy()
#     tag = True
#     for k in set(j):
#         if k in tcc.keys():
#             if tcc[k] - j.count(k) < 0:
#                 if '?' not in tcc.keys() or ('?' in tcc.keys() and tcc['?'] - j.count(k) + tcc[k] < 0):
#                     tag = False
#                     break
#                 else:
#                     tcc['?'] -= j.count(k) - tcc[k]
#         else:
#             if '?' not in tcc.keys() or ('?' in tcc.keys() and tcc['?'] - j.count(k) < 0):
#                 tag = False
#                 break
#             else:
#                 tcc['?'] -= j.count(k)
#     if tag:
#         count += 1
# print(count)


# 41

# 输入
# 2 2
# 1 1
# 2 2
# 输出
# 1 2

# 输入
# 1 2
# 2
# 1 3
# 输出
# 2 3

# 输入
# 3 2
# 1 2 5
# 2 4
# 输出
# 5 4

# l1, l2 = map(int, '5 5'.split())
#
# sl1 = list(map(int, '17 23 42 50 60'.split()))
# sl1.sort()
#
# sl2 = list(map(int, '22 35 37 41 55'.split()))
#
# tl1 = sum(sl1)
# tl2 = sum(sl2)
#
# print(tl1)
# print(tl2)
#
# dsl2 = {}
# for i in sl2:
#     dsl2[i] = dsl2.get(i, 0) + 1
#
# hd = round((tl1 - tl2) / 2)
# print(hd)
#
# for j in sl1:
#     b = j - hd
#     if b in dsl2 and dsl2[b] > 0:
#         print(j, b)
#         break


# 42

# 输入
# 5
# -5
# -5 1 6 0 -7
# 输出
# 1

# n = int('5')
# luck = int('-5')
# s = list(map(int, '-5 1 6 0 -7'.split()))
#
# ss = [0]
#
# for i in s:
#     if i == luck:
#         if i > 0:
#             ss.append(ss[-1] + i + 1)
#         else:
#             ss.append(ss[-1] + i - 1)
#     else:
#         ss.append(ss[-1] + i)
#
# print(max(ss))


# 43

# 输入
# 10 2 4
# 输出
# 2


# def conversion(n, d):
#     res = ''
#     if n < d:
#         return str(n)
#     else:
#         while n // d > 0:
#             res += str(n % d)
#             n = n // d
#         if n % d != 0:
#             res += str(n % d)
#         return res[::-1]
#
#
# k, n, m = map(int, '10 2 4'.split())
#
# print(conversion(k, m))
# print(conversion(k, m).count(str(n)))


# 44

# 输入
# 3 3
# 0 0 0
# 0 1 0
# 0 0 0
# 输出
# 2

# n, m = map(int, '3 7'.split())
# s = [[0, 0, 0, 1, 0, 0, 0],
#      [0, 1, 0, 0, 0, 1, 0],
#      [0, 0, 0, 0, 1, 0, 0]]


# s = []
# for i in range(n):
#     s.append(list(map(int, input().split())))


# def getroad(s, n, m, x=0, y=0, ss=[(0, 0)], count=[]):
#     if x + 1 < n and s[x + 1][y] == 0:
#         if (x + 1, y) not in ss:
#             getroad(s, n, m, x + 1, y, ss + [(x + 1, y)], count)  # 向下
#     if y + 1 < m and s[x][y + 1] == 0:  # 向右
#         if (x, y + 1) not in ss:
#             getroad(s, n, m, x, y + 1, ss + [(x, y + 1)], count)
#     if x - 1 >= 0 and s[x - 1][y] == 0:
#         if (x - 1, y) not in ss:
#             getroad(s, n, m, x - 1, y, ss + [(x - 1, y)], count)  # 向上
#     if y - 1 >= 0 and s[x][y - 1] == 0:  # 向左
#         if (x, y - 1) not in ss:
#             getroad(s, n, m, x, y - 1, ss + [(x, y - 1)], count)
#
#     if x == n - 1 and y == m - 1:
#         count.append(ss)
#         # for j in ss:
#         #     print('(' + str(j[0]) + ',' + str(j[1]) + ')')
#     return count
#
#
# print(getroad(s, n, m))
# print(len(getroad(s, n, m)))


# 45

# 输入
# I love you
# He
# 输出
# He

# 输入
# The Furthest distance in the world,Is not between life and death,
# But when I stand in front of you,Yet you don't know that I love you.
# f
# 输出
# fron furthest


# sentence = 'The furthest distance in the world,Is not between life and death,
# But when I stand in front of you,Yet you don\'t know that I love you.'
#
# prefix = 'f'
#
# # ss = [i for i in sentence if i in string.punctuation]
# # print(ss)
#
#
# sentence = sentence.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
# print(sentence)
# word_set = set(sentence.split())
# ans = ''
#
# for s in sorted(word_set):
#     if s.startswith(prefix):
#         ans += s + ' '
# if ans:
#     print(ans)
# else:
#     print(prefix)


# 46

# 输入
# AbCdeFG
# 3
# 输出
# 5


# s = 'AbCdeFG'
# k = int('3')
#
# ss = sorted(s)
# # print(s)
# # print(ss[k-1])
# if k > len(s):
#     print(len(s))
# else:
#     print(s.index(ss[k-1]))


# 47

# 输入
# /abc/,/bcd
# 输出
# /abc/bcd

# s = '/abc/def12//,2a1/ghi/jkl'.split(',')
# res = ''
#
# s[0] = s[0].rstrip('/12')
# s[1] = s[1].lstrip('/12')
# print('/'.join(s))


# 48

# 输入
# 1,1,0,0,1,1,1,0,1
# 输出
# 2

# 输入
# 1,0,0,0,0,0,1,1,0,1,0,0,1
# 输出
# 4


# s = (''.join(i for i in ('1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,1,1'.split(',')))).split('0')
# mincars = 0
#
# print(s)
#
# for j in s:
#     jl = len(j)
#     if j == 0:
#         mincars = mincars
#     elif not jl % 3 and jl != 0:
#         mincars += jl // 3
#     elif jl % 3:
#         mincars += jl // 3
#         # mincars += (jl - jl % 3) // 3
#         mincars += 1
#
# print(mincars)


# 49

# 输入
# 5
# /huawei/computing/no/one
# /huawei/computing
# /huawei
# /huawei/cloud/no/one
# /huawei/wireless/no/one
# 2 computing
# 输出
# 2

# 输入
# 5
# /huawei/computing/no/one
# /huawei/computing
# /huawei
# /huawei/cloud/no/one
# /huawei/wireless/no/one
# 4 two
# 输出
# 0

# 输入
# 5
# /huawei/computing/no/one
# /huawei/computing
# /huawei/one
# /huawei/cloud/no/one
# /huawei/wireless/no/one
# 4 one
# 输出
# 3


# n = int('5')
#
# # s = []
# # for i in range(s):
# #     s.append(input().split('/'))
#
# s = [['huawei', 'computing', 'no', 'one'],
#      ['huawei', 'computing'],
#      ['huawei', 'one'],
#      ['huawei', 'cloud', 'no', 'one'],
#      ['huawei', 'wireless', 'no', 'one']]
#
# m = '4 one'.split()
#
# count = 0
#
# for i in s:
#     if len(i) >= int(m[0]):
#         if i[int(m[0]) - 1] == m[1]:
#             count += 1
#
# print(count)


# 50

# 输入
# 5
# 3 1 5 7 9
# 8
# 输出
# 3

# 输入
# 5
# 3 1 5 7 9 2 6
# 8
# 输出
# 4

# 输入
# 3
# 1 1 9
# 8
# 输出
# 1

# 输入
# 8
# 1 2 3 4 5 6 7 8
# 10
# 输出
# 3


# n = int('7')
# en = list(map(int, '1 1 1 4 5 6 7'.split()))
# en.sort()
# m = int('1')
# left = 0
# right = n-1
# res = 0
#
# while left < right:
#     if en[right] >= m:
#         res += 1
#         right -= 1
#     elif en[right] + en[left] >= m:
#         res += 1
#         right -= 1
#         left += 1
#     else:
#         left += 1
#
# if left == right and en[left] >= m:
#     res += 1
#
# print(res)


# 51

# 输入
# 3 7
# 3 4 7
# 输出
# 4

# 51

# 输入
# 10 10000
# 1 2 3 4 5 6 7 8 9 10
# 输出
# 0


# n, x = map(int, '3 7'.split())
# nums = list(map(int, '4 3 7'.split()))
# left = 0
# right = 0
# count = 0
# sn = 0
#
# while right < n:
#     sn += nums[right]
#     while sn >= x:
#         count += n - right
#         sn -= nums[left]
#         left += 1
#     right += 1
#
# print(count)


# 52

# 输入
# 3
# 12abc-abCABc-4aB@
# 输出
# 12abc-abc-ABC-4aB-@

# 输入
# 12
# 12abc-abCABc-4aB@
# 输出
# 12abc-abCABc4aB@


# def cs(ss: str):
#     ucount = 0
#     lcount = 0
#     for j in ss:
#         if j.isupper():
#             ucount += 1
#         elif j.islower():
#             lcount += 1
#     if ucount > lcount:
#         return ss.upper()
#     elif ucount < lcount:
#         return ss.lower()
#     else:
#         return ss
#
#
# n = int('4')
# s = 'aBcDe-FgHiJ-KlMnO'.split('-')
#
# res = []
#
# res.append(s[0])
# s = ''.join(s[1:])
# # print(res)
# # print(s)
#
# for i in range(0, len(s), n):
#     if i != len(s) // n * n:
#         res.append(cs(s[i:i + n]))
#     else:
#         res.append(cs(s[i:len(s)]))
# # print(res)
# print('-'.join(res))


# 53

# 输入
# AAAAHHHBBCDHHHH
# 3
# 输出
# 2

# s = 'AAAAHHHBBCDHHHHBAAAAACCE'
# k = int('3')
#
# left = 0
# right = 0
# count = 0
# d = s[0]
#
# res = {}
#
# for i in range(len(s)):
#     if s[i] == d:
#         right = i
#     else:
#         res[d] = max(res.get(d, 0), right - left + 1)
#         d = s[i]
#         left = i
#         right = i
# if right == len(s) - 1:
#     res[d] = max(res.get(d, 0), right - left + 1)
#
# print(res)
# res = sorted(res.values(), reverse=True)
# print(res[k - 1])


# 54

# x#y = 2*x+3*y+4
# x$y = 3*x+y+2

# 输入
# 7#6$5#12
# 输出
# 226
# 说明
# 7#25#12
# 93#12
# 226


# s = '7#6$5$3#12$2'
#
# while '$' in s:
#     k = s.index('$')
#     x, y = '', ''
#     a, b = 0, 0
#     while k - 1 >= 0 and s[k - 1].isdigit():
#         x += s[k - 1]
#         k -= 1
#         a = k
#     x = int(x[::-1])
#     k = s.index('$')
#     while k + 1 < len(s) and s[k + 1].isdigit():
#         y += s[k + 1]
#         k += 1
#         b = k
#     y = int(y)
#
#     m = 3 * x + y + 2
#
#     s = s[0:a] + str(m) + s[b + 1:]
#
#     print(s)
#
# while '#' in s:
#     k = s.index('#')
#     x, y = '', ''
#     while k - 1 >= 0 and s[k - 1].isdigit():
#         x += s[k - 1]
#         k -= 1
#         a = k
#     x = int(x[::-1])
#     k = s.index('#')
#     while k + 1 < len(s) and s[k + 1].isdigit():
#         y += s[k + 1]
#         k += 1
#         b = k
#     y = int(y)
#
#     m = 2 * x + 3 * y + 4
#
#     s = s[0:a] + str(m) + s[b + 1:]
#     print(s)


# 55

# 输入
# 5 100 10
# 10 20 30 40 50
# 3 4 5 6 10
# 20 30 20 40 30
# 输出
# 0 30 0 40 0

# m, N, X = map(int, '5 100 10'.split())
# returns = list(map(int, '10 20 30 40 50'.split()))
# risks = list(map(int, '3 4 5 6 10'.split()))
# max_investments = list(map(int, '20 30 20 40 30'.split()))
#
# max_return = 0
# best_investments = [0] * m
#
# for i in range(m):
#     if risks[i] <= X:
#         investment_for_i = min(N, max_investments[i])
#
#         current_return = investment_for_i * returns[i]
#
#         if current_return > max_return:
#             max_return = current_return
#             best_investments = [0] * m
#             best_investments[i] = investment_for_i
#
#     for j in range(i + 1, m):
#         if risks[i] + risks[j] <= X:
#             if returns[i] > returns[j]:
#                 investment_for_i = min(N, max_investments[i])
#                 investment_for_j = min(N - investment_for_i, max_investments[j])
#             else:
#                 investment_for_j = min(N, max_investments[j])
#                 investment_for_i = min(N - investment_for_j, max_investments[i])
#
#             current_return = investment_for_i * returns[i] + investment_for_j * returns[j]
#             if current_return > max_return:
#                 max_return = current_return
#                 best_investments = [0] * m
#                 best_investments[i] = investment_for_i
#                 best_investments[j] = investment_for_j
# print(' '.join(map(str, best_investments)))


# 56

# 输入
# 4 10
# 1 1
# 2 1
# 3 1
# 4 -2
# 输出
# 12

# n, e = map(int, '4 10'.split())
#
# if e == 0:
#     print(0)
#
# offsets = [0]*e
#
# # for i in range(n):
# #     cur_x, offset_y = map(int, input().split())
# #     offsets[cur_x] = offset_y
#
# offsets[1] = 1
# offsets[2] = 1
# offsets[3] = 1
# offsets[4] = -2
# print(offsets)
#
# dp = [0]*e
# dp[0] = offsets[0]
# for i in range(1,e):
#     dp[i] = offsets[i] + dp[i-1]
# print(dp)
#
# ans = 0
# for num in dp:
#     ans += abs(num)
# print(ans)


# 57

# 输入
# CA3385,CZ6678,SC6508,DU7523,HK4456,MK0987
# 输出
# CA3385,CZ6678,DU7523,HK4456,MK0987,SC6508

# 输入
# MU1087,CA9908,3U0045,FM1703
# 输出
# 3U0045,CA9908,FM1703,MU1087

# s = 'MU1087,CA9908,3U0045,FM1703'.split(',')
# s.sort(key=lambda x: (x[:2], s[2:]))
# print(','.join(s))


# 58

# 输入
# 0 5 8 9 9 10
# 5 0 9 9 9 8
# 输出
# 8 7

# b = list(map(int, '0 5 8 9 9 10'.split()))
# w = list(map(int, '5 0 9 9 9 8'.split()))
#
# q = [[0] * 19 for _ in range(19)]
#
# bl = []
# wl = []
#
#
# def zz(s, l, qp, k):
#     for i in range(0, len(s), 2):
#         l.append([s[i], s[i + 1]])
#         qp[s[i]][s[i + 1]] = k
#
#     return l, qp
#
#
# bl, q = zz(b, bl, q, 1)
# wl, q = zz(w, wl, q, 2)
#
# bq = 0
# wq = 0
#
#
# def cq(s, qp):
#     count = []
#     for j in s:
#         if j[0] - 1 >= 0 and qp[j[0] - 1][j[1]] == 0 and [j[0] - 1, j[1]] not in count:  # 向上
#             count.append([j[0] - 1, j[1]])
#         if j[0] + 1 < 19 and qp[j[0]+1][j[1]] == 0 and [j[0]+1, j[1]] not in count:  # 向下
#             count.append([j[0] + 1, j[1]])
#         if j[1] - 1 >= 0 and qp[j[0]][j[1]-1] == 0 and [j[0], j[1]-1] not in count:  # 向左
#             count.append([j[0], j[1]-1])
#         if j[1] + 1 < 19 and qp[j[0]][j[1]+1] == 0 and [j[0], j[1]+1] not in count:  # 向左
#             count.append([j[0], j[1]+1])
#
#     return len(count)
#
# print(cq(bl,q),cq(wl,q))


# 59

# 输入
# 40 40 18
# 输出
# 1484

# 输入
# 5 4 7
# 输出
# 20


# import sys
#
# sys.setrecursionlimit(10000)
#
#
# def sum_of_digits(num):
#     sum = 0
#     while num > 0:
#         sum += num % 10
#         num //= 10
#
#     return sum


# def dfs(x, y, m, n, k, visited):
#     if x < 0 or y < 0 or x >= m or y >= n or visited[x][y] or sum_of_digits(x) + sum_of_digits(y) > k:
#         return 0
#     visited[x][y] = True
#     return (1 + dfs(x + 1, y, m, n, k, visited) + dfs(x - 1, y, m, n, k, visited) +
#             dfs(x, y + 1, m, n, k, visited) + dfs(x, y - 1, m, n, k, visited))
#
#
# m, n, k = map(int, '40 40 18'.split())
#
# visited = [[False for _ in range(n)] for _ in range(m)]
#
#
# # start = time.time()
# print(dfs(0, 0, m, n, k, visited))
# # end = time.time()
# # print(end - start)


# # start = time.time()
# m, n, k = map(int, '40 40 18'.split())
#
# count = 0
# for i in range(m):
#     for j in range(n):
#         if sum_of_digits(i) + sum_of_digits(j) <= k:
#             count += 1
# # end = time.time()
#
# print(count)
# # print(end-start)


# 60

# 输入
# 5
# 5000 2000 5000 8000 1800
# 输出
# 3

# 输入
# 3
# 5000 4000 3000
# 输出
# 3

# 输入
# 9
# 5000 2000 5000 8000 1800 7500 4500 1400 8100
# 输出
# 4


# class TreeNode:
#     def __init__(self, val):
#         self.val = val
#         self.left = self.mid = self.right = None
#
#
# class Tree:
#     def insert(self, root, val):
#         if root is None:
#             return TreeNode(val)
#         if val < root.val - 500:
#             root.left = self.insert(root.left, val)
#         elif val > root.val + 500:
#             root.right = self.insert(root.right, val)
#             print(root.right.val)
#         else:
#             root.mid = self.insert(root.mid, val)
#         return root
#
#     def get_height(self, root):
#         if root is None:
#             return 0
#         left_height = self.get_height(root.left)
#         mid_height = self.get_height(root.mid)
#         right_height = self.get_height(root.right)
#         return max(left_height, mid_height, right_height) + 1
#
#
# tree = Tree()
# N = int('9')
# root = None
# nums = list(map(int, '5000 2000 5000 8000 1800 7500 4500 1400 8100'.split()))
#
# for num in nums:
#     root = tree.insert(root, num)
# height = tree.get_height(root)
# print(height)


# 61

# 输入
# abc1 A
# xyz B
# 输出
# abc1

# 输入
# abc1 A
# xyz A
# 输出
# NULL

# 输入
# abc1 A
# def A
# alic A
# xyz B
# 输出
# abc1
# alic
# def

#
# def pd(s):
#     res = []
#     if len(set(s.values())) != 2:
#         return 'NULL'
#     else:
#         if 'A' in s.values() and 'B' in s.values():
#             res = [i for i in s.keys() if s[i] == 'A']
#         elif 'A' in s.values() and 'C' in s.values():
#             res = [i for i in s.keys() if s[i] == 'C']
#         elif 'B' in s.values() and 'C' in s.values():
#             res = [i for i in s.keys() if s[i] == 'B']
#         res.sort()
#         return res
#
#
# # s = {'abc': 'C', 'ddc': 'A'}
# # print(pd(s))
#
# s = {}
# while True:
#     try:
#         inp = input()
#         if inp == '':
#             print(pd(s))
#             s = {}
#         else:
#             key, value = map(str, inp.split())
#             s[key] = value
#
#     except:
#         break
#
# # res = [i for i in s.keys() if s[i] == 'C']
# # res.sort()
# # print(res)


# 62

# 输入
# 2 8 3 7 3 6 3 5 4 4 5 3 6 2 7 3 8 4 7 5
# 输出
# 2 8 3 7 3 5 6 2 8 4 7 5


# def is_truning_point(prev, curr, next):
#     dx1 = curr[0] - prev[0]
#     dy1 = curr[1] - prev[1]
#     dx2 = next[0] - curr[0]
#     dy2 = next[1] - curr[1]
#
#     return dx1 * dy2 != dy1 * dx2
#
#
# def simplify_path(points):
#     if len(points) < 2:
#         return points
#
#     result = [points[0]]
#
#     for i in range(1, len(points) - 1):
#         if is_truning_point(points[i - 1], points[i], points[i + 1]):
#             result.append(points[i])
#
#     result.append(points[-1])
#     return result
#
#
# s = list(map(int, '2 8 3 7 3 6 3 5 4 4 5 3 6 2 7 3 8 4 7 5'.split()))
# p = []
# for i in range(0, len(s), 2):
#     # p.append((s[i], s[i + 1]))
#     p.append([s[i], s[i + 1]])
#
# simplified_points = simplify_path(p)
#
# # print(' '.join(f"{x} {y}" for x,y in simplified_points))
# print(' '.join(f'{x} {y}' for x, y in simplified_points))


# 63

# 输入
# bb1234aa
# 输出
# 10

# 输入
# bb12-34aa
# 输出
# -31
# 说明
# 1+2+（-34） = -31

# 输入
# a-1b-2c-3d-4e-5f-6g-7h-8i-9j-10k11
# 输出
# -53
# 说明
# -1-2-3-4-5-6-7-8-9-10+1+1 = -53


# s = 'bb1234aa'
#
# p = 0
# tag = False
# sum = 0
# for i, value in enumerate(s):
#     if value == '-':
#         p = i
#         tag = True
#     elif tag and value.isalpha():
#         sum += int(s[p:i])
#         tag = False
#     elif not tag and value.isdigit():
#         sum += int(value)
#
# print(sum)


# 64

# 输入
# 1,2,3,4,5,6,7,8,9
# 4
# 3
# 输出
# 13

# nums = list(map(int, '1,2,3,4,5,6,7,8,9,10'.split(',')))
# j = int('2')
# left = int('4')
#
# i = 0
# s = []
# while left < len(nums):
#     if i + j + 1 < len(nums):
#         nums.pop(i + j + 1)
#         print(nums)
#         i = i + j
#     else:
#         nums.pop(j - len(nums) + i + 1)
#         i = j - len(nums) + i - 1
#         print(nums)
#
# print(nums)
# print(sum(nums))


# 65

# 输入
# 0 9 20 -1 -1 15 7 -1 -1 -1 -1 3 2
# 输出
# 38


# from collections import deque

# s = list(map(int, '0 9 20 -1 -1 15 7 -1 -1 -1 -1 3 2'.split()))

# max_time = 0
#
# node_queue = deque([0])
#
# while node_queue:
#     parent_node_index = node_queue.popleft()
#
#     left_child_index = 2 * parent_node_index + 1
#     right_child_index = 2 * parent_node_index + 2
#
#     if left_child_index < len(s) and s[left_child_index] != -1:
#         s[left_child_index] += s[parent_node_index]
#         node_queue.append(left_child_index)
#         max_time = max(max_time,s[left_child_index])
#
#     if right_child_index < len(s) and s[right_child_index] != -1:
#         s[right_child_index] += s[parent_node_index]
#         node_queue.append(right_child_index)
#         max_time = max(max_time,s[right_child_index])
#
# print(max_time)


# 66

# 输入
# 20*19*20
# 输出
# tst


# s = list(map(int, '20*19*20'.split('*')))
# mw = 'abcdefghijklmnopqrstuvwxyz'
#
# res = []
#
# for i in s:
#     res.append(mw[i-1])
#
# print(''.join(res))


# 67

# 输入
# 5
# 5 15 40 30 10
# 输出
# 40 100 30 60 15 30 5 15 10

# n = int('5')
# nn = list(map(int, '5 15 40 30 10'.split()))
# nn.sort()
#
# print(nn)
# res = [[nn[1]]]
# for i in range(1, n):
#     if i == 1:
#         left = nn[0]
#         right = nn[0] + nn[i]
#         res.append([left, right])
#     else:
#         left = nn[i]
#         res.append([left, left + right])
#         right += left
# print(res)
# res = res[::-1]
# print(' '.join(f'{x} {y}' for x, y in res[:-1]), *res[-1])


# 68

# 输入
# 5
# 1,2
# 1,1,0,1,0
# 1,1,0,0,0
# 0,0,1,0,1
# 1,0,0,1,0
# 0,0,1,0,1
# 输出
# 3


# N = int('5')
# CN = list(map(int, '1,2'.split(',')))
#
# s = [[1, 1, 0, 1, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 1], [1, 0, 0, 1, 0], [0, 0, 1, 0, 1]]
#
# CCN = CN.copy()
# count = 0
#
# for i in range(N):
#     for j in range(N):
#         if s[i][j] == 1 and i != j and j not in CCN:
#             CCN.append(j)
#         count += 1
# print(CCN)
# print(len(CCN)-len(CN))
# print(count)


# 69

# 输入
# 7
# 1 2 2 7 3 6 1
# 3
# 输出
# 10

# 输入
# 3
# 1 2 3
# 3
# 输出
# 6

# 输入
# 4
# 4 2 2 3
# 2
# 输出
# 7

# import sys
#
# ln = int('7')
# nums = list(map(int, '1 2 2 7 3 6 1'.split()))
# N = int('3')
#
# if ln == N:
#     print(sum(nums))
# else:
#     total = sum(nums)
#     min_total = sys.maxsize
#     for i in range(ln - N):
#         min_total = min(min_total, sum(nums[i:i + ln - N]))
#
#     print(total - min_total)


# 70

# 输入
# 10 10 255 34 0 1 255 8 0 3 255 6 0 5 255 4 0 7 255 2 0 9 255 21
# 3 4
# 输出
# 0

# 输入
# 10 10 56 34 99 1 87 8 99 3 255 6 99 5 255 4 99 7 255 2 99 9 255 21
# 3 4
# 输出
# 99

# 输入
# 10 10 255 34 0 1 255 8 0 3 255 6 0 5 255 4 0 7 255 2 0 9 255 21
# 3 5
# 输出
# 255

# s = list(map(int, '10 10 255 34 0 1 255 8 0 3 255 6 0 5 255 4 0 7 255 2 0 9 255 21'.split()))
#
# x, y = map(int, '3 5'.split())
#
# posn = x * s[0] + y + 1
#
# poss = 0
# for i in range(2, len(s), 2):
#     poss += s[i + 1]
#     if poss >= posn:
#         print(s[i])
#         break


# 71

# 输入
# 1
# App1 1 09:00 10:00
# 09：30
# 输出
# App1

# 输入
# 2
# App1 1 09:00 10:00
# App2 2 09:10 09:30
# 09：20
# 输出
# App2

# 输入
# 2
# App1 1 09:00 10:00
# App2 2 09:10 09:30
# 09：50
# 输出
# NA


# N = int('2')
# s = [['App1', '1', '09:00', '10:00'], ['App2', '2', '09:30', '09:50'], ['App3', '2', '09:20', '09:40']]
# sr = '09:40'
#
# res = []
# s.sort(key=lambda x: time.strptime(x[2], '%H:%M'))
# # print(time.strptime(sr, '%H:%M'))
#
# for i in s:
#     if len(res) == 0:
#         res.append(i)
#     else:
#         if int(i[1]) > int(res[-1][1]) and time.strptime(i[2], '%H:%M') <= time.strptime(res[-1][3], '%H:%M'):
#             res[-1][3] = i[2]
#             res.append(i)
#         elif int(i[1]) > int(res[-1][1]) and time.strptime(i[2], '%H:%M') > time.strptime(res[-1][3], '%H:%M'):
#             res.append(i)
#         elif int(i[1]) == int(res[-1][1]) and time.strptime(i[2], '%H:%M') > time.strptime(res[-1][3], '%H:%M'):
#             res.append(i)
#         elif int(i[1]) < int(res[-1][1]) and time.strptime(i[2], '%H:%M') > time.strptime(res[-1][3], '%H:%M'):
#             res.append(i)
# print(res)
# tag = True
# for j in res:
#     if time.strptime(j[2], '%H:%M') <= time.strptime(sr, '%H:%M') <= time.strptime(j[3], '%H:%M'):
#         print(j[0])
#         tag = False
#
# if tag:
#     print('NA')


# 72

# 输入
# 2 2 3
# 输出
# 2

# 输入
# 2 2 2 2 2 2 2 2 4 4 4 4 4 6 6
# 输出
# 5

# import math
#
# s = list(map(int, '2 2 2 2 2 2 2 2 4 4 4 4 4 6 6'.split()))

# counts = []
# res = 0

# for i in s:
#     while i >= len(counts):
#         counts.append(0)
#     counts[i] += 1
# print(counts)
# for j, count in enumerate(counts):
#     if count > 0:
#         d = j + 1
#         res += math.ceil(count / d)
# print(res)

# counts = {}
# for i in s:
#     counts[i + 1] = counts.get(i + 1, 0) + 1
# print(counts)
# res = 0
# for j in counts:
#     res += math.ceil(counts[j] / j)
# print(res)


# 73

# 输入
# 5 4
# 1
# 1
# 2
# 3
# 5
# 1 2 3
# 1 4
# 3 4 5
# 2 3 4
# 输出
# 3 4 1 2

# 输入
# 3 3
# 3
# 1
# 5
# 1 2 3
# 1 2 3
# 1 2 3
# 输出
# 1 2 3

# N, M = map(int, '5 4'.split())
#
# # T = []
# # for i in range(N):
# #     T.append(int(input()))
#
# T = [1, 1, 2, 3, 5]
#
# # Y = []
# # for j in range(M):
# #     Y.append(list(map(int,input().split())))
#
# Y = [[1, 2, 3], [1, 4], [3, 4, 5], [2, 3, 4]]
#
# res = {}
# for k in range(M):
#     values = 0
#     for p in Y[k]:
#         values += T[p - 1]
#     res[k + 1] = values
#
# res = sorted(res.items(), key=lambda x: (-x[1], x[0]))
#
# for key in res:
#     print(key[0])


# 74

# 输入
# 9 4
# 输出
# 1 2 3
# * * 4
# 9 * 5
# 8 7 6

# 输入
# 3 5
# 输出
# 1
# 2
# 3
# *
# *

# import math
#
# n, m = map(int, '120 7'.split())
# col = math.ceil(n / m)
#
# res = [['*' for _ in range(col)] for _ in range(m)]
#
# num = 1
# top, bottom, left, right = 0, m - 1, 0, col - 1
#
# while num <= n:
#     for i in range(left, right + 1):  # 从左到右
#         if num <= n:
#             res[top][i] = num
#             num += 1
#     top += 1
#     for i in range(top, bottom + 1):  # 从上到下
#         if num <= n:
#             res[i][right] = num
#             num += 1
#     right -= 1
#     for i in range(right, left - 1, -1):  # 从右到左
#         if num <= n:
#             res[bottom][i] = num
#             num += 1
#     bottom -= 1
#     for i in range(bottom, top - 1, -1):  # 从下到上
#         if num <= n:
#             res[i][left] = num
#             num += 1
#     left += 1
#
# for j in res:
#     print(*j)


# 75

# 输入
# 1
# 0 1
# 3 2
# 输出
# 1

# m = int('2')
# um = [[0, 1], [3, 2]]
#
# if m <= 0 or m >= 100:
#     print(-1)
# else:
#     um.sort(key=lambda x: x[0])
#     start = 0
#     bfstart = -1
#     minSizeDiff = float('inf')
#
#     for i in um:
#         blockStart, blockSize = i
#         if blockStart < start or blockSize <= 0 or blockStart + blockSize > 100:
#             print(-1)
#         else:
#             freeSpace = blockStart - start
#             if m <= freeSpace and (freeSpace - m) < minSizeDiff:
#                 bfstart = start
#                 minSizeDiff = freeSpace - m
#             start = blockStart + blockSize
#
#     if 100 - start >= m and (100 - start - m) < minSizeDiff:
#         bfstart = start
#
#     print(bfstart)

# a = float('inf')
# if 1000> a:
#     print(1)
# else:
#     print(0)


# 76

# 输入
# 2 11
# 3
# 输出
# 5.5

# M, N = map(int, '3 11'.split())
# speeds = [3, 4, 8]
#
# arrivalTimes = [0] * M
# arrivalTimes[0] = N / speeds[0]
#
# for index in range(1, M):
#     estimatedTime = N / speeds[index] + index
#
#     adjustedTime = max(estimatedTime, arrivalTimes[index - 1])
#     arrivalTimes[index] = adjustedTime
#
# print(arrivalTimes[M - 1] - M + 1)


# 77

# 输入
# 4 4
# 2 1 0 3
# 0 1 2 1
# 0 3 0 0
# 0 0 0 0
# 输出
# 2

# 输入
# 4 4
# 2 1 2 3
# 0 1 0 0
# 0 1 0 0
# 0 1 0 0
# 输出
# 0


# dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]  # 上，下，右，左
#
#
# def dfs(currX, currY, targetX, targetY, map, visited, person):
#     if currX == targetX and currY == targetY:
#         return True
#
#     for dir in dirs:
#         nextX, nextY = currX + dir[0], currY + dir[1]
#         if nextX < 0 or nextY < 0 or nextX >= len(map) or nextY >= len(map[0]) or map[nextX][nextY] == 1 or \
#                 visited[nextX][nextY][person]:
#             continue
#         visited[nextX][nextY][person] = True
#         if dfs(nextX, nextY, targetX, targetY, map, visited, person):
#             return True
#
#     return False
#
#
# m, n = map(int, '4 4'.split())
# map = [[2, 1, 0, 3], [0, 1, 2, 1], [0, 3, 0, 0], [0, 0, 0, 0]]
# visited = [[[False, False] for _ in range(n)] for _ in range(m)]
# persons = []
# targets = []
#
# for i in range(m):
#     for j in range(n):
#         if map[i][j] == 2:
#             persons.append([i, j])
#         elif map[i][j] == 3:
#             targets.append([i, j])
#
# xiaohua = persons[0]
# xiaowei = persons[1]
# res = 0
#
# for target in targets:
#     visited = [[[False, False] for _ in range(n)] for _ in range(m)]
#     if dfs(xiaohua[0], xiaohua[1], target[0], target[1], map, visited, 0):
#         visited = [[[False, False] for _ in range(n)] for _ in range(m)]
#         if dfs(xiaowei[0], xiaowei[1], target[0], target[1], map, visited, 1):
#             res += 1
#
# print(res)


# 78

# 输入
# 2 2
# 1 0
# 1 1
# 输出
# 3

# 输入
# 3 3
# 1 0 1
# 0 1 0
# 1 0 1
# 输出
# 0

# 输入
# 5 4
# 1 0 1 1
# 0 1 1 0
# 1 0 0 1
# 0 1 1 0
# 1 0 0 1
# 输出
# 4


# def dfs(i, j):
#     if i < 0 or i >= n or j < 0 or j >= m or s[i][j] == 0:
#         return 0
#     if visited[i][j]:
#         return 0
#     visited[i][j] = True
#
#     count = 1
#     count += dfs(i - 1, j)
#     count += dfs(i + 1, j)
#     count += dfs(i, j - 1)
#     count += dfs(i, j + 1)
#
#     return count
#
#
# n, m = map(int, '5 4'.split())
# s = [[1, 0, 1, 1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]]
#
# visited = [[False for _ in range(m)] for _ in range(n)]
#
# ans = 0
#
# for i in range(n):
#     for j in range(m):
#         ans = max(ans, dfs(i, j))
#
# print(ans)


# 79

# 输入
# 1,2<A>00
# 输出
# 1,2100

# 输入
# <B>12,1
# 输出
# 112,1

# 输入
# <B<12,1
# 输出
# -1


# s = '<C>12,1A,32e'.split(',')
#
# bh = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#
# res = []
# tag = True
#
# for i in s:
#     if '<' not in i and '>' not in i:
#         res.append(i)
#     elif ('<' in i and '>' not in i) or ('<' not in i and '>' in i):
#         print(-1)
#         tag = False
#         break
#     else:
#         left = i.index('<')
#         right = i.index('>')
#         if left > right or right - left != 2 or bh.index(i[left+1]) >= len(s):
#             print(-1)
#             tag = False
#             break
#         else:
#             i = i[:left] + s[bh.index(i[left+1])] + i[right+1:]
#             res.append(i)
#
# if tag:
#     print(','.join(res))


# 80

# 输入
# 3
# 3
# 1 2 3 0
# 1 3 1 0
# 2 3 5 0
# 输出
# 4

# 输入
# 3
# 3
# 1 2 3 0
# 1 3 1 0
# 2 3 5 1
# 输出
# 1

# 输入
# 3
# 1
# 1 2 5 0
# 输出
# -1

# N = int('3')
# M = int('3')
#
# # s = []
#
# # for i in range(M):
# #     s1 = input().split()
# #     if s1:
# #         s.append(list(map(int, s1)))
#
#
# s = [[1, 2, 3, 0], [1, 3, 1, 0], [2, 3, 5, 0]]
# s.sort(key=lambda x: (-x[3], x[2]))
#
# minZ = 0
# PP = []
#
# if len(s) < M:
#     print(-1)
# else:
#     for i in s:
#         if i[3] == 0:
#             if i[0] not in PP:
#                 PP.append(i[0])
#             if i[1] not in PP:
#                 PP.append(i[1])
#             minZ += i[2]
#         else:
#             if i[0] not in PP:
#                 PP.append(i[0])
#             if i[1] not in PP:
#                 PP.append(i[1])
#         if len(PP) == N:
#             print(minZ)
#             break
# if len(PP) != N:
#     print(-1)


'''
描述
输入int型数组，询问该数组能否分成两组，使得两组中各元素加起来的和相等，并且，所有5的倍数必须在其中一个组中，所有3的倍数在另一个组中（不包括5的倍数），
不是5的倍数也不是3的倍数能放在任意一组，可以将数组分为空数组，能满足以上条件，输出true；不满足时输出false。
数据范围：每个数组大小满足
1≤n≤50  ，输入的数据大小满足
输入描述：
第一行是数据个数，第二行是输入的数据
输出描述：
返回true或者false
输入：
4
1 5 -5 1
输出：
true
说明：
第一组：5 -5 1
第二组：1

输入：
3
3 5 8
输出：
false
说明：
由于3和5不能放在同一组，所以不存在一种分法。

输入：
5
1 0 2 3 -2
输出：
true
'''

# def dfs(sum_five, sum_three, other):
#     if len(other) == 0:
#         if sum_five != sum_three:
#             return False
#         else:
#             return True
#     else:
#         return dfs(sum_five + other[0], sum_three, other[1:]) or dfs(
#             sum_five, sum_three + other[0], other[1:]
#         )
#
#
# n = int(input())
# s = list(map(int, input().split()))
#
# other = []
# five = []
# three = []
# for i in s:
#     if abs(i) > 0:
#         if i % 3 == 0:
#             three.append(i)
#         elif i % 5 == 0:
#             five.append(i)
#         else:
#             other.append(i)
#
# sum_three = sum(three)
# sum_five = sum(five)
#
#
# if sum(s) % 2 != 0:
#     print("false")
# else:
#     if dfs(sum_five, sum_three, other):
#         print("true")
#     else:
#         print("false")


'''
矩阵乘法的运算量与矩阵乘法的顺序强相关。
例如：
A是一个50×10的矩阵，B是10×20的矩阵，C是20×5的矩阵
计算A*B*C有两种顺序：((AB)C)或者(A(BC))，前者需要计算15000次乘法，后者只需要3500次。
编写程序计算不同的计算顺序需要进行的乘法次数。
数据范围：矩阵个数：
1≤n≤15 ，行列数：
保证给出的字符串表示的计算顺序唯一。
进阶：时间复杂度：
O(n) ，空间复杂度：
O(n)
输入描述：
输入多行，先输入要计算乘法的矩阵个数n，每个矩阵的行数，列数，总共2n的数，最后输入要计算的法则
计算的法则为一个字符串，仅由左右括号和大写字母（'A'~'Z'）组成，保证括号是匹配的且输入合法！
输出描述：
输出需要进行的乘法次数
输入：
3
50 10
10 20
20 5
(A(BC))

输出：
3500
'''

# while True:
#     try:
#         n = int(input())
#         arr = []
#         order = []
#         res = 0
#         for i in range(n):
#             arr.append(list(map(int, input().split())))  # 处理输入的矩阵行列数据
#         f = input()
#         for i in f:
#             if i.isalpha():
#                 order.append(arr[ord(i) - 65])  # 将字母转换成第几个矩阵的处理信息
#             elif i == ")" and len(order) >= 2:  # 读到右括号就处理最近的两个矩阵相乘的结果
#                 b = order.pop()
#                 a = order.pop()
#                 res += a[1] * b[1] * a[0]  # 累计到res中
#                 order.append([a[0], b[1]])
#         print(res)
#     except:
#         break


'''
描述
计算24点是一种扑克牌益智游戏，随机抽出4张扑克牌，通过加(+)，减(-)，乘(*), 除(/)四种运算法则计算得到整数24，本问题中，扑克牌通过如下字符或者字符串表示，其中，小写joker表示小王，大写JOKER表示大王：
3 4 5 6 7 8 9 10 J Q K A 2 joker JOKER
本程序要求实现：输入4张牌，输出一个算式，算式的结果为24点。
详细说明：
1.运算只考虑加减乘除运算，没有阶乘等特殊运算符号，没有括号，友情提醒，整数除法要当心，是属于整除，比如2/3=0，3/2=1；
2.牌面2~10对应的权值为2~10, J、Q、K、A权值分别为为11、12、13、1；
3.输入4张牌为字符串形式，以一个空格隔开，首尾无空格；如果输入的4张牌中包含大小王，则输出字符串“ERROR”，表示无法运算；
4.输出的算式格式为4张牌通过+-*/四个运算符相连，中间无空格，4张牌出现顺序任意，只要结果正确；
5.输出算式的运算顺序从左至右，不包含括号，如1+2+3*4的结果为24，2 A 9 A不能变为(2+1)*(9-1)=24
6.如果存在多种算式都能计算得出24，只需输出一种即可，如果无法得出24，则输出“NONE”表示无解。
7.因为都是扑克牌，不存在单个牌为0的情况，且没有括号运算，除数(即分母)的数字不可能为0
数据范围：一行由4张牌组成的字符串
输入描述：
输入4张牌为字符串形式，以一个空格隔开，首尾无空格；
输出描述：
输出怎么运算得到24，如果无法得出24，则输出“NONE”表示无解，如果输入的4张牌中包含大小王，则输出字符串“ERROR”，表示无法运算；

输入：
A A A A
输出：
NONE
说明：
不能实现

输入：
4 2 K A
输出：
K-A*4/2
说明：
A+K*2-4也是一种答案，输出任意一种即可

输入：
B 5 joker 4
输出：
ERROR
说明：
存在joker，输出ERROR

输入：
K Q 6 K
输出：
NONE
说明：
按一般的计算规则来看，K+K-(Q/6)=24 或 K-((Q/6)-K)=24，但是因为这个题目的运算不许有括号，
所以去掉括号后变为 K+K-Q/6=26-Q/6=14/6=2 或 K-Q/6-K=1/6-K=0-K=-13，其它情况也不能运算出24点，故不存在，输出NONE

'''

# from itertools import permutations
#
# # a = 'abc'
# # a = [1,2,3]
# #
# # print(permutations(a, 3))
#
# card = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# order = range(1, 14)
# card_order = dict(zip(card, order))
# opts = ["+", "-", "*", "/"]
#
#
# def cal(a1, a2, opt):
#     if opt == 0:
#         return a1 + a2
#     elif opt == 1:
#         return a1 - a2
#     elif opt == 2:
#         return a1 * a2
#     elif opt == 3:
#         return a1 / a2
#
#
# def cal24(cards):
#     if "joker" in cards or "JOKER" in cards:
#         print("ERROR")
#         return
#     num_orders = permutations(cards, 4)
#     for nums in num_orders:
#         for i in range(4):
#             a = cal(card_order[nums[0]], card_order[nums[1]], i)
#             for j in range(4):
#                 b = cal(a, card_order[nums[2]], j)
#                 for k in range(4):
#                     c = cal(b, card_order[nums[3]], k)
#                     if c == 24:
#                         print("%s%s%s%s%s%s%s" % (nums[0], opts[i], nums[1], opts[j], nums[2], opts[k], nums[3]))
#                         return
#     print("NONE")
#     return
#
#
# # cards = input().split()
# cards = '4 2 K A'.split()
# cal24(cards)


# cards_dict = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
#               'K': 13}
#
#
# def dfs(wait, target, out):
#     if len(wait) == 1:
#         c = cards_dict[wait[0]]
#         if c == target:
#             res.append(wait[0] + out)
#     else:
#         for i in range(len(wait)):
#             c = cards_dict[wait[i]]
#             w = wait[:i] + wait[i + 1:]
#             dfs(w, target - c, '+' + wait[i] + out)
#             dfs(w, target + c, '-' + wait[i] + out)
#             dfs(w, target * c, '/' + wait[i] + out)
#             dfs(w, target / c, '*' + wait[i] + out)
#
#
# cards = '4 2 K A'.split()
# res = []
# if "joker" in cards or "JOKER" in cards:
#     print("ERROR")
# else:
#     dfs(cards, 24, '')
#     if not res:
#         print('NONE')
#     else:
#         print(res)


# 81
# 输入
# 4
# 1 1 2 2
# 输出
# 2

# 输入
# 10
# 1 1 1 1 1 9 8 3 7 10
# 输出
# 3


# def dfs(stones, targetWeight, i=0, res=None, count=None):
#     global m
#     m += 1
#     if res is None:
#         res = []
#     if count is None:
#         count = []
#     if sum(count) == targetWeight:
#         if count not in res:
#             res.append(count)
#         count = []
#         return
#     if i == len(stones) or sum(count) > targetWeight:
#         return
#
#     dfs(stones, targetWeight, i + 1, res, count + [stones[i]])
#     dfs(stones, targetWeight, i + 1, res, count)
#     return res
#
#
# n = int('10')
#
# stones = list(map(int, '1 1 1 1 1 9 8 3 7 10'.split()))
#
# totalWeight = sum(stones)
# targetWeight = totalWeight // 2
#
# m = 0
# start_time = time.time()
# print(start_time)
# if totalWeight % 2 == 0:
#     res = dfs(stones, targetWeight)
#     print(res)
#     print(min([len(i) for i in res]))
#     print(m)
# else:
#     print(-1)
#
# end_time = time.time()
# print(f'{(end_time-start_time)*1000:.4f}')


# 82
# 输入
# 5 14 30 100
# 1 3 5 20 21 200 202 230
# 输出
# 2

# price = list(map(int, '10 14 30 100'.split()))
# date = list(map(int, '1 3 5 20 21 200 202 230'.split()))
#
# res = []
#
# for i in range(len(price)):
#     totalPrice = 0
#     if i == 0:
#         totalPrice = price[i] * len(date)
#     elif i == 1:
#         start = 0
#         count = 0
#         for j in range(1, len(date)):
#             if date[j] - date[start] + 1 > 3:
#                 count += 1
#                 start = j
#         totalPrice = price[i] * (count + 1)
#     elif i == 2:
#         start = 0
#         count = 0
#         for j in range(1, len(date)):
#             if date[j] - date[start] + 1 > 7:
#                 count += 1
#                 start = j
#         totalPrice = price[i] * (count + 1)
#     elif i == 3:
#         start = 0
#         count = 0
#         for j in range(1, len(date)):
#             if date[j] - date[start] + 1 > 30:
#                 count += 1
#                 start = j
#         totalPrice = price[i] * (count + 1)
#
#     res.append(totalPrice)
# print(res)
# print(min(res))


#
#
# a = ['1', '2', '3']
# b = 'abc'
# for i in permutations(a):
#     print(i)
# for i in permutations(b,2):
#     print(i)


'''
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。
有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
每个右括号都有一个对应的相同类型的左括号。
输入：s = "()[]{}" 或者 "{[]}"
输出：true
'''

# def test(s):
#     if len(s) % 2 != 0:
#         return False
#
#     stack = []
#     pairs = {
#         ')': '(',
#         '}': '{',
#         ']': '['
#     }
#     for i in s:
#         if i in pairs:
#             if not stack or stack[-1] != pairs[i]:
#                 return False
#             stack.pop()
#         else:
#             stack.append(i)
#     return not stack
#
#
# s = "]()["
# print(test(s))


'''
给定一个循环数组 nums （ nums[nums.length - 1] 的下一个元素是 nums[0] ），返回 nums 中每个元素的 下一个更大元素 。
数字 x 的 下一个更大的元素 是按数组遍历顺序，这个数字之后的第一个比它更大的数，这意味着你应该循环地搜索它的下一个更大的数。如果不存在，则输出 -1 。
输入: nums = [1,2,3,4,3]
输出: [2,3,4,-1,4]
'''

# nums = [1, 2, 3, 4, 3]
#
# n = len(nums)
# res = []
#
# for i in range(n):
#     tag = True
#     for j in range(i + 1, 2 * n):
#         if nums[j % n] > nums[i]:
#             res.append(nums[j % n])
#             tag = False
#             break
#     if tag:
#         res.append(-1)
#
# print(res)

'''
给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
'''

# def test(temperatures):
#     stack = []
#     answer = [0] * len(temperatures)
#     for i in range(len(temperatures)):
#         tem = temperatures[i]
#         while stack and tem > temperatures[stack[-1]]:
#             index = stack.pop()
#             answer[index] = i - index
#         stack.append(i)
#     return answer
#
#
# temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
# print(test(temperatures))
#
# print(temperatures.pop())


#  创建类
# class Person():
#     """ 实例方法 """
#
#     def __init__(self, name='xiaosan', age='18', sex='female'):
#         self.name = name
#         self.age = age
#         self.sex = sex
#         print("构造方法。")
#
#     # 实例方法
#     def say(self):
#         print("实例方法。")
#
#     # 类方法
#     @classmethod
#     def info(cls):
#         print("正在调用类方法。")
#
#     def __repr__(self):
#         return 'Person=' + self.name
#
#
# pp = Person()
# # print(dir(pp))
# print(pp.__dict__)
# print(getattr(pp, 'name'))
