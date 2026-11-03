import unittest
import sys
from io import StringIO
from main import main

class TestMain(unittest.TestCase):
    def test_main_prints_help(self):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
        except SystemExit:
            pass
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Color Converter CLI Tool", output)
        self.assertIn("사용 가능한 색상 형식: RGB, HEX, HSL", output)

if __name__ == "__main__":
    unittest.main()