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



plus = lambda x,y : (x or 0) + (y or 0)
print(list(map(plus,[1,2,3,4,5],[4,5,6,7])))
from functools import reduce
print(reduce(plus,[1,2,3,4,5],10))

mode = lambda x : x % 2
print(list(filter(mode,[3,4,5,6,8,7])))

print_num = lambda x : (x==1 and print('one')) or (x==2 and print('two')) or (print('other'))
print_num(2)
