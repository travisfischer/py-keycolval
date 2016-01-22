"""
Quick and dirty implementation of BinaryTree for testing as data structure for storing
columns.
"""


class Node(object):
    """
    A Basica Binary Tree Node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

        self.left = None
        self.right = None

        self.parent = None


class BinaryTree(object):
    """
    Quick and dirty binary tree data structure.
    """

    def __init__(self):
        self._root = None

    def insert(self, key, value):
        """
        Insert a key/value pair into binary tree as a node. If the key already exists
        overwrite the existing value at the node for this key with the new value.
        """
        node = Node(key, value)

        if self._root is None:
            self._root = node
        else:
            self._insert_in_subtree(node, self._root)

    def _insert_in_subtree(self, node, subtree_root):
        """
        Insert a node into a subtree.
        """
        # If node key is greater than current node, insert into right subtree.
        if node.key > subtree_root.key:

            # No right child so make this the right child.
            if subtree_root.right is None:
                subtree_root.right = node
                subtree_root.right.parent = subtree_root
            # Right child so perform insert against right subtree
            else:
                self._insert_in_subtree(node, subtree_root.right)

        # If node key is less than current node, insert into left subtree.
        elif node.key < subtree_root.key:

            # No left subtree so make this the left child.
            if subtree_root.left is None:
                subtree_root.left = node
                subtree_root.left.parent = subtree_root
            # Left child so perform insert against right subtree.
            else:
                self._insert_in_subtree(node, subtree_root.left)

        # If node key is equal, just overwrite the value / aka update.
        elif node.key == subtree_root.key:
            subtree_root.value = node.value
            
    def _iterate_subtree(self, sub_tree):
        """
        Iterator over subtree in order from min to max.
        """
        if sub_tree is not None:
            # First iteratate over the left subtree...
            for cur_node in self._iterate_subtree(sub_tree.left):
                yield cur_node

            # Then the root...
            yield sub_tree

            # Finally the right subtree...
            for cur_node in self._iterate_subtree(sub_tree.right):
                yield cur_node

    def _find_node_for_key(self, key):
        """
        Find a node in the entire tree for a given key.
        """
        return self._find_node(key, self._root)

    def _find_node(self, key, sub_tree):
        """
        Find a node in a subtree with a given key.
        """

        if sub_tree == None or sub_tree.key == key:
            # We either found the target key or it doesn't exist.
            # We return the value of sub_tree which is either
            # None for doesn't exist
            # or the node if we found the key
            return sub_tree

        elif sub_tree.key > key:
            # The current node key is greater than our search key
            # so we go left.
            return self._find_node(key, sub_tree.left)
        elif sub_tree.key < key:
            # The current node key is less than our search key
            # so we go right.
            return self._find_node(key, sub_tree.right)

    def all(self):
        """
        Return the full list of all key/value pairs in the binary tree.
        """
        return [(node.key, node.value) for node in self._iterate_subtree(self._root)]

    def get(self, key):
        """
        Get a value from the tree for the key.
        """
        node = self._find_node_for_key(key)
        # node may be None so perform safe attribute access.
        return getattr(node, 'value', None)

    def find_range(self, start_key=None, end_key=None):
        """
        Allow for finding a range of nodes which have keys within some
        boundary values.
        
        This algorithm is unoptimal it currently iterates over an entire
        subtree where the target slice is contained rather than using the
        fact that we have effecient means of finding the boundary nodes.
        """

        def _find_range_root(start_key, end_key, subtree_root):
            """
            Given a start_key and end_key find the root node that
            contains the entire range within the tree rooted at subtree_root.
            """
            if ((start_key is None or subtree_root.key >= start_key) and
                (end_key is None or subtree_root.key <= end_key)):
               return subtree_root
            elif end_key is not None and subtree_root.key > end_key:
                _find_range_root(start_key, end_key, subtree_root.left)
            elif start_key is not None and subtree_root.key < start_key:
                _find_range_root(start_key, end_key, subtree_root.right)

        range_root = _find_range_root(start_key, end_key, self._root)

        node_range = []

        # Inneffeciency here. Iterating the entire subtree.
        for node in self._iterate_subtree(range_root):
            if ((start_key is None or node.key >= start_key) and
                 (end_key is None or node.key <= end_key)):

                node_range.append(node)

            if node.key > end_key:
                # Short circuit if we find our entire range.
                # Note: short circuiting out of for loops is usually not
                # ideal for readiblity. May want to look into re-working this
                # loop.
                return node_range

        return node_range

    def delete(self, key):
        """
        Delete a node from the binary tree.
        """

        # First we get the node in question.
        node = self._find_node_for_key(key)

        # If it exists we delete it.
        if node:

            if node.left and node.right:
                # The node has two children.

                # So we find it's successor (next highest value in tree)
                successor_node = self._find_successor(node)

                # We swap out the successor_node for our current node by overwriting values.
                node.key = successor_node.key
                node.value = successor_node.value
                
                # We drop the old successor node from the tree.
                self._kill_node(successor_node)

            elif node.left:
                # The target node only has a left child.
                # So we replace target node with it's left child.
                self._replace_parent_with_child(node, node.left)
            elif node.right:
                # The target node only has a right child.
                # So we replace target node with it's right child.
                self._replace_parent_with_child(node, node.right)
            else:
                # No children so we can just drop it.
                self._kill_node(node)

    def _kill_node(self, node):
        """
        Actually remove a node from the tree by detaching it.
        """
        # Grab it's parent so we can clean the child link.
        parent = node.parent
        
        # Clean the parent's child link.
        if parent.left == node:
            parent.left = None
        elif parent.right == node:
            parent.right = None

        # Clean this node's parent link.
        node.parent = None

        # The node is orphaned we can remove it.
        del node

    def _replace_parent_with_child(self, parent, child):
        """
        Swap a parent node with one of it's child nodes removing the parent node.
        """

        # Update parent node's parent node to point to child.
        if hasattr(parent, 'parent'):
            parents_parent = parent.parent

            if parents_parent.left == parent:
                parents_parent.left = child
            elif parents_parent.right == parent:
                parents_parent.right = child

            child.parent = parents_parent
        else:
            # Edge case where parent was root.
            self._root = child

        del parent

    def _find_successor(self, node):
        """
        Find the next largest node in the tree.
        """
        # Find the next largest node.

        # Start by going one to the right.
        cur_node = node.right

        # If there is a left subtree descend it.
        while cur_node.left:
            cur_node = cur_node.left

        return cur_node
