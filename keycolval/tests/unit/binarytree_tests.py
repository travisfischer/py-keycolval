from keycolval.data_structures.binarytree import BinaryTree
import unittest

class ColumnTreeTests(unittest.TestCase):
    """
    Quick and dirty tests for our BinaryTree implementation.
    """
    
    def test_tree_delete_success(self):
        tree = BinaryTree()
        tree.insert('aa', 'xaxx')
        tree.insert('ab', 'xbxx')
        tree.insert('ac', 'xcxx')
        tree.insert('ad', 'xdxx')
        tree.insert('ae', 'xexx')
        tree.insert('af', 'xfxx')
        tree.insert('ag', 'xgxx')

        self.assertEqual(tree.get('ae'), 'xexx')
        self.assertEqual(tree.get('ag'), 'xgxx')

        tree.delete('ad')
        tree.delete('ab')

        self.assertEqual(tree.get('ad'), None)
        self.assertEqual(tree.get('ab'), None)
        self.assertEqual(tree.get('ae'), 'xexx')
        self.assertEqual(tree.get('ag'), 'xgxx')

    def test_tree_insert_get_success(self):
        tree = BinaryTree()
        tree.insert('aa', 'xaxx')
        tree.insert('ab', 'xbxx')
        tree.insert('ac', 'xcxx')
        tree.insert('ad', 'xdxx')
        tree.insert('ae', 'xexx')
        tree.insert('af', 'xfxx')
        tree.insert('ag', 'xgxx')

        self.assertEqual(tree.get('ae'), 'xexx')
        self.assertEqual(tree.get('ag'), 'xgxx')


    def test_tree_insert_get_all_success(self):
        tree = BinaryTree()
        tree.insert('ac', 'xcxx')
        tree.insert('ad', 'xdxx')
        tree.insert('ae', 'xexx')
        tree.insert('af', 'xfxx')
        tree.insert('aa', 'xaxx')
        tree.insert('ab', 'xbxx')
        tree.insert('ag', 'xgxx')

        self.assertEqual(tree.all(),
                         [('aa', 'xaxx'),
                          ('ab', 'xbxx'),
                          ('ac', 'xcxx'),
                          ('ad', 'xdxx'),
                          ('ae', 'xexx'),
                          ('af', 'xfxx'),
                          ('ag', 'xgxx')])

