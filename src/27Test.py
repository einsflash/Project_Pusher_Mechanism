import unittest
from four_bar_linkage import FourBarLinkage


class TestFourBarLinkage27Cases(unittest.TestCase):

    def check_motion_case(self, T1, T2, T3, T1T2, T1T3, expected_input, expected_output):
        # Set linkage values manually
        linkage = FourBarLinkage(1.0, 1.0, 1.0, 1.0, 45.0, 0.0, 0.5, 0.3, 0.01, 1.0)
        linkage.T1 = T1
        linkage.T2 = T2
        linkage.T3 = T3

        # classification
        linkage.find_Linkage_Type()

        # Assert input and output classifications
        self.assertEqual(linkage.Input_Link_Type, expected_input)
        self.assertEqual(linkage.Output_Link_Type, expected_output)

    # Define separate test methods for each case based on Table 3

    def test_case_1(self):
        # Case 1: T1 > 0, T2 > 0, T3 > 0 -> Crank-Rocker
        self.check_motion_case(1, 1, 1, 1, 1, "crank", "rocker")

    def test_case_2(self):
        # Case 2: T1 = 0, T2 > 0, T3 > 0 -> Crank-π-Rocker
        self.check_motion_case(0, 1, 1, 0, 0, "crank", "π-rocker")

    def test_case_3(self):
        # Case 3: T1 < 0, T2 > 0, T3 > 0 -> π-Rocker-π-Rocker
        self.check_motion_case(-1, 1, 1, -1, -1, "π-rocker", "π-rocker")

    def test_case_4(self):
        # Case 4: T1 > 0, T2 = 0, T3 > 0 -> Crank-0-Rocker
        self.check_motion_case(1, 0, 1, 0, 1, "crank", "0-rocker")

    def test_case_5(self):
        # Case 5: T1 = 0, T2 = 0, T3 > 0 -> Crank-Crank
        self.check_motion_case(0, 0, 1, 0, 0, "crank", "crank")

    def test_case_6(self):
        # Case 6: T1 < 0, T2 = 0, T3 > 0 -> Crank-Crank
        self.check_motion_case(-1, 0, 1, 0, -1, "crank", "crank")

    def test_case_7(self):
        # Case 7: T1 > 0, T2 < 0, T3 > 0 -> π-Rocker-0-Rocker
        self.check_motion_case(1, -1, 1, -1, 1, "π-rocker", "0-rocker")

    def test_case_8(self):
        # Case 8: T1 = 0, T2 < 0, T3 > 0 -> Crank-Crank
        self.check_motion_case(0, -1, 1, 0, 0, "crank", "crank")

    def test_case_9(self):
        # Case 9: T1 < 0, T2 < 0, T3 > 0 -> Crank-Crank
        self.check_motion_case(-1, -1, 1, 1, -1, "crank", "crank")

    def test_case_10(self):
        # Case 10: T1 > 0, T2 > 0, T3 = 0 -> Crank-π-Rocker
        self.check_motion_case(1, 1, 0, 1, 0, "crank", "π-rocker")

    def test_case_11(self):
        # Case 11: T1 = 0, T2 > 0, T3 = 0 -> Crank-π-Rocker
        self.check_motion_case(0, 1, 0, 0, 0, "crank", "π-rocker")

    def test_case_12(self):
        # Case 12: T1 < 0, T2 > 0, T3 = 0 -> π-Rocker-π-Rocker
        self.check_motion_case(-1, 1, 0, -1, 0, "π-rocker", "π-rocker")

    def test_case_13(self):
        # Case 13: T1 > 0, T2 = 0, T3 = 0 -> Crank-Crank
        self.check_motion_case(1, 0, 0, 0, 0, "crank", "crank")

    def test_case_14(self):
        # Case 14: T1 = 0, T2 = 0, T3 = 0 -> Crank-Crank
        self.check_motion_case(0, 0, 0, 0, 0, "crank", "crank")

    def test_case_15(self):
        # Case 15: T1 < 0, T2 = 0, T3 = 0 -> Crank-Crank
        self.check_motion_case(-1, 0, 0, 0, 0, "crank", "crank")

    def test_case_16(self):
        # Case 16: T1 > 0, T2 < 0, T3 = 0 -> π-Rocker-Crank
        self.check_motion_case(1, -1, 0, -1, 0, "π-rocker", "crank")

    def test_case_17(self):
        # Case 17: T1 = 0, T2 < 0, T3 = 0 -> Crank-Crank
        self.check_motion_case(0, -1, 0, 0, 0, "crank", "crank")

    def test_case_18(self):
        # Case 18: T1 < 0, T2 < 0, T3 = 0 -> Crank-Crank
        self.check_motion_case(-1, -1, 0, 1, 0, "crank", "crank")

    def test_case_19(self):
        # Case 19: T1 > 0, T2 > 0, T3 < 0 -> 0-Rocker-π-Rocker
        self.check_motion_case(1, 1, -1, 1, -1, "0-rocker", "π-rocker")

    def test_case_20(self):
        # Case 20: T1 = 0, T2 > 0, T3 < 0 -> 0-Rocker-π-Rocker
        self.check_motion_case(0, 1, -1, 0, 0, "0-rocker", "π-rocker")

    def test_case_21(self):
        # Case 21: T1 < 0, T2 > 0, T3 < 0 -> Rocker-Rocker
        self.check_motion_case(-1, 1, -1, -1, 1, "rocker", "rocker")

    def test_case_22(self):
        # Case 22: T1 > 0, T2 = 0, T3 < 0 -> 0-Rocker-Crank
        self.check_motion_case(1, 0, -1, 0, -1, "0-rocker", "crank")

    def test_case_23(self):
        # Case 23: T1 = 0, T2 = 0, T3 < 0 -> 0-Rocker-Crank
        self.check_motion_case(0, 0, -1, 0, 0, "0-rocker", "crank")

    def test_case_24(self):
        # Case 24: T1 < 0, T2 = 0, T3 < 0 -> 0-Rocker-0-Rocker
        self.check_motion_case(-1, 0, -1, 0, 1, "0-rocker", "0-rocker")

    def test_case_25(self):
        # Case 25: T1 > 0, T2 < 0, T3 < 0 -> Rocker-Crank
        self.check_motion_case(1, -1, -1, -1, 1, "rocker", "crank")

    def test_case_26(self):
        # Case 26: T1 = 0, T2 < 0, T3 < 0 -> 0-Rocker-Crank
        self.check_motion_case(0, -1, -1, 0, 0, "0-rocker", "crank")

    def test_case_27(self):
        # Case 27: T1 < 0, T2 < 0, T3 < 0 -> 0-Rocker-0-Rocker
        self.check_motion_case(-1, -1, -1, 1, 1, "0-rocker", "0-rocker")


if __name__ == '__main__':
    unittest.main()
