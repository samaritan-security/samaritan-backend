import unittest

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):
        self.one = get_video_from_file("test_ann.mov")
        self.two = get_video_from_file("test1.jpeg")
        self.employee_dir = "../images/employees"
        self.encoded_encoding = np.array([np.array([-0.07063383, 0.02878015, 0.05416149, -0.10670603, -0.13722023,
                                                    -0.05650453, -0.03629829, -0.05086626, 0.18291645, -0.23563424,
                                                    0.13024117, -0.00359503, -0.13731785, 0.12908527, -0.08619729,
                                                    0.21283808, -0.12906972, -0.17573585, -0.10839737, -0.09430396,
                                                    0.02256017, 0.07462557, -0.03060025, 0.18510376, -0.14298002,
                                                    -0.29697168, -0.01997105, -0.0429626 , -0.01896584, -0.08128347,
                                                    -0.01475876, 0.10289355, -0.21164593, 0.0289116 , 0.03797239,
                                                    0.0823147 , -0.04332963, -0.03347269, 0.2012253 , 0.10708141,
                                                    -0.29046834, 0.05566958, 0.10955733, 0.27149427, 0.12844163,
                                                    -0.02833725, 0.04876959, -0.1034203 , 0.07432768, -0.33201072,
                                                    0.04247754, 0.14000165, -0.01993888, 0.08753159, 0.08294127,
                                                    -0.13576105, 0.04603299, 0.10927497, -0.13324609, 0.09219016,
                                                    0.09935712, -0.02051641, -0.034951  , -0.05556136, 0.23945117,
                                                    0.12930557, -0.1263825 , -0.14319395, 0.13248381, -0.2188347 ,
                                                    -0.10654277, 0.11296161, -0.04500875, -0.15431832, -0.23243541,
                                                    0.00912048, 0.47345614, 0.2435423 , -0.12773702, 0.10140106,
                                                    -0.08210471, -0.04554504, 0.08401806, 0.13095039, -0.04402576,
                                                    0.06041193, 0.00333249, 0.11035658, 0.21155259, 0.11335653,
                                                    -0.01609784, 0.23269477, 0.06295085, -0.00866854, 0.02417279,
                                                    0.07548255, -0.17241934, -0.08638225, -0.18000424, -0.09064093,
                                                    -0.05553617, 0.0424331 , -0.01545827, 0.1409488 , -0.22490998,
                                                    0.25139722, -0.08974768, -0.08836984, -0.01908991, 0.21224216,
                                                    -0.05056393, -0.03638487, 0.04942798, -0.1913013 , 0.11532155,
                                                    0.15028153, 0.07013018, 0.09526444, 0.07928529, 0.03249301,
                                                    0.00280419, -0.02759515, -0.16716257, -0.0818591 , 0.06019405,
                                                    -0.09417901, 0.10270834, 0.00520589])])
        # self.encoded_encoding = pickle.dumps(self.encoded_encoding)
        self.encoded_encoding = self.encoded_encoding.tolist()

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
        self.assertTrue(foo)

if __name__ == '__main__':
    unittest.main()
