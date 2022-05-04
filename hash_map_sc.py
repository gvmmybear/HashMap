# Name: Christian Castro
# OSU Email: castroch@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 
# Due Date: 03/11/2022
# Description: Hash Map ADT implementation using singly linked chains.


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Class HashMap: This class method is used to clear
        a HashMap's key-value pairs without changing the
        underlying storage capacity. 
        :return: {None}
        """

        buckets = self.buckets
        length = buckets.length()

        # iterates through the length of the array which
        # contains our chains and reinitializes then to
        # empty LinkedList().
        for i in range(length):
            buckets[i] = LinkedList()
        self.size = 0
        return None
       
    def get(self, key: str) -> object:
        """
        Class HashMap: This class method is used to get the
        value associated with the param key.
        :param key: {str}
        :return: {object}
        """
        # calculate hashed index 
        hash = self.hash_function(key)
        index = hash % self.buckets.length()

        # then if a non-empty linked list exists at
        # the target index, we search the LL for the
        # key-value pair.
        search_LL = self.buckets[index]
        if search_LL.length() > 0:
            contains = search_LL.contains(key)
            if contains:
                return contains.value
        return None

    def put(self, key: str, value: object) -> None:
        """
        Class HashMap: This class method is used to put
        a new key-value pair into the HashMap.
        :param key: {str}
        :param value: {object}
        :return: {None}
        """
        # calculate target index with hash function
        hash = self.hash_function(key)
        index = hash % self.buckets.length()

        # then if non-empty linked list exists, we
        # check if we are inserting new pair or 
        # whether we need to update the key-value pair.
        search_LL = self.buckets[index]
        if search_LL.length() > 0:
            contains = search_LL.contains(key)
            if contains:
                contains.value = value
            else:
                search_LL.insert(key, value)
                self.size += 1
        else:
            search_LL.insert(key, value)
            self.size += 1
        return None

    def remove(self, key: str) -> None:
        """
        Class HashMap: This class method is used to 
        remove a key-value pair from the HashMap.
        :param key: {str}
        :return: {None}
        """
        # calculate key's index with hash function
        hash = self.hash_function(key)
        index = hash % self.buckets.length()
        search_LL = self.buckets[index]

        # use LL method to remove key-value pair if
        # it exists in the chain.
        if search_LL.remove(key):
            self.size -= 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Class HashMap: This class method is used to 
        determine whether the HashMap contains the
        key-value pair.
        :param key: {str}
        :return: {bool}
        """
        # calculate hashed index
        hash = self.hash_function(key)
        index = hash % self.buckets.length()
        search_LL = self.buckets[index]

        # search LL at index for key
        if search_LL.contains(key):
            return True
        return False

    def empty_buckets(self) -> int:
        """
        Class HashMap: This class method is used to 
        determine the number of empty buckets in the
        HashMap.
        :return empty_count: {int}
        """
        buckets = self.buckets
        length = buckets.length()

        # iterate through the array containing the LL's
        # and add to empty count if we have empty LL.
        empty_count = 0
        for i in range(length):
            if buckets[i].length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Class HashMap: This class method is used to 
        determine the load factor of the HashMap table.
        :return: {float}
        """
        # returns load factor
        return self.size / self.buckets.length()

    def resize_table(self, new_capacity: int) -> None:
        """
        Class HashMap: This class method is used to 
        resize a Hash table. 
        :param new_capacity: {int}
        :return: {None}
        """
        if new_capacity < 1:
            return None

        # first we copy all of the key/val pairs
        # onto a DA. 
        buckets = self.buckets
        key_val_pairs = DynamicArray()
        for i in range(buckets.length()):
            if buckets[i].length() > 0:
                for node in buckets[i]:
                    key_val_pairs.append(node)

        # next we resize buckets/capacity according 
        # to the input param new_capacity.
        self.buckets = DynamicArray()
        for i in range(new_capacity):
            self.buckets.append(LinkedList())
        self.capacity = new_capacity

        # finally we rehash the key's and place in the
        # new resized array. 
        self.size = 0
        length = key_val_pairs.length()
        while length > 0:
            node = key_val_pairs.pop()
            self.put(node.key, node.value)
            length -= 1
        return None

    def get_keys(self) -> DynamicArray:
        """
        Class HashMap: This class method is used to 
        get the keys which are contained in the Hash
        table.
        :return keys: {DynamicArray}
        """
        # iterates through each of the array indices
        # and non-empty LL's then appends to output
        # array for return.
        keys = DynamicArray()
        buckets = self.buckets
        for i in range(buckets.length()):
            if buckets[i].length() > 0:
                for node in buckets[i]:
                    keys.append(node.key)
        return keys
