# Hashmap with open addressing

# Description: The hashmap class represents a hashmap with an underlying dynamic array. Collisions
# are resolved with open addressing via quadratic probing. Class contains methods to put a key/value
# pair in the hashmap, get the value of a key, remove a key, determine if a key is present within
# the hashmap, clear the hashmap, return the empty bucket count, resize the capacity, return the load
# factor, get a dynamic array of key/value pairs, and iterate through the hashmap.

from data_structures import (DynamicArray, DynamicArrayException, HashEntry,
                             hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
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
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and value pair as parameters. Places the key/value pair in
        the hash map via quadratic probing. Returns nothing.
        """
        if self.table_load() >= .5:    # compare load factor
            self.resize_table(self._capacity*2)

        hash = self._hash_function(key) % self._buckets.length()
        count = 1
        index = hash

        while self._buckets.get_at_index(index) is not None:    # find an empty index or tombstone
            entry = self._buckets.get_at_index(index)
            if entry.key == key and entry.is_tombstone is False:    # replace a matching key w/ new value
                self._buckets.set_at_index(index, None)
                self._size -= 1
            elif entry.is_tombstone is True:    # make tombstone index None so it can be hashed
                self._buckets.set_at_index(index, None)
            else:
                index = (hash + count**2) % self._capacity  # quadratic probing
                count += 1

        new_hash = HashEntry(key, value)
        self._buckets.set_at_index(index, new_hash)
        self._size += 1

    def table_load(self) -> float:
        """
        Takes no parameters. Returns the table load factor as a float.
        """
        load_factor = self._size / self._buckets.length()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Returns the amount of empty buckets in the table as
        an integer.
        """
        count = 0

        for index in range(self._buckets.length()):
            entry = self._buckets.get_at_index(index)
            if entry is None:       # increase count for None and tombstones
                count += 1
            elif entry.is_tombstone is True:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity integer as a parameter. Returns nothing.
        Resizes the table based on the new capacity and rehashes all key/value pairs
        within the table.
        """
        if new_capacity < self._size:
            return

        da = self.get_keys_and_values()  # get an array of all keys and values

        if self._is_prime(new_capacity) is False:       # table capacity must be a prime number
            new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        self.clear()    # appends the new capacity to resize the table

        for index in range(da.length()):    # rehash all key/value pairs
            key = da.get_at_index(index)[0]
            value = da.get_at_index(index)[1]
            self.put(key, value)

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter. Returns the value of the key if the key exists in
        the table. Returns None if the key is not in the table.
        """
        hash = self._hash_function(key) % self._buckets.length()  # gives the first potential index
        count = 1
        index = hash

        while self._buckets.get_at_index(index) is not None:    # find an empty index
            entry = self._buckets.get_at_index(index)
            if entry.key == key and entry.is_tombstone is False:    # a matching key/value pair has been found
                return entry.value
            else:
                index = (hash + count**2) % self._capacity
                count += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter. Uses quadratic probing to determine if the key is
        in the hash map. Returns true if the given key is in the hash map or false if not.
        """
        hash = self._hash_function(key) % self._buckets.length()  # gives the first potential index
        count = 1
        index = hash

        while self._buckets.get_at_index(index) is not None:  # find an empty index
            entry = self._buckets.get_at_index(index)
            if entry.key == key and entry.is_tombstone is False:
                return True
            else:
                index = (hash + count**2) % self._capacity
                count += 1

        return False    # key not found

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter. Removes the key from the hash map using quadratic probing.
        Returns nothing.
        """
        hash = self._hash_function(key) % self._buckets.length()  # gives the first potential index
        count = 1
        index = hash

        while self._buckets.get_at_index(index) is not None:  # find an empty index
            entry = self._buckets.get_at_index(index)
            if entry.key == key and entry.is_tombstone is False:
                entry.is_tombstone = True
                self._size -= 1
                return  # end the loop when they key has been found and removed
            else:
                index = (hash + count ** 2) % self._capacity
                count += 1

    def clear(self) -> None:
        """
        Takes no parameters. Clears all elements from the hash map. Returns nothing.
        """
        self._size = 0
        self._buckets = DynamicArray()  # reset the DA
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters. Creates a dynamic array with tuples of the key/value pairs
        from the hash map. Returns the dynamic array.
        """
        DA = DynamicArray()

        for index in range(self._buckets.length()):
            entry = self._buckets.get_at_index(index)

            if entry is not None:
                if entry.is_tombstone is False: # keys that are tombstones are not added
                    DA.append((entry.key, entry.value))

        return DA

    def __iter__(self):
        """
        Takes no parameters. Creates an iterator to iterate through the hash map.
        Returns the iterator.
        """
        self._index = 0     # initializes the first iteration to index 0
        return self

    def __next__(self):
        """
        Takes no parameters. Returns the next value within the hash map based on
        the iterator.
        """

        try:
            entry = self._buckets.get_at_index(self._index)
        except DynamicArrayException:   # in case the next index value is out of range
            raise StopIteration

        while entry is None or entry.is_tombstone:
            self._index += 1
            try:
                entry = self._buckets.get_at_index(self._index)
            except DynamicArrayException:   # in case an index after None/tombstone is out of range
                raise StopIteration

        self._index += 1    # sets the index for the next iteration
        return entry


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
