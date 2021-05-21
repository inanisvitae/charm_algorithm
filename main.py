from src.charm_algorithm import Charm

c = Charm()
map = c.populate_from_file(filename='test.txt')
test = c.charm(map, 5)
print(test)

f = open("result.txt", "a")
for key in test.keys():
    f.write(key + '\t' + ' '.join([str(elem) for elem in test[key]]) + '\n')
f.close()
