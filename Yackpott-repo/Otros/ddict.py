from collections import defaultdict

d = defaultdict(int)
e = defaultdict(int)

lista = [1,1,1,2,3,4,5,6,7,7,4,3,2,1]
for i in lista:
	d.update({i:d[i]+1})
	print(d[i])
print(len(d))
print(d)

for j in lista:
	e[j] += 1
	print(e[j])
print(len(e))
print(e)