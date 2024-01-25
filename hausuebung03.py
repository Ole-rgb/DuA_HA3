
from __future__ import annotations
from functools import partial
import math
import random
from typing import Any, Dict, List


class Node:
    left: Node
    right: Node
    parent: Node
    key: int
    value: Any

    def __init__(self, key: int, value: Any, parent: Node = None) -> None:
        """
        Initializes a new node with the given key and value.
        """
        self.key, self.value = key, value
        self.left, self.right, self.parent = None, None, parent

    def set_left(self, x: Node) -> None:
        """
        Sets the left child. Updates the parent of x.
        """
        if x == self: # no self reference
            return
        self.left = x
        if x is not None: 
            x.parent = self

    def set_right(self, x: Node) -> None:
        """
        Sets the right child. Updates the parent of x.
        """
        if x == self: # no self reference
            return
        self.right = x
        if x is not None:
            x.parent = self

    def remove_child(self, x: Node) -> None:
        """
        Removes the child x.
        """
        self.replace_child(x, None)

    def replace_child(self, x:Node, y:Node) -> None:
        """
        Replaces x with y, if x is a child of this node.
        """
        if x == self.left:
            self.set_left(y)
        if x == self.right:
            self.set_right(y)

class SplayTree:
    def __init__(self) -> None:
        """
        Initializes an empty SplayTree.
        """
        self.root = None

    def set_root(self, x: Node) -> None:
        """
        Updates the root of the SplayTree.
        """
        self.root = x
        if x is not None:
            x.parent = None

    def splay(self, x: Node) -> None:
        """
        Rotates the tree using 'zig', 'zig-zig' and 'zig-zag' steps to bring x to the root of the tree.
        """
        # TODO: Aufgabe 1
        pass

    def insert(self, key: int, value: Any) -> None:
        """
        Inserts the key, value pair into the SplayTree.
        """
        current = None
        next = self.root
        x = Node(key, value)

        if next is None:
            self.set_root(x)
            return

        while next is not None:
            if key < next.key:
                current, next = next, next.left
            else:
                current, next = next, next.right

        if key < current.key:
            current.set_left(x)
        else:
            current.set_right(x)

        self.splay(x)

    def inorder_successor(self, x: Node) -> Node:
        """
        Returns the inorder successor of x. 
        """
        current, next = None, x.right
        while next:
            current, next = next, next.left
        return current

    def delete(self, key: int) -> tuple[int, Any]:
        """
        Removes a Node given a key. Returns the key, value pair as a tuple or None if no Node was found.
        """
        x = self.find_node(key)
        if x is None:
            return None
        
        self.splay(x)
        if x.left is None:
            self.set_root(x.right)
        elif x.right is None:
            self.set_root(x.left)
        else:
            suc = self.inorder_successor(x)
            suc.parent.replace_child(suc, suc.right)
            self.set_root(suc)
            suc.set_left(x.left)
            suc.set_right(x.right)
        
        return x.key, x.value            

    def find_node(self, key: int) -> Node:
        """
        Returns a Node given its key. If no Node is found returns None.
        """
        node = self.root
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def access(self, key: int) -> tuple[int, Any]:
        """
        Returns the key, value tuple given a key, or None if no Node was found.
        """
        x = self.find_node(key)
        if x is None:
            return None
        self.splay(x)
        return x.key, x.value

    def __str__(self) -> str:
        def helper(x: Node, l: int):
            if x is None: return [] # base case
            return helper(x.left, l+1) + [(l, x.key)] + helper(x.right, l+1)
        
        inorder = helper(self.root, 1)
        result = ""
        level = 1
        for _ in range(max(inorder)[0]):
            for l, x in inorder:
                if l == level:            
                    result += str(x) + " "
                else:
                    result += " " * (len(str(x)) + 1)
            level += 1
            result += "\n"

        return result


def hash_family(r:int, a: list[int], x: int) -> int:
    return sum([(x ** i) * ai for i, ai in enumerate(a)]) % r

class CuckooHashtable:
    def __init__(self, size: int) -> None:
        """
        Initializes the CuckooHashtable for a given size.
        """
        self.size = size # save the size
        self.k = int(math.log2(self.size)) # number of parameters for the hash functions
        self.maxLoops = int(3 * math.log2(self.size)) + 1 # max number of loops in insert method
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        self.hash1 = partial(hash_family, size, random.choices(range(1, self.size), k=self.k)) # hashfunction 1
        self.hash2 = partial(hash_family, size, random.choices(range(1, self.size), k=self.k)) # hashfunction 2

    def rehash(self) -> None:
        """
        Recalculates the hash-functions and reinserts all values into the hash-tables.
        """
        self.hash1 = partial(hash_family, self.size, random.choices(range(1, self.size), k=self.k))
        self.hash2 = partial(hash_family, self.size, random.choices(range(1, self.size), k=self.k))

        values = self.table1.copy()
        values.extend(self.table2)
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        for v in filter(lambda x: (x is not None), values):
            self.insert(v)

    def insert(self, value: int) -> None:
        """
        Inserts value into the Hashtable. Iterates a maximum of self.maxLoops times.
        Uses self.hash1(x: int) -> int and self.hash2(x: int) -> int as current hashfunctions.
        """
        # TODO Aufgabe 2b
        print(self.hash1(value), self.hash2(value)) # example for hash1 and hash2
        pass

    def delete(self, value: int) -> None:
        """
        Removes value from table1 or table2, if it is contain in either
        """
        # TODO Aufgabe 2b
        print(self.hash1(value), self.hash2(value)) # example for hash1 and hash2
        pass

    def lookup(self, value: int) -> bool:
        """
        Returns True if value is in table1 or table2
        """
        # TODO Aufgabe 2b
        print(self.hash1(value), self.hash2(value)) # example for hash1 and hash2
        pass

    def __str__(self) -> str:
        return f"{self.table1}{self.table2}"
    

def dice_game(sides: int, DEBUG:bool=False) -> int:
    """
    Given a 'sides'-sided die. Returns the number x0 > sides which is most likely to reach sum, when rolling the die multiple times and adding the results. 
    """    
    assert sides > 1 # sides is always greater than 1!
    
    max_probability:int = 0 # The highest probability of all analysed numbers
    
    memo: Dict[int, float] = {} # Saves all the previously calculated results so we dont have to calculate them again
    
    '''
    Die Aufgabenstellung lässt besondere Einschränkungen von x0 zu:
        x0 > sides 
        x0 <= 2*sides + 1
    Nur diese Kandidaten werden durchsucht 
    '''
    for x in range(sides + 1, 2 * sides + 2):
        propability = calculate_probability(x, sides, memo, DEBUG) # calculate the probability for x
        
        if propability < max_probability: # skip the number, if its not a new maximum
            continue
        
        max_probability = propability 
        x0 = x # updates the value for x0 if we found higher probability 
    
    return x0


def calculate_probability(x:int, n:int, memo:Dict[int, float], DEBUG:bool) -> int:
    # if x is already calculated, return the value for x 
    if x in memo: 
        return memo[x]
    
    # calculate probability for unseen x and save results in memo
    if x <= n: # formular "wenn x ≤ n"
        memo[x] =(1/n) + (1/n) * sum(calculate_probability(i, n, memo, DEBUG) for i in range(1, x))
    else: # x > n -> formular "sonst"
        memo[x] = (1/n) * sum(calculate_probability(i, n, memo, DEBUG) for i in range(x-n, x))

    if DEBUG:  print("********  " , memo , " ********")
    
    return memo[x]


if __name__ == "__main__":
    print("Write your own tests here execute the 'hausuebung03_test.py' file!")
    # Beispiel für einen 2-seitigen Würfel ohne debugging
    n = 2
    x0 = dice_game(n)
    print(f'Die optimale Zahl x0 für einen {n}-seitigen Würfel ist {x0}.')
    
    # Beispiel für einen 3-seitigen Würfel mit debugging
    n = 4
    x0 = dice_game(n, True)
    print(f'Die optimale Zahl x0 für einen {n}-seitigen Würfel ist {x0}.')