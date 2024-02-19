"""磁盘的容量单位常用的有M，G，T这三个等级，它们之间的换算关系为1T = 1024G，1G =
1024M，现在给定n块磁盘的容量，请对它们按从小到大的顺序进行稳定排序，例如给定5
块盘的容量，1T，20M，3G，10G6T，3M12G9M排序后的结果为20M，3G，3M12G9M，
1T，10G6T。注意单位可以重复出现，上述3M12G9M表示的容量即为3M+12G+9M，和
12M12G相等。
输入描述：
输入第一行包含一个整数n(2 <= n <= 100)，表示磁盘的个数，接下的n行，每行一个字符串
(长度大于2，小于30)，表示磁盘的容量，由一个或多个格式为mv的子串组成，其中m表示
容量大小，v表示容量单位，例如20M，1T，30G，10G6T，3M12G9M。
磁盘容量m的范围为1到1024的正整数，容量单位v的范围只包含题目中提到的M，G，T三
种，换算关系如题目描述。
输出描述：
输出n行，表示n块磁盘容量排序后的结果。"""
# import datetime

# def mem_calc(s):
#     try:
#         a = ''
#         num = 0
#         if s[-1].isalpha():
#             for i in s:
#                 if i.isdigit():
#                     a = a + i
#                 if i.isalpha():
#                     if i == 'M':
#                         num = num + int(a)
#                     elif i == 'G':
#                         num = num + int(a) * 1024
#                     elif i == 'T':
#                         num = num + int(a) * 1024 * 1024
#                     else:
#                         return '格式错误'
#                     a = ''
#             return num
#         else:
#             return '格式错误'
#     except Exception:
#         return '格式错误'
#
#
# while True:
#     try:
#         s = []
#
#         n = int(input())
#         for i in range(n):
#             s1 = input()
#             s.append(s1)
#
#         s = sorted(s, key=lambda x: (mem_calc(x), s.index(x)))
#         for i in s:
#             print(i)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
一群大雁往南飞，给定一个字符串记录地面上的游客听到的大雁叫声，请给出叫声最少由
几只大雁发出。具体的：
1. 大雁发出的完整叫声为"quack"，因为有多只大雁同一时间嘎嘎作响，所以字符串中可能
会混合多个 "quack"。
2. 大雁会依次完整发出 "quack"，即字符串中‘q’, ’u’, ’a’, ’c’, ’k’ 这 5个
字母按顺序完整存在才能计数为一只大雁。如果不完整或者没有按顺序则不予计数。
3. 如果字符串不是由‘q’, ’u’, ’a’, ’c’, ’k’字符组合而成，或者没有找到一
只大雁，请返回 -1。
输入描述：
一个字符串，包含大雁quack的叫声。1 <= 字符串长度 <= 10000
字符串中的字符只有'q', 'u', 'a', 'c', 'k'
输出描述：
大雁的数量'''

# while True:
#     try:
#         s = input()
#         s_list = list(s)
#         if len(s_list) % 5 == 0:
#             flag = True
#             for i in range(int(len(s_list) / 5)):
#                 q_num = s_list.index('q')
#                 u_num = s_list.index('u')
#                 a_num = s_list.index('a')
#                 c_num = s_list.index('c')
#                 k_num = s_list.index('k')
#                 if q_num < u_num and u_num < a_num and a_num < c_num and c_num < k_num:
#                     s_list.pop(s_list.index('q'))
#                     s_list.pop(s_list.index('u'))
#                     s_list.pop(s_list.index('a'))
#                     s_list.pop(s_list.index('c'))
#                     s_list.pop(s_list.index('k'))
#                 else:
#                     print('-1')
#                     flag = False
#                     break
#             if flag:
#                 print(int(len(s) / 5))
#         else:
#             print('-1')
#
#     except Exception:
#         print('-1')

# s = 'quack'
# s1 = list(s)
# print(int(len(s1)/5))
# print(s[-1].isalpha())

'''题目描述：
相对开音节构成的结构为辅音+元音（aeiou）+辅音(r除外)+e，常见的单词有bike、cake
等。
给定一个字符串，以空格为分隔符，反转每个单词中的字母，若单词中包含如数字等其他
非字母时不进行反转。
反转后计算其中含有相对开音节结构的子串个数（连续的子串中部分字符可以重复）。
输入描述：
字符串，以空格分割的多个单词，字符串长度<10000，字母只考虑小写
输出描述：
含有相对开音节结构的子串个数，注：个数<10000'''

# def reverse_word(s):
#     for i in s:
#         if not i.isalpha():
#             return 0
#     return 1
#
# while True:
#     try:
#         s = input().strip().split(' ')
#         print(s)
#         num = 0
#         for i in s:
#             num += reverse_word(i)
#         print(num)
#     except Exception:
#         print('格式错误')

'''题目描述：
一个文件目录的数据格式为：目录id，本目录中文件大小，(子目录id列表)。其中目录id全
局唯一，取值范围[1,200]，本目录中文件大小范围[1,1000]，子目录id列表个数[0,10]
例如：1 20 (2,3）表示目录1中文件总大小是20，有两个子目录，id分别是2和3
现在输入一个文件系统中所有目录信息，以及待查询的目录 id ，返回这个目录和及该目
录所有子目录的大小之和。
输入描述：
第一行为两个数字M，N，分别表示目录的个数和待查询的目录id，1 <= M <=100, 1<= N
<=200
接下来M行，每行为1个目录的数据：目录id 本目录中文件大小 (子目录id列表)，子目录
列表中的子目录id以逗号分隔。
输出描述：
待查询目录及其子目录的大小之和
 输入：3 1
      3 15 ()
      1 20 (2)
      2 10 (3)
输出：45
 输入：4 2
      4 20 ()
      5 30 ()
      2 10 (4,5)
      1 40 ()
输出：60
 输入：5 2
      4 20 (1,3)
      5 30 ()
      2 10 (4,5)
      1 40 ()
      3 15 ()
输出：115
'''

# def calc_file(n, f):
#     num = 0
#     for j in f:
#         j_f = j.split(' ')[0]
#         j_n = j.split(' ')[1]
#         n_i = j.split(' ')[2].strip('(').strip(')').split(',')
#         if j_f == n:
#             num = int(j_n)
#             if n_i[0]:
#                 s = 0
#                 for i in n_i:
#                     s += calc_file(i, f)
#                 return num + s
#             return num
#
#
# while True:
#     try:
#         M, N = input().split(' ')
#         file = []
#         for i in range(int(M)):
#             file.append(input())
#         s = calc_file(N, file)
#         print(s)
#
#     except Exception as e:
#         print(e)


'''题目描述：
给一个正整数NUM1，计算出新正整数NUM2，NUM2为NUM1中移除N位数字后的结果，
需要使得NUM2的值最小。
输入描述：
1.输入的第一行为一个字符串，字符串由0-9字符组成，记录正整数NUM1，NUM1长度小
于32。
2.输入的第二行为需要移除的数字的个数，小于NUM1长度。
如：
2615371
4
输出描述：
输出一个数字字符串，记录最小值NUM2。
如：131
补充说明：
输入：2615371  4615371 2548542536
     4 4 4
输出：131 131 242536
'''

# while True:
#     try:
#         NUM1 = input()
#         NUM2 = input()
#         l1 = len(NUM1)
#         l = l1 - int(NUM2)
#         index_n = 0
#         num_min = ''
#         index_m = 0
#         for i in range(l, 0, -1):
#             n1 = NUM1[-i]
#             index_m = l1 - i + 1
#             for j in range(l1 - i - 1, index_n - 1, -1):
#                 if int(NUM1[j]) <= int(n1):
#                     n1 = NUM1[j]
#                     index_m = j + 1
#             num_min += n1
#             index_n = index_m
#         print(num_min)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
给定两个字符集合，一个为全量字符集，一个为已占用字符集。已占用的字符集中的字符
不能再使用，要求输出剩余可用字符集。
输入描述：
1、输入为一个字符串，一定包含@符号。@前的为全量字符集，@后的字为已占用字符
集。
2、已占用字符集中的字符一定是全量字符集中的字符。字符集中的字符跟字符之间使用英
文逗号分隔。
3、每个字符都表示为字符加数字的形式，用英文冒号分隔，比如a:1，表示1个a字符。
4、字符只考虑英文字母，区分大小写，数字只考虑正整形，数量不超过100。
5、如果一个字符都没被占用，@标识仍然存在，例如a:3,b:5,c:2@
输出描述：
输出可用字符集，不同的输出字符集之间回车换行。
注意，输出的字符顺序要跟输入一致。不能输出b:3,a:2,c:2
如果某个字符已全被占用，不需要再输出。
补充说明：
示例1
输入：
a:3,b:5,c:2@a:1,b:2
输出：
a:2,b:3,c:2
说明：
全量字符集为3个a，5个b，2个c。
已占用字符集为1个a，2个b。
由于已占用字符不能再使用，因此，剩余可用字符为2个a，3个b，2个c。
因此输出a:2,b:3,c:2'''

# import re
#
#
# def to_dict(ls: list) -> dict:
#     keys = []
#     values = []
#     for i in ls:
#         if i.isalpha():
#             keys.append(i)
#         elif i.isdigit():
#             values.append(i)
#         else:
#             return {"error": "格式错误"}
#     d = dict(zip(keys, values))
#     return d
#
#
# def subtract_dicts(dict1, dict2):
#     keys = set(dict1.keys()) & set(dict2.keys())
#     result = {}
#     for key in keys:
#         result[key] = int(dict1[key]) - int(dict2[key])
#     for key in dict1.keys():
#         if key not in keys:
#             result[key] = int(dict1[key])
#     return result
#
# # s = 'a:3,b:5,c:2@a:1,b:2'
# # a = s.split('@')
#
# while True:
#     try:
#         s = input().split('@')
#         s1 = re.split('[,:]', s[0])
#         s2 = re.split('[,:]', s[1])
#         r1 = subtract_dicts(to_dict(s1), to_dict(s2))
#         r = ''
#         for k in r1.keys():
#             r += k + ':' + str(r1[k]) + ','
#         print(r[:-1])
#     except Exception:
#         print('格式错误')

'''题目描述：
误码率是最常用的数据通信传输质量指标。它可以理解为“在多少位数据中出现一位差
错”。
移动通信网络中的误码率主要是指比特误码率，其计算公式如下：比特误码率=错误比特
数/传输总比特数，
为了简单，我们使用字符串来标识通信的信息，一个字符错误了，就认为出现了一个误码
输入一个标准的字符串，和一个传输后的字符串，计算误码率
字符串会被压缩，
例如：“2A3B4D5X1Z” 表示 “AABBBDDDDXXXXXZ
用例会保证两个输入字符串解压后长度一致，解压前的长度不一定一致。
每个生成后的字符串长度<100000000。
输入描述：
两行，分别为两种字符串的压缩形式。 每行字符串（压缩后的）长度<100000
输出描述：
一行，错误的字符数量 / 展开后的总长度
补充说明：
注意：展开后的字符串不含数字。
输入：3A3B
     2A4B
输出：1/6
输入：5Y5Z
     5Y5Z
输出：0/10
输入：4Y5Z
     9Y
输出：5/9
'''

# def decompression_s(s):
#     r = ''
#     n = ''
#     for i in s:
#         if i.isdigit():
#             n += i
#         if i.isalpha():
#             r += int(n) * i
#             n = ''
#     return r
#
#
# while True:
#     try:
#         s1 = input()
#         s2 = input()
#
#         dec_s1 = decompression_s(s1)
#         dec_s2 = decompression_s(s2)
#
#         num = 0
#         for i in range(len(dec_s1)):
#             if dec_s1[i] != dec_s2[i]:
#                 num += 1
#
#         print(str(num) + '/' + str(len(dec_s1)))
#     except Exception as e:
#         print('格式错误')

'''题目描述：
给定一个元素类型为小写字符串的数组，请计算两个没有相同字符的元素 长度乘积的最大
值，如果没有符合条件的两个元素，返回0。
输入描述：
输入为一个半角逗号分隔的小写字符串的数组，2 <= 数组长度<=100，0 < 字符串长度<=
50。
输出描述：
两个没有相同字符的元素 长度乘积的最大值。
输入：iwdvpbn,hk,iuop,iikd,kadgpf
输出：14
说明：数组中有5个元素
iwdvpbn 与 hk 无相同的字符，满足条件，iwdvpbn长度为7，hk的长度为2，乘积为14（7*2）
iwdvpbn 与 iuop、iikd、kadgpf均有相同的字符，不满足条件
iuop 与 iikd、kadgpf均有相同的字符，不满足条件
iikd 与 kadgpf有相同的字符，不满足条件
因此，输出为14
'''
# s = 'iwdvpbn,hk,iuop,iikd,kadgpf'
# while True:
#     try:
#         s = input().split(',')
#         ll = len(s)
#         num = 0
#         for i in range(ll):
#             for j in range(i + 1, ll):
#                 if not set(s[i]) & set(s[j]):
#                     num_m = int(len(s[i])) * int(len(s[j]))
#                     if num_m > num:
#                         num = num_m
#         print(num)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
有一个数列a[N] (N=60)，从a[0]开始，每一项都是一个数字。数列中a[n+1]都是a[n]的描
述。其中a[0]=1。
规则如下：
a[0]:1
a[1]:11(含义：其前一项a[0]=1是1个1，即“11”。表示a[0]从左到右，连续出现了1次
“1”）
a[2]:21(含义：其前一项a[1]=11，从左到右：是由两个1组成，即“21”。表示a[1]从左到
右，连续出现了两次“1”)
a[3]:1211(含义：其前一项a[2]=21，从左到右：是由一个2和一个1组成，即“1211”。表示
a[2]从左到右，连续出现了1次“2”，然后又连续出现了1次“1”)
a[4]:111221(含义：其前一项a[3]=1211，从左到右：是由一个1、一个2、两个1组成，即
“111221”。表示a[3]从左到右，连续出现了1次“1”，连续出现了1次“2”，连续出现
了两次“1”)
请输出这个数列的第n项结果（a[n]，0≤n≤59）。
输入描述：
数列的第n项(0≤n≤59)：
4
输出描述：
数列的内容：
111221
'''

# def netx_n(s):
#     num1 = 1
#     n_s = ''
#     for i in range(len(s)):
#         if i < len(s)-1:
#             if s[i] == s[i+1]:
#                 num1 += 1
#                 continue
#             n_s += str(num1) + str(s[i])
#             num1 = 1
#             continue
#         n_s += str(num1) + str(s[i])
#     return n_s
#
# while True:
#     try:
#         n = int(input())
#         if n == 0:
#             print('1')
#         else:
#             f_s = '1'
#             for j in range(n):
#                 f_s = netx_n(f_s)
#             print(f_s)
#     except Exception:
#         print('格式错误')

'''题目描述：
题目描述：
给定一个仅包含0和1的N*N二维矩阵，请计算二维矩阵的最大值，计算规则如下：
1、 每行元素按下标顺序组成一个二进制数（下标越大越排在低位），二进制数的值就是
该行的值。矩阵各行值之和为矩阵的值。
2、允许通过向左或向右整体循环移动每行元素来改变各元素在行中的位置。
 比如： [1,0,1,1,1]向右整体循环移动2位变为[1,1,1,0,1]，二进制数为11101，值为
29。
 [1,0,1,1,1]向左整体循环移动2位变为[1,1,1,1,0]，二进制数为11110，值
为30。
输入描述：
1、输入的第一行为正整数，记录了N的大小，0 < N <= 20。
2、输入的第2到N+1行为二维矩阵信息，行内元素边角逗号分隔。
输出描述：
矩阵的最大值。
输入：5
     1,0,0,0,1
     0,0,0,1,1
     0,1,0,1,0
     1,0,0,1,1
     1,0,1,0,1
输出：122
第一行向右整体循环移动1为，得到本行的最大值[1,1,0,0,0]，二进制值为11000，十进制值为24
第二行向右整体循环移动2为，得到本行的最大值[1,1,0,0,0]，二进制值为11000，十进制值为24
第三行向左整体循环移动1为，得到本行的最大值[1,0,1,0,0]，二进制值为10100，十进制值为20
第四行向右整体循环移动2为，得到本行的最大值[1,1,1,0,0]，二进制值为11100，十进制值为28
第五行向右整体循环移动1为，得到本行的最大值[1,1,0,1,0]，二进制值为11010，十进制值为26
'''

# # def two_ten(s):
# #     num = 0
# #     s = s[::-1]
# #     for i in range(len(s)):
# #         if s[i] == '1':
# #             num += 2 ** i
# #     return num
#
#
# def loop_mov_max(l):
#     max_num = 0
#     for j in range(len(l)):
#         l_end = l[0]
#         l.pop(0)
#         l.append(l_end)
#         # m_num = two_ten(''.join(l))
#         m_num = int(''.join(l), 2)        #2进制转化为10进制
#         if m_num > max_num:
#             max_num = m_num
#     return max_num
#
#
# while True:
#     try:
#         sum_max = 0
#         n = int(input())
#         for k in range(n):
#             two_s = input().split(',')
#             sum_max += loop_mov_max(two_s)
#
#         print(sum_max)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
存在一种虚拟IPv4地址，由4小节组成，每节的范围为0~255，以#号间隔，虚拟IPv4地址可
以转换为一个32位的整数，例如：
128#0#255#255，转换为32位整数的结果为2147549183（0x8000FFFF）
1#0#0#0，转换为32位整数的结果为16777216（0x01000000）
现以字符串形式给出一个虚拟IPv4地址，限制第1小节的范围为1~128，即每一节范围分别
为(1~128)#(0~255)#(0~255)#(0~255)，要求每个IPv4地址只能对应到唯一的整数上。如果是
非法IPv4，返回invalid IP
输入描述：
输入一行，虚拟IPv4地址格式字符串
输出描述：
输出以上，按照要求输出整型或者特定字符
补充说明：
输入不能确保是合法的IPv4地址，需要对非法IPv4（空串，含有IP地址中不存在的字符，
非合法的#分十进制，十进制整数不在合法区间内）进行识别，返回特定错误
输入：100#101#1#5
输出：1684340997
输入：1#2#3
输出：invalid IP
'''

# while True:
#     try:
#         s = input().split('#')
#         ipx = ''
#         tag = True
#         if 1 <= int(s[0]) <= 128:
#             ipx = hex(int(s[0]))[2:].zfill(2)
#         else:
#             print('invalid IP')
#             tag = False
#         for i in range(1, 4):
#             if 0 <= int(s[i]) <= 255:
#                 ipx += hex(int(s[i]))[2:].zfill(2)
#             else:
#                 print('invalid IP')
#                 tag = False
#         if tag:
#             print(int(ipx, 16))
#
#     except Exception:
#         print('invalid IP')


'''题目描述：
有N（3<=N<10000）个运动员，他们的id为0到N-1,他们的实力由一组整数表示。他们之间
进行比赛，需要决出冠亚军。比赛的规则是0号和1号比赛，2号和3号比赛，以此类推，每
一轮，相邻的运动员进行比赛，获胜的进入下一轮;实力值大的获胜，实力值相等的情况，
id小的情况下获胜;,轮空的直接进入下一轮.
输入描述：
输入一行N个数字代表N的运动员的实力值(0<=实力值<=10000000000)。
输出描述：
输出冠亚军的id，用空格隔开。
输入：2 3 4 5
输出：3 1 2
第一轮比赛，id为0实力值为2的运动员和id为1实力值为3的运动员比赛，1号胜出进入下一轮争夺冠亚军，
id为2的运动员和id为3的运动员比赛，3号胜出进入下一轮争夺冠亚军;
冠亚军比赛，3号胜1号;故冠军为3号，亚军为1号。
2号与0号，比赛进行季军的争夺，2号实力值为4，0号实力值2，故2号胜出，得季军。冠亚季军为3 1 2。
'''

# def get_win(d: dict):
#     one = {}
#     two = {}
#     key_list = list(d.keys())
#     for i in range(0, len(key_list) - 1, 2):
#         if int(d[key_list[i]]) < int(d[key_list[i + 1]]):
#             one[key_list[i + 1]] = d[key_list[i + 1]]
#             two[key_list[i]] = d[key_list[i]]
#         elif int(d[key_list[i]]) == int(d[key_list[i + 1]]):
#             if key_list[i] < key_list[i + 1]:
#                 one[key_list[i]] = d[key_list[i]]
#                 two[key_list[i + 1]] = d[key_list[i + 1]]
#             else:
#                 one[key_list[i + 1]] = d[key_list[i + 1]]
#                 two[key_list[i]] = d[key_list[i]]
#         else:
#             one[key_list[i]] = d[key_list[i]]
#             two[key_list[i + 1]] = d[key_list[i + 1]]
#     if len(key_list) % 2 == 1:
#         one[key_list[-1]] = d[key_list[-1]]
#     return one, two
#
#
# def get_sort(a, a_d):
#     for j in a_d:
#         a += str(j) + ' '
#     return a
#
#
# while True:
#     try:
#         N = input().strip().split(' ')
#         M = [i for i in range(len(N))]
#
#         one_n = dict(zip(M, N))
#         two_n = {}
#
#         while len(one_n) > 2:
#             one_n, two_n = get_win(one_n)
#
#         first, second = get_win(one_n)
#         third, forth = get_win(two_n)
#
#         a = ''
#         a = get_sort(a, first)
#         a = get_sort(a, second)
#         a = get_sort(a, third)
#         print(a.strip())
#     except Exception:
#         print('格式错误')


'''题目描述：
A，B两个人玩一个数字比大小的游戏，在游戏前，两个人会拿到相同长度的两个数字序
列，两个数字序列不相同的，且其中的数字是随机的。
A，B各自从数字序列中挑选出一个数字进行大小比较，赢的人得1分，输的人扣1分，相等
则各自的分数不变。 用过的数字需要丢弃。
求A可能赢B的最大分数。
输入描述：
输入数据的第1个数字表示数字序列的长度N，后面紧跟着两个长度为N的数字序列。
输出描述：
A可能赢B的最大分数
补充说明：
提示：
1、这里要求计算A可能赢B的最大分数，不妨假设，A知道B的数字序列，且总是B先挑选
数字并明示。
2、可以采用贪心策略，能赢的一定要赢，要输的尽量减少损失
输入：3
     4 8 10
     3 6 4
输出：3
输入：5
     3 6 7 8 10
     6 6 7 8 9
输出：2
'''

# while True:
#     try:
#         N = int(input())
#         A = list(map(int, input().split()))
#         B = list(map(int, input().split()))
#
#         A.sort(reverse=True)
#         B.sort(reverse=True)
#
#         a_num = 0
#         C = B.copy()
#         for i in range(N):
#             if A[0] > C[i]:
#                 a_num += 1
#                 A.pop(0)
#                 B.remove(C[i])
#         B.sort()
#         for j in range(len(B)):
#             if A[j] < B[j]:
#                 a_num -= 1
#         print(a_num)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
给定一个N*M矩阵，请先找出M个该矩阵中每列元素的最大值，然后输出这M个值中的最
小值
补充说明：
N和M的取值范围均为：[0, 100]
输入：[[1,2],[3,4]]
输出：3
第一列元素1和3，最大值为3；第二列元素2和4，最大值为4；各列最大值3和4的最小值为3
输入：[[1,5,2],[3,4,6],[7,4,8]]
输出：5
'''

# import ast
#
# while True:
#     try:
#         s = input()
#         s = ast.literal_eval(s)
#         max_num = []
#         num = 0
#         for j in range(len(s[0])):
#             for i in range(len(s)):
#                 num = s[0][j]
#                 if s[i][j] > num:
#                     num = s[i][j]
#             max_num.append(num)
#         print(min(max_num))
#
#     except Exception:
#         print('格式错误')
#         pass


'''题目描述：
现在有一队小朋友，他们高矮不同，我们以正整数数组表示这一队小朋友的身高，如数组
{5,3,1,2,3}。
我们现在希望小朋友排队，以“高”“矮”“高”“矮”顺序排列，每一个“高”位置的
小朋友要比相邻的位置高或者相等；每一个“矮”位置的小朋友要比相邻的位置矮或者相
等；
要求小朋友们移动的距离和最小，第一个从“高”位开始排，输出最小移动距离即可。
例如，在示范小队{5,3,1,2,3}中，{5, 1, 3, 2, 3}是排序结果。{5, 2, 3, 1, 3} 虽然也满足
“高”“矮”“高”“矮”顺序排列，但小朋友们的移动距离大，所以不是最优结果。
移动距离的定义如下所示：
第二位小朋友移到第三位小朋友后面，移动距离为1，若移动到第四位小朋友后面，移动距
离为2；
输入描述：
排序前的小朋友，以英文空格的正整数：
4 3 5 7 8
注：小朋友<100个
输出描述：
排序后的小朋友，以英文空格分割的正整数：
4 3 7 5 8
补充说明：
4（高）3（矮）7（高）5（矮）8（高）， 输出结果为最小移动距离，只有5和7交换了位
置，移动距离都是1。
输入：4 1 3 5 2
输出：4 1 5 2 3

输入：5 3 1 2 3
输出：5 1 3 2 3

输入：6 3 1 3 4 3
输出：6 1 3 3 4 3

输入：1 1 1 1 1
输出：1 1 1 1 1

输入：xxx
输出：[]
'''

# while True:
#     try:
#         s = list(map(int, input().split(' ')))
#
#         if len(s) % 2 == 1:
#             for i in range(1, len(s) - 1, 2):
#                 if s[i - 1] < s[i]:
#                     s[i], s[i - 1] = s[i - 1], s[i]
#                 if s[i] > s[i + 1]:
#                     s[i], s[i + 1] = s[i + 1], s[i]
#         else:
#             for i in range(1, len(s) - 1, 2):
#                 if s[i - 1] < s[i]:
#                     s[i], s[i - 1] = s[i - 1], s[i]
#                 if i == len(s) - 3:
#                     if s[i] > s[i + 1]:
#                         s[i], s[i + 1] = s[i + 1], s[i]
#                     if s[i + 1] < s[i + 2]:
#                         s[i + 1], s[i + 2] = s[i + 2], s[i + 1]
#                 else:
#                     if s[i] > s[i + 1]:
#                         s[i], s[i + 1] = s[i + 1], s[i]
#
#         s_end = ''
#         for i in s:
#             s_end += str(i) + ' '
#         print(s_end.strip())
#     except Exception:
#         print('[]')


'''题目描述：
总共有n个人在机房，每个人有一个标号（1 <= 标号 <=n），他们分成了多个团队，需要
你根据收到的m条消息判定指定的两个人是否在一个团队中，具体的：
1、消息构成为：a b c，整数a、b分别代表了两个人的标号，整数c代表指令。
2、c==0代表a和b在一个团队内。
3、c==1代表需要判定a和b的关系，如果a和b是一个团队，输出一行“we are a team”，如
果不是，输出一行“we are not a team”。
4、c为其它值，或当前行a或b超出1~n的范围，输出“da pian zi”。
输入描述：
1、第一行包含两个整数n, m(1 <= n, m <= 100000)，分别表示有n个人和m条消息。
2、随后的m行，每行一条消息，消息格式为:a b c (1 <= a, b <= n, 0 <= c <= 1)。
输出描述：
1、c==1时，根据a和b是否在一个团队中输出一行字符串，在一个团队中输出“we are a 
team”，不在一个团队中输出“we are not a team”。
2、c为其他值，或当前行a或b的标号小于1或者大于n时，输出字符串“da pian zi”。
3、如果第一行n和m的值超出约定的范围时，输出字符串"NULL"。
输入：5 6
     1 2 0
     1 2 1
     1 5 0
     2 3 1
     2 5 1
     1 3 2
输出：we are a team
     we are not a team
     we are a team
     da pian zi
第2行定义了1和2是一个团队
第3行要求进行判定，输出we are a team
第4行定义了1和5是一个团队，自然2和5也是一个团队
第5行要求进行判定，输出 we are not a team
第6行要求进行判定，输出we are a team
第7行c为其他值，输出da pian zi
'''

# while True:
#     try:
#         n, m = input().split(' ')
#         team = []
#         p_team = []
#         for i in range(int(m)):
#             c = input().split(' ')
#             if int(c[2]) == 0:
#                 team.append(c[0])
#                 team.append(c[1])
#             elif int(c[2]) == 1:
#                 if c[0] in set(team) and c[1] in set(team):
#                     p_team.append('we are a team')
#                 else:
#                     p_team.append('we are not a team')
#             else:
#                 p_team.append('da pian zi')
#         for i in p_team:
#             print(i)
#
#     except Exception:
#         print('格式错误')
#         pass


'''题目描述：
斗地主起源于湖北十堰房县，据传是一位叫吴修全的年轻人根据当地流行的扑克玩法“跑
得快”改编的，如今已风靡整个中国，并流行于互联网上。
牌型:
单顺, 又称顺子，最少5张牌，最多12张牌（3⋯A），不能有2，也不能有大小王，不计花
色
例如：3-4-5-6-7-8，7-8-9-10-J-Q，3-4-5-6-7-8-9-10-J-Q-K-A
可用的牌 3<4<5<6<7<8<9<10<J<Q<K<A<2 < B(小王)< C(大王)，每种牌除大小王外有4种
花色(共有 13X4 + 2 张牌)
输入1. 手上已有的牌 2. 已经出过的牌（包括对手出的和自己出的牌）
输出: 对手可能构成的最长的顺子(如果有相同长度的顺子, 输出牌面最大的那一个)，如果
无法构成顺子, 则输出 NO-CHAIN
输入描述：
输入的第一行为当前手中的牌
输入的第二行为已经出过的牌
输出描述：
最长的顺
输入：3-3-3-3-4-4-5-5-6-7-8-9-10-J-Q-K-A
     4-5-6-7-8-8-8
输出：9-10-J-Q-K-A
输入：3-3-3-3-8-8-8-8
     K-K-K-K
输出：NO-CHAIN
输入：3-3-3-4-4-5-5-6-7-8-9-10-J-Q-K-A
     4-5-6-7-8-8-8-9-9-9
输出：10-J-Q-K-A
输入：3-3-3-4-4-5-5-6-7-8-9-10-J-Q-K-A
     3-4-5-6-7-8-8-9-9-9-10-10-10
输出：4-5-6-7-8
输入：3-3-3-4-4-5-5-6-7-8-9-10-J-Q-K-A
     3-4-5-6-7-8-8-8-9-9-10-10-10
输出：NO-CHAIN
'''

# while True:
#     try:
#         a = input().split('-')
#         b = input().split('-')
#         p = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
#         a.extend(b)
#         c = []
#         for i in p:
#             if a.count(i) == 4:
#                 c.append(p.index(i))
#         a_min = 0
#         a_max = 12
#         p_l = []
#         for j in c:
#             if len(p[a_min:j]) >= 5 and len(p[a_min:j]) >= len(p_l):
#                 p_l = p[a_min:j]
#             a_min = j + 1
#
#         if len(p[a_min: a_max]) >= 5 and len(p[a_min: a_max]) >= len(p_l):
#             p_l = p[a_min:a_max]
#
#         if len(p_l) == 0:
#             print('NO-CHAIN')
#         else:
#             p_s = '-'.join(p_l)
#             print(p_s)
#
#     except Exception:
#         print('格式错误')


'''题目描述：
给定一个长度为n的整型数组，表示一个选手在n轮内可选择的牌面分数。选手基于规则选
牌，请计算所有轮结束后其可以获得的最高总分数。选择规则如下：
1、在每轮里选手可以选择获取该轮牌面，则其总分数加上该轮牌面分数，为其新的总分
数。
2、选手也可不选择本轮牌面直接跳到下一轮，此时将当前总分数还原为3轮前的总分数，
若当前轮次小于等于3（即在第1、2、3轮选择跳过轮次），则总分数置为0。
3、选手的初始总分数为0，且必须依次参加每一轮。
输入描述：
第一行为一个小写逗号分割的字符串，表示n轮的牌面分数，1<= n <=20。
分数值为整数，-100 <= 分数值 <= 100。
不考虑格式问题。
输出描述：
所有轮结束后选手获得的最高总分数。
输入：1,-5,-6,4,3,6,-2
输出：11
第一轮选择该牌面，总分数为1
第二轮不选择该轮牌面，总分数还原为0
第三轮不选择该轮牌面，总分数还原为0
第四轮选择该轮牌面，总分数为4
第五轮选择该轮牌面，总分数为7
第六轮选择该轮牌面，总分数为13
第七轮如果不选择该轮牌面，则总分数还原为3轮前分数，即第四轮的总分数4，如果选择该轮牌面，总分数为11，所以选择该轮牌面，最终的最高总分为11
输入：-2,-3,2,6,7,2,3,-6,9,-5
输出：20
'''

# while True:
#     try:
#         s = input().split(',')
#         num = 0
#         s_num = []
#         for i in range(len(s)):
#             num += int(s[i])
#             if i < 3 and num < 0:
#                 num = 0
#             elif i > 3:
#                 if num < s_num[i - 3]:
#                     num = s_num[i - 3]
#             s_num.append(num)
#         print(s_num[-1])
#
#     except Exception:
#         print('格式错误')


'''
题目描述:有一堆长方体积木,它们的宽度和高度都相同,但长度不一。小橙想把这堆积木叠成一面墙,墙的每层可以放一个积木,也可以将两个积木拼接起
来,要求每层的长度相同。若必须用完这些积木,叠成的墙最多为多少层?
输入描述:输入为一行,为各个积木的长度,数字为正整数,并由空格分隔。积木的数量和长度都不超过5000。
输出描述:输出一个数字,为墙的最大层数,如果无法按要求叠成每层长度一致的墙,则输出-1。
补充说明:
示例1
输入:3 6 6 3
输出:3
说明:可以每层都是长度3和6的积木拼接起来,这样每层的长度为9,层数为2;也可以其中两层直接用长度6的积木,两个长度3的积木拼接为一层,这样层数为
3,故输出3。
示例2
输入:1 4 2 3 6
输出:-1
说明:无法用这些积木叠成每层长度一致的墙,故输出-1。
输入:5 5 4 1
输出:3
输入:1 4 2 3 6 4 7 5
输出:4
输入:8 4 2 4 6 3 5 8
输出:5
输入:7 4 3 2 5
输出:3
输入:11 9 2 5 6
输出:3
输入:11 9 2 4 5 8
输出:3
'''

# while True:
#     try:
#         s_a = list(map(int, input().split(' ')))
#         s_b = s_a.copy()
#
#         num_a = 0
#         num_b = 0
#         l = len(s_a)
#         s_c = max(s_a)
#         s_d = sum(s_b) // (len(s_b) // 2)
#
#         for i in range(l):
#             if len(s_a):
#                 if s_a[0] == s_c:
#                     num_a += 1
#                     s_a.remove(s_a[0])
#                 else:
#                     s_e = s_c - s_a[0]
#                     if s_e in s_a[1:]:
#                         s_a.remove(s_a[0])
#                         s_a.remove(s_e)
#                         num_a += 1
#                     else:
#                         num_a = -1
#                         break
#             else:
#                 break
#
#         for i in range(l):
#             if len(s_b):
#                 s_f = s_d - s_b[0]
#                 if s_f in s_b[1:]:
#                     s_b.remove(s_b[0])
#                     s_b.remove(s_f)
#                     num_b += 1
#                 else:
#                     num_b = -1
#                     break
#             else:
#                 break
#
#         print(max(num_a, num_b))
#
#     except Exception:
#         print('格式错误')


'''题目描述:在坐标系中,给定3个矩形,求相交区域的面积。
输入描述:3行输入分别为3个矩形的位置,分别代表
        '左上角x坐标',左上角y坐标',矩形宽',‘矩形高’
        -1000<= x,y < 1000
输出描述:输出3个矩形相交的面积,不相交的输出0
输入：1 6 4 4
     3 5 3 4
     0 3 7 3
输出:2
说明:给定3个矩形A,B,C
A:左上角坐标(1,6),宽4,高4
B:左上角坐标(3,5),宽3,高4
C:左上角坐标(0,3),宽7,高3
3个矩形的相交面积为2
'''

# def get_s(s: list):
#     s_s = []
#     for i in range(s[2] + 1):
#         for j in range(s[3] + 1):
#             s_s.append([s[0] + i, s[1] - j])
#     return s_s
#
#
# while True:
#     try:
#         A = list(map(int, input().split(' ')))
#         B = list(map(int, input().split(' ')))
#         C = list(map(int, input().split(' ')))
#
#         A_S = get_s(A)
#         B_S = get_s(B)
#         C_S = get_s(C)
#         D_S = []
#
#         for k in A_S:
#             if k in B_S and k in C_S:
#                 D_S.append(k)
#         D_C = max(D_S)[0] - min(D_S)[0]
#         D_K = max(D_S)[1] - min(D_S)[1]
#         print(D_C * D_K)
#     except Exception:
#         print('格式错误')


'''题目描述：
在斗地主扑克牌游戏中， 扑克牌由小到大的顺序为：3,4,5,6,7,8,9,10,J,Q,K,A,2，玩家可以
出的扑克牌阵型有：单张、对子、顺子、飞机、炸弹等。
其中顺子的出牌规则为：由至少5张由小到大连续递增的扑克牌组成，且不能包含2。
例如：{3,4,5,6,7}、{3,4,5,6,7,8,9,10,J,Q,K,A}都是有效的顺子；而{J,Q,K,A,2}、
{2,3,4,5,6}、{3,4,5,6}、{3,4,5,6,8}等都不是顺子。
给定一个包含13张牌的数组，如果有满足出牌规则的顺子，请输出顺子。
如果存在多个顺子，请每行输出一个顺子，且需要按顺子的第一张牌的大小（必须从小到
大）依次输出。
如果没有满足出牌规则的顺子，请输出No。
输入描述：
13张任意顺序的扑克牌，每张扑克牌数字用空格隔开，每张扑克牌的数字都是合法的，并
且不包括大小王：
2 9 J 2 3 4 K A 7 9 A 5 6
不需要考虑输入为异常字符的情况
输出描述：
组成的顺子，每张扑克牌数字用空格隔开：
3 4 5 6 7

输入：2 9 J 2 3 4 K A 7 9 A 5 6
输出：3 4 5 6 7
说明：13张牌中,可以组成的顺子只有1组:3 4 5 6 7

输入：2 9 J 10 3 4 K A 7 Q A 5 6
输出：3 4 5 6 7
     9 10 J Q K A
说明：13张牌中,可以组成2组顺子,从小到大分别为:3 4 5 6 7和9 10 J Q K A

输入：2 9 9 9 3 4 K A 10 Q A 5 6
输出：No
说明：13张牌中,无法组成顺子

输入：2 9 9 9 3 4 8 8 J A 10 Q A 5 6 7
输出：3 4 5 6 7 8 9 10 J Q
说明：不输出 3 4 5 6 7 8 9 、 8 9 10 J Q
'''

# while True:
#     try:
#         r = input().split(' ')
#         p = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
#
#         s = []
#
#         a = sorted(list(set(r)), key=lambda n: p.index(n))
#         a_min = p.index(a[0])
#         for i in range(len(p) - 2):
#             if p[i] in r and p[i + 1] not in r:
#                 if len(p[a_min:i + 1]) >= 5:
#                     s.append(p[a_min:i + 1])
#                 if a.index(p[i]) + 1 < len(a):
#                     a_min = p.index(a[a.index(p[i]) + 1])
#             elif i == 10 and p[i] in r and p[i + 1] in r:
#                 if len(p[a_min:i + 1]) >= 5:
#                     s.append(p[a_min:i + 2])
#         if len(s):
#             for j in s:
#                 print(' '.join(j))
#         else:
#             print('No')
#     except Exception:
#         print('格式错误')


'''题目描述：
给定非空字符串s，将该字符串分割成一些子串，使每个子串的ASCII码值的和均为水仙花
数。
1、若分割不成功，则返回0
2、若分割成功且分割结果不唯一，则返回-1
3、若分割成功且分割结果唯一，则返回分割后子串的数目
输入描述：
1、输入字符串的最大长度为200
输出描述：
根据题目描述中情况，返回相应的结果
补充说明：
“水仙花数”是指一个三位数，每位上数字的立方和等于该数字本身，如371是“水仙花
数”，因为：371 = 3^3 + 7^3 + 1^3
输入:abc
输出:0
说明:分割不成功

输入:f3@d5a8
输出:-1
说明:分割成功但分割结果不唯一,可以分割为两组,一组"f3"和"@d5a8",另外一组"f3@d5"和"a8"

输入:AXdddF
输出:2
说明:成功分割且分割结果唯一,可以分割"AX"(153)和"dddF"(370)成两个子串

输入:AXdddFf3
输出:3
说明:成功分割且分割结果唯一,可以分割"AX"(153)和"dddF"(370)和"f3"(153)成三个子串
'''

# def get_s(ss: int):
#     num = 0
#     for i in str(ss):
#         num += int(i) ** 3
#     if num == ss:
#         return True
#     return False
#
#
# while True:
#     try:
#         s = list(map(lambda x: ord(x), input()))
#         s_num = list(map(int, s))
#
#         s_n = []
#         p = 0
#         for j in range(len(s)):
#             n = 0
#             m = 0
#             if p == 0:
#                 for k in range(j, len(s)):
#                     if get_s(sum(s_num[n:k + 1])):
#                         n = k + 1
#                         m += 1
#                         if m == 1:
#                             p = k + 1
#                     if n == len(s):
#                         s_n.append(m)
#                 if m == 0:
#                     break
#             else:
#                 for q in range(p, len(s)):
#                     if get_s(sum(s_num[n:q + 1])):
#                         n = q + 1
#                         m += 1
#                         if m == 1:
#                             p = q + 1
#                     if n == len(s):
#                         s_n.append(m)
#                 if m == 0:
#                     break
#
#         if len(s_n) == 0:
#             print(0)
#         elif len(s_n) == 1:
#             print(s_n[0])
#         else:
#             print('-1')
#
#     except Exception:
#         print('格式错误')


'''题目描述:小明和朋友玩跳格子游戏,有n个连续格子,每个格子有不同的分数,小朋友可以选择从任意格子起跳,但是不能跳连续的格子,也不能回头跳
给定一个代表每个格子得分的非负整数数组,计算能够得到的最高分数。
补充说明:1<=nums.length<=100
        0<= nums[i] <= 1000

输入:1 2 3 1
输出:4
说明:选择跳第一个格子和第三个格子

输入:2 7 9 3 1
输出:12
说明:2+9+1=12
'''

# while True:
#     try:
#         s = list(map(int, input().split(' ')))
#
#         sum1 = 0
#         sum2 = 0
#         flag = True
#         if 1 <= len(s) <= 100:
#             for i in range(0, len(s), 2):
#                 if 0 <= s[i] <= 1000:
#                     sum1 += s[i]
#                 else:
#                     flag = False
#
#             for j in range(1, len(s), 2):
#                 if 0 <= s[j] <= 1000:
#                     sum2 += s[j]
#                 else:
#                     flag = False
#         else:
#             flag = False
#         if flag:
#             print(max(sum1, sum2))
#         else:
#             print('格式错误')
#
#     except Exception:
#         print('格式错误')


'''题目描述：
小牛的孩子生日快要到了，他打算给孩子买蛋糕和小礼物，蛋糕和小礼物各买一个，他的
预算不超过x元。蛋糕cake和小礼物gift都有多种价位的可供选择。
请返回小牛共有多少种购买方案。
输入描述：
第一行表示cake的单价，以逗号分隔
第一行表示gift的单价，以逗号分隔
第三行表示x预算
输出描述：
输出数字表示购买方案的总数
补充说明：
1 <= cake.length <= 10^5
1 <= gift.length <= 10^5
1 <= cake[i],gift[i] <= 10^5
1 <= x <= 2*10^5
输入：10,20,5
     5,5,2
     15
输出：6
说明:解释:小牛有6种购买方案,所选蛋糕与所选礼物在数组中对应的下标分别是
第1种方案:cake[0]+gift[0]=10+5=15;
第2种方案:cake[0]+gift[1]=10+5=15;
第3种方案:cake[0]+gift[2]=10+2=12;
第4种方案:cake[2]+gift[0]=5+5=10;
第5种方案:cake[2]+gift[1]=5+5=10;
第6种方案:cake[2]+gift[2]=5+2=7。
'''

# while True:
#     try:
#         cake = list(map(int, input().split(',')))
#         gift = list(map(int, input().split(',')))
#         x = int(input())
#
#         num = 0
#         for i in cake:
#             for j in gift:
#                 if i + j <= x:
#                     num += 1
#         print(num)
#
#     except Exception:
#         print('格式错误')


'''题目描述:有一个简易内存池,内存按照大小粒度分类,每个应度有若干个可用内存资源,用户会进行一系列内存申请,需要按需分配内存池中的资源,返回申
请结果成功失败列表。分配规则如下:
1、分配的内存要大于等于内存申请量,存在满足需求的内存就必须分配,优先分配粒度小的,但内存不能拆分使用。
2、需要按申请顺序分配,先申请的先分配。
3、有可用内存分配则申请结果为true,没有可用内存分配则返回false
注:不考虑内存释放。
输入描述:输入为两行字符串:
第一行为内存池资源列表,包含内存粒度数据信息,粒度数据间用逗号分割,一个粒度信息内部用冒号分割,冒号前为内存度大小,冒号后为数
量。资源列表不大于1024,每个粒度的数量不大于4096
第二行为申请列表,申请的内存大小间用逗号分隔。申请列表不大100000
输入：64:2,128:1,32:4,1:128
     50,36,64,128,127
输出：true,true,true,false,false
说明:内存池资源包含:64K共2个、128K共1个、32K共4个、1K共128个的内存资源
针对50,36,64,128,127的内存申请序列,分配的内存依次是:64,644,128,NULL,NULL,第三次申请内存时已经将128分配出去,
因此输出结果是:true,true,true,false,false
'''

# while True:
#     try:
#         s = input().split(',')
#         r = list(map(int, input().split(',')))
#
#         keys = list(map(lambda x: int(x.split(':')[0]), s))
#         values = list(map(lambda x: int(x.split(':')[1]), s))
#
#         s_d = dict(sorted(dict(zip(keys, values)).items(), key=lambda x: x[0]))
#         keys = s_d.keys()
#
#         ss = []
#
#         for i in r:
#             flag = True
#             for j in keys:
#                 if i <= j and s_d[j] > 0:
#                     s_d[j] -= 1
#                     ss.append('true')
#                     flag = False
#                     break
#             if flag:
#                 ss.append('false')
#         print(','.join(ss))
#     except Exception:
#         print('格式错误')


'''题目描述:某长方形停车场,每个车位上方都有对应监控器,兰当且仅当在当前车位或者前后左右四个方向任意一个车位范围停车时,监控器才需要打开;
给出某一时刻停车场的停车分布,请统计最少需要打开多少个监控器;
输入描述:第一行输入m,n表示长宽,满足1<m.n<=20;后面输入m行,每行有n个0或1的整数,整数间使用一个空格隔开,表示该行已停车情况,其中0表示
空位,1表示已停;
输出描述:最少需要打开监控器的数量;
输入：3 3
     0 0 0
     0 1 0
     0 0 0
输出：5
'''

# while True:
#     try:
#         m, n = map(int, input().split(' '))
#         s = []
#         for i in range(m):
#             s.append(list(map(int, input().split(' '))))
#
#         num = 0
#         for i in range(m):
#             for j in range(n):
#                 if s[i][j] == 1:
#                     num += 1
#                 elif i - 1 >= 0 and s[i - 1][j] == 1:
#                     num += 1
#                 elif i + 1 < m and s[i + 1][j] == 1:
#                     num += 1
#                 elif j - 1 >= 0 and s[i][j - 1] == 1:
#                     num += 1
#                 elif j + 1 < n and s[i][j + 1] == 1:
#                     num += 1
#         print(num)
#
#     except Exception:
#         print('格式错误')


'''题目描述:C语言有一个库函数:char*strstr(const char *haystack,cornst char *needle),实现在字符串haystack中查找第一次出现字符串 needle的位置,如
果未找到则返回null。
现要求实现一个strstr的增强函数,可以使用带可选段的字符串来模糊查询,与strstr一样返回首次查找到的字符串位置。
可选段使用"[]"标识,表示该位置是可选段中任意一个字符即可满足匹配条件。比如"a[bc]"表示可以匹配"ab"或"ac"
注意目标字符串中可选段可能出现多次。
输入描述:与strstr函数一样,输入参数是两个字符串指针,分别是源字符串和目标字符串。
输出描述:与strstr函数不同,返回的是源字符串中,匹配子字:符串相对于源字符串地址的偏移(从0开始算),如果没有匹配返回-1
补充说明:源字符串中必定不包含'[];目标字符串中[]必定成对出现,且不会出现嵌套。
输入的字符串长度在[1,100]之间。
输入：abcd
     b[cd]
输出：1
说明:相当于是在源字符串中查找bc或者bd,bc子字符串目对于abcd的偏移是1
'''

# def get_s(x, y, ss, sp):
#     for i in range(x + 1, y):
#         sp.append(ss[x - 1] + ss[i])
#     return sp
#
#
# while True:
#     try:
#         a = input()
#         b = list(input())
#         s = []
#
#         while '[' in b:
#             b_x = b.index('[')
#             b_y = b.index(']')
#             s = get_s(b_x, b_y, b, s)
#             b.pop(b_y)
#             b.pop(b_x)
#
#         flag = True
#         for j in s:
#             if j in a:
#                 print(a.index(j))
#                 flag = False
#                 break
#
#         if flag:
#             print('-1')
#
#     except Exception:
#         print('格式错误')


# print(format(round(1.64, 3), '-.4f'))
# print(format(round(23, 3), '8>3d'))
# print('{:8<3d}'.format(round(24, 3)))
# print('%.3f'%round(1.64, 3))


# 华为机试

'''
描述
计算字符串最后一个单词的长度，单词以空格隔开，字符串长度小于5000。（注：字符串末尾不以空格为结尾）
输入描述：
输入一行，代表要计算的字符串，非空，长度小于5000。
输出描述：
输出一个整数，表示输入字符串最后一个单词的长度。
输入：
hello nowcoder
输出：
8
说明：
最后一个单词为nowcoder，长度为8  
'''

# while True:
#     try:
#         s = input().strip().split(' ')
#         print(len(s[-1]))
#
#     except Exception:
#         break


'''
描述
写出一个程序，接受一个由字母、数字和空格组成的字符串，和一个字符，然后输出输入字符串中该字符的出现次数。（不区分大小写字母）
数据范围： 
1≤n≤1000 
输入描述：
第一行输入一个由字母、数字和空格组成的字符串，第二行输入一个字符（保证该字符不为空格）。
输出描述：
输出输入字符串中含有该字符的个数。（不区分大小写字母）
输入：
ABCabc
A
输出：
2
'''

# while True:
#     try:
#         str1 = input().lower()
#         str2 = input().lower()
#
#         print(str1.count(str2))
#     except Exception:
#         break


'''
描述
明明生成了N个1到500之间的随机整数。请你删去其中重复的数字，即相同的数字只保留一个，把其余相同的数去掉，然后再把这些数从小到大排序，按照排好的顺序输出。
数据范围： 
1≤n≤1000  ，输入的数字大小满足 1≤val≤500 
输入描述：
第一行先输入随机整数的个数 N 。 接下来的 N 行每行输入一个整数，代表明明生成的随机数。 具体格式可以参考下面的"示例"。
输出描述：
输出多行，表示输入数据处理后的结果
输入：
3
2
2
1
输出：
1
2
说明：
输入解释：
第一个数字是3，也即这个小样例的N=3，说明用计算机生成了3个1到500之间的随机整数，接下来每行一个随机数字，共3行，也即这3个随机数字为：
2
2
1
所以样例的输出为：
1
2       
'''
# while True:
#     try:
#         N = int(input())
#         str1 = []
#         for i in range(N):
#             s = int(input())
#             if s not in str1:
#                 str1.append(s)
#         str1.sort()
#         for j in str1:
#             print(j)
#
#     except Exception:
#         break


'''
输入一个字符串，请按长度为8拆分每个输入字符串并进行输出；
长度不是8整数倍的字符串请在后面补数字0，空字符串不处理。
输入描述：
连续输入字符串(每个字符串长度小于等于100)
输出描述：
依次输出所有分割后的长度为8的新字符串
输入：
abc
输出：
abc00000
'''

# while True:
#     try:
#         s = input()
#         for i in range(0, len(s), 8):
#             print('{:0<8}'.format(s[i:i+8]))
#
#     except Exception:
#         break

'''
写出一个程序，接受一个十六进制的数，输出该数值的十进制表示。
输入描述：
输入一个十六进制的数值字符串。
输出描述：
输出该数值的十进制字符串。不同组的测试用例用\n隔开。
输入：
0xAA
输出：
170
'''

# while True:
#     try:
#         s = input()
#         print(int(s, 16))
#     except Exception:
#         break


'''
描述
功能:输入一个正整数，按照从小到大的顺序输出它的所有质因子（重复的也要列举）（如180的质因子为2 2 3 3 5 ）
输入描述：
输入一个整数
输出描述：
按照从小到大的顺序输出它的所有质数的因子，以空格隔开。
输入：
180
输出：
2 2 3 3 5
'''

# while True:
#     try:
#         num = int(input())
#         for i in range(2, int(num ** 0.5) + 1):
#             while num % i == 0:
#                 print(i, end=" ")
#                 num = int(num / i)
#         if num > 2:
#             print(num)
#     except Exception:
#         break


'''
描述
数据表记录包含表索引index和数值value（int范围的正整数），请对表索引相同的记录进行合并，即将相同索引的数值进行求和运算，输出按照index值升序进行输出。
提示:
0 <= index <= 11111111
1 <= value <= 100000

输入描述：
先输入键值对的个数n（1 <= n <= 500）
接下来n行每行输入成对的index和value值，以空格隔开

输出描述：
输出合并后的键值对（多行）
输入：
4
0 1
0 2
1 2
3 4
输出：
0 3
1 2
3 4

输入：
3
0 1
0 2
8 9
输出：
0 3
8 9
'''

# while True:
#     try:
#         n = int(input())
#         s = {}
#         for i in range(n):
#             key, value = map(int, input().split(' '))
#             s[key] = s.get(key, 0) + value
#
#         for each in sorted(s):
#             print(each, s[each])
#
#     except Exception:
#         break


'''
描述
输入一个 int 型整数，按照从右向左的阅读顺序，返回一个不含重复数字的新的整数。
保证输入的整数最后一位不是 0 。
输入描述：
输入一个int型整数
输出描述：
按照从右向左的阅读顺序，返回一个不含重复数字的新的整数
输入：
9876673
输出：
37689
'''

# while True:
#     try:
#         a = []
#         s = input()
#         for i in s[::-1]:
#             if i not in a:
#                 a.append(i)
#         print(''.join(a))
#     except Exception as e:
#         print(e)


'''
描述
编写一个函数，计算字符串中含有的不同字符的个数。字符在 ASCII 码范围内( 0~127 ，包括 0 和 127 )，换行表示结束符，不算在字符里。不在范围内的不作统计。多个相同的字符只计算一次
例如，对于字符串 abaca 而言，有 a、b、c 三种不同的字符，因此输出 3 。
数据范围： 
1≤n≤500 
输入描述：
输入一行没有空格的字符串。
输出描述：
输出 输入字符串 中范围在(0~127，包括0和127)字符的种数。
输入：
abc
输出：
3

输入：
aaa
输出：
1
'''

# while True:
#     try:
#         s = input()
#         print(len(set(s)))
#     except Exception:
#         break


'''
描述
输入一个整数，将这个整数以字符串的形式逆序输出
程序不考虑负数的情况，若数字含有0，则逆序形式也含有0，如输入为100，则输出为001
数据范围： 
0≤n≤2 
输入描述：
输入一个int整数
输出描述：
将这个整数以字符串的形式逆序输出
输入：
1516000
输出：
0006151

输入：
0
输出：
0
'''

# while True:
#     try:
#         s = str(input())
#         print(s[::-1])
#     except Exception:
#         break


'''
描述
将一个英文语句以单词为单位逆序排放。例如“I am a boy”，逆序排放后为“boy a am I”
所有单词之间用一个空格隔开，语句中除了英文字母外，不再包含其他字符
数据范围：输入的字符串长度满足 
1≤n≤1000 
注意本题有多组输入
输入描述：
输入一个英文语句，每个单词用空格隔开。保证输入只包含空格和字母。
输出描述：
得到逆序的句子
输入：
I am a boy
输出：
boy a am I

输入：
nowcoder
输出：
nowcoder
'''

# while True:
#     try:
#         s = input().split(' ')
#         print(' '.join(s[::-1]))
#     except Exception:
#         break


'''
描述
给定 n 个字符串，请对 n 个字符串按照字典序排列。
数据范围： 
1≤n≤1000  ，字符串长度满足 
1≤len≤100 
输入描述：
输入第一行为一个正整数n(1≤n≤1000),下面n行为n个字符串(字符串长度≤100),字符串中只含有大小写字母。
输出描述：
数据输出n行，输出结果为按照字典序排列的字符串。
输入：
9
cap
to
cat
card
two
too
up
boat
boot
输出：
boat
boot
cap
card
cat
to
too
two
up
'''

# while True:
#     try:
#         n = int(input())
#         s = []
#         for i in range(n):
#             s.append(input())
#
#         for j in sorted(s):
#             print(j)
#
#     except Exception:
#         break


'''
描述
输入一个 int 型的正整数，计算出该 int 型数据在内存中存储时 1 的个数。
数据范围：保证在 32 位整型数字范围内
输入描述：
输入一个整数（int类型）
输出描述：
这个数转换成2进制后，输出1的个数
输入：
5
输出：
2

输入：
0
输出：
0
'''

# while True:
#     try:
#         n = int(input())
#         print(bin(n).count('1'))
#
#     except Exception:
#         break


'''
描述
王强决定把年终奖用于购物，他把想买的物品分为两类：主件与附件，附件是从属于某个主件的，下表就是一些主件与附件的例子：
主件	附件
电脑	打印机，扫描仪
书柜	图书
书桌	台灯，文具
工作椅	无
如果要买归类为附件的物品，必须先买该附件所属的主件，且每件物品只能购买一次。
每个主件可以有 0 个、 1 个或 2 个附件。附件不再有从属于自己的附件。
王强查到了每件物品的价格（都是 10 元的整数倍），而他只有 N 元的预算。除此之外，他给每件物品规定了一个重要度，用整数 1 ~ 5 表示。他希望在花费不超过 N 元的前提下，使自己的满意度达到最大。
输入描述：
输入的第 1 行，为两个正整数N，m，用一个空格隔开：
（其中 N （ N<32000 ）表示总钱数， m （m <60 ）为可购买的物品的个数。）
从第 2 行到第 m+1 行，第 j 行给出了编号为 j-1 的物品的基本数据，每行有 3 个非负整数 v p q
（其中 v 表示该物品的价格（ v<10000 ）， p 表示该物品的重要度（ 1 ~ 5 ）， q 表示该物品是主件还是附件。如果 q=0 ，表示该物品为主件，如果 q>0 ，表示该物品为附件， q 是所属主件的编号）
输出描述：
 输出一个正整数，为张强可以获得的最大的满意度。
 
 输入：
1000 5
800 2 0
400 5 1
300 5 1
400 3 0
500 2 0
输出：
2200

输入：
50 5
20 3 5
20 3 5
10 3 0
10 2 0
10 1 0
输出：
130
说明：
由第1行可知总钱数N为50以及希望购买的物品个数m为5；
第2和第3行的q为5，说明它们都是编号为5的物品的附件；
第4~6行的q都为0，说明它们都是主件，它们的编号依次为3~5；
所以物品的价格与重要度乘积的总和的最大值为10*1+20*3+20*3=130  

输入：
1000 5
800 2 0
400 5 1
200 5 1
400 3 0
500 2 0
输出：
2600  

输入：
2000 10
500 1 0    
400 4 0   1600
300 5 1
400 5 1   
200 5 0   1000
500 4 5   2000
400 4 0   1600
320 2 0
410 3 0   1230
400 3 5
输出：
7430
'''

# n, m = map(int, input().split())
# primary, annex = {}, {}
# for i in range(1, m + 1):
#     x, y, z = map(int, input().split())
#     if z == 0:
#         primary[i] = [x, y]
#     else:
#         if z in annex:
#             annex[z].append([x, y])
#         else:
#             annex[z] = [[x, y]]
#
# dp = [0] * (n + 1)
# for key in primary:
#     w, v = [], []
#     w.append(primary[key][0])  # 1、主件
#     v.append(primary[key][0] * primary[key][1])
#     if key in annex:  # 存在附件
#         w.append(w[0] + annex[key][0][0])  # 2、主件+附件1
#         v.append(v[0] + annex[key][0][0] * annex[key][0][1])
#         if len(annex[key]) > 1:  # 附件个数为2
#             w.append(w[0] + annex[key][1][0])  # 3、主件+附件2
#             v.append(v[0] + annex[key][1][0] * annex[key][1][1])
#             w.append(w[0] + annex[key][0][0] + annex[key][1][0])  # 4、主件+附件1+附件2
#             v.append(v[0] + annex[key][0][0] * annex[key][0][1] + annex[key][1][0] * annex[key][1][1])
#     for j in range(n, -1, -10):  # 物品的价格是10的整数倍
#         for k in range(len(w)):
#             if j - w[k] >= 0:
#                 dp[j] = max(dp[j], dp[j - w[k]] + v[k])
# print(dp[n])


'''
描述
开发一个坐标计算工具， A表示向左移动，D表示向右移动，W表示向上移动，S表示向下移动。从（0,0）点开始移动，从输入字符串里面读取一些坐标，并将最终输入结果输出到输出文件里面。
输入：
合法坐标为A(或者D或者W或者S) + 数字（两位以内）
坐标之间以;分隔。
非法坐标点需要进行丢弃。如AA10;  A1A;  $%$;  YAD; 等。
下面是一个简单的例子 如：
A10;S20;W10;D30;X;A1A;B10A11;;A10;
处理过程：
起点（0,0）
+   A10   =  （-10,0）
+   S20   =  (-10,-20)
+   W10  =  (-10,-10)
+   D30  =  (20,-10
+   x    =  无效
+   A1A   =  无效
+   B10A11   =  无效
+  一个空 不影响
+   A10  =  (10,-10)
结果 （10， -10）
数据范围：每组输入的字符串长度满足 
1≤n≤10000
输入描述：
一行字符串
输出描述：
最终坐标，以逗号分隔
输入：
A10;S20;W10;D30;X;A1A;B10A11;;A10;
输出：
10,-10
输入：
ABC;AKL;DA1;
输出：
0,0
'''

# while True:
#     try:
#         s = input().split(';')
#         q = [0, 0]
#         for i in s:
#             if i[1:].isdigit():
#                 match i[0]:
#                     case 'A':
#                         q[0] -= int(i[1:])
#                     case 'D':
#                         q[0] += int(i[1:])
#                     case 'W':
#                         q[1] += int(i[1:])
#                     case 'S':
#                         q[1] -= int(i[1:])
#
#         print(','.join(map(str, q)))
#     except Exception:
#         break


'''
描述
请解析IP地址和对应的掩码，进行分类识别。要求按照A/B/C/D/E类地址归类，不合法的地址和掩码单独归类。
所有的IP地址划分为 A,B,C,D,E五类
A类地址从1.0.0.0到126.255.255.255;
B类地址从128.0.0.0到191.255.255.255;
C类地址从192.0.0.0到223.255.255.255;
D类地址从224.0.0.0到239.255.255.255；
E类地址从240.0.0.0到255.255.255.255
私网IP范围是：
从10.0.0.0到10.255.255.255
从172.16.0.0到172.31.255.255
从192.168.0.0到192.168.255.255
子网掩码为二进制下前面是连续的1，然后全是0。（例如：255.255.255.32就是一个非法的掩码）
（注意二进制下全是1或者全是0均为非法子网掩码）
注意：
1. 类似于【0.*.*.*】和【127.*.*.*】的IP地址不属于上述输入的任意一类，也不属于不合法ip地址，计数时请忽略
2. 私有IP地址和A,B,C,D,E类地址是不冲突的

输入描述：
多行字符串。每行一个IP地址和掩码，用~隔开。
请参考帖子https://www.nowcoder.com/discuss/276处理循环输入的问题。
输出描述：
统计A、B、C、D、E、错误IP地址或错误掩码、私有IP的个数，之间以空格隔开。

输入：
10.70.44.68~255.254.255.0
1.0.0.1~255.0.0.0
192.168.0.2~255.255.255.0
19..0.~255.255.255.0
输出：
1 0 1 0 0 2 1
说明：
10.70.44.68~255.254.255.0的子网掩码非法，19..0.~255.255.255.0的IP地址非法，所以错误IP地址或错误掩码的计数为2；
1.0.0.1~255.0.0.0是无误的A类地址；
192.168.0.2~255.255.255.0是无误的C类地址且是私有IP；
所以最终的结果为1 0 1 0 0 2 1 

输入：
0.201.56.50~255.255.111.255
127.201.56.50~255.255.111.255
输出：
0 0 0 0 0 0 0
说明：
类似于【0.*.*.*】和【127.*.*.*】的IP地址不属于上述输入的任意一类，也不属于不合法ip地址，计数时请忽略    
'''

# ipClass2num = {
#     'A': 0,
#     'B': 0,
#     'C': 0,
#     'D': 0,
#     'E': 0,
#     'ERROR': 0,
#     'PRIVATE': 0,
# }
#
#
# # 私有IP地址和A,B,C,D,E类地址是不冲突的，也就是说需要同时+1
#
#
# def check_ip(ip: str):
#     ip_bit = ip.split('.')
#     if len(ip_bit) != 4 or '' in ip_bit:  # ip 的长度为4 且每一位不为空
#         return False
#     for i in ip_bit:
#         if int(i) < 0 or int(i) > 255:  # 检查Ip每一个10位的值范围为0~255
#             return False
#     return True
#
#
# def check_mask(mask: str):
#     if not check_ip(mask):
#         return False
#     if mask == '255.255.255.255' or mask == '0.0.0.0':
#         return False
#     mask_list = mask.split('.')
#     if len(mask_list) != 4:
#         return False
#     mask_bit = []
#     for i in mask_list:  # 小数点隔开的每一数字段
#         i = bin(int(i))  # 每一数字段转换为每一段的二进制数字段
#         i = i[2:]  # 从每一段的二进制数字段的第三个数开始，因为前面有两个ob
#         mask_bit.append(i.zfill(8))  # .zfill:返回指定长度的字符串，原字符串右对齐，前面填充0
#     whole_mask = ''.join(mask_bit)
#     whole0_find = whole_mask.find('0')  # 查0从哪里开始
#     whole1_rfind = whole_mask.rfind('1')  # 查1在哪里结束
#     if whole1_rfind + 1 == whole0_find:  # 两者位置差1位为正确
#         return True
#     else:
#         return False
#
#
# def check_private_ip(ip: str):
#     # 三类私网
#     ip_list = ip.split('.')
#     if ip_list[0] == '10':
#         return True
#     if ip_list[0] == '172' and 16 <= int(ip_list[1]) <= 31:
#         return True
#     if ip_list[0] == '192' and ip_list[1] == '168':
#         return True
#     return False
#
#
# while True:
#     try:
#         s = input()
#         ip = s.split('~')[0]
#         mask = s.split('~')[1]
#         if check_ip(ip):
#             first = int(ip.split('.')[0])
#             if first == 127 or first == 0:
#                 # 若不这样写，当类似于【0.*.*.*】和【127.*.*.*】的IP地址的子网掩码错误时，会额外计数
#                 continue
#             if check_mask(mask):
#                 if check_private_ip(ip):
#                     ipClass2num['PRIVATE'] += 1
#                 if 0 < first < 127:
#                     ipClass2num['A'] += 1
#                 elif 127 < first <= 191:
#                     ipClass2num['B'] += 1
#                 elif 192 <= first <= 223:
#                     ipClass2num['C'] += 1
#                 elif 224 <= first <= 239:
#                     ipClass2num['D'] += 1
#                 elif 240 <= first <= 255:
#                     ipClass2num['E'] += 1
#             else:
#                 ipClass2num['ERROR'] += 1
#         else:
#             ipClass2num['ERROR'] += 1
#     except Exception:
#         break
#
# for v in ipClass2num.values():
#     print(v, end=' ')


'''
描述
开发一个简单错误记录功能小模块，能够记录出错的代码所在的文件名称和行号。
处理：
1、 记录最多8条错误记录，循环记录，最后只用输出最后出现的八条错误记录。对相同的错误记录只记录一条，但是错误计数增加。最后一个斜杠后面的带后缀名的部分（保留最后16位）和行号完全匹配的记录才做算是“相同”的错误记录。
2、 超过16个字符的文件名称，只记录文件的最后有效16个字符；
3、 输入的文件可能带路径，记录文件名称不能带路径。也就是说，哪怕不同路径下的文件，如果它们的名字的后16个字符相同，也被视为相同的错误记录
4、循环记录时，只以第一次出现的顺序为准，后面重复的不会更新它的出现时间，仍以第一次为准
数据范围：错误记录数量满足 
1≤n≤100  ，每条记录长度满足 
1≤len≤100 
输入描述：
每组只包含一个测试用例。一个测试用例包含一行或多行字符串。每行包括带路径文件名称，行号，以空格隔开。
输出描述：
将所有的记录统计并将结果输出，格式：文件名 代码行数 数目，一个空格隔开，如：

输入：
# r"D:\\zwtymj\\xccb\\ljj\\cqzlyaszjvlsjmkwoqijggmybr 645"
# E:\\je\\rzuwnjvnuz 633
# C:\\km\\tgjwpb\\gy\\atl 637
# F:\\weioj\\hadd\\connsh\\rwyfvzsopsuiqjnr 647
# E:\\ns\\mfwj\\wqkoki\\eez 648
# D:\\cfmwafhhgeyawnool 649
# E:\\czt\\opwip\\osnll\\c 637
# G:\\nt\\f 633
# F:\\fop\\ywzqaop 631
# F:\\yay\\jc\\ywzqaop 631
# D:\\zwtymj\\xccb\\ljj\\cqzlyaszjvlsjmkwoqijggmybr 645

输出：
rzuwnjvnuz 633 1
atl 637 1
rwyfvzsopsuiqjnr 647 1
eez 648 1
fmwafhhgeyawnool 649 1
c 637 1
f 633 1
ywzqaop 631 2

# 说明：
# 由于D:\\cfmwafhhgeyawnool 649的文件名长度超过了16个字符，达到了17，所以第一个字符'c'应该被忽略。
# 记录F:\\fop\\ywzqaop 631和F:\\yay\\jc\\ywzqaop 631由于文件名和行号相同，因此被视为同一个错误记录，哪怕它们的路径是不同的。
# 由于循环记录时，只以第一次出现的顺序为准，后面重复的不会更新它的出现时间，仍以第一次为准，所以D:\\zwtymj\\xccb\\ljj\\cqzlyaszjvlsjmkwoqijggmybr 645不会被记录。  
'''

# error_list = []
# error_num = {}
# while True:
#     try:
#         s = input().split('\\')[-1]
#         s = s.split(' ')[0][-16:] + ' ' + s.split(' ')[1]
#         error_list.append(s)
#
#     except Exception:
#         break
#
# for i in error_list:
#     error_num[i] = error_num.get(i, 0) + 1
# error_num_len = len(error_num)
# for j in error_num:
#     if error_num_len <= 8:
#         print(j, error_num[j])
#     error_num_len -= 1


'''
描述
密码要求:
1.长度超过8位
2.包括大小写字母.数字.其它符号,以上四种至少三种
3.不能有长度大于2的包含公共元素的子串重复 （注：其他符号不含空格或换行）
数据范围：输入的字符串长度满足 
1≤n≤100 
输入描述：
一组字符串。
输出描述：
如果符合要求输出：OK，否则输出NG
输入：
021Abc9000
021Abc9Abc1
021ABC9000
021$bc9000

输出：
OK
NG
NG
OK
'''

# def check_secret(s: str):
#     a, b, c, d = 0, 0, 0, 0
#
#     if len(s) <= 8:
#         return 0
#
#     for i in s:
#         if ord('a') <= ord(i) <= ord('z'):
#             a = 1
#         elif ord('A') <= ord(i) <= ord('Z'):
#             b = 1
#         elif ord('0') <= ord(i) <= ord('9'):
#             c = 1
#         else:
#             d = 1
#
#     if a + b + c + d < 3:
#         return 0
#
#     for j in range(len(s) - 3):
#         if len(s.split(s[j:j + 3])) >= 3:
#             return 0
#
#     return 1
#
# while True:
#     try:
#         s = input()
#         if check_secret(s):
#             print('OK')
#         else:
#             print('NG')
#
#     except Exception:
#         break


'''
描述
现在有一种密码变换算法。
九键手机键盘上的数字与字母的对应： 1--1， abc--2, def--3, ghi--4, jkl--5, mno--6, pqrs--7, tuv--8 wxyz--9, 0--0，把密码中出现的小写字母都变成九键键盘对应的数字，
如：a 变成 2，x 变成 9.
而密码中出现的大写字母则变成小写之后往后移一位，如：X ，先变成小写，再往后移一位，变成了 y ，例外：Z 往后移是 a 。
数字和其它的符号都不做变换。
数据范围： 输入的字符串长度满足 
1≤n≤100 
输入描述：
输入一组密码，长度不超过100个字符。
输出描述：
输出密码变换后的字符串
输入：
YUANzhi1987

输出：
zvbo9441987
'''

# while True:
#     try:
#         s = input()
#
#         sp = ''
#         for i in s:
#             if i == '1':
#                 sp += '1'
#             elif i in 'abc':
#                 sp += '2'
#             elif i in 'def':
#                 sp += '3'
#             elif i in 'ghi':
#                 sp += '4'
#             elif i in 'jkl':
#                 sp += '5'
#             elif i in 'mno':
#                 sp += '6'
#             elif i in 'pqrs':
#                 sp += '7'
#             elif i in 'tuv':
#                 sp += '8'
#             elif i in 'wxyz':
#                 sp += '9'
#             elif i == '0':
#                 sp += '0'
#             elif ord('A') <= ord(i) <= ord('Y'):
#                 sp += chr(ord(i.lower()) + 1)
#             elif i == 'Z':
#                 sp += 'a'
#             else:
#                 sp += i
#
#         print(sp)
#     except Exception:
#         break


'''
描述
某商店规定：三个空汽水瓶可以换一瓶汽水，允许向老板借空汽水瓶（但是必须要归还）。
小张手上有n个空汽水瓶，她想知道自己最多可以喝到多少瓶汽水。
数据范围：输入的正整数满足 
1≤n≤100 
注意：本题存在多组输入。输入的 0 表示输入结束，并不用输出结果。
输入描述：
输入文件最多包含 10 组测试数据，每个数据占一行，仅包含一个正整数 n（ 1<=n<=100 ），表示小张手上的空汽水瓶数。n=0 表示输入结束，你的程序不应当处理这一行。
输出描述：
对于每组测试数据，输出一行，表示最多可以喝的汽水瓶数。如果一瓶也喝不到，输出0。
输入：
3
10
81
0

输出：
1
5
40

说明：
样例 1 解释：用三个空瓶换一瓶汽水，剩一个空瓶无法继续交换
样例 2 解释：用九个空瓶换三瓶汽水，剩四个空瓶再用三个空瓶换一瓶汽水，剩两个空瓶，向老板借一个空瓶再用三个空瓶换一瓶汽水喝完得一个空瓶还给老板
'''

# def get_num(s: int, n=0):
#     if s // 3 != 0:
#         n += s // 3
#         m = s // 3 + s % 3
#         return get_num(m, n)
#     elif s % 3 == 2:
#         return n + 1
#     else:
#         return n
#
#
# s1 = []
# while True:
#     try:
#         s2 = int(input())
#         if s2 != 0:
#             s1.append(get_num(s2))
#         else:
#             for i in s1:
#                 print(i)
#             break
#     except Exception:
#         break


'''
描述
实现删除字符串中出现次数最少的字符，若出现次数最少的字符有多个，则把出现次数最少的字符都删除。输出删除这些单词后的字符串，字符串中其它字符保持原来的顺序。
数据范围：输入的字符串长度满足 
1≤n≤20  ，保证输入的字符串中仅出现小写字母
输入描述：
字符串只包含小写英文字母, 不考虑非法输入，输入的字符串长度小于等于20个字节。

输出描述：
删除字符串中出现次数最少的字符后的字符串。
输入：
aabcddd

输出：
aaddd
'''

# while True:
#     try:
#         s = input()
#         s_d = {}
#
#         for i in set(s):
#             s_d[i] = s.count(i)
#
#         for j in s_d:
#             if s_d[j] == min(s_d.values()):
#                 s = s.replace(j, '')
#
#         print(s)
#     except Exception:
#         break


'''
描述
信息社会，有海量的数据需要分析处理，比如公安局分析身份证号码、 QQ 用户、手机号码、银行帐号等信息及活动记录。
采集输入大数据和分类规则，通过大数据分类处理程序，将大数据分类输出。
数据范围：
1≤I,R≤100  ，输入的整数大小满足 
输入描述：
一组输入整数序列I和一组规则整数序列R，I和R序列的第一个整数为序列的个数（个数不包含第一个整数）；整数范围为0~(2^31)-1，序列个数不限
输出描述：
从R依次中取出R<i>，对I进行处理，找到满足条件的I： 
I整数对应的数字需要连续包含R<i>对应的数字。比如R<i>为23，I为231，那么I包含了R<i>，条件满足 。 
按R<i>从小到大的顺序:
(1)先输出R<i>； 
(2)再输出满足条件的I的个数； 
(3)然后输出满足条件的I在I序列中的位置索引(从0开始)； 
(4)最后再输出I。 
附加条件： 
(1)R<i>需要从小到大排序。相同的R<i>只需要输出索引小的以及满足条件的I，索引大的需要过滤掉 
(2)如果没有满足条件的I，对应的R<i>不用输出 
(3)最后需要在输出序列的第一个整数位置记录后续整数序列的个数(不包含“个数”本身)
序列I：15,123,456,786,453,46,7,5,3,665,453456,745,456,786,453,123（第一个15表明后续有15个整数） 
序列R：5,6,3,6,3,0（第一个5表明后续有5个整数） 
输出：30, 3,6,0,123,3,453,7,3,9,453456,13,453,14,123,6,7,1,456,2,786,4,46,8,665,9,453456,11,456,12,786
说明：
30----后续有30个整数
3----从小到大排序，第一个R<i>为0，但没有满足条件的I，不输出0，而下一个R<i>是3
6--- 存在6个包含3的I 
0--- 123所在的原序号为0 
123--- 123包含3，满足条件 
输入：
15 123 456 786 453 46 7 5 3 665 453456 745 456 786 453 123
5 6 3 6 3 0

输出：
30 3 6 0 123 3 453 7 3 9 453456 13 453 14 123 6 7 1 456 2 786 4 46 8 665 9 453456 11 456 12 786

说明：
将序列R：5,6,3,6,3,0（第一个5表明后续有5个整数）排序去重后，可得0,3,6。
序列I没有包含0的元素。
序列I中包含3的元素有：I[0]的值为123、I[3]的值为453、I[7]的值为3、I[9]的值为453456、I[13]的值为453、I[14]的值为123。
序列I中包含6的元素有：I[1]的值为456、I[2]的值为786、I[4]的值为46、I[8]的值为665、I[9]的值为453456、I[11]的值为456、I[12]的值为786。
最后按题目要求的格式进行输出即可。

输入：
7 6396 4598 8539 6047 2019 11269 7402
3 16 4 26
输出：
12 4 3 1 4598 3 6047 6 7402 26 1 5 11269 
'''

# while True:
#     try:
#         I = input().split(' ')
#         R = input().split(' ')
#         R = sorted(set(map(int, R[1:])))
#         s = []
#
#         for i in R:
#             n = 0
#             s1 = []
#             n1 = 0
#             for j in I[1:]:
#                 if str(i) in j:
#                     n += 1
#                     s1.append(str(n1))
#                     s1.append(j)
#                 n1 += 1
#             if n > 0:
#                 s.append(str(i))
#                 s.append(str(n))
#                 s.extend(s1)
#
#         s.insert(0, str(len(s)))
#         print(' '.join(s))
#     except Exception:
#         break


'''
描述
编写一个程序，将输入字符串中的字符按如下规则排序。
规则 1 ：英文字母从 A 到 Z 排列，不区分大小写。
如，输入： Type 输出： epTy
规则 2 ：同一个英文字母的大小写同时存在时，按照输入顺序排列。
如，输入： BabA 输出： aABb
规则 3 ：非英文字母的其它字符保持原来的位置。
如，输入： By?e 输出： Be?y
数据范围：输入的字符串长度满足 
1≤n≤1000 
输入描述：
输入字符串
输出描述：
输出字符串
输入：
A Famous Saying: Much Ado About Nothing (2012/8).

输出：
A aaAAbc dFgghh: iimM nNn oooos Sttuuuy (2012/8).
'''

# while True:
#     try:
#         s = input()
#
#         a = ''
#         for i in s:
#             if i.isalpha():
#                 a += i
#         a = sorted(a, key=lambda x: x.upper())
#         b = ''
#         index = 0
#         for i in s:
#             if i.isalpha():
#                 b += a[index]
#                 index += 1
#             else:
#                 b += i
#
#         print(b)
#     except Exception:
#         break


'''
描述
定义一个单词的“兄弟单词”为：交换该单词字母顺序（注：可以交换任意次），而不添加、删除、修改原有的字母就能生成的单词。
兄弟单词要求和原来的单词不同。例如： ab 和 ba 是兄弟单词。 ab 和 ab 则不是兄弟单词。
现在给定你 n 个单词，另外再给你一个单词 x ，让你寻找 x 的兄弟单词里，按字典序排列后的第 k 个单词是什么？
注意：字典中可能有重复单词。
数据范围：
1≤n≤1000 ，输入的字符串长度满足 
1≤len(str)≤10  ， 
1≤k<n 
输入描述：
输入只有一行。 先输入字典中单词的个数n，再输入n个单词作为字典单词。 然后输入一个单词x 最后后输入一个整数k
输出描述：
第一行输出查找到x的兄弟单词的个数m 第二行输出查找到的按照字典顺序排序后的第k个兄弟单词，没有符合第k个的话则不用输出。
输入：
3 abc bca cab abc 1
输出：
2
bca

输入：
6 cab ad abcd cba abc bca abc 1
复制
输出：
3
bca
说明：
abc的兄弟单词有cab cba bca，所以输出3
经字典序排列后，变为bca cab cba，所以第1个字典序兄弟单词为bca    
'''

# while True:
#     try:
#         s = input().split(' ')
#
#         s_b = s[-2]
#         s_n = s[-1]
#         ss = []
#
#         for i in range(1, len(s) - 2):
#             if s[i] != s_b and sorted(s[i]) == sorted(s_b):
#                 ss.append(s[i])
#
#         ss.sort()
#         print(len(ss))
#         print(ss[int(s_n) - 1])
#     except Exception:
#         break


'''
描述
题目描述
若两个正整数的和为素数，则这两个正整数称之为“素数伴侣”，如2和5、6和13，它们能应用于通信加密。现在密码学会请你设计一个程序，从已有的 N （ N 为偶数）个正整数中挑选出若干对组成“素数伴侣”，
挑选方案多种多样，例如有4个正整数：2，5，6，13，如果将5和6分为一组中只能得到一组“素数伴侣”，而将2和5、6和13编组将得到两组“素数伴侣”，能组成“素数伴侣”最多的方案称为“最佳方案”，当然密码学会希望你寻找出“最佳方案”。
输入:
有一个正偶数 n ，表示待挑选的自然数的个数。后面给出 n 个具体的数字。
输出:
输出一个整数 K ，表示你求得的“最佳方案”组成“素数伴侣”的对数。
数据范围： 
1≤n≤100  ，输入的数据大小满足 
2≤val≤30000 
输入描述：
输入说明
1 输入一个正偶数 n
2 输入 n 个整数
输出描述：
求得的“最佳方案”组成“素数伴侣”的对数。
输入：
4
2 5 6 13
输出：
2

输入：
2
3 6
输出：
0

输入：
6
2 4 6 11 5 13
输出：
3
'''

# def bool_ss(num: int):
#     for i in range(2, int(num ** 0.5) + 1):
#         if num % i == 0:
#             return False
#     return True
#
#
# def find_cp(even, visited, choose, odds):  # 配对
#     for k, odd in enumerate(odds):
#         if bool_ss(even + odd) and not visited[k]:  # 如果能配对，且两个数之前没有配过对
#             visited[k] = True
#             if choose[k] == 0 or find_cp(choose[k], visited, choose, odds):  # 如果当前奇数没有和任何一个偶数配对，那么认为找到一组可以连接的，如果当前的偶数
#                 # 已经配对，那么就让那个与之配对的偶数断开连接，让他再次寻找能够配对的奇数
#                 choose[k] = even
#                 return True
#     return False  # 如果当前不能配对则返回False
#
#
# while True:
#     try:
#         n = int(input())
#         s = list(map(int, input().split(' ')))
#
#         evens = []  # 存放偶数
#         odds = []  # 存放奇数
#         count = 0
#         for j in s:
#             if j % 2 == 0:
#                 evens.append(j)
#             else:
#                 odds.append(j)
#
#         print(evens)
#         print(odds)
#         choose = [0] * len(odds)  # choose存放当前和这个奇数配对的偶数
#         for even in evens:
#             visited = [False] * len(odds)  # visit用来存放当前奇数是否已经配过对
#             if find_cp(even, visited, choose, odds):
#                 count += 1
#         print(count)
#     except Exception as e:
#         print(e)


'''
描述
对输入的字符串进行加解密，并输出。
加密方法为：
当内容是英文字母时则用该英文字母的后一个字母替换，同时字母变换大小写,如字母a时则替换为B；字母Z时则替换为a；
当内容是数字时则把该数字加1，如0替换1，1替换2，9替换0；
其他字符不做变化。
解密方法为加密的逆过程。
数据范围：输入的两个字符串长度满足 
1≤n≤1000  ，保证输入的字符串都是只由大小写字母或者数字组成
输入描述：
第一行输入一串要加密的密码
第二行输入一串加过密的密码
输出描述：
第一行输出加密后的字符
第二行输出解密后的字符
输入：
abcdefg
BCDEFGH

输出：
BCDEFGH
abcdefg
'''

# def get_encrypt(s: str):
#     ss = ''
#     for i in s:
#         if i.isalpha() and ord(i) != ord('Z') and ord(i) != ord('z'):
#             i = chr(ord(i) + 1)
#             if i.islower():
#                 ss += i.upper()
#             else:
#                 ss += i.lower()
#         elif i.isalpha() and ord(i) == ord('Z'):
#             ss += 'a'
#         elif i.isalpha() and ord(i) == ord('z'):
#             ss += 'A'
#         elif i.isdigit():
#             ss += str((int(i) + 1) % 10)
#         else:
#             ss += i
#     return ss
#
#
# def get_decrypt(c: str):
#     cc = ''
#     for j in c:
#         if j.isalpha() and ord(j) != ord('a') and ord(j) != ord('A'):
#             if j.islower():
#                 j = j.upper()
#             else:
#                 j = j.lower()
#             cc += chr(ord(j) - 1)
#         elif j.isalpha() and ord('a') == ord(j):
#             cc += 'Z'
#         elif j.isalpha() and ord('A') == ord(j):
#             cc += 'z'
#         elif j.isdigit() and j != '0':
#             cc += str(abs(int(j) - 1))
#         elif j.isdigit() and j == '0':
#             cc += '9'
#         else:
#             cc += j
#     return cc
#
#
# while True:
#     try:
#         s1 = input()
#         s2 = input()
#         print(get_encrypt(s1))
#         print(get_decrypt(s2))
#     except Exception:
#         break


'''
描述
按照指定规则对输入的字符串进行处理。
详细描述：
第一步：将输入的两个字符串str1和str2进行前后合并。如给定字符串 "dec" 和字符串 "fab" ， 合并后生成的字符串为 "decfab"
第二步：对合并后的字符串进行排序，要求为：下标为奇数的字符和下标为偶数的字符分别从小到大排序。这里的下标的意思是字符在字符串中的位置。注意排序后在新串中仍需要保持原来的奇偶性。
例如刚刚得到的字符串“decfab”，分别对下标为偶数的字符'd'、'c'、'a'和下标为奇数的字符'e'、'f'、'b'进行排序（生成 'a'、'c'、'd' 和 'b' 、'e' 、'f'），
再依次分别放回原串中的偶数位和奇数位，新字符串变为“abcedf”
第三步：对排序后的字符串中的'0'~'9'、'A'~'F'和'a'~'f'字符，需要进行转换操作。
转换规则如下：
对以上需要进行转换的字符所代表的十六进制用二进制表示并倒序，然后再转换成对应的十六进制大写字符（注：字符 a~f 的十六进制对应十进制的10~15，大写同理）。
如字符 '4'，其二进制为 0100 ，则翻转后为 0010 ，也就是 2 。转换后的字符为 '2'。
如字符 ‘7’，其二进制为 0111 ，则翻转后为 1110 ，对应的十进制是14，转换为十六进制的大写字母为 'E'。
如字符 'C'，代表的十进制是 12 ，其二进制为 1100 ，则翻转后为 0011，也就是3。转换后的字符是 '3'。
根据这个转换规则，由第二步生成的字符串 “abcedf” 转换后会生成字符串 "5D37BF"。
数据范围：输入的字符串长度满足 
1≤n≤100 
输入描述：
样例输入两个字符串，用空格隔开。
输出描述：
输出转化后的结果。

输入：
dec fab
输出：
5D37BF

输入：
ab CD
输出：
3B5D
说明：
合并后为abCD，按奇数位和偶数位排序后是CDab（请注意要按ascii码进行排序，所以C在a前面，D在b前面），转换后为3B5D 

输入：
123 15
输出：
88C4A
'''

# def get_entrypt(x: list):
#     y = []
#     for i in x:
#         if (
#                 ord("0") <= ord(i) <= ord("9")
#                 or ord("a") <= ord(i) <= ord("f")
#                 or ord("A") <= ord(i) <= ord("F")
#         ):
#             y.append(hex(int(bin(int(i, 16))[2:].rjust(4, "0")[::-1], 2))[2:].upper())
#         else:
#             y.append(i)
#     return y
#
#
# while True:
#     try:
#         s = list(input().replace(" ", ""))
#
#         s[::2] = sorted(s[::2])
#         s[1::2] = sorted(s[1::2])
#
#         print(''.join(get_entrypt(s)))
#     except Exception:
#         break


'''
描述
对字符串中的所有单词进行倒排。
说明：
1、构成单词的字符只有26个大写或小写英文字母；
2、非构成单词的字符均视为单词间隔符；
3、要求倒排后的单词间隔符以一个空格表示；如果原字符串中相邻单词间有多个间隔符时，倒排转换后也只允许出现一个空格间隔符；
4、每个单词最长20个字母；
数据范围：字符串长度满足 
1≤n≤10000 
输入描述：
输入一行，表示用来倒排的句子
输出描述：
输出句子的倒排结果
输入：
I am a student
输出：
student a am I
输入：
$bo*y gi!r#l
输出：
l r gi y bo
'''

# while True:
#     try:
#         s = input()
#
#         for i in s:
#             if not (ord('a') <= ord(i) <= ord('z') or ord('A') <= ord(i) <= ord('Z')):
#                 s = s.replace(i, ' ')
#
#         s = s.split()
#         print(*s[::-1])
#     except Exception:
#         break


'''
描述
Catcher是MCA国的情报员，他工作时发现敌国会用一些对称的密码进行通信，比如像这些ABBA，ABA，A，123321，但是他们有时会在开始或结束时加入一些无关的字符以防止别国破解。
比如进行下列变化 ABBA->12ABBA,ABA->ABAKK,123321->51233214　。因为截获的串太长了，而且存在多种可能的情况（abaaab可看作是aba,或baaab的加密形式），
Cathcer的工作量实在是太大了，他只能向电脑高手求助，你能帮Catcher找出最长的有效密码串吗？
数据范围：字符串长度满足 
1≤n≤2500 
输入描述：
输入一个字符串（字符串的长度不超过2500）
输出描述：
返回有效密码串的最大长度
输入：
ABBA
输出：
4

输入：
ABBBA
输出：
5

输入：
12HHHHA
输出：
4
'''

# while True:
#     try:
#         s = input()
#         n = []
#
#         for i in range(len(s)):
#             k = i - 1
#             j = i + 1
#             len_aba = 1
#             while k >= 0 and j < len(s):
#                 if s[k] == s[j]:
#                     len_aba += 2
#                     k -= 1
#                     j += 1
#                 else:
#                     break
#
#             k = i
#             j = i + 1
#             len_abba = 0
#             while k >= 0 and j < len(s):
#                 if s[k] == s[j]:
#                     len_abba += 2
#                     k -= 1
#                     j += 1
#                 else:
#                     break
#
#             n.append(len_aba)
#             n.append(len_abba)
#
#         print(max(n))
#     except Exception:
#         break


'''
描述
原理：ip地址的每段可以看成是一个0-255的整数，把每段拆分成一个二进制形式组合起来，然后把这个二进制数转变成
一个长整数。
举例：一个ip地址为10.0.3.193
每段数字             相对应的二进制数
10                   00001010
0                    00000000
3                    00000011
193                  11000001
组合起来即为：00001010 00000000 00000011 11000001,转换为10进制数就是：167773121，即该IP地址转换后的数字就是它了。
数据范围：保证输入的是合法的 IP 序列
输入描述：
输入 
1 输入IP地址
2 输入10进制型的IP地址
输出描述：
输出
1 输出转换成10进制的IP地址
2 输出转换后的IP地址

输入：
10.0.3.193
167969729
输出：
167773121
10.3.3.193

输入：
66.72.41.66
299867972
输出：
1112025410
17.223.159.68
'''

# while True:
#     try:
#         ip = input().split('.')
#         ip_num = input()
#
#         ip_bin = ''
#         for i in ip:
#             ip_bin += bin(int(i))[2:].rjust(8, '0')
#
#         print(int(ip_bin, 2))
#
#         ip_num_bin = bin(int(ip_num))[2:].rjust(32, '0')
#         ip_num_int = []
#         for j in range(0, 32, 8):
#             ip_num_int.append(str(int(ip_num_bin[j:j + 8], 2)))
#         print('.'.join(ip_num_int))
#     except Exception:
#         break


'''
描述
Lily上课时使用字母数字图片教小朋友们学习英语单词，每次都需要把这些图片按照大小（ASCII码值从小到大）排列收好。请大家给Lily帮忙，通过代码解决。
Lily使用的图片使用字符"A"到"Z"、"a"到"z"、"0"到"9"表示。
数据范围：每组输入的字符串长度满足 
1≤n≤1000 
输入描述：
一行，一个字符串，字符串中的每个字符表示一张Lily使用的图片。
输出描述：
Lily的所有图片按照从小到大的顺序输出

输入：
Ihave1nose2hands10fingers
输出：
0112Iaadeeefghhinnnorsssv
'''

# while True:
#     try:
#         s = input()
#         print(''.join(sorted(s)))
#     except Exception:
#         break


'''
描述
有一种技巧可以对数据进行加密，它使用一个单词作为它的密匙。下面是它的工作原理：首先，选择一个单词作为密匙，如TRAILBLAZERS。如果单词中包含有重复的字母，
只保留第1个，将所得结果作为新字母表开头，并将新建立的字母表中未出现的字母按照正常字母表顺序加入新字母表。如下所示：
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
T R A I L B Z E S C D F G H J K M N O P Q U V W X Y (实际需建立小写字母的字母表，此字母表仅为方便演示）

上面其他用字母表中剩余的字母填充完整。在对信息进行加密时，信息中的每个字母被固定于顶上那行，并用下面那行的对应字母一一取代原文的字母(字母字符的大小写状态应该保留)。
因此，使用这个密匙， Attack AT DAWN (黎明时攻击)就会被加密为Tpptad TP ITVH。
请实现下述接口，通过指定的密匙和明文得到密文。
数据范围：
1≤n≤100  ，保证输入的字符串中仅包含小写字母
输入描述：
先输入key和要加密的字符串
输出描述：
返回加密后的字符串
输入：
nihao
ni
输出：
le
'''

# while True:
#     try:
#         s1 = input()
#         s2 = input()
#         sk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#         sk_s = ""
#         for i in s1:
#             if i not in sk_s:
#                 sk_s += i
#
#         for j in sk:
#             if j not in sk_s:
#                 sk_s += j
#
#         ss = ""
#         for k in s2:
#             ss += sk_s[sk.index(k)]
#         print(ss)
#     except:
#         break


'''
描述
有一种兔子，从出生后第3个月起每个月都生一只兔子，小兔子长到第三个月后每个月又生一只兔子。
例子：假设一只兔子第3个月出生，那么它第5个月开始会每个月生一只兔子。
一月的时候有一只兔子，假如兔子都不死，问第n个月的兔子总数为多少？
数据范围：输入满足 
1≤n≤31 
输入描述：
输入一个int型整数表示第n个月
输出描述：
输出对应的兔子总数

输入：
3
输出：
2
'''

# while True:
#     try:
#         n = int(input())
#
#         a = 1  # 出生不短于两个月的兔子
#         b = 0  # 出生一个月的兔子
#         c = 0  # 刚出生的兔子
#         for i in range(3, n + 1):
#             a += b
#             b = c
#             c = a
#
#         print(a + b + c)
#     except:
#         break


'''
描述
假设一个球从任意高度自由落下，每次落地后反跳回原高度的一半; 再落下, 求它在第5次落地时，共经历多少米?第5次反弹多高？
数据范围：输入的小球初始高度满足 
1≤n≤1000  ，且保证是一个整数
输入描述：
输入起始高度，int型
输出描述：
分别输出第5次落地时，共经过多少米以及第5次反弹多高。
注意：你可以认为你输出保留六位或以上小数的结果可以通过此题。
输入：
1
输出：
2.875
0.03125
'''

# n = int(input())
#
# a = 0
#
#
# for i in range(5):
#     if i == 0:
#         a = n
#     else:
#         a += n*2
#     n = float(n/2)
# print(n)
# print(a)


'''
描述
IP地址是由4个0-255之间的整数构成的，用"."符号相连。
二进制的IP地址格式有32位，例如：10000011，01101011，00000011，00011000;每八位用十进制表示就是131.107.3.24
子网掩码是用来判断任意两台计算机的IP地址是否属于同一子网络的根据。
子网掩码与IP地址结构相同，是32位二进制数，由1和0组成，且1和0分别连续，其中网络号部分全为“1”和主机号部分全为“0”。
你可以简单的认为子网掩码是一串连续的1和一串连续的0拼接而成的32位二进制数，左边部分都是1，右边部分都是0。
利用子网掩码可以判断两台主机是否在同一子网中。
若两台主机的IP地址分别与它们的子网掩码进行逻辑“与”运算（按位与/AND）后的结果相同，则说明这两台主机在同一子网中。
示例：
I P 地址　 192.168.0.1
子网掩码　 255.255.255.0
转化为二进制进行运算：
I P 地址　  11000000.10101000.00000000.00000001
子网掩码　11111111.11111111.11111111.00000000
AND运算   11000000.10101000.00000000.00000000
转化为十进制后为：
192.168.0.0
I P 地址　 192.168.0.254
子网掩码　 255.255.255.0
转化为二进制进行运算：
I P 地址　11000000.10101000.00000000.11111110
子网掩码  11111111.11111111.11111111.00000000
AND运算  11000000.10101000.00000000.00000000
转化为十进制后为：
192.168.0.0
通过以上对两台计算机IP地址与子网掩码的AND运算后，我们可以看到它运算结果是一样的。均为192.168.0.0，所以这二台计算机可视为是同一子网络。
输入一个子网掩码以及两个ip地址，判断这两个ip地址是否是一个子网络。
若IP地址或子网掩码格式非法则输出1，若IP1与IP2属于同一子网络输出0，若IP1与IP2不属于同一子网络输出2。
注:
有效掩码与IP的性质为：
1. 掩码与IP每一段在 0 - 255 之间
2. 掩码的二进制字符串前缀为网络号，都由‘1’组成；后缀为主机号，都由'0'组成
输入描述：
3行输入，第1行是输入子网掩码、第2，3行是输入两个ip地址
题目的示例中给出了三组数据，但是在实际提交时，你的程序可以只处理一组数据（3行）。
输出描述：
若IP地址或子网掩码格式非法则输出1，若IP1与IP2属于同一子网络输出0，若IP1与IP2不属于同一子网络输出2
输入：
255.255.255.0
192.168.224.256
192.168.10.4
255.0.0.0
193.194.202.15
232.43.7.59
255.255.255.0
192.168.0.254
192.168.0.1

输出：
1
2
0

说明：
对于第一个例子:
255.255.255.0
192.168.224.256
192.168.10.4
其中IP:192.168.224.256不合法，输出1

对于第二个例子:
255.0.0.0
193.194.202.15
232.43.7.59
2个与运算之后，不在同一个子网，输出2
对于第三个例子，2个与运算之后，如题目描述所示，在同一个子网，输出0
'''

# def bool_ip_mask(ip: str):
#     ip = ip.split(".")
#     if len(ip) != 4 or "" in ip:
#         return False
#     if ip == "255.255.255.255" or ip == "0.0.0.0":
#         return False
#
#     s = ""
#     for i in ip:
#         if not i.isdigit():
#             return False
#         if int(i) < 0 or int(i) > 255:
#             return False
#         s += bin(int(i))[2:].rjust(8, "0")
#
#     if s.find("0") - s.rfind("1") == 1:
#         return "mask"
#     else:
#         return "ip"
#
#
# def bool_b(m: str, p1: str, p2: str):
#     m = m.split(".")
#     p1 = p1.split(".")
#     p2 = p2.split(".")
#     for j in range(4):
#         if int(m[j]) & int(p1[j]) != int(m[j]) & int(p2[j]):
#             return False
#     return True
#
#
# while True:
#     try:
#         mask = input()
#         ip1 = input()
#         ip2 = input()
#
#         if bool_ip_mask(mask) == "mask" and bool_ip_mask(ip1) and bool_ip_mask(ip2):
#             if bool_b(mask, ip1, ip2):
#                 print(0)
#             else:
#                 print(2)
#         else:
#             print(1)
#     except:
#         break


'''
描述
N 位同学站成一排，音乐老师要请最少的同学出列，使得剩下的 K 位同学排成合唱队形。
设
K位同学从左到右依次编号为 1，2…，K ，他们的身高分别为
K名同学排成了合唱队形。
通俗来说，能找到一个同学，他的两边的同学身高都依次严格降低的队形就是合唱队形。
例子：
123 124 125 123 121 是一个合唱队形
123 123 124 122不是合唱队形，因为前两名同学身高相等，不符合要求
123 122 121 122不是合唱队形，因为找不到一个同学，他的两侧同学身高递减。
你的任务是，已知所有N位同学的身高，计算最少需要几位同学出列，可以使得剩下的同学排成合唱队形。
注意：不允许改变队列元素的先后顺序 且 不要求最高同学左右人数必须相等
数据范围： 
1≤n≤3000 
输入描述：
用例两行数据，第一行是同学的总数 N ，第二行是 N 位同学的身高，以空格隔开
输出描述：
最少需要几位同学出列
输入：
8
186 186 150 200 160 130 197 200

输出：
4
说明：
由于不允许改变队列元素的先后顺序，所以最终剩下的队列应该为186 200 160 130或150 200 160 130 
'''

# def len_o(lst):
#     dp = []
#     for i in range(len(lst)):
#         dp.append(1)
#         for j in range(i):
#             if lst[i] > lst[j]:
#                 dp[i] = max(dp[i], dp[j] + 1)
#     return dp  # 每人左边可以站的人数


# import bisect
#
#
# def len_o(lst):
#     arr = [lst[0]]  # 定义列表，将传入函数的列表第一个元素放入当前元素
#     dp = [1] * len(lst)  # 定义一个列表，默认子序列有当前元素1，长度是传入函数的列表长度
#     for i in range(1, len(lst)):  # 从第二个元素开始查找
#         if lst[i] > arr[-1]:  # 如果元素大于arr列表的最后一个元素，就把它插入列表末尾
#             arr.append(lst[i])
#             dp[i] = len(arr)
#         else:  # 否则，利用二分法找到比元素大的元素的位置，用新的元素替代比它大的那个元素的值，这样就能制造出一个顺序排列的子序列
#             pos = bisect.bisect_left(arr, lst[i])
#             arr[pos] = lst[i]
#             dp[i] = pos + 1  # 获取这个元素子序列的长度
#     return dp


# while True:
#     try:
#         n, n_lst = int(input()), list(map(int, input().split()))
#         # dp1:每人左边可以站的人数，dp2:每人右边可以站的人数
#         dp1, dp2 = len_o(n_lst), len_o(n_lst[::-1])[::-1]
#         res = []
#         for k in range(n):
#             res.append(dp1[k] + dp2[k] - 1)
#         print(n - max(res))
#     except:
#         break

# lst = list(map(int, '186 186 150 180 200 160 130 140 197 200'.split()))
# print(len_o(lst))


'''
描述
输入一行字符，分别统计出包含英文字母、空格、数字和其它字符的个数。
数据范围：输入的字符串长度满足 
1≤n≤1000 
输入描述：
输入一行字符串，可以有空格
输出描述：
统计其中英文字符，空格字符，数字字符，其他字符的个数
输入：
1qazxsw23 edcvfr45tgbn hy67uj m,ki89ol.\\/;p0-=\\][
输出：
26
3
10
12
'''

# while True:
#     try:
#         s = input()
#         num_w, num_sp, num, num_o = 0, 0, 0, 0
#         for i in s:
#             if i.isalpha():
#                 num_w += 1
#             elif i.isspace():
#                 num_sp += 1
#             elif i.isdigit():
#                 num += 1
#             else:
#                 num_o += 1
#         print(num_w)
#         print(num_sp)
#         print(num)
#         print(num_o)
#     except:
#         break


'''
描述
现有n种砝码，重量互不相等，分别为 m1,m2,m3…mn ；
每种砝码对应的数量为 x1,x2,x3...xn 。现在要用这些砝码去称物体的重量(放在同一侧)，问能称出多少种不同的重量。
注：
称重重量包括 0
数据范围：每组输入数据满足 
输入描述：
对于每组测试数据：
第一行：n --- 砝码的种数(范围[1,10])
第二行：m1 m2 m3 ... mn --- 每种砝码的重量(范围[1,2000])
第三行：x1 x2 x3 .... xn --- 每种砝码对应的数量(范围[1,10])
输出描述：
利用给定的砝码可以称出的不同的重量数
输入：
2
1 2
2 1
输出：
5
说明：
可以表示出0，1，2，3，4五种重量。
'''

# while True:
#     try:
#         n = int(input())
#         m = list(map(int, input().split()))
#         x = list(map(int, input().split()))
#
#         h = []
#         w = [0]
#         for i in range(n):
#             for j in range(x[i]):
#                 h.append(m[i])
#         for i in h:
#             for j in list(w):
#                 w.append(i + j)
#         print(len(set(w)))
#     except:
#         break

# a = [1, 2, 3]
# b = list(a)
# d = a.copy()
# a.append(4)
# b.append(5)
# print(a)
# print(b)
# c = {1, 2, 3, 4, 5}
# c.add(5)
# c.add(6)
# print(c)
# print(d)

# import copy
#
# a = [[1, 2], [3, 4]]
# b = a.copy()
# c = a
# d = copy.deepcopy(a)
# e = list(a)
# a[0][0] = 5
# print(a)
# print(b)
# print(c)
# print(d)
# print(e)

# c = {1, 2, 3, 4, 5}
# d = {4,5,6,7,8}
# # c.pop()
# # c.remove(4)
# # c.update({6,7})
# e = c.intersection(d)
# f = c.difference(d)
# g = c.union(d)
# print(e)
# print(f)
# print(g)


'''
描述
Jessi初学英语，为了快速读出一串数字，编写程序将数字转换成英文：
具体规则如下:
1.在英语读法中三位数字看成一整体，后面再加一个计数单位。从最右边往左数，三位一单位，例如12,345 等
2.每三位数后记得带上计数单位 分别是thousand, million, billion.
3.公式：百万以下千以上的数 X thousand X, 10亿以下百万以上的数：X million X thousand X, 10 亿以上的数：X billion X million X thousand X. 
每个X分别代表三位数或两位数或一位数。
4.在英式英语中百位数和十位数之间要加and，美式英语中则会省略，我们这个题目采用加上and，百分位为零的话，这道题目我们省略and
下面再看几个数字例句：
22: twenty two
100:  one hundred
145:  one hundred and forty five
1,234:  one thousand two hundred and thirty four
8,088:  eight thousand (and) eighty eight (注:这个and可加可不加，这个题目我们选择不加)
486,669:  four hundred and eighty six thousand six hundred and sixty nine
1,652,510:  one million six hundred and fifty two thousand five hundred and ten
说明：
数字为正整数，不考虑小数，转化结果为英文小写；
保证输入的数据合法
关键字提示：and，billion，million，thousand，hundred。
数据范围：
1≤n≤2000000 
输入描述：
输入一个long型整数

输出描述：
输出相应的英文写法
'''

# num1 = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
#         'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
# num2 = [0, 0, 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
#
#
# # 100以内转英文
# def n2w(n: int, word: list):
#     if 0 <= n < 20:
#         word.append(num1[n])
#     else:
#         word.append(num2[n // 10])
#         if n % 10 != 0:
#             word.append(num1[n % 10])
#
#     return word
#
#
# # 1000以内转英文
# def n3w(n: int, word: list):
#     if n >= 100:
#         word.append(num1[n // 100])
#         word.append('hundred')
#         if n % 100 != 0:
#             word.append('and')
#     word = n2w(n % 100, word)
#     return word
#
#
# while True:
#     try:
#         n = int(input())
#
#         word = []
#         a = n % 1000  # 个、十、百位
#         b = (n // 1000) % 1000  # 千、万、十万
#         c = (n // 1000000) % 1000  # 百万、千万、亿
#         d = n // 1000000000  # 十亿、百亿、千亿
#
#         if d > 0:
#             word = n3w(d, word)
#             word.append('billion')
#         if c > 0:
#             word = n3w(c, word)
#             word.append('million')
#         if b > 0:
#             word = n3w(b, word)
#             word.append('thousand')
#         if a > 0:
#             word = n3w(a, word)
#
#         print(*word)
#     except:
#         break


'''
描述
定义一个二维数组 N*M ，如 5 × 5 数组下所示：
int maze[5][5] = {
0, 1, 0, 0, 0,
0, 1, 1, 1, 0,
0, 0, 0, 0, 0,
0, 1, 1, 1, 0,
0, 0, 0, 1, 0,
};
它表示一个迷宫，其中的1表示墙壁，0表示可以走的路，只能横着走或竖着走，不能斜着走，要求编程序找出从左上角到右下角的路线。入口点为[0,0],既第一格是可以走的路。
数据范围： 
2≤n,m≤10  ， 输入的内容只包含 
0≤val≤1 
输入描述：
输入两个整数，分别表示二维数组的行数，列数。再输入相应的数组，其中的1表示墙壁，0表示可以走的路。数据保证有唯一解,不考虑有多解的情况，即迷宫只有一条通道。
输出描述：
左上角到右下角的最短路径，格式如样例所示。
输入：
5 5
0 1 0 0 0
0 1 1 1 0
0 0 0 0 0
0 1 1 1 0
0 0 0 1 0
输出：
(0,0)
(1,0)
(2,0)
(2,1)
(2,2)
(2,3)
(2,4)
(3,4)
(4,4)

输入：
5 5
0 1 0 0 0
0 1 0 1 0
0 0 0 0 1
0 1 1 1 0
0 0 0 0 0
输出：
(0,0)
(1,0)
(2,0)
(3,0)
(4,0)
(4,1)
(4,2)
(4,3)
(4,4)
'''

# def get_m(s: list, n: int, m: int, x: int = 0, y: int = 0, ss=None):
#     if ss is None:
#         ss = [(0, 0)]
#     if x + 1 < n and s[x + 1][y] == 0:  # 向下
#         if (x + 1, y) not in ss:
#             get_m(s, n, m, x + 1, y, ss + [(x + 1, y)])
#     if y + 1 < m and s[x][y + 1] == 0:  # 向右
#         if (x, y + 1) not in ss:
#             get_m(s, n, m, x, y + 1, ss + [(x, y + 1)])
#     if x - 1 >= 0 and s[x - 1][y] == 0:  # 向上
#         if (x - 1, y) not in ss:
#             get_m(s, n, m, x - 1, y, ss + [(x - 1, y)])
#     if y - 1 >= 0 and s[x][y - 1] == 0:  # 向左
#         if (x, y - 1) not in ss:
#             get_m(s, n, m, x, y - 1, ss + [(x, y - 1)])
#
#     if x == n - 1 and y == m - 1:
#         for j in ss:
#             print('(' + str(j[0]) + ',' + str(j[1]) + ')')
# while True:
#     try:
#         n, m = list(map(int, input().split()))
#         s = []
#         for i in range(n):
#             s.append(list(map(int,input().split())))
#
#         get_m(s, n, m)
#     except Exception as e:
#         print(e)
#         break


'''
描述
问题描述：数独（Sudoku）是一款大众喜爱的数字逻辑游戏。玩家需要根据9X9盘面上的已知数字，推算出所有剩余空格的数字，并且满足每一行、每一列、每一个3X3粗线宫内的数字均含1-9，并且不重复。
输入描述：
包含已知数字的9X9盘面数组[空缺位以数字0表示]
输出描述：
完整的9X9盘面数组
输入：
0 9 2 4 8 1 7 6 3
4 1 3 7 6 2 9 8 5
8 6 7 3 5 9 4 1 2
6 2 4 1 9 5 3 7 8
7 5 9 8 4 3 1 2 6
1 3 8 6 2 7 5 9 4
2 7 1 5 3 8 6 4 9
3 8 6 9 1 4 2 5 7
0 4 5 2 7 6 8 3 1
输出：
5 9 2 4 8 1 7 6 3
4 1 3 7 6 2 9 8 5
8 6 7 3 5 9 4 1 2
6 2 4 1 9 5 3 7 8
7 5 9 8 4 3 1 2 6
1 3 8 6 2 7 5 9 4
2 7 1 5 3 8 6 4 9
3 8 6 9 1 4 2 5 7
9 4 5 2 7 6 8 3 1

输入
0 9 5 0 2 0 0 6 0
0 0 7 1 0 3 9 0 2
6 0 0 0 0 5 3 0 4
0 4 0 0 1 0 6 0 7
5 0 0 2 0 7 0 0 9
7 0 3 0 9 0 0 2 0
0 0 9 8 0 0 0 0 6
8 0 6 3 0 2 1 0 5
0 5 0 0 7 0 2 8 3
输出
3 9 5 7 2 4 8 6 1
4 8 7 1 6 3 9 5 2
6 2 1 9 8 5 3 7 4
9 4 2 5 1 8 6 3 7
5 6 8 2 3 7 4 1 9
7 1 3 4 9 6 5 2 8
2 3 9 8 5 1 7 4 6
8 7 6 3 4 2 1 9 5
1 5 4 6 7 9 2 8 3
'''

# def bool_value(s_l: list, x, y):
#     for i in range(9):
#         if i != x and s_l[i][y] == s_l[x][y]:
#             return False
#     for j in range(9):
#         if j != y and s_l[x][j] == s_l[x][y]:
#             return False
#     m, n = (x // 3) * 3, (y // 3) * 3
#     for p in range(3):
#         for q in range(3):
#             if (p + m != x or q + n != y) and s_l[p + m][q + n] == s_l[x][y]:
#                 return False
#
#     return True
#
#
# def set_value(s_l: list):
#     for a in range(9):
#         for b in range(9):
#             if s_l[a][b] == 0:
#                 for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
#                     s_l[a][b] = c
#                     if bool_value(s_l, a, b) and set_value(s_l):
#                         return True
#                     s_l[a][b] = 0
#                 return False
#     return True
#
#
# s = [[0, 0, 8, 7, 1, 9, 2, 4, 5],
#      [9, 0, 5, 2, 3, 4, 0, 8, 6],
#      [0, 7, 4, 8, 0, 6, 1, 0, 3],
#      [7, 0, 3, 0, 9, 2, 0, 0, 0],
#      [5, 0, 0, 0, 0, 0, 0, 0, 0],
#      [8, 6, 1, 4, 0, 3, 5, 2, 9],
#      [4, 0, 0, 0, 2, 0, 0, 0, 8],
#      [0, 0, 0, 0, 0, 0, 0, 7, 0],
#      [1, 0, 7, 0, 6, 8, 0, 5, 0]]

# s = []
# for k in range(9):
#     s.append(list(map(int, input().split())))
#     print(s)

# set_value(s)
#
# for z in s:
#     print(*z)


'''
描述
给出一个字符串，该字符串仅由小写字母组成，定义这个字符串的“漂亮度”是其所有字母“漂亮度”的总和。
每个字母都有一个“漂亮度”，范围在1到26之间。没有任何两个不同字母拥有相同的“漂亮度”。字母忽略大小写。
给出多个字符串，计算每个字符串最大可能的“漂亮度”。
本题含有多组数据。
数据范围：输入的名字长度满足 
1≤n≤10000 
输入描述：
第一行一个整数N，接下来N行每行一个字符串
输出描述：
每个字符串可能的最大漂亮程度
输入：
2
zhangsan
lisi
输出：
192
101
说明：
对于样例lisi，让i的漂亮度为26，l的漂亮度为25，s的漂亮度为24，lisi的漂亮度为25+26+24+26=101.
'''

# while True:
#     try:
#         # n = 2
#         # s = ['zhangsan', 'lisi']
#
#         n = int(input())
#         s = []
#         for p in range(n):
#             s.append(input())
#
#         beauty_score = []
#         for i in s:
#             beauty = {}
#             b_s = 0
#             sc = 26
#             for j in i:
#                 beauty[j] = beauty.get(j, 0) + 1
#             beauty = dict(sorted(beauty.items(), key=lambda x: x[1], reverse=True))
#
#             for k in beauty:
#                 b_s += beauty[k] * sc
#                 sc -= 1
#             beauty_score.append(b_s)
#
#         for c in beauty_score:
#             print(c)
#     except:
#         break


'''
描述
输入一个字符串和一个整数 k ，截取字符串的前k个字符并输出
数据范围：字符串长度满足 
1≤n≤1000  ， 
1≤k≤n 
输入描述：
1.输入待截取的字符串
2.输入一个正整数k，代表截取的长度
输出描述：
截取后的字符串
输入：
abABCcDEF
6
输出：
abABCc

输入：
bdxPKBhih
6
输出：
bdxPKB
'''

# while True:
#     try:
#         s = input()
#         n = int(input())
#         print(s[:n])
#     except:
#         break


'''
描述
输入一个单向链表和一个节点的值，从单向链表中删除等于该值的节点，删除后如果链表中无节点则返回空指针。
链表的值不能重复。
构造过程，例如输入一行数据为:
6 2 1 2 3 2 5 1 4 5 7 2 2
则第一个参数6表示输入总共6个节点，第二个参数2表示头节点值为2，剩下的2个一组表示第2个节点值后面插入第1个节点值，为以下表示:
1 2 表示为
2->1
链表为2->1
3 2表示为
2->3
链表为2->3->1
5 1表示为
1->5
链表为2->3->1->5
4 5表示为
5->4
链表为2->3->1->5->4
7 2表示为
2->7
链表为2->7->3->1->5->4
最后的链表的顺序为 2 7 3 1 5 4
最后一个参数为2，表示要删掉节点为2的值
删除 结点 2
则结果为 7 3 1 5 4
数据范围：链表长度满足 
1≤n≤1000  ，节点中的值满足 
0≤val≤10000 
测试用例保证输入合法

输入描述：
输入一行，有以下4个部分：
1 输入链表结点个数
2 输入头结点的值
3 按照格式插入各个结点
4 输入要删除的结点的值

输出描述：
输出一行
输出删除结点后的序列，每个数后都要加空格
输入：
5 2 3 2 4 3 5 2 1 4 3
输出：
2 5 4 1
复制
说明：
形成的链表为2->5->3->4->1
删掉节点3，返回的就是2->5->4->1  

输入：
6 2 1 2 3 2 5 1 4 5 7 2 2
输出：
7 3 1 5 4
说明：
如题 
'''

# s = '6 2 1 2 3 2 5 1 4 5 7 2 2'.split()
# ss = []

# while True:
#     try:
#         s = input().split()
#         ss = []
#         for i in range(len(s)):
#             if i == 0:
#                 n = int(s[i])
#             elif i == 1:
#                 ss.append(s[i])
#             elif i % 2 == 0 and i < n * 2:
#                 ss.insert(ss.index(s[i + 1]) + 1, s[i])
#
#         ss.remove(s[-1])
#         print(*ss)
#     except:
#         break


'''
描述
输入一个表达式（用字符串表示），求这个表达式的值。
保证字符串中的有效字符包括[‘0’-‘9’],‘+’,‘-’, ‘*’,‘/’ ,‘(’， ‘)’,‘[’, ‘]’,‘{’ ,‘}’。且表达式一定合法。
数据范围：表达式计算结果和过程中满足 
∣val∣≤1000  ，字符串长度满足 
1≤n≤1000 
输入描述：
输入一个算术表达式
输出描述：
得到计算结果
输入：
3+2*{1+2*[-4/(8-6)+7]}

输出：
25
'''

# while True:
#     try:
#         s = input()
#         s = s.replace('{', '(')
#         s = s.replace('}', ')')
#         s = s.replace('[', '(')
#         s = s.replace(']', ')')
#         print(int(eval(s)))
#
#
#     except:
#         break


'''
描述
输入一个单向链表，输出该链表中倒数第k个结点，链表的倒数第1个结点为链表的尾指针。
链表结点定义如下：
struct ListNode
{
    int m_nKey;
    ListNode* m_pNext;
};
正常返回倒数第k个结点指针，异常返回空指针.
要求：
(1)正序构建链表;
(2)构建后要忘记链表长度。
数据范围：链表长度满足 
1≤n≤1000  ， 
k≤n  ，链表中数据满足 
0≤val≤10000 
本题有多组样例输入。

输入描述：
输入说明
1 输入链表结点个数
2 输入链表的值
3 输入k的值

输出描述：
输出一个整数

输入：
8
1 2 3 4 5 6 7 8
4

输出：
5
'''

# a = int('8')
# b = '1 2 3 4 5 6 7 8'.split()
# c = int('9')

# while True:
#     try:
#         a = int(input())
#         b = input().split()
#         c = int(input())
#
#         if c <= a:
#             print(b[-c])
#         else:
#             print(None)
#     except:
#         break


'''
以上三角形的数阵，第一行只有一个数1，以下每行的每个数，是恰好是它上面的数、左上角数和右上角的数，3个数之和（如果不存在某个数，认为该数就是0）。
求第n行第一个偶数出现的位置。如果没有偶数，则输出-1。例如输入3,则输出2，输入4则输出3，输入2则输出-1。
数据范围： 
1≤n≤10 
输入描述：
输入一个int整数
输出描述：
输出返回的int值
输入：
4

输出：
3
'''

# while True:
#     try:
#         n = int(input())
#         s = []
#
#         for i in range(n):
#             ss = []
#             for j in range(2 * i + 1):
#                 if j == 0 or j == 2 * i:
#                     ss.append(1)
#                 elif j - 2 < 0 and j < 2 * i - 1:  # 左上角无值
#                     ss.append(s[j - 1] + s[j])
#                 elif j - 2 < 0 and j > 2 * i - 2:  # 左上角右上角无值
#                     ss.append(s[j - 1])
#                 elif j - 2 > 0 and j > 2 * i - 2:  # 右上角无值
#                     ss.append(s[j - 2] + s[j - 1])
#                 else:  # 均有值
#                     ss.append(s[j - 2] + s[j - 1] + s[j])
#             s = list(ss)
#         print(s)
#         for k, v in enumerate(s, 1):
#             if v % 2 == 0:
#                 print(k)
#                 break
#             if k == len(s):
#                 print(-1)
#     except:
#         break

# while True:
#     try:
#         x1 = int(input())
#         if x1 == 1 or x1 == 2:
#             print(-1)
#         elif (x1 + 1) % 2 == 0:
#             print(2)
#         elif x1 % 4 == 0:
#             print(3)
#         elif (x1 - 2) % 4 == 0:
#             print(4)
#     except:
#         break


'''
描述
输出 1到n之间 的与 7 有关数字的个数。
一个数与7有关是指这个数是 7 的倍数，或者是包含 7 的数字（如 17 ，27 ，37 ... 70 ，71 ，72 ，73...）
数据范围： 
1≤n≤30000 
输入描述：
一个正整数 n 。( n 不大于 30000 )
输出描述：
一个整数，表示1到n之间的与7有关的数字个数。
输入：
20
输出：
3
说明：
输入20，1到20之间有关的数字包括7,14,17共3个。 
'''

# while True:
#     try:
#         n = int(input())
#         count = 0
#         for i in range(1, n + 1):
#             if i % 7 == 0:
#                 count += 1
#             elif '7' in str(i):
#                 count += 1
#
#         print(count)
#     except:
#         break


'''
描述
完全数（Perfect number），又称完美数或完备数，是一些特殊的自然数。
它所有的真因子（即除了自身以外的约数）的和（即因子函数），恰好等于它本身。
例如：28，它有约数1、2、4、7、14、28，除去它本身28外，其余5个数相加，1+2+4+7+14=28。
输入n，请输出n以内(含n)完全数的个数。
数据范围： 
1≤n≤5×10**5

输入描述：
输入一个数字n

输出描述：
输出不超过n的完全数的个数

输入：
1000
输出：
3
'''

# while True:
#     try:
#         n = int(input())
#
#         count = 0
#         for i in range(25, n + 1):
#             s = 0
#             for j in range(1, int(i ** 0.5) + 1):
#                 if i % j == 0:
#                     s += j
#                     if j != 1 and j != int(i / j):
#                         s += int(i / j)
#             if s == i:
#                 count += 1
#         print(count)
#     except:
#         break


'''
描述
找出字符串中第一个只出现一次的字符
数据范围：输入的字符串长度满足 
1≤n≤1000 
输入描述：
输入一个非空字符串

输出描述：
输出第一个只出现一次的字符，如果不存在输出-1
输入：
asdfasdfo

输出：
o
'''

# while True:
#     try:
#         s = input()
#         tag = True
#         for i in s:
#             if s.count(i) == 1:
#                 print(i)
#                 tag = False
#                 break
#
#         if tag:
#             print(-1)
#     except:
#         break


'''
描述
任意一个偶数（大于2）都可以由2个素数组成，组成偶数的2个素数有很多种情况，本题目要求输出组成指定偶数的两个素数差值最小的素数对。
数据范围：输入的数据满足 
4≤n≤1000 
输入描述：
输入一个大于2的偶数

输出描述：
从小到大输出两个素数
输入：
20
输出：
7
13

输入：
4
输出：
2
2
'''

# def bool_pn(n: int):
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return False
#     return True
#
#
# while True:
#     try:
#         m = int(input())
#         for j in range(int(m / 2), 1, -1):
#             if bool_pn(j) and bool_pn(m - j):
#                 print(j)
#                 print(m - j)
#                 break
#     except:
#         break


'''
描述
把m个同样的苹果放在n个同样的盘子里，允许有的盘子空着不放，问共有多少种不同的分法？
注意：如果有7个苹果和3个盘子，（5，1，1）和（1，5，1）被视为是同一种分法。
数据范围：
0≤m≤10 ，
1≤n≤10 。

输入描述：
输入两个int整数
输出描述：
输出结果，int型

输入：
7 3
输出：
8
'''

# def solution(m, n):
#     if m == 0 or m == 1 or n == 1:
#         return 1
#     elif n > m:
#         return solution(m, m)
#     else:
#         return solution(m, n - 1) + solution(m - n, n)
#
#
# while True:
#     try:
#         m, n = map(int, input().split())
#         print(solution(m, n))
#     except:
#         break


'''
描述
一个 DNA 序列由 A/C/G/T 四个字母的排列组合组成。 G 和 C 的比例（定义为 GC-Ratio ）是序列中 G 和 C 两个字母的总的出现次数除以总的字母数目（也就是序列长度）。
在基因工程中，这个比例非常重要。因为高的 GC-Ratio 可能是基因的起始点。
给定一个很长的 DNA 序列，以及限定的子串长度 N ，请帮助研究人员在给出的 DNA 序列中从左往右找出 GC-Ratio 最高且长度为 N 的第一个子串。
DNA序列为 ACGT 的子串有: ACG , CG , CGT 等等，但是没有 AGT ， CT 等等
数据范围：字符串长度满足 
1≤n≤1000  ，输入的字符串只包含 A/C/G/T 字母
输入描述：
输入一个string型基因序列，和int型子串的长度
输出描述：
找出GC比例最高的子串,如果有多个则输出第一个的子串
输入：
ACGT
2
输出：
CG
说明：
ACGT长度为2的子串有AC,CG,GT3个，其中AC和GT2个的GC-Ratio都为0.5，CG为1，故输出CG

输入：
AACTGTGCACGACCTGA
5
输出：
GCACG
说明：
虽然CGACC的GC-Ratio也是最高，但它是从左往右找到的GC-Ratio最高的第2个子串，所以只能输出GCACG。
'''

# s = 'AACTGTGCACGACCTGA'
# n = int('5')

# while True:
#     try:
#         s = input()
#         n = int(input())
#         ss = ['', 0]
#         for i in range(0, len(s) - n + 1):
#             sn = (s[i:i + n].count('C') + s[i:i + n].count('G')) / n
#             if sn > ss[1]:
#                 ss[0] = s[i:i + n]
#                 ss[1] = sn
#         print(ss[0])
#     except:
#         break


'''
描述
MP3 Player因为屏幕较小，显示歌曲列表的时候每屏只能显示几首歌曲，用户要通过上下键才能浏览所有的歌曲。为了简化处理，假设每屏只能显示4首歌曲，光标初始的位置为第1首歌。
现在要实现通过上下键控制光标移动来浏览歌曲列表，控制逻辑如下：
歌曲总数<=4的时候，不需要翻页，只是挪动光标位置。
光标在第一首歌曲上时，按Up键光标挪到最后一首歌曲；光标在最后一首歌曲时，按Down键光标挪到第一首歌曲。
其他情况下用户按Up键，光标挪到上一首歌曲；用户按Down键，光标挪到下一首歌曲。
2. 歌曲总数大于4的时候（以一共有10首歌为例）：
特殊翻页：屏幕显示的是第一页（即显示第1 – 4首）时，光标在第一首歌曲上，用户按Up键后，屏幕要显示最后一页（即显示第7-10首歌），同时光标放到最后一首歌上。
同样的，屏幕显示最后一页时，光标在最后一首歌曲上，用户按Down键，屏幕要显示第一页，光标挪到第一首歌上。
一般翻页：屏幕显示的不是第一页时，光标在当前屏幕显示的第一首歌曲时，用户按Up键后，屏幕从当前歌曲的上一首开始显示，光标也挪到上一首歌曲。光标当前屏幕的最后一首歌时的Down键处理也类似。
其他情况，不用翻页，只是挪动光标就行。
数据范围：命令长度
1≤s≤100 ，歌曲数量
1≤n≤150 
进阶：时间复杂度：
O(n) ，空间复杂度：
O(n) 
输入描述：
输入说明：
1 输入歌曲数量
2 输入命令 U或者D

输出描述：
输出说明
1 输出当前列表
2 输出当前选中歌曲

输入：
10
UUUU
输出：
7 8 9 10
7
'''

# n = int('10')
# s = 'UUUUUD'

# while True:
#     try:
#         n = int(input())
#         s = input()
#
#         s_index = 1
#         s_p = 0
#
#         for i in s:
#             if s_index == 1 and i == "U":
#                 s_index = n
#                 s_p = 3
#             elif s_index == n and i == "D":
#                 s_index = 1
#                 s_p = 0
#             elif i == "U":
#                 s_index -= 1
#                 if s_p == 0:
#                     s_p = 0
#                 else:
#                     s_p -= 1
#             else:
#                 s_index += 1
#                 if s_p == 3:
#                     s_p = 3
#                 else:
#                     s_p += 1
#
#         if n > 4:
#             if s_p == 0:
#                 print(s_index, s_index + 1, s_index + 2, s_index + 3)
#                 print(s_index)
#             elif s_p == 1:
#                 print(s_index - 1, s_index, s_index + 1, s_index + 2)
#                 print(s_index)
#             elif s_p == 2:
#                 print(s_index - 2, s_index - 1, s_index, s_index + 1)
#                 print(s_index)
#             else:
#                 print(s_index - 3, s_index - 2, s_index - 1, s_index)
#                 print(s_index)
#         else:
#             print(*[j for j in range(1, n + 1)])
#             print(s_index)
#     except:
#         break


'''
描述
查找两个字符串a,b中的最长公共子串。若有多个，输出在较短串中最先出现的那个。
注：子串的定义：将一个字符串删去前缀和后缀（也可以不删）形成的字符串。请和“子序列”的概念分开！
数据范围：字符串长度
1≤length≤300 
进阶：时间复杂度：
O(n**3) ，空间复杂度：
O(n) 
输入描述：
输入两个字符串
输出描述：
返回重复出现的字符
输入：
abcdefghijklmnop
abcsafjklmnopqrstuvw
输出：
jklmnop
'''

# s1 = 'abcdefghijklmnop'
# s2 = 'abcsafjklmnopqrstuvw'

# while True:
#     try:
#         s1 = input()
#         s2 = input()
#
#         if len(s1) > len(s2):
#             s1, s2 = s2, s1
#
#         s = ""
#
#         for i in range(len(s1)):
#             for j in range(len(s1), i, -1):
#                 if s1[i:j] in s2 and len(s1[i:j]) > len(s):
#                     s = s1[i:j]
#
#         print(s)
#     except:
#         break


'''
有6条配置命令，它们执行的结果分别是：
命   令	            执   行
reset	            reset what
reset board	        board fault
board add	        where to add
board delete	    no board at all
reboot backplane	impossible
backplane abort	    install first
he he	            unknown command
注意：he he不是命令。
为了简化输入，方便用户，以“最短唯一匹配原则”匹配（注：需从首字母开始进行匹配）：
1、若只输入一字串，则只匹配一个关键字的命令行。例如输入：r，根据该规则，匹配命令reset，执行结果为：reset what；输入：res，根据该规则，匹配命令reset，执行结果为：reset what；
2、若只输入一字串，但匹配命令有两个关键字，则匹配失败。例如输入：reb，可以找到命令reboot backpalne，但是该命令有两个关键词，所有匹配失败，执行结果为：unknown command
3、若输入两字串，则先匹配第一关键字，如果有匹配，继续匹配第二关键字，如果仍不唯一，匹配失败。
例如输入：r b，找到匹配命令reset board 和 reboot backplane，执行结果为：unknown command。
例如输入：b a，无法确定是命令board add还是backplane abort，匹配失败。
4、若输入两字串，则先匹配第一关键字，如果有匹配，继续匹配第二关键字，如果唯一，匹配成功。例如输入：bo a，确定是命令board add，匹配成功。
5、若输入两字串，第一关键字匹配成功，则匹配第二关键字，若无匹配，失败。例如输入：b addr，无法匹配到相应的命令，所以执行结果为：unknow command。
6、若匹配失败，打印“unknown command”
注意：有多组输入。
数据范围：数据组数：
1≤t≤800 ，字符串长度
1≤s≤20 
进阶：时间复杂度：
O(n) ，空间复杂度：
O(n) 
输入描述：
多行字符串，每行字符串一条命令
输出描述：
执行结果，每条命令输出一行

输入：
reset
reset board
board add
board delet
reboot backplane
backplane abort

输出：
reset what
board fault
where to add
no board at all
impossible
install first
'''

# while True:
#     try:
#         s = input().split()
#
#         command = [['reset', 'reset what'], ['reset', 'board', 'board fault'], ['board', 'add', 'where to add'],
#                    ['board', 'delete', 'no board at all'],
#                    ['reboot', 'backplane', 'impossible'], ['backplane', 'abort', 'install first']]
#
#         s_command = []
#         if len(s) == 1:
#             if s[0] == command[0][0][:len(s[0])]:
#                 print(command[0][1])
#             else:
#                 print('unknown command')
#         elif len(s) == 2:
#             for i in range(1, 6):
#                 if s[0] == command[i][0][:len(s[0])] and s[1] == command[i][1][:len(s[1])]:
#                     s_command.append(command[i])
#             if len(s_command) == 1:
#                 print(s_command[0][2])
#             else:
#                 print('unknown command')
#         else:
#             print('unknown command')
#     except:
#         break


'''
描述
给定一些同学的信息（名字，成绩）序列，请你将他们的信息按照成绩从高到低或从低到高的排列,相同成绩
都按先录入排列在前的规则处理。
例示：
jack      70
peter     96
Tom       70
smith     67

从高到低  成绩
peter     96
jack      70
Tom       70
smith     67

从低到高
smith     67
jack      70
Tom       70
peter     96
注：0代表从高到低，1代表从低到高

数据范围：人数：

1≤n≤200 
进阶：时间复杂度：
O(nlogn) ，空间复杂度：
O(n) 
输入描述：
第一行输入要排序的人的个数n，第二行输入一个整数表示排序的方式，之后n行分别输入他们的名字和成绩，以一个空格隔开
输出描述：
按照指定方式输出名字和成绩，名字和成绩之间以一个空格隔开
输入：
3
0
fang 90
yang 50
ning 70
输出：
fang 90
ning 70
yang 50

输入：
3
1
fang 90
yang 50
ning 70
输出：
yang 50
ning 70
fang 90
'''

# n = int('3')
# tag = int('1')
# s = [['fang', '90'], ['yang', '50'], ['ning', '70']]

# while True:
#     try:
#         n = int(input())
#         tag = int(input())
#         s = []
#         if tag == 0:
#             tag = True
#         else:
#             tag = False
#         for i in range(n):
#             s1 = input().split()
#             s.append(s1)
#
#         s = sorted(s, key=lambda x: int(x[1]), reverse=tag)
#         for j in s:
#             print(*j)
#     except:
#         break


'''
描述
如果A是个x行y列的矩阵，B是个y行z列的矩阵，把A和B相乘，其结果将是另一个x行z列的矩阵C。这个矩阵的每个元素是由下面的公式决定的
矩阵的大小不超过100*100
输入描述：
第一行包含一个正整数x，代表第一个矩阵的行数
第二行包含一个正整数y，代表第一个矩阵的列数和第二个矩阵的行数
第三行包含一个正整数z，代表第二个矩阵的列数
之后x行，每行y个整数，代表第一个矩阵的值
之后y行，每行z个整数，代表第二个矩阵的值
输出描述：
对于每组输入数据，输出x行，每行z个整数，代表两个矩阵相乘的结果
输入：
2
3
2
1 2 3
3 2 1
1 2
2 1
3 3
输出：
14 13
10 11

说明：
1 2 3
3 2 1 
乘以
1 2
2 1
3 3
等于
14 13
10 11  

输入：
16
8
7
17 19 16 19 14 1 14 9 
7 2 7 9 16 14 16 12 
13 3 3 17 5 9 8 16 
1 14 16 10 13 13 14 1 
13 13 15 4 7 2 6 16 
16 15 5 5 15 13 1 11 
11 5 0 16 14 7 7 15 
0 16 4 7 16 6 0 15 
2 14 11 2 17 17 5 12 
8 13 11 10 1 17 10 8 
15 16 17 15 7 8 13 14 
5 19 11 3 11 14 5 4 
9 16 13 11 15 18 0 3 
15 3 19 9 5 14 12 3 
9 8 7 11 18 19 14 18 
12 19 9 1 0 18 17 10 
5 18 16 19 6 12 5 
1 17 1 5 9 16 3 
14 16 4 0 19 3 6 
11 9 15 18 11 17 13 
5 5 19 3 16 1 12 
12 13 19 1 10 5 18 
19 18 6 18 19 12 3 
15 11 6 5 10 17 19 

输出：
1020 1490 1063 1100 1376 1219 884
966 1035 1015 715 1112 772 920
822 948 888 816 831 920 863
855 1099 828 578 1160 717 724
745 1076 644 595 930 838 688
635 1051 970 600 880 811 846
748 879 952 772 864 872 878
526 722 645 335 763 688 748
764 996 868 362 1026 681 897
836 1125 785 637 940 849 775
1082 1476 996 968 1301 1183 953
609 987 717 401 894 657 662
700 1083 1022 527 1016 746 875
909 1162 905 722 1055 708 720
1126 1296 1240 824 1304 1031 1196
905 1342 766 715 1028 956 749  
'''

# x = int('16')
# y = int('8')
# z = int('7')
# A = [[17, 19, 16, 19, 14, 1, 14, 9], [7, 2, 7, 9, 16, 14, 16, 12], [13, 3, 3, 17, 5, 9, 8, 16],
#      [1, 14, 16, 10, 13, 13, 14, 1],
#      [13, 13, 15, 4, 7, 2, 6, 16], [16, 15, 5, 5, 15, 13, 1, 11], [11, 5, 0, 16, 14, 7, 7, 15],
#      [0, 16, 4, 7, 16, 6, 0, 15],
#      [2, 14, 11, 2, 17, 17, 5, 12], [8, 13, 11, 10, 1, 17, 10, 8], [15, 16, 17, 15, 7, 8, 13, 14],
#      [5, 19, 11, 3, 11, 14, 5, 4],
#      [9, 16, 13, 11, 15, 18, 0, 3], [15, 3, 19, 9, 5, 14, 12, 3], [9, 8, 7, 11, 18, 19, 14, 18],
#      [12, 19, 9, 1, 0, 18, 17, 10]]
# B = [[5, 18, 16, 19, 6, 12, 5], [1, 17, 1, 5, 9, 16, 3], [14, 16, 4, 0, 19, 3, 6], [11, 9, 15, 18, 11, 17, 13],
#      [5, 5, 19, 3, 16, 1, 12], [12, 13, 19, 1, 10, 5, 18],
#      [19, 18, 6, 18, 19, 12, 3], [15, 11, 6, 5, 10, 17, 19]]


# while True:
#     try:
#         x = int(input())
#         y = int(input())
#         z = int(input())
#         A = []
#         B = []
#         for a in range(x):
#             A.append(list(map(int, input().split())))
#
#         for b in range(y):
#             B.append(list(map(int, input().split())))
#
#         C = [[0 for i in range(z)]
#              for j in range(x)]
#
#         for k in range(x):
#             for v in range(z):
#                 for w in range(y):
#                     C[k][v] += A[k][w] * B[w][v]
#
#         for i in range(x):
#             print(*C[i])
#     except:
#         break


'''
描述
问题描述：在计算机中，通配符一种特殊语法，广泛应用于文件搜索、数据库、正则表达式等领域。现要求各位实现字符串通配符的算法。
要求：
实现如下2个通配符：
*：匹配0个或以上的字符（注：能被*和?匹配的字符仅由英文字母和数字0到9组成，下同）
？：匹配1个字符
注意：匹配时不区分大小写。
输入：
通配符表达式；
一组字符串。
输出：
返回不区分大小写的匹配结果，匹配成功输出true，匹配失败输出false
数据范围：字符串长度：
1≤s≤100 
进阶：时间复杂度：
O(n**2) ，空间复杂度：
O(n) 
输入描述：
先输入一个带有通配符的字符串，再输入一个需要匹配的字符串

输出描述：
返回不区分大小写的匹配结果，匹配成功输出true，匹配失败输出false
输入：
te?t*.*
txt12.xls
输出：
false

输入：
z
zz
输出：
false

输入：
pq
pppq
输出：
false

输入：
**Z
0QZz
输出：
true

输入：
?*Bc*?
abcd
输出：
true

输入：
h*?*a
h#a
输出：
false
说明：
根据题目描述可知能被*和?匹配的字符仅由英文字母和数字0到9组成，所以?不能匹配#，故输出false      

输入：
p*p*qp**pq*p**p***ppq
pppppppqppqqppqppppqqqppqppqpqqqppqpqpppqpppqpqqqpqqp
输出：
false
'''

# def match_str(str1: str, str2: str):
#     if str1 == '' and str2 == '':
#         return True
#     elif str1 == '' and str2 != '':
#         return False
#     elif str1 != '' and str2 == '':
#         if str1.replace('*', '') == '':
#             return True
#         else:
#             return False
#     else:
#         m, n = len(str1), len(str2)
#         if (str1[m - 1] == '?' and str2.isalnum()) or str1[m - 1] == str2[n - 1]:
#             return match_str(str1[: m - 1], str2[: n - 1])
#         elif str1[m - 1] == '*':
#             return match_str(str1[: m - 1], str2) or match_str(str1, str2[: n - 1])
#         else:
#             return False
#
#
# while True:
#     try:
#         str1, str2 = input().lower(), input().lower()
#         if match_str(str1, str2):
#             print('true')
#         else:
#             print('false')
#     except:
#         break


'''
描述
公元五世纪，我国古代数学家张丘建在《算经》一书中提出了“百鸡问题”：鸡翁一值钱五，鸡母一值钱三，鸡雏三值钱一。百钱买百鸡，问鸡翁、鸡母、鸡雏各几何？
现要求你打印出所有花一百元买一百只鸡的方式。
输入描述：
输入任何一个整数，即可运行程序。
输出描述：
输出有数行，每行三个整数，分别代表鸡翁，母鸡，鸡雏的数量
输入：
1
输出：
0 25 75
4 18 78
8 11 81
12 4 84
'''

# while True:
#     try:
#         n = input()
#         s = []
#         for i in range(21):
#             for j in range(34):
#                 s1 = []
#                 if i * 5 + j * 3 + (100 - i - j) / 3 == 100:
#                     s1.append(i)
#                     s1.append(j)
#                     s1.append(100 - i - j)
#                     s.append(s1)
#         for k in s:
#             print(*k)
#
#     except:
#         break


'''
描述
根据输入的日期，计算是这一年的第几天。
保证年份为4位数且日期合法。
进阶：时间复杂度：
O(n) ，空间复杂度：
O(1) 
输入描述：
输入一行，每行空格分割，分别是年，月，日
输出描述：
输出是这一年的第几天
输入：
2012 12 31
输出：
366

输入：
1982 3 4
输出：
63
'''

# s = '2012 12 31'.split()
# s = '-'.join(s)

# print(datetime.datetime.strptime(s,'%Y-%m-%d').timetuple().tm_yday)
# print(datetime.datetime.strptime(s,'%Y-%m-%d'))
# print(datetime.datetime.strptime(s,'%Y-%m-%d').timetuple())

# print(datetime.datetime.strptime(s,'%Y-%m-%d').date())
# print(datetime.datetime.strptime(s,'%Y-%m-%d').day)
# print(datetime.datetime.strptime(s,'%Y-%m-%d').weekday())

# while True:
#     try:
#         s = input().split()
#         s = '-'.join(s)
#         print(datetime.datetime.strptime(s, '%Y-%m-%d').timetuple().tm_yday)
#     except:
#         break


'''
描述
在命令行输入如下命令：
xcopy /s c:\\ d:\\e，
各个参数如下：
参数1：命令字xcopy
参数2：字符串/s
参数3：字符串c:\\
参数4: 字符串d:\\e
请编写一个参数解析程序，实现将命令行各个参数解析出来。
解析规则：
1.参数分隔符为空格
2.对于用""包含起来的参数，如果中间有空格，不能解析为多个参数。比如在命令行输入xcopy /s "C:\\program files" "d:\"时，参数仍然是4个，
第3个参数应该是字符串C:\\program files，而不是C:\\program，注意输出参数时，需要将""去掉，引号不存在嵌套情况。
3.参数不定长
4.输入由用例保证，不会出现不符合要求的输入
数据范围：字符串长度：
1≤s≤1000 
进阶：时间复杂度：O(n) ，
空间复杂度：O(n) 
输入描述：
输入一行字符串，可以有空格
输出描述：
输出参数个数，分解后的参数，每个参数都独占一行

输入：
xcopy /s c:\\ d:\\e
输出：
4
xcopy
/s
c:\\
d:\\e

输入：
u "a e i o u" r
输出：
3
u
a e i o u
r
'''

# while True:
#     try:
#         str1 = str(input()).replace(' ', '\n')
#
#         flag = False
#         e = ''
#         for i in str1:
#             if i == '"':
#                 flag = not flag
#             elif flag == True and i == '\n':
#                 e += ' '
#             else:
#                 e += i
#
#         b = e.count('\n') + 1
#         print(b)
#         print(e)
#     except:
#         break


'''
描述
给定两个只包含小写字母的字符串，计算两个字符串的最大公共子串的长度。
注：子串的定义指一个字符串删掉其部分前缀和后缀（也可以不删）后形成的字符串。
数据范围：字符串长度：
1≤s≤150 
进阶：时间复杂度： 
O(n**3) ，空间复杂度：
O(n) 
输入描述：
输入两个只包含小写字母的字符串

输出描述：
输出一个整数，代表最大公共子串的长度

输入：
asdfas
werasdfaswer
输出：
6
'''

# while True:
#     try:
#         s1 = input()
#         s2 = input()
#
#         if len(s1) > len(s2):
#             s1, s2 = s2, s1
#
#         s = ""
#
#         for i in range(len(s1)):
#             for j in range(len(s1), i, -1):
#                 if s1[i:j] in s2 and len(s1[i:j]) > len(s):
#                     s = s1[i:j]
#
#         print(len(s))
#     except:
#         break


'''
描述
验证尼科彻斯定理，即：任何一个整数m的立方都可以写成m个连续奇数之和。
例如：
1^3=1
2^3=3+5
3^3=7+9+11
4^3=13+15+17+19
输入一个正整数m（m≤100），将m的立方写成m个连续奇数之和的形式输出。
数据范围：
1≤m≤100 
进阶：时间复杂度：
O(m) ，空间复杂度： 
O(1) 
输入描述：
输入一个int整数
输出描述：
输出分解后的string

输入：
6
输出：
31+33+35+37+39+41
'''

# while True:
#     try:
#         n = int(input())
#
#         m = n ** 2
#         s = []
#         if m % 2 == 0:
#             for i in range(n // 2):
#                 s.append(m - 2 * i - 1)
#                 s.append(m + 2 * i + 1)
#         else:
#             s.append(m)
#             for i in range(n // 2):
#                 s.append(m - 2 * i - 2)
#                 s.append(m + 2 * i + 2)
#         s = list(map(str, sorted(s)))
#         print('+'.join(s))
#     except:
#         break


'''
描述
给定一个正整数N代表火车数量，0<N<10，接下来输入火车入站的序列，一共N辆火车，每辆火车以数字1-9编号，火车站只有一个方向进出，同时停靠在火车站的列车中，只有后进站的出站了，先进站的才能出站。
要求输出所有火车出站的方案，以字典序排序输出。
数据范围：
1≤n≤10 
进阶：时间复杂度： 
O(n!) ，空间复杂度：
O(n) 
输入描述：
第一行输入一个正整数N（0 < N <= 10），第二行包括N个正整数，范围为1到10。
输出描述：
输出以字典序从小到大排序的火车出站序列号，每个编号以空格隔开，每个输出序列换行，具体见sample。

输入：
3
1 2 3
输出：
1 2 3
1 3 2
2 1 3
2 3 1
3 2 1
说明：
第一种方案：1进、1出、2进、2出、3进、3出
第二种方案：1进、1出、2进、3进、3出、2出
第三种方案：1进、2进、2出、1出、3进、3出
第四种方案：1进、2进、2出、3进、3出、1出
第五种方案：1进、2进、3进、3出、2出、1出
请注意，[3,1,2]这个序列是不可能实现的。   
'''

# def dfs(wait, stack, out):
#     if not wait and not stack:
#         res.append(out)
#     if wait:
#         dfs(wait[1:], stack + [wait[0]], out)
#     if stack:
#         dfs(wait, stack[:-1], out + [stack[-1]])
#
#
# while True:
#     try:
#         n = int(input())
#         s = input().split()
#
#         res = []
#         dfs(s, [], [])
#         for i in sorted(res):
#             print(*i)
#     except:
#         break


'''
描述
题目标题：
将两个整型数组按照升序合并，并且过滤掉重复数组元素。
输出时相邻两数之间没有空格。
输入描述：
输入说明，按下列顺序输入：
1 输入第一个数组的个数
2 输入第一个数组的数值
3 输入第二个数组的个数
4 输入第二个数组的数值
输出描述：
输出合并之后的数组
输入：
3
1 2 5
4
-1 0 3 2
输出：
-101235
'''

# while True:
#     try:
#         n1 = input()
#         s1 = list(map(int, input().split()))
#         n2 = input()
#         s2 = list(map(int, input().split()))
#         s1.extend(s2)
#         s1 = list(map(str, sorted(set(s1))))
#         print(''.join(s1))
#
#     except:
#         break


'''
描述
分子为1的分数称为埃及分数。现输入一个真分数(分子比分母小的分数，叫做真分数)，请将该分数分解为埃及分数。如：8/11 = 1/2+1/5+1/55+1/110。
注：真分数指分子小于分母的分数，分子和分母有可能gcd不为1！
如有多个解，请输出任意一个。
输入描述：
输入一个真分数，String型
输出描述：
输出分解后的string

输入：
8/11
2/4
输出：
1/2+1/5+1/55+1/110
1/3+1/6
说明：
第二个样例直接输出1/2也是可以的 
'''

# while True:
#     try:
#         m, n = map(int, input().split('/'))
#         m = m * 10
#         n = n * 10
#         res = []
#         while m:
#             for i in range(m, 0, -1):
#                 if n % i == 0:
#                     res.append('1' + '/' + str(int(n / i)))
#                     m -= i
#                     break
#         print('+'.join(res))
#     except:
#         break


'''
描述
给定一个仅包含小写字母的字符串，求它的最长回文子串的长度。
所谓回文串，指左右对称的字符串。
所谓子串，指一个字符串删掉其部分前缀和后缀（也可以不删）的字符串
数据范围：字符串长度
1≤s≤350 
进阶：时间复杂度：
O(n) ，空间复杂度：
O(n) 
输入描述：
输入一个仅包含小写字母的字符串
输出描述：
返回最长回文子串的长度
输入：
cdabbacc
输出：
4
说明：
abba为最长的回文子串 
'''

# while True:
#     try:
#         s = input()
#         n = 0
#         n_l = len(s)
#         for i in range(n_l):
#             for j in range(n_l, 0, -1):
#                 if len(s[i:j]) <= n:
#                     break
#                 if s[i:j] == s[i:j][::-1]:
#                     n = len(s[i:j])
#                     break
#         print(n)
#     except:
#         break


'''
描述
求一个int类型数字对应的二进制数字中1的最大连续数，例如3的二进制为00000011，最大连续2个1
数据范围：数据组数：
1≤t≤5 ，
1≤n≤500000 
进阶：时间复杂度：
O(logn) ，空间复杂度：
O(1) 
输入描述：
输入一个int类型数字
输出描述：
输出转成二进制之后连续1的个数

输入：
200
输出：
2
说明：
200的二进制表示是11001000，最多有2个连续的1。
'''

# while True:
#     try:
#         s = int(input())
#         s = bin(s)[2:].split('0')
#         count = 0
#         for i in s:
#             if len(i)>count:
#                 count = len(i)
#         print(count)
#     except:
#         break


'''
描述
密码按如下规则进行计分，并根据不同的得分为密码进行安全等级划分。
一、密码长度:
5 分: 小于等于4 个字符
10 分: 5 到7 字符
25 分: 大于等于8 个字符
二、字母:
0 分: 没有字母
10 分: 密码里的字母全都是小（大）写字母
20 分: 密码里的字母符合”大小写混合“
三、数字:
0 分: 没有数字
10 分: 1 个数字
20 分: 大于1 个数字
四、符号:
0 分: 没有符号
10 分: 1 个符号
25 分: 大于1 个符号
五、奖励（只能选符合最多的那一种奖励）:
2 分: 字母和数字
3 分: 字母、数字和符号
5 分: 大小写字母、数字和符号
最后的评分标准:
>= 90: 非常安全
>= 80: 安全（Secure）
>= 70: 非常强
>= 60: 强（Strong）
>= 50: 一般（Average）
>= 25: 弱（Weak）
>= 0:  非常弱（Very_Weak）
对应输出为：
VERY_SECURE
SECURE
VERY_STRONG
STRONG
AVERAGE
WEAK
VERY_WEAK
请根据输入的密码字符串，进行安全评定。
注：
字母：a-z, A-Z
数字：0-9
符号包含如下： (ASCII码表可以在UltraEdit的菜单view->ASCII Table查看)
!"#$%&'()*+,-.\/     (ASCII码：0x21~0x2F)
:;<=>?@             (ASCII码：0x3A~0x40)
[\]^_`              (ASCII码：0x5B~0x60)
{|}~                (ASCII码：0x7B~0x7E)
提示:
1 <= 字符串的长度<= 300
输入描述：
输入一个string的密码
输出描述：
输出密码等级

输入：
38$@NoNoN
输出：
VERY_SECURE
说明：
样例的密码长度大于等于8个字符，得25分；大小写字母都有所以得20分；有两个数字，所以得20分；包含大于1符号，所以得25分；
由于该密码包含大小写字母、数字和符号，所以奖励部分得5分，经统计得该密码的密码强度为25+20+20+25+5=95分。

输入：
Jl)M:+
输出：
AVERAGE
说明：
示例2的密码强度为10+20+0+25+0=55分。
'''

# while True:
#     try:
#         s = input()
#         score = 0
#         if len(s) >= 8:
#             score += 25
#         elif len(s) > 4:
#             score += 10
#         else:
#             score += 5
#
#         upper = 0
#         lower = 0
#         n = 0
#         other = 0
#
#         for i in s:
#             if i.islower():
#                 lower += 1
#             elif i.isupper():
#                 upper += 1
#             elif i.isdigit():
#                 n += 1
#             else:
#                 other += 1
#
#         if lower and upper:
#             score += 20
#         elif lower or upper:
#             score += 10
#
#         if n > 1:
#             score += 20
#         elif n == 1:
#             score += 10
#
#         if other > 1:
#             score += 25
#         elif other == 1:
#             score += 10
#
#         if lower and upper and n and other:
#             score += 5
#         elif (lower or upper) and n and other:
#             score += 3
#         elif (lower or upper) and n:
#             score += 2
#
#         if score >= 90:
#             print('VERY_SECURE')
#         elif score >= 80:
#             print('SECURE')
#         elif score >= 70:
#             print('VERY_STRONG')
#         elif score >= 60:
#             print('STRONG')
#         elif score >= 50:
#             print('AVERAGE')
#         elif score > 25:
#             print('WEAK')
#         else:
#             print('VERY_WEAK')
#
#     except:
#         break


