from src.charm_algorithm import Charm

c = Charm()
map = c.populate_from_file(filename='test.txt')
test = c.charm(map, 3)
<<<<<<< Updated upstream
=======
print(test)
>>>>>>> Stashed changes

f = open("result.txt", "a")
for key in test.keys():
    f.write(key + '\t' + ' '.join([str(elem) for elem in test[key]]) + '\n')
<<<<<<< Updated upstream
f.close()
=======
f.close()
>>>>>>> Stashed changes
