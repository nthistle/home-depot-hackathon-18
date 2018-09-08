import unittest 

class TestApp(unittest.TestCase): 

  # initialization logic for the test suite declared in the test module
  # code that is executed before all tests in one test run
  @classmethod
  def setUpClass(cls):
       pass 

  # clean up logic for the test suite declared in the test module
  # code that is executed after all tests in one test run
  @classmethod
  def tearDownClass(cls):
       pass 

  # initialization logic
  # code that is executed before each test
  def setUp(self):
    pass 

  # clean up logic
  # code that is executed after each test
  def tearDown(self):
    pass 

  # TEST DECODING BASE64 STRINGS
  def test_decode_base64(self):
    from face_detection import decode_b64

    sample_request = "data:image/png;base64,QUJDREU="
    outString = "ABCDE"
    self.assertEqual(decode_b64(sample_request), outString) 


  # TEST ENCODING PICTURE AS B64 STRING
  def test_encode_base64(self):
    from face_detection import decode_b64

    in_vec = [[255, 255, 135, 1]]

    sample_request = "data:image/png;base64,QUJDREU="
    outString = "ABCDE"
    self.assertEqual(decode_b64(sample_request), outString) 

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()