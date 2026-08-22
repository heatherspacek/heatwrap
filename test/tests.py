import unittest
import heatwrap.scaffolding as scaff


class TestWrApp(unittest.TestCase):
    def test_singleton(self):
        App1 = scaff.WrApp()
        with self.assertRaises(RuntimeError):
            App2 = scaff.WrApp()


if __name__ == "__main__":
    unittest.main()
