import unittest
from datetime import datetime
import os

from keycolval.stores.doubledictstore import DoubleDictKeyColValStore
from keycolval.stores.binarytreestore import BinaryTreeKeyColValStore


class KeyColValStorePersistenceUnitTests(unittest.TestCase):
    """
    Unit tests for testing the persistence functionality of KeyColValStore implementations.

    You can configure which data store to test against using the STORE_CLASS class variable below.
    """

    # Configuration setting for which KeyColValStore implementation these tests
    # should be run against.
    STORE_CLASS = DoubleDictKeyColValStore

    @classmethod
    def _keycolvalstore_factory(cls, file_path):
        """
        A factory function which produces an instance of the KeyColValStore to be tested.
        """
        return cls.STORE_CLASS(path=file_path)

    def test_set_persists_data(self):
        TEST_FILE_PATH = '/tmp/keycolval.testdata.%s.csv' % datetime.now()

        store = self._keycolvalstore_factory(TEST_FILE_PATH)
        store.set('a-key', 'my-column', 'the-value')
        store.set('b-key', 'other-column', 'value')
        del store

        second_store = self._keycolvalstore_factory(TEST_FILE_PATH)
        self.assertEqual(second_store.get('a-key', 'my-column'), 'the-value')
        self.assertEqual(second_store.get('b-key', 'other-column'), 'value')

    def test_set_persists_update_to_data(self):
        TEST_FILE_PATH = '/tmp/keycolval.testdata.%s.csv' % datetime.now()

        store = self._keycolvalstore_factory(TEST_FILE_PATH)
        store.set('a-key', 'my-column', 'the-value')
        store.set('b-key', 'other-column', 'value')
        store.set('a-key', 'my-column', 'new-value')

        del store

        second_store = self._keycolvalstore_factory(TEST_FILE_PATH)
        self.assertEqual(second_store.get('a-key', 'my-column'), 'new-value')
        self.assertEqual(second_store.get('b-key', 'other-column'), 'value')

    def test_delete_persists_data(self):
        TEST_FILE_PATH = '/tmp/keycolval.testdata.%s.csv' % datetime.now()

        store = self._keycolvalstore_factory(TEST_FILE_PATH)
        store.set('a-key', 'my-column', 'the-value')
        store.set('a-key', 'other-column', 'value')
        store.delete('a-key', 'my-column')

        del store
        
        second_store = self._keycolvalstore_factory(TEST_FILE_PATH)
        self.assertEqual(second_store.get_key('a-key'),
                         [('other-column', 'value')])

    def test_delete_persists_data(self):
        TEST_FILE_PATH = '/tmp/keycolval.testdata.%s.csv' % datetime.now()

        store = self._keycolvalstore_factory(TEST_FILE_PATH)
        store.set('a-key', 'my-column', 'the-value')
        store.set('a-key', 'other-column', 'value')
        store.set('b-key', 'b-column', 'b-value')
        store.delete_key('a-key')

        del store
        
        second_store = self._keycolvalstore_factory(TEST_FILE_PATH)
        self.assertEqual(second_store.get_key('a-key'), [])
        self.assertEqual(second_store.get('b-key', 'b-column'), 'b-value')



class KeyColValStoreUnitTests(unittest.TestCase):
    """
    Unit tests for testing the basic interface functionality of KeyColValStore implementations.

    Can be run against a new KeyColValStore implementation by swapping the value assigned
    to the '''STORE_CLASS''' class variable.
    """

    # Configuration setting for which KeyColValStore implementation these tests
    # should be run against.
    STORE_CLASS = DoubleDictKeyColValStore

    @classmethod
    def _keycolvalstore_factory(self):
        """
        A factory function which produces an instance of the KeyColValStore to be tested.
        """
        return self.STORE_CLASS()

    def test_set_then_get_success(self):
        """
        Test that a KeyColValStore behaves as expected in the simple case of a set followed by a get.

        Note: The set functionality of a KeyColValStore can only be properly tested by also inspecting
        that the get function returns what is expected after a get. Testing a set function in isolation
        would require either testing against implementation details which is something we want to avoid.
        """
        store = self._keycolvalstore_factory()
        
        store.set('a-key', 'column-name', 'my-little-value')
        self.assertEqual(store.get('a-key', 'column-name'), 'my-little-value')

    def test_non_string_lookups(self):
        """
        Keys, Columns and Values are all defined to be strings. Test for the case when a non-string is
        passed. Should raise an appriate exception.
        """
        store = self._keycolvalstore_factory()
        
        not_a_string = object()

        # TODO: Add assertions for proper exceptions.
        store.set(not_a_string, 'column-name', 'my-little-value')
        store.set('a-key', not_a_string, 'my-little-value')
        store.set('a-key', 'column-name', not_a_string)

    def test_get_key_success(self):
        """
        Test the get_key function works as expected by returning the exepected ordered list of
        tuple column/value pairs.
        """

        store = self._keycolvalstore_factory()

        # We set values in sequence that is not ordered by column name to ensure we test
        # the ordering behavior of get_key
        store.set('a-key', 'column-b', 'value-2')
        store.set('a-key', 'column-c', 'value-3')
        store.set('a-key', 'column-a', 'value-1')
        store.set('a-key', 'column-d', 'value-4')

        self.assertEqual(store.get_key('a-key'),
                         [('column-a', 'value-1'),
                          ('column-b', 'value-2'),
                          ('column-c', 'value-3'),
                          ('column-d', 'value-4')])


    def test_get_nonexistent_key_success(self):
        """
        Test that when get is called on a non-existant key None value is returned.
        """
        store = self._keycolvalstore_factory()

        # Set a dummy key/column/value just so we have a valid data initialization
        # KeyColValStore
        store.set('a-key', 'column-name', 'my-little-value')

        self.assertIsNone(store.get('z-key', 'column'))

    def test_get_nonexistent_column_success(self):
        """
        Test that when we call get on a key that does exist but a column that does
        not we get None value returned.
        """
        store = self._keycolvalstore_factory()
        
        # Set a key/column/value so that we have a valid key.
        store.set('a-key', 'column-name', 'my-little-value')

        # Assert that when we get a valid value but a non-existent column None is returned.
        self.assertIsNone(store.get('a-key', 'other-column'))

    def test_get_key_nonexistent_key_success(self):
        """
        Test that when you call get_key on a non-existent key you get back an empty list.
        """
        store = self._keycolvalstore_factory()

        # Set a dummy key/column/value so that our KeyColValStore has initialized value.
        store.set('a-key', 'column-name', 'my-little-value')

        self.assertEqual(store.get_key('z-key'), [])

    def test_set_update_value_success(self):
        """
        Test that when set is called repeatadly for some key/column it correctly
        updates the value stored in that key/column.
        """
        store = self._keycolvalstore_factory()

        # Set some initial values.
        store.set('a-key', 'column-b', 'value-2')
        store.set('a-key', 'column-c', 'value-3')
        store.set('a-key', 'column-a', 'value-1')
        store.set('a-key', 'column-d', 'value-4')      

        # First assert that expected values are returned after intial set.
        self.assertEqual(store.get_key('a-key'),
                         [('column-a', 'value-1'),
                          ('column-b', 'value-2'),
                          ('column-c', 'value-3'),
                          ('column-d', 'value-4')])

        # Update some already set column values.
        store.set('a-key', 'column-c', 'someone-was-here')
        store.set('a-key', 'column-a', 'whahhh-happened?')

        # Assert that both get and get_key return updated values.
        self.assertEqual(store.get('a-key', 'column-a'), 'whahhh-happened?')
        self.assertEqual(store.get('a-key', 'column-c'), 'someone-was-here')
        self.assertEqual(store.get_key('a-key'),
                         [('column-a', 'whahhh-happened?'),
                          ('column-b', 'value-2'),
                          ('column-c', 'someone-was-here'),
                          ('column-d', 'value-4')])


    def test_delete_column_success(self):
        """
        Test that calling delete on a column removes that column from
        the KeyColValStore.
        """
        store = self._keycolvalstore_factory()

        # Set some initial values.
        store.set('a-key', 'column-b', 'value-2')
        store.set('a-key', 'column-c', 'value-3')
        store.set('a-key', 'column-a', 'value-1')
        store.set('a-key', 'column-d', 'value-4')      

        # Delete a column
        store.delete('a-key', 'column-c')
        
        # Assert the column has been removed.
        self.assertIsNone(store.get('a-key', 'column-c'))
        self.assertEqual(store.get_key('a-key'),
                         [('column-a', 'value-1'),
                          ('column-b', 'value-2'),
                          ('column-d', 'value-4')])

    def test_delete_key_success(self):
        """
        Test that calling delete on a key removes that entire key
        from the KeyColValStore.
        """
        store = self._keycolvalstore_factory()
        
        # Set some initial values.
        store.set('a-key', 'column-a1', 'value-1')
        store.set('a-key', 'column-a2', 'value-2')
        store.set('b-key', 'column-b1', 'value-3')
        store.set('b-key', 'column-b2', 'value-4')   
        
        # Delete an entire key
        store.delete_key('a-key')
        
        # Assert that the removed key is gone.
        self.assertEqual(store.get_key('a-key'), [])
        self.assertIsNone(store.get('a-key', 'column-a1'))

        # Assert that remaining key is unscathed.
        self.assertEqual(store.get_key('b-key'),
                         [('column-b1', 'value-3'),
                          ('column-b2', 'value-4')])

        # Assert that get_keys has also removed the key in question
        self.assertSetEqual(store.get_keys(),
                            set(['b-key']))      
        

    def test_get_keys_success(self):
        """
        We want to test that the get_keys function returns the expected set of all unique keys.
        """
        store = self._keycolvalstore_factory()

        # Set some initial values.
        store.set('a-key', 'column-a1', 'value-1')
        store.set('a-key', 'column-a2', 'value-2')
        store.set('b-key', 'column-b1', 'value-3')
        store.set('b-key', 'column-b2', 'value-4')
        store.set('c-key', 'column-c1', 'value-5')

        self.assertSetEqual(store.get_keys(),
                            set(['a-key', 'b-key', 'c-key']))

    def test_get_slice_success(self):
        """
        Test that get_slice returns accurate ordered slices for both bounded
        and unbounded slices.
        """
        store = self._keycolvalstore_factory()

        # Set a bunch of column-values in a key. Do so out of order to check ordering functionality
        store.set('a-key', 'column-a4', 'val')
        store.set('a-key', 'column-a5', 'val')
        store.set('a-key', 'column-a2', 'val')
        store.set('a-key', 'column-a1', 'val')
        store.set('a-key', 'column-a7', 'val')
        store.set('a-key', 'column-a3', 'val')
        store.set('a-key', 'column-a6', 'val')

        # Set a column-value in another to check for that unrelated keys don't impact get_slice
        store.set('b-key', 'column-b1', 'value-3')

        # Test that a slice in the middle will return the correct slice.
        self.assertEqual(store.get_slice('a-key', 'column-a3', 'column-a6'),
                                        [('column-a3', 'val'),
                                         ('column-a4', 'val'),
                                         ('column-a5', 'val'),
                                         ('column-a6', 'val')])

        # Test that an end-unbounded slice returns the expected result.
        self.assertEqual(store.get_slice('a-key', 'column-a3', None),
                         [('column-a3', 'val'),
                          ('column-a4', 'val'),
                          ('column-a5', 'val'),
                          ('column-a6', 'val'),
                          ('column-a7', 'val')])

        # Test that a start-unbounded slice returns the expected result.
        self.assertEqual(store.get_slice('a-key', None, 'column-a5'),
                         [('column-a1', 'val'),
                          ('column-a2', 'val'),
                          ('column-a3', 'val'),
                          ('column-a4', 'val'),
                          ('column-a5', 'val')])

    def test_invalid_slice_handling(self):
        """
        Test that when get_slice is called with boundary values that are not of a valid range,
        it raises the appropriate exception.
        """
        store = self._keycolvalstore_factory()

        # Set a bunch of column-values in a key. Do so out of order to check ordering functionality
        store.set('a-key', 'column-a2', 'val')
        store.set('a-key', 'column-a1', 'val')
        store.set('a-key', 'column-a3', 'val')

        # Set a column-value in another to check for that unrelated keys don't impact get_slice
        store.set('b-key', 'column-b1', 'value-3')

        # TODO: Assert raises
        store.get_slice('a-key', 'column-a3', 'column-a1')

    def test_level_1_spec(self):
        """
        The following test runs the exact test commands outlined in the problem specification.
        We include these as a unit test in order to ensure accurate translation of requirements.
        """
        store = self._keycolvalstore_factory()

        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('c', 'cc', 'x')
        store.set('c', 'cd', 'x')
        store.set('d', 'de', 'x')

        store.set('d', 'df', 'x')   

        # the statements below will evaluate to True
        self.assertEqual(store.get('a', 'aa'), 'x')

        self.assertEqual(store.get_key('a'), [('aa', 'x'), ('ab', 'x')])
        
        # nonexistent keys/columns, the statements below

        # will evaluate to True
        self.assertIsNone(store.get('z', 'yy'))
        self.assertEqual(store.get_key('z'), [])

        # if we set different values on the 'a' key:
        store.set('a', 'aa', 'y')
        store.set('a', 'ab', 'z')

        # the statements below will evaluate to True
        self.assertEqual(store.get('a', 'aa'), 'y')
        self.assertEqual(store.get_key('a'), [('aa', 'y'), ('ab', 'z')])
        
        # deleting
        store.delete('d', 'df')

        # this will evaluate to True
        self.assertEqual(store.get_key('d'), [('de', 'x')])

        # delete an entire key
        store.delete_key('c')
        
        # this will evaluate to True
        self.assertEqual(store.get_key('c'), [])

    def test_level_2_spec(self):
        """
        The following test runs the exact test commands outlined in the problem specification.
        We include these as a unit test in order to ensure accurate translation of requirements.
        """
        store = self._keycolvalstore_factory()

        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('a', 'ac', 'x')
        store.set('a', 'ad', 'x')
        store.set('a', 'ae', 'x')
        store.set('a', 'af', 'x')
        store.set('a', 'ag', 'x')

        # the following statements will evaluate to True
        self.assertEqual(store.get_slice('a', 'ac', 'ae'), [('ac', 'x'), ('ad', 'x'), ('ae', 'x')])
        self.assertEqual(store.get_slice('a', 'ae', None), [('ae', 'x'), ('af', 'x'), ('ag', 'x')])
        self.assertEqual(store.get_slice('a', None, 'ac'), [('aa', 'x'), ('ab', 'x'), ('ac', 'x')])

