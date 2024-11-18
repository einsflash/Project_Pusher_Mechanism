import unittest
from four_bar_linkage import FourBarLinkage

class TestFourBarLinkageCases(unittest.TestCase):

    def setUp(self):
        # Example link lengths and angles; these will be varied to test different cases.
        self.linkage = FourBarLinkage(1.0, 1.0, 1.0, 1.0, 45.0, 0.0, 0.5, 0.3, 0.01, 1.0)

    def test_crank_rocker(self):
        # Case where T1 > 0, T2 > 0, T3 > 0 -> Crank-Rocker
        self.linkage.AB = 2.0
        self.linkage.BC = 3.0
        self.linkage.CD = 2.5
        self.linkage.DA = 1.0
        self.linkage.run()
        self.assertGreater(self.linkage.T1, 0)
        self.assertGreater(self.linkage.T2, 0)
        self.assertGreater(self.linkage.T3, 0)
        print("Crank-Rocker test passed.")

    def test_double_crank(self):
        # Case where T1 > 0, T2 = 0, T3 > 0 -> Double Crank
        self.linkage.AB = 2.5
        self.linkage.BC = 2.5
        self.linkage.CD = 3.0
        self.linkage.DA = 2.0
        self.linkage.run()
        self.assertGreater(self.linkage.T1, 0)
        self.assertEqual(self.linkage.T2, 0)
        self.assertGreater(self.linkage.T3, 0)
        print("Double Crank test passed.")

    def test_double_rocker(self):
        # Case where T1 < 0, T2 < 0, T3 < 0 -> Double Rocker
        self.linkage.AB = 2.25
        self.linkage.BC = 2.25
        self.linkage.CD = 2.25
        self.linkage.DA = 3.25
        self.linkage.run()
        self.assertLess(self.linkage.T1, 0)
        self.assertLess(self.linkage.T2, 0)
        self.assertLess(self.linkage.T3, 0)
        print("Double Rocker test passed.")

    def test_rocker_crank(self):
        # Case where T1 > 0, T2 < 0, T3 < 0 -> Rocker-Crank
        self.linkage.AB = 2.75
        self.linkage.BC = 1.75
        self.linkage.CD = 2.75
        self.linkage.DA = 2.75
        self.linkage.run()
        self.assertGreater(self.linkage.T1, 0)
        self.assertLess(self.linkage.T2, 0)
        self.assertLess(self.linkage.T3, 0)
        print("Rocker-Crank test passed.")

if __name__ == '__main__':
    unittest.main()

