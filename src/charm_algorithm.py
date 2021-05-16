from sys import setprofile

class Charm():

    def __init__(self):
        self.skip_set = set()
        print('smth')

    def populate_from_file(self, filename='test.txt'):
        f = open(filename, "r")
        map = dict()
        for line in f.readlines():
            key = line.split('\t')[0]
            values = set()
            for value in line.split('\t')[1].split(','):
                values.add(int(value))
            map[key] = values
        return map    

    def get_string_union(self, str1, str2):
        """
        Function to compute the union of two item sets - (Xi U Xj). Items are ordered lexicographically
        """
        str = str1+str2
        char_array = list(set(str))
        char_array.sort()  
        string_value = "" 
    
        # traverse in the string  
        for ele in char_array: 
            string_value += ele
        return string_value
    
    def replace_in_items(self, current, target, map):
        temp = []

        for key in map.keys():
           if(key in current):
               temp.append(key)

        for key in temp:
            values = map[key]
            map.pop(key, None)
            key = key.replace(current, target)
            key = self.get_string_union(key, "")
            map[key] = values

        return map

    def charmProp(self, x1, x2, y:set, minSup:int, map:dict, newN:dict):
        if len(y) >= minSup:
            if map[x1] == map[x2]:
                self.skip_set.add(map[x1])
                temp = self.get_string_union(x1,x2)
                newN = self.replace_in_items(x1, temp, newN)
                map = self.replace_in_items(x1, temp, map)
                return temp, map, newN
            elif map[x2] in map[x1]:
                temp = self.get_string_union(x1,x2)
                newN = self.replace_in_items(x1, temp, newN)
                map = self.replace_in_items(x1, temp, map)
                return temp, map, newN
            elif map[x1] in map[x2]:
                self.skip_set.add(map[x2])
                newN[self.get_string_union(x1,x2)] = y
                return x1, map, newN
            else:
                if map[x1] == map[x2]:
                    newN[self.get_string_union(x1,x2)] = y
                    return x1, map, newN
        return x1, map, newN

    def is_subsmed(self, map:dict, y:set):
        for s in map.values():
            if set(s) == set(y):
                return True
        return False

    def charm_extended(self, nodes:dict, c:dict, minSup:int):
        i = 0
        items = list(nodes.keys())
        for i in range(len(items)):
            xi = items[i]
            if items[i] in self.skip_set:
                continue
            x_prev = items[i]
            y = set()
            x = None
            newN = dict()
            for j in range(i+1, len(items)):
                xj = items[j]
                if items[j] in self.skip_set:
                    continue
                x = self.get_string_union(xi, xj)
                y = nodes[xi]
                temp = y
                temp = [value for value in temp if value not in nodes[xj]]
                xi, nodes, newN = self.charmProp(xi, xj, temp, minSup, nodes, newN)
            if len(newN) != 0:
                self.charm_extended(newN, c, minSup)
            if x_prev != None and nodes.get(x_prev, None) != None and not self.is_subsmed(c, nodes.get(x_prev, None)):  
                c[x_prev] = nodes[x_prev]
            if x != None and nodes.get(x, None) != None and not self.is_subsmed(x, nodes.get(x, None)):
                c[x] = nodes[x]
        return c

    def charm(self, nodes:dict, minSup:int):
        for key in nodes.keys():
            if len(nodes[key]) < minSup:
                nodes.pop(key, None)
        
        c = dict()
        c = self.charm_extended(nodes, c, minSup)
        return c
