import argparse
import unittest
from module.modules.argument_parser import ArgumentParser


class TestArgumentParser(unittest.TestCase):

    def setUp(self):
        self.arg_parser = ArgumentParser()

    def test_custom_positive_int(self):
        self.assertEqual(self.arg_parser._custom_positive_int("10"), 10)
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_positive_int("-1")
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_positive_int("abc")

    def test_custom_sorting_list(self):
        self.assertEqual(
            self.arg_parser._custom_sorting_list("rating descending"),
            [('rating', 'descending')]
        )
        self.assertEqual(
            self.arg_parser._custom_sorting_list("rating descending, availability ascending"),
            [('rating', 'descending'), ('availability', 'ascending')]
        )
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_sorting_list("invalid ascending")
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_sorting_list("rating invalid")
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_sorting_list("rating descending, invalid ascending")

    def test_custom_filtering_list(self):
        self.assertEqual(
            self.arg_parser._custom_filtering_list("availability < 5"),
            [{'filter_choice': 'availability', 'filter_operator': '<', 'filter_value': '5'}]
        )
        self.assertEqual(
            self.arg_parser._custom_filtering_list("rating >= 4, price = 20"),
            [{'filter_choice': 'rating', 'filter_operator': '>=', 'filter_value': '4'},
             {'filter_choice': 'price', 'filter_operator': '=', 'filter_value': '20'}]
        )
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_filtering_list("invalid_operator < 5")
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_filtering_list("availability < invalid_value")
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser._custom_filtering_list("availability < 5, invalid_filter 10")


if __name__ == "__main__":
    unittest.main()