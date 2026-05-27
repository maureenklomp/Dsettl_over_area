import unittest
from app import get_filter_list  # Adjust the import based on your project structure

class TestGetLocationIDs(unittest.TestCase):

    def test_get_location_IDs(self):
        input_csv = "test_data/Locations.csv"
        expected_output = ["LOC001", "LOC002", "LOC003", "LOC004", "LOC005"]  # Replace with actual expected output
        
        # Your test code here
        self.assertEqual(get_filter_list(input_csv), expected_output)

if __name__ == '__main__':
    unittest.main()