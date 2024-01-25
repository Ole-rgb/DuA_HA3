import random
import unittest
from hausuebung03 import dice_game, SplayTree, CuckooHashtable, Node

class TestExercise1(unittest.TestCase):
    def test_zig_left(self):
        st = SplayTree()
        st.root = Node(4, 4)
        st.root.set_left(Node(2, 2))
        st.root.set_right(Node(5, 5))
        st.root.left.set_left(Node(1, 1))
        st.root.left.set_right(Node(3, 3))

        st.splay(st.root.left)
        self.assertEqual(st.root.key, 2)
        self.assertEqual(st.root.left.key, 1)
        self.assertEqual(st.root.right.key, 4)
        self.assertEqual(st.root.right.left.key, 3)
        self.assertEqual(st.root.right.right.key, 5)

    def test_zig_zig_left(self):
        st = SplayTree()
        st.root = Node(6, 6)
        st.root.set_left(Node(4, 4))
        st.root.set_right(Node(7, 7))
        st.root.left.set_left(Node(2, 2))
        st.root.left.set_right(Node(5, 5))
        st.root.left.left.set_left(Node(1, 1))
        st.root.left.left.set_right(Node(3, 3))
        
        st.splay(st.root.left.left)
        self.assertEqual(st.root.key, 2)
        self.assertEqual(st.root.left.key, 1)
        self.assertEqual(st.root.right.key, 4)
        self.assertEqual(st.root.right.left.key, 3)
        self.assertEqual(st.root.right.right.key, 6)
        self.assertEqual(st.root.right.right.left.key, 5)
        self.assertEqual(st.root.right.right.right.key, 7)

    def test_zig_zag_left(self):
        st = SplayTree()
        st.root = Node(6, 6)
        st.root.set_left(Node(2, 2))
        st.root.set_right(Node(7, 7))
        st.root.left.set_left(Node(1, 1))
        st.root.left.set_right(Node(4, 4))
        st.root.left.right.set_left(Node(3, 3))
        st.root.left.right.set_right(Node(5, 5))
        
        st.splay(st.root.left.right)
        self.assertEqual(st.root.key, 4)
        self.assertEqual(st.root.left.key, 2)
        self.assertEqual(st.root.right.key, 6)
        self.assertEqual(st.root.left.left.key, 1)
        self.assertEqual(st.root.left.right.key, 3)
        self.assertEqual(st.root.right.left.key, 5)
        self.assertEqual(st.root.right.right.key, 7)

    def test_insert(self):
        st = SplayTree()
        st.insert(1, 1)
        st.insert(6, 6)
        st.insert(3, 3)
        st.insert(5, 5)
        st.insert(2, 2)
        st.insert(4, 4)

        self.assertEqual(st.root.key, 4)

    def test_access(self):
        st = SplayTree()
        st.insert(1, 1)
        st.insert(6, 6)
        st.insert(3, 3)
        st.insert(5, 5)
        st.insert(2, 2)
        st.insert(4, 4)
        self.assertEqual(st.access(3), (3, 3))
        self.assertEqual(st.root.key, 3)

    def test_delete(self):
        st = SplayTree()
        st.insert(1, 1)
        st.insert(6, 6)
        st.insert(3, 3)
        st.insert(5, 5)
        st.insert(2, 2)
        st.insert(4, 4)
        self.assertEqual(st.delete(1), (1, 1))
        self.assertEqual(st.root.key, 2)    

    def consistence(self, node):
        if node.left:
            self.assertLessEqual(node.left.key, node.key)
            self.consistence(node.left)
        if node.right:
            self.assertLessEqual(node.key, node.right.key)
            self.consistence(node.right)

    def test_random_small(self):
        st = SplayTree()
        values = []
        for i in random.sample(range(20), 10):
            st.insert(i, i)
            values.append(i)
            self.assertEqual(st.root.key, i)
        self.consistence(st.root)
        for i in random.sample(values, len(values) // 2):
            values.remove(i)
            self.assertEqual(st.access(i), (i, i))
            self.assertEqual(st.root.key, i)
        for i in values:
            self.assertEqual(st.delete(i), (i, i))

    def test_random_big(self):
        st = SplayTree()
        values = []
        for i in random.sample(range(250), 100):
            st.insert(i, i)
            values.append(i)
            self.assertEqual(st.root.key, i)
        self.consistence(st.root)
        for i in random.sample(values, len(values) // 2):
            values.remove(i)
            self.assertEqual(st.access(i), (i, i))
            self.assertEqual(st.root.key, i)
        for i in values:
            self.assertEqual(st.delete(i), (i, i))


class TestExercise2(unittest.TestCase):
    def test_insert1(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: x % 3
        ch.insert(1)
        self.assertEqual(ch.table1, [None, 1, None])
        self.assertEqual(ch.table2, [None, None, None])

    def test_insert3(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: x % 3
        ch.insert(1)
        ch.insert(2)
        ch.insert(3)
        self.assertEqual(ch.table1, [3, 1, 2])
        self.assertEqual(ch.table2, [None, None, None])

    def test_insert_collision4(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: 1
        ch.hash2 = lambda x: {1:2, 2:1, 3:2, 4:0}[x]
        ch.insert(1)
        ch.insert(2)
        ch.insert(3)
        ch.insert(4)
        self.assertEqual(ch.table1, [None, 1, None])
        self.assertEqual(ch.table2, [4, 2, 3])

    def test_insert12_seed0(self):
        random.seed(0)
        ch = CuckooHashtable(9)
        for i in range(12):
            ch.insert(i)
        self.assertEqual(ch.table1, [10, 6, 8, 7, 3, 5, 4, 9, 11])
        self.assertEqual(ch.table2, [None, 2, 1, None, None, None, 0, None, None])

    def test_lookup1(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: x % 3
        ch.insert(1)
        self.assertEqual(ch.lookup(1), True)
        self.assertEqual(ch.lookup(2), False)

    def test_lookup3(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: x % 3
        ch.insert(1)
        ch.insert(2)
        ch.insert(3)
        self.assertEqual(ch.lookup(1), True)
        self.assertEqual(ch.lookup(2), True)
        self.assertEqual(ch.lookup(3), True)
        self.assertEqual(ch.lookup(4), False)
        self.assertEqual(ch.lookup(5), False)
        self.assertEqual(ch.lookup(6), False)

    def test_lookup_collision4(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: 1
        ch.hash2 = lambda x: {1:2, 2:1, 3:2, 4:0, 5:1, 6:2}[x]
        ch.insert(1)
        ch.insert(2)
        ch.insert(3)
        ch.insert(4)
        self.assertEqual(ch.lookup(1), True)
        self.assertEqual(ch.lookup(2), True)
        self.assertEqual(ch.lookup(3), True)
        self.assertEqual(ch.lookup(4), True)
        self.assertEqual(ch.lookup(5), False)
        self.assertEqual(ch.lookup(6), False)

    def test_lookup12_seed0(self):
        random.seed(0)
        ch = CuckooHashtable(9)
        for i in range(12):
            ch.insert(i)
        for i in range(12):
            self.assertEqual(ch.lookup(i), True)
        for i in range(13,20):
            self.assertEqual(ch.lookup(i), False)

    def test_delete1(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: x % 3
        ch.insert(1)
        self.assertEqual(ch.lookup(1), True)
        ch.delete(1)
        self.assertEqual(ch.lookup(1), False)
        self.assertEqual(ch.table1, [None, None, None])
        self.assertEqual(ch.table2, [None, None, None])

    def test_delete_collision4(self):
        ch = CuckooHashtable(3)
        ch.hash1 = lambda x: 1
        ch.hash2 = lambda x: {1:2, 2:1, 3:2, 4:0, 5:1, 6:2}[x]
        ch.insert(1)
        ch.insert(2)
        ch.insert(3)
        ch.insert(4)
        self.assertEqual(ch.lookup(1), True)
        self.assertEqual(ch.lookup(2), True)
        self.assertEqual(ch.lookup(3), True)
        self.assertEqual(ch.lookup(4), True)
        ch.delete(4)
        self.assertEqual(ch.lookup(4), False)
        ch.delete(2)
        self.assertEqual(ch.lookup(2), False)
        ch.delete(3)
        self.assertEqual(ch.lookup(3), False)
        ch.delete(1)
        self.assertEqual(ch.lookup(1), False)
        self.assertEqual(ch.table1, [None, None, None])
        self.assertEqual(ch.table2, [None, None, None])

    def test_delete12_seed0(self):
        random.seed(0)
        ch = CuckooHashtable(9)
        for i in range(12):
            ch.insert(i)
        for i in range(12):
            self.assertEqual(ch.lookup(i), True)
        for i in range(12):
            ch.delete(i)
        for i in range(12):
            self.assertEqual(ch.lookup(i), False)

class TestExercise3(unittest.TestCase):
    def test_dice_game6(self):
        self.assertEqual(dice_game(6), 11)
        
    def test_dice_game12(self):
        self.assertEqual(dice_game(12), 21)
        
    def test_dice_game20(self):
        self.assertEqual(dice_game(20), 35)
        
    def test_dice_game100(self):
        self.assertEqual(dice_game(100), 173)

    def test_dice_game1000(self):
        self.assertEqual(dice_game(1000), 1719)

    # def test_dice_game10000(self): # can take a few seconds    
    #     self.assertEqual(dice_game(10000), 17184)

    def test_dice_game_first100(self):
        sol = [4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 34, 35, 37, 39, 40, 42, 44, 46, 47, 49, 51, 52, 54, 56, 58, 59, 61, 63, 64, 66, 68, 70, 71, 73, 75, 76, 78, 80, 82, 83, 85, 87, 88, 90, 92, 94, 95, 97, 99, 101, 102, 104, 106, 107, 109, 111, 113, 114, 116, 118, 119, 121, 123, 125, 126, 128, 130, 131, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 157, 159, 161, 162, 164, 166, 168, 169, 171, 173]

        self.assertEqual([dice_game(n) for n in range(2, 101)], sol)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    # print("---------------- Test Exercise 1  ----------------")
    # runner.run(unittest.TestLoader().loadTestsFromTestCase(TestExercise1))
    # print("---------------- Test Exercise 2  ----------------")
    # runner.run(unittest.TestLoader().loadTestsFromTestCase(TestExercise2))
    print("---------------- Test Exercise 3  ----------------")
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestExercise3))