print('aaa'[:])

def maxFromMap(map):
    list = []
    for key in map:
        list.append(map[key])
    max1 = max(list)
    rez = {}
    for key in map:
        if map[key] == max1:
            rez[key] = max1
            return rez


map = {'aaa': '1', 'bbb': '3', 'ccc': '2'}
# map = {'aaa': 1}
v = maxFromMap(map)
print(v)


list = 'abcde'
print(list[:5-2])