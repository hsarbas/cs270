import unittest
import weakref
from app.model.infra.node import Node


class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_node(self):
        node = Node(0, 100, 'src')

        self.assertEqual(node.x, 0, 'incorrect x')
        self.assertEqual(node.y, 100, 'incorrect y')
        self.assertEqual(node.dir_, 'src', 'incorrect dir')
