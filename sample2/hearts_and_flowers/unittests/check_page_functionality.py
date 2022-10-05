import unittest
from financial_concern.hearts_and_flowers import MyPage


class MyTestCase(unittest.TestCase):
    def testListGeneration(self):
        # generate a list of h with 10 elements and print it and see if it is correct
        list1 = MyPage.generate_image_list(10, True, False, False)
        print(list1)
        self.assertEqual(list1, ['h'] * 10)

        # generate a list of f with 10 elements and print it and see if it is correct
        list2 = MyPage.generate_image_list(10, False, True, False)
        print(list2)
        self.assertEqual(list2, ['f'] * 10)

        # generate half h and half f with 10 elements
        list3 = MyPage.generate_image_list(10, False, False, True)
        print("half and half", list3)
        self.assertEqual(len(list3), 10)

        # generate a list of h and f with 10 elements
        list4 = MyPage.generate_image_list(30, False, False, False)
        print("totally randomized", list4)
        self.assertEqual(len(list4), 30)


if __name__ == '__main__':
    unittest.main()
