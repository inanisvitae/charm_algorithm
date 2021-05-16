from src.charm_algorithm import Charm

c = Charm()
map = c.populate_from_file()
test = c.charm(map, 3)
print(test)
