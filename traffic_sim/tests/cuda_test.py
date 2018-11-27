import unittest
from numba import cuda


class TestCuda(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_device(self):
        print cuda.gpus
