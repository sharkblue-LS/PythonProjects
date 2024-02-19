# import requests
# import unittest
#
# class GetEventListTest(unittest.TestCase):
# 	'''查询发布会接口测试'''
#
# 	def setUp(self):
# 		self.url = 'http://127.0.0.1:8000/api/get_event_list/'
#
# 	def test_get_event_null(self):
# 		'''发布会id为空'''
# 		r = requests.get(self.url,params={'eid':''})
# 		result = r.json()
# 		self.assertEqual(result['status'],10021)
# 		self.assertEqual(result['message'],'parameter error')
#
# 	def test_get_event_error(self):
# 		'''发布会id不存在'''
# 		r = requests.get(self.url,params={'eid':'901'})
# 		result = r.json()
# 		self.assertEqual(result['status'],10022)
# 		self.assertEqual(result['message'],'query result is empty')
#
# 	def test_get_event_success(self):
# 		'''发布会id为1，查询成功'''
# 		r = requests.get(self.url,params={'eid':'1'})
# 		result = r.json()
# 		self.assertEqual(result['status'],200)
# 		self.assertEqual(result['message'],'success')
# 		self.assertEqual(result['data']['name'],'小米11发布会')
# 		self.assertEqual(result['data']['address'],'深圳体育中心')
#
# if __name__ == '__main__':
#     unittest.main()
import random

# plus = lambda x,y : (x or 0) + (y or 0)
# print(list(map(plus,[1,2,3,4,5],[4,5,6,7])))
# from functools import reduce
# print(reduce(plus,[1,2,3,4,5],10))
#
# mode = lambda x : x % 2
# print(list(filter(mode,[3,4,5,6,8,7])))
#
# print_num = lambda x : (x==1 and print('one')) or (x==2 and print('two')) or (print('other'))
# print_num(2)

# while True:
#
# 	try:
# 		s = int(input())
# 		if 1 <= int(s) <= 500:
# 			print('111')
# 		else:
# 			print('请输入1至500的整数')
#
# 	except Exception as e:
# 		print('请输入1至500的整数', e)
# 		continue


# random.seed(1)
# print(random.random())
# print(random.getrandbits(4))
# print(random.uniform(2, 10))
# print(random.choice([1, 5, 10, 7, 6]))
# a = [1, 5, 10, 7, 6]
# random.shuffle(a)
# print(a)
# print(' '.join(map(str, random.sample([i for i in range(1, 101)], 3))))

# while True:
#     try:
#         a = input()
#         b = input()
#
#         la = len(a)
#         lb = len(b)
#
#         if la > lb:
#             a, b = b, a
#
#         for i in range(1, la):
#             if i == 0 and a in b:
#                 print(a)
#                 break
#             elif a[i:] in b:
#                 print(a[i:])
#                 break
#             elif a[:-i] in b:
#                 print(a[:-i])
#                 break
#
#     except:
#         break

# while True:
#     try:
#         a, b = input(), input() # a保存短，b保存长
#         if len(a) > len(b):
#             a, b = b, a
#         res = ''
#         for i in range(0, len(a)):
#             for j in range(len(a), i, -1):
#                 if a[i:j] in b and j-i > len(res):
#                     res = a[i:j]
#         print(res)
#     except:
#         break


# while True:
#     try:
#         m = input().strip().split()
#         key = ["reset", "reset board", "board add", "board delete", "reboot backplane", "backplane abort"]
#         value=["reset what", "board fault", "where to add", "no board at all", "impossible", "install first"]
#         # 不建字典，用列表的方式避免了双层循环，如果实在要用列表，直接用dict(zip（list1,list2）)合成字典都行.
#         if len(m) < 1 or len(m) > 2:   # 判断当输入为小于1个或者输入大于2个字符串时，不符合命令，就报未知命令
#             print("unknown command")
#         elif len(m) == 1:   # 当输入一个字符串
#             if m[0] == key[0][:len(m[0])]:  # 这里才是解决这个题的最佳思想，利用切片的思想来匹配
#                 print(value[0])
#             else:
#                 print("unknown command")
#         else:
#             index = []
#             for i in range(1, len(key)):   # 这里把所有原始命令遍历，如果这里写成(len(key)+1),也就是1..6，那么下面的key[i]要改成k[i-1]才符合逻辑
#                 a = key[i].split()   # 将具体的一个KEY分割成两部分
#                 if m[0] == a[0][:len(m[0])] and m[1] == a[1][:len(m[1])]:  # 然后去匹配被分割的key,这里不可能有reset这种单独的，因为上面条件已经限制了。
#                     index.append(i)  # 符合条件就把这个位置入列表
#             if len(index) != 1:
#                 print("unknown command")
#             else:
#                 print(value[index[0]])   # 输出对应的value值
#     except:
#         break


a = 2
match a:
    case 1:
        print('aaaa')
    case 2:
        print('bbb')


