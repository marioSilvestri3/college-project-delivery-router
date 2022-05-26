from __future__ import annotations
from typing import Optional

"""
Chaining Hash Table implementation with Linked List and Node classes for buckets and key/value objects.
"""


# Time Complexity: O(1)
# Space Complexity: O(1)
class Node:
    def __init__(self, key, value):
        # Time Complexity: O(1)
        # Space Complexity: O(1)
        self.key = key
        self.value = value
        self.next: Optional[Node] = None


# Time Complexity: O(N)
# Space Complexity: O(N) [number of nodes]
class LinkedList:

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self):
        self.head: Optional[Node] = None

    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        else:
            self.pointer = self.current
            self.current = self.current.next
            return self.pointer

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def ll_delete(self, node: Node):
        if self.head == node:
            if self.head.next is not None:
                self.head = node.next
            else:
                self.head = None
        else:
            pointer = self.head
            while pointer.next is not None:  # O(N)
                if pointer.next == node:
                    pointer.next = node.next
                else:
                    pointer = pointer.next

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def ll_prepend(self, key, value):
        new_node = Node(key, value)
        if self.head is None:
            self.head = new_node
        else:
            pointer = self.head
            self.head = new_node
            new_node.next = pointer


# Time Complexity: O(N)
# Space Complexity: O(N)
# Lookup Time Complexity: O(1) -> O(N) as number of collisions approaches number of objects
class ChainingHashTable:

    # Time Complexity: O(N)
    # Space Complexity: O(N)
    def __init__(self, size=10):
        self.size = size
        self.hash_table: [LinkedList] = [LinkedList() for _ in range(size)]

    def __iter__(self):
        self.n = -1
        return self

    def __next__(self):
        self.n += 1
        if self.n < self.size:
            return self.hash_table[self.n]
        raise StopIteration

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def __len__(self):
        length = 0
        for table in self.hash_table:
            if table.head is None:
                continue
            else:
                for _ in table:
                    length += 1
        return length

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def hash_(self, key: int):
        return key % self.size

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def insert_(self, key: int, value):
        self.hash_table[self.hash_(key)].ll_prepend(key, value)

    def delete_(self, key):
        bucket = self.hash_table[self.hash_(key)]
        for node in bucket:
            if node.key == key:
                bucket.ll_delete(node)

    # Time Complexity: O(1) -> O(N) as number of collisions approaches number of objects
    # Space Complexity: O(1)
    def lookup_(self, key):
        bucket = self.hash_table[self.hash_(key)]
        for node in bucket:
            if node is not None and node.key == key:
                return node.value

    def get_all(self) -> list:
        all_objects = []
        for bucket in self.hash_table:
            for node in bucket:
                if node is not None:
                    all_objects.append(node.value)
        return all_objects
