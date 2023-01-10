
from django.test import TestCase
from users.utils.algo import UserInteractionBinaryTree, create_binary_tree

from random import randrange

from print_pp.logging import Print


class BinaryTreeDataNode:
    
    def __init__(self, score:int, next_node:'BinaryTreeDataNode'=None):
        self.score = score
        self.next_node = next_node


class TestBinaryTree(TestCase):

    def setUp(self) -> None:
        self.head:BinaryTreeDataNode = None
        prev_node:BinaryTreeDataNode = None
        
        for _ in range(10_000):
            new_node = BinaryTreeDataNode(randrange(1, 101))
            if prev_node:
                prev_node.next_node = new_node
            
            if not self.head:
                self.head = new_node

            prev_node = new_node

        return super().setUp()


    def create_binary_tree_test(self):

        # create a set of data to add to the binary tree with the BinaryTreeDataNode class
        # reverse the linked list to test it 
        root:UserInteractionBinaryTree = create_binary_tree(self.head)
        objective = root.find(50)
        self.assertEqual(objective.score, 50)
        root.delete(50)
        objective = root.find(50)
        self.assertEqual(objective, None)

    
    def get_values_test(self):
        root:UserInteractionBinaryTree = create_binary_tree(self.head)

        current_val = 100
        for node in root.get_values():
            if node is None: break
            self.assertEqual(node.score, current_val)
            current_val -= 1

        current_val = 1
        for node in root.get_values(direction='min'):
            if node is None: break
            self.assertEqual(node.score, current_val)
            current_val += 1

        # NOTE: it's possible that the node.score is not equal to current_val
        # since the values are place randomly in the binary tree, causing a leaf 
        # to have a value that is not equal to the current_val
        # not that it's a problem, but it's something to keep in mind
        # very unlikely to happen thou, but it's possible


    def test_create_binary_tree(self):
        self.create_binary_tree_test()
        self.get_values_test()
