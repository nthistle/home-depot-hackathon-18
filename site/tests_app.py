import unittest 

class TestApp(unittest.TestCase): 

  # # initialization logic for the test suite declared in the test module
  # # code that is executed before all tests in one test run
  # @classmethod
  # def setUpClass(cls):
  #      pass 

  # # clean up logic for the test suite declared in the test module
  # # code that is executed after all tests in one test run
  # @classmethod
  # def tearDownClass(cls):
  #      pass 

  # # initialization logic
  # # code that is executed before each test
  # def setUp(self):
  #   pass 

  # # clean up logic
  # # code that is executed after each test
  # def tearDown(self):
  #   pass 

  # test method
  def test_encode_decode_base64(self):

    from face_detection import image_to_b64, request_to_image

    testString = "data:image/png;base64,QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVoxMjM0NTY3ODkwMDk4NzY1NDMyMSFAIyQl"

    outString = 

    self.assertEqual(2, 2) 

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()