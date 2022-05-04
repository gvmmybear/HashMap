# Name: Christian Castro
# OSU Email: castroch@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 03/11/2022
# Description: Hash Map ADT implementation using open addressing.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Class HashMap: This class method is used to clear
        a HashMap's key-value pairs without changing the
        underlying storage capacity. 
        :return: {None}
        """
        # simply iterate through the length of the 
        # bucket array and set to None.
        for i in range(self.buckets.length()):
            self.buckets[i] = None
        self.size = 0
        return  None

    def get(self, key: str) -> object:
        """
        Class HashMap: This class method is used to get the
        value associated with the input parameter "key".
        :param key: {str}
        :return: {object}
        """
        # calculate hashed index
        hash = self.hash_function(key)
        length = self.buckets.length()
        index = hash % length
        # if no key-val found, returns None
        if self.buckets[index] is None:
            return None
        else:
            # else we have a key-val pair at index and now
            # we check that index for matching key. If key
            # found at index does not match, we search for
            # the key using quadratic probing. 
            j = 0
            i = (index + j**2) % length
            while self.buckets[i] is not None:
                if self.buckets[i].key == key and not self.buckets[i].is_tombstone:
                    return self.buckets[i].value
                j += 1
                i = (index + j**2) % length
        return None

    def put(self, key: str, value: object) -> None:
        """
        Class HashMap: This class method is used to put
        a new key-value pair into the HashMap.
        :param key: {str}
        :param value: {object}
        :return: {None}
        """
        # resizes table if load factor is too large.
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity*2)

        # computes hashed index for key
        hash = self.hash_function(key)
        length = self.buckets.length()
        index = hash % length

        # if no pre-existing key-value pair is found, we
        # set bucket[index] to new Hash entry.
        if self.buckets[index] is None:
            self.size += 1
            self.buckets[index] = HashEntry(key, value)
            return None
        else:
            # else we have a collision so we use quadratic
            # probing until we find appropriate placement.
            j = 0
            i = (index + j**2) % length
            while self.buckets[i] is not None:
                if self.buckets[i].is_tombstone:
                    self.size += 1
                    self.buckets[i] = HashEntry(key, value)
                    return None
                elif self.buckets[i].key == key:
                    self.buckets[i].value = value
                    return None
                j += 1
                i = (index + j**2) % length
            self.size += 1
            self.buckets[i] = HashEntry(key, value)
        return None

    def remove(self, key: str) -> None:
        """
        Class HashMap: This class method is used to 
        remove a key-value pair from the HashMap.
        :param key: {str}
        :return: {None}
        """
        # computes hashed index
        hash = self.hash_function(key)
        length = self.buckets.length()
        index = hash % length
        
        # if no key-val pair is found, we return None
        if self.buckets[index] is None:
            return None
        else:
            # else, we begin searching for a key match so
            # we can delete. (Using quadratic probing)
            j = 0
            i = (index + j**2) % length
            while self.buckets[i] is not None:
                if self.buckets[i].key == key:
                    if not self.buckets[i].is_tombstone:
                        self.buckets[i].is_tombstone = True
                        self.size -= 1
                    return None
                j += 1
                i = (index + j**2) % length
        return None
            
    def contains_key(self, key: str) -> bool:
        """
        Class HashMap: This class method is used to 
        determine whether the HashMap contains the
        key-value pair.
        :param key: {str}
        :return: {bool}
        """
        if self.size < 1:
            return False

        # computes hashed index for key
        hash = self.hash_function(key)
        length = self.buckets.length()
        index = hash % length

        # returns false if no key-val pair is found at index
        if self.buckets[index] is None:
            return False
        else:
            # else, we begin searching for a key match 
            # (Using quadratic probing)
            j = 0
            i = (index + j**2) % length
            while self.buckets[i] is not None:
                if self.buckets[i].key == key:
                    if not self.buckets[i].is_tombstone:
                        return True
                    else:
                        return False
                j += 1
                i = (index + j**2) % length
        return False

    def empty_buckets(self) -> int:
        """
        Class HashMap: This class method is used to 
        determine the number of empty buckets in the
        HashMap.
        :return empty_count: {int}
        """
        # iterates through the array and counts empty
        # buckets and tombstone key-val pairs.
        empty_count = 0
        for i in range(self.buckets.length()):
            if self.buckets[i] is None:
                empty_count += 1
            elif self.buckets[i] is not None:
                if self.buckets[i].is_tombstone:
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
        if new_capacity < 1 or new_capacity < self.size:
            return None
        # using a helper function, we can rehash our key-value pairs into
        # a new hash map then copy the desired attributes over to self.
        new_hash = rehash(self.buckets, new_capacity, self.hash_function)
        self.buckets = new_hash.buckets
        self.capacity = new_hash.capacity
        return None

    def get_keys(self) -> DynamicArray:
        """
        Class HashMap: This class method is used to 
        get the keys which are contained in the Hash
        table.
        :return keys: {DynamicArray}
        """
        # iterates through the array and appends non-tombstone
        # and non-none keys to return DA.
        keys = DynamicArray()
        for i in range(self.buckets.length()):
            if self.buckets[i] is not None:
                if not self.buckets[i].is_tombstone:
                    keys.append(self.buckets[i].key)
        return keys

def rehash(old_buckets, new_capacity, hash_func):
    """
    Helper Function For resize(): this function is used
    to rehash keys to a new HashMap. 
    :param old_buckets: {DynamicArray}
    :param new_capacity: {int}
    :hash_func: {function}
    """
    # creates new hashmap with desired capacity and then
    # iterates through the input hash table to rehash keys
    hash_map = HashMap(new_capacity, hash_func)
    for i in range(old_buckets.length()):
        if old_buckets[i] is not None:
            if not old_buckets[i].is_tombstone:
                hash_map.put(old_buckets[i].key, old_buckets[i].value)
    return hash_map

def peek_array(HashMap: object) -> None:
    """
    Helper method for debugging: Prints out the 
    key-value pairs in human readable form through
    iteration.
    :param HashMap: {HashMap} 
    """
    for i in range(HashMap.buckets.length()):
        print(HashMap.buckets[i].__str__())
