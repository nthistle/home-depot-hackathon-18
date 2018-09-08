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
    from face_detection import image_to_b64
    import numpy as np

    in_vec = np.array([[1, 0],
                      [0, 1]])

    outString = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAAAAABX3VL4AAAADklEQVQIHWNk/M/IwAgABBEBBJhoyrMAAAAASUVORK5CYII="
    self.assertEqual(image_to_b64(in_vec), outString)

  
  def test_normalize_distance(self):
    from normalize import find_distance
    self.assertEqual(find_distance((-2, 2), (4, 2)), 6)
  
  def test_normalize_mid(self):
    from normalize import find_mid
    self.assertEqual(find_mid((-2, 2), (4, 2)), (1,2))
  
  def test_normalize_scale(self): #scales two points about their midpoint
    from normalize import scale
    self.assertEqual(scale(2.4, (64, 34), (36, 34)), ((83, 34), (16, 34)))
  

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()