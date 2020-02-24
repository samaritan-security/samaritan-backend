import unittest

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):
        self.encoded_encoding = "k05VTVBZAQB2AHsnZGVzY3InOiAnPGY4JywgJ2ZvcnRyYW5fb3JkZXInOiBGYWxzZSwgJ3NoYXBlJzogKDEyOCwpLCB9ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAoAAAAAtqWBPwAAAMDqDb0/AAAAYM0Iiz8AAABgahCFvwAAAKCjGby/AAAAACTicj8AAACARNijvwAAAADmYMG/AAAAIOzDuT8AAABAcF/AvwAAAEAlys8/AAAAAEpPej8AAABAT0vKvwAAAAAE7Yk/AAAAAM/klD8AAADACvO2PwAAAKBoibe/AAAAAOLwqr8AAAAAZ9bCvwAAAADW2rW/AAAAAGT7X78AAACgcFLAPwAAAGCpHqw/AAAAwICitz8AAABgIhC6vwAAAOCdDda/AAAAICBNu78AAAAAyGJdPwAAAMDjuLg/AAAAwI4xub8AAABAHZyqvwAAAOCjMKe/AAAAIBNfwb8AAADAj02VvwAAAABqV4w/AAAAALxPlz8AAAAA9+7HvwAAAMBZCMC/AAAAwJf8yD8AAACgg0umPwAAAMCF9sC/AAAAAKtHrj8AAAAA9xqUPwAAAGD+tdI/AAAAQHwewz8AAAAg6jabPwAAAIBR3Lg/AAAAAFKzwr8AAAAA9gSvPwAAAECm8sq/AAAAgMz4tj8AAAAgGri9PwAAAIDxcLE/AAAA4Plluz8AAAAA/0iuPwAAAEA57cC/AAAAAPc4pb8AAAAAJa/BPwAAAECTBce/AAAAYDJlsz8AAACAX3alPwAAAADEqWy/AAAAALN/aD8AAABA86qzvwAAAGDtts4/AAAAoJxKxD8AAAAgEq60vwAAAGD7i8O/AAAAgFwmwj8AAABAc83LvwAAAKDujrm/AAAAgPReqT8AAACAEGGkvwAAAMAMKcu/AAAA4CiQyL8AAACAhHWoPwAAAID/ktg/AAAAQJFixz8AAACA3sHCvwAAAEBT2Zc/AAAAgE2utL8AAACAv9iovwAAAEBxIL4/AAAAACNClD8AAAAA/vKyvwAAAAAHdZy/AAAAgHKcsb8AAAAAvLO6PwAAAKBeUtA/AAAAQDcvrb8AAACAxX+uvwAAAKCcNdA/AAAAAD/Dsj8AAAAA8H1mPwAAAOA0QL4/AAAAAMXOrT8AAABgyNfAvwAAAEBQWbA/AAAAoOpau78AAACAWkyePwAAAIA0Tao/AAAAwHqqvL8AAAAAq46zPwAAAEA3T6Y/AAAAAFvPxL8AAAAgFJzTPwAAAIC4WKE/AAAAAKg0ob8AAAAAnM24PwAAAADmPKw/AAAAwIPDx78AAAAAPyGuvwAAAEBrN8c/AAAAwOi81L8AAABAwm/PPwAAAEC6XL4/AAAAwNMDsz8AAAAApE/KPwAAAICPpqU/AAAAQOYBwT8AAAAAmIVrvwAAAACe8qO/AAAAoA4Owb8AAADAcGCxvwAAACBZC6g/AAAAAI//gr8AAACAIk20PwAAAACSdbA/"
        self.one = get_video_from_file("test_ann.mov")
        self.two = get_video_from_file("test1.jpeg")
        self.employee_dir = "../images/employees"
        pass

    # all tests must start with "test"
    def test_headless_encoding_one(self):
        encodings = process_video_to_encode(self.one, self.employee_dir, "../images/temp.jpeg")
        # asserts true that the video was able to find Ann and ONLY ann
        # this looks a bit gross
        same = [[[False]], [[False]], [[False]], [[True]]]
        self.assertEqual(encodings[0], same)

    # this doesn't work yet
    def test_encodings_from_db(self):
        foo = scan_for_known_people_from_db(self.encoded_encoding)

if __name__ == '__main__':
    unittest.main()
