# Hashmap with separate chaining

# Description: The hashmap class represents a hashmap with an underlying dynamic array. Collisions
# are resolved with chaining via a singly linked list. Class contains methods to put a key/value
# pair in the hashmap, get the value of a key, remove a key, determine if a key is present within
# the hashmap, clear the hashmap, return the empty bucket count, resize the capacity, return the load
# factor, and get a dynamic array of key/value pairs. A function is available to find the mode of
# a given dynamic array.


from data_structures import (DynamicArray, LinkedList,
                             hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and value pair as parameters. Places the key/value pair in
        the hash map. Returns nothing.
        """
        if self.table_load() >= 1:    # double the capacity based on the load factor
            self.resize_table(self._capacity*2)

        hash = self._hash_function(key)  # gives the bucket index
        index = hash % self._buckets.length()
        linked_list = self._buckets.get_at_index(index)

        if linked_list.contains(key) is not None:
            self._size -= 1
            linked_list.remove(key)     # remove the node to update the value

        self._size += 1
        linked_list.insert(key, value)

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Returns the amount of empty buckets in the hash map as
        an integer.
        """
        count = 0

        for index in range(self._buckets.length()):
            linked_list = self._buckets.get_at_index(index)
            if linked_list.length() == 0:  # an empty bucket has an empty linked list
                count += 1

        return count

    def table_load(self) -> float:
        """
        Takes no parameters. Returns the table load factor as a float.
        """
        load_factor = self._size / self._buckets.length()
        return load_factor

    def clear(self) -> None:
        """
        Takes no parameters. Clears all element from the hash map. Returns nothing.
        """
        self._buckets = DynamicArray() # reset DA and size
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity integer as a parameter. Returns nothing.
        Resizes the table based on the new capacity and rehashes all key/value pairs
        within the table.
        """
        if new_capacity < 1:
            return
        DA = self.get_keys_and_values()     # get a DA of all key/value pairs

        if self._is_prime(new_capacity) is False:  # capacity must be prime
            new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        self.clear()        # updates the table with the new capacity

        for index in range(DA.length()):    # rehash all key/value pairs
            key = DA.get_at_index(index)[0]
            value = DA.get_at_index(index)[1]
            self.put(key, value)

    def get(self, key: str):
        """
        Takes a key as a parameter. Returns the value of the key if the key exists in
        the table. Returns None if the key is not in the table.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        linked_list = self._buckets.get_at_index(index)

        if linked_list.contains(key):
            node = linked_list.contains(key)    # gives the node within the linked list
            return node.value

        else:
            return None     # no matching key was found

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter.
        Returns true if the given key is in the hash map or false if not.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        linked_list = self._buckets.get_at_index(index)

        if linked_list.contains(key):   # true if the linked list contains the key
            return True

        else:
            return False

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter. Removes the given key/value pair from the hash map.
        Returns nothing.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        linked_list = self._buckets.get_at_index(index)

        if linked_list.contains(key):
            linked_list.remove(key)     # removes the node
            self._size -= 1     # update the size

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters. Creates a dynamic array with tuples of the key/value pairs
        from the hash map. Returns the dynamic array.
        """
        DA = DynamicArray()
        for index in range(self._buckets.length()):
            linked_list = self._buckets.get_at_index(index)
            if linked_list.length() != 0:   # iterates through the linked list
                iterator = linked_list.__iter__()
                for nodes in range(linked_list.length()):
                    next_node = iterator.__next__()
                    DA.append((next_node.key, next_node.value))     # appends each key/value pair

        return DA


def hash_function(key: str):
    """
    Takes a key as a parameter. Hashes the key based on its value for placement within a
    hash map. Returns the hash.
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a dynamic array as a parameter. Find the mode(s) and frequency of the given
    dynamic array. Returns a new dynamic array with the mode(s) and returns the frequency.
    """
    mode = DynamicArray()   # a new DA holds the mode(s)
    count = 0   # counts the frequency
    map = HashMap(11, hash_function)
    for index in range(da.length()):
        key = da.get_at_index(index)
        if map.contains_key(key):   # if the key is in the hash map, it increases the value
            value = map.get(key)
            value += 1
            map.put(key, value)     # the value represents the count
            if value > count:   # the key has beat the previous mode
                mode = DynamicArray()
                mode.append(key)
                count = value
            elif value == count:    # the key is equal in count to the mode
                mode.append(key)
        else:                       # if the key is not in the hash map, it is hashed with the put method
            value = 1
            map.put(key, value)
            if value > count:       # places the first key in the DA as the mode
                mode = DynamicArray()
                mode.append(key)
                count = value
            elif value == count:
                mode.append(key)

    return mode, count


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    m = HashMap(23, hash_function_1)
    m.put('key343', 944)
    m.put('key506', 734)

    m.put('key516', -456)
    m.put('key59', -715)
    m.put('key184', -296)
    m.put('key265', -391)
    m.put('key680', 289)
    m.put('key473', -380)

    m.put('key196', 549)
    m.put('key892', 399)
    m.put('key379', -286)

    m.put('key668', 712)
    m.put('key696', 136)
    m.put('key789', -209)
    m.put('key411', 307)
    m.put('key214', -788)
    print(m.get_size())
    m.resize_table(1)
    print(m.get_size())


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")



