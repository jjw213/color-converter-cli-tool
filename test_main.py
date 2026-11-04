import unittest
import sys
from io import StringIO
from main import main, rgb_to_hex

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

    def test_rgb_to_hex(self):
        # 테스트 케이스: (r, g, b), 기대하는 hex 값
        test_cases = [
            ((0, 0, 0), "#000000"),
            ((255, 255, 255), "#ffffff"),
            ((255, 0, 0), "#ff0000"),
            ((0, 255, 0), "#00ff00"),
            ((0, 0, 255), "#0000ff"),
            ((128, 128, 128), "#808080"),
        ]

        for (r, g, b), expected in test_cases:
            with self.subTest(r=r, g=g, b=b):
                result = rgb_to_hex(r, g, b)
                self.assertEqual(result, expected)

    def test_rgb_to_hex_invalid_values(self):
        # 유효하지 않은 RGB 값에 대해 예외를 발생시켜야 합니다.
        with self.assertRaises(ValueError):
            rgb_to_hex(-1, 0, 0)
        
        with self.assertRaises(ValueError):
            rgb_to_hex(0, 256, 0)

    def test_main_rgb_to_hex_conversion(self):
        # RGB에서 HEX로의 변환 테스트
        original_argv = sys.argv
        try:
            sys.argv = ["main.py", "--from", "rgb", "--to", "hex", "255", "0", "0"]
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                main()
            except SystemExit:
                pass
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "#ff0000")
        finally:
            sys.argv = original_argv

    def test_main_invalid_conversion(self):
        # 지원되지 않는 변환 형식 테스트
        original_argv = sys.argv
        try:
            sys.argv = ["main.py", "--from", "rgb", "--to", "hsl"]
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                main()
            except SystemExit:
                pass
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue().strip()
            self.assertIn("지원되지 않는 변환 형식입니다.", output)
        finally:
            sys.argv = original_argv

if __name__ == "__main__":
    unittest.main()