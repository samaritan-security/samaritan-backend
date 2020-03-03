import unittest

from FacialRecog import *


class ScriptTest(unittest.TestCase):

    def test_get_names_and_encodings_from_known(self):
        known_names, known_encodings = get_names_and_encodings_from_known()
        print(known_names)
        print(known_encodings)
        self.assertEqual(len(known_names) > 0, True)

    def test_get_all_people_information(self):
        all_ids, all_encodings = get_all_people_information()
        print(all_ids)
        self.assertEqual(len(all_ids) > 0, True)

if __name__ == '__main__':
    unittest.main()