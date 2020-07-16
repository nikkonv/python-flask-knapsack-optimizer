import numpy as np
from operator import itemgetter

"""
# Nicolas Navarrete - 19697438
# Diseno y analisis de algoritmos
"""

try:
    from functools import lru_cache
except ImportError:
    # For Python2
    # pip install backports.functools_lru_cache
    from backports.functools_lru_cache import lru_cache
# Top-down Dynamic programming knapsack 
class knapsack:
	def __init__(self, size, weight):
		self.size = size
		self.weight = weight
	@lru_cache()
	def solve(self, cap, i=0):
		if cap < 0: return -sum(self.weight), []
		if i == len(self.size): return 0, []
		res1 = self.solve(cap,  i + 1)
		res2 = self.solve(cap - self.size[i], i + 1)
		res2 = (res2[0] + self.weight[i], [i] + res2[1])
		return res1 if res1[0] >= res2[0] else res2

def dp_knapsack_int(weights, values, W):
	for i,x in enumerate(values):
		if x <= 0:
			del values[i]
			del weights[i]
	knapsack_value, ids = knapsack(weights, values).solve(W)
	knapsack_weight = 0
	for i in ids:
		knapsack_weight += weights[i]
	return ids, knapsack_weight, knapsack_value

# For greedy
def weight(item):
	return item[1]
def value(item):
	return item[2]
def ratio(item):
	try:
		return item[3]
	except:
		return 'no_ratio'

# Greedy knapsack implementation 
def greedy_knapsack_int(weights, values, max_weight):
	items = []
	for i in range(len(values)):
		tmp = [i,weights[i],values[i]]
		items.append(tmp)

	# item = [[id,weight,value]]
	knapsack, ids, knapsack_weight, knapsack_value = [], [], 0, 0

	# sort items
	for i in items:
		try:
			ratio = float(value(i)/weight(i))
		except:
			ratio = value(i)
		i.append(ratio)
	# now item = [[id,weight,value,ratio]]
	
	# order by 1:value, 2:weight, 3:ratio
	items_sorted = sorted(items, key=itemgetter(3))

	while len(items_sorted) > 0:
		item = items_sorted.pop()
		if weight(item) + knapsack_weight <= max_weight:
			if value(item) >= 0:
				knapsack.append(item) 
				ids.append(item[0]) # id of the each item in the sack
				knapsack_weight += weight(knapsack[-1])
				knapsack_value += value(knapsack[-1])

	return sorted(ids), knapsack_weight, knapsack_value




items = [[1,1.5,60],[2,2,100],[3,3,120]]
W = 4

w = [1.5,2,3,0,0,0,0,0]
v = [60,100,120,10,20,0,1,5]


"""
w = [80,82,85,70,72,70,66,50,55,25,50,55,40,48,50,32,22,60,30,32,40,38,35,32,
25,28,30,22,50,30,45,30,60,50,20,65,20,25,30,10,20,25,15,10,10,10,4,4,2,1]
v = [220,208,198,192,180,180,165,162,160,158,155,130,125,122,120,118,115,110,105,101,100,100,98,96,95,90,88,82,80,77,75,73,72,70,69,66,65,63,60,58,56,50,30,20,15,10,8,5,3,1]
W = 1000
"""


#print('greedy: ', greedy_knapsack_int(w,v,W))
#print('dp: ', dp_knapsack_int(w, v, W))
#print('dp2: ',knapsack_dp(w,v,W))

# to use library knapsack

# -> knapsack.knapsack(size, weight).solve(capacity)