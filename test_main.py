import unittest
import sys
from io import StringIO
from main import main, rgb_to_hex, hex_to_rgb, hsl_to_rgb

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

    def test_hex_to_rgb(self):
        # 테스트 케이스: hex 값, 기대하는 (r, g, b) 튜플
        test_cases = [
            ("#000000", (0, 0, 0)),
            ("#ffffff", (255, 255, 255)),
            ("#ff0000", (255, 0, 0)),
            ("#00ff00", (0, 255, 0)),
            ("#0000ff", (0, 0, 255)),
            ("#808080", (128, 128, 128)),
            ("00ff00", (0, 255, 0)), # # 없이 입력해도 됩니다.
        ]

        for hex_value, expected in test_cases:
            with self.subTest(hex_value=hex_value):
                result = hex_to_rgb(hex_value)
                self.assertEqual(result, expected)

    def test_hex_to_rgb_invalid_values(self):
        # 유효하지 않은 HEX 값에 대해 예외를 발생시켜야 합니다.
        with self.assertRaises(ValueError):
            hex_to_rgb("#gg0000")  # 잘못된 HEX 문자
        
        with self.assertRaises(ValueError):
            hex_to_rgb("#ff00")   # 4자리
        
        with self.assertRaises(ValueError):
            hex_to_rgb("#ff00000")  # 8자리

    def test_main_hex_to_rgb_conversion(self):
        # HEX에서 RGB로의 변환 테스트
        original_argv = sys.argv
        try:
            sys.argv = ["main.py", "--from", "hex", "--to", "rgb", "#ff0000"]
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                main()
            except SystemExit:
                pass
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "255 0 0")
        finally:
            sys.argv = original_argv

    def test_hsl_to_rgb(self):
        # 테스트 케이스: (h, s, l), 기대하는 (r, g, b) 튜플
        test_cases = [
            ((0, 0, 0), (0, 0, 0)),     # 검정
            ((0, 0, 100), (255, 255, 255)), # 흰색
            ((0, 100, 50), (255, 0, 0)),   # 빨강
            ((120, 100, 50), (0, 255, 0)), # 녹색
            ((240, 100, 50), (0, 0, 255)), # 파랑
            ((60, 100, 50), (255, 255, 0)), # 노랑
            ((300, 100, 50), (255, 0, 255)), # 마젠타
            ((180, 100, 50), (0, 255, 255)), # 청록
            ((0, 0, 50), (128, 128, 128)),  # 회색
        ]

        for (h, s, l), expected in test_cases:
            with self.subTest(h=h, s=s, l=l):
                result = hsl_to_rgb(h, s, l)
                self.assertEqual(result, expected)

    def test_hsl_to_rgb_invalid_values(self):
        # 유효하지 않은 HSL 값에 대해 예외를 발생시켜야 합니다.
        with self.assertRaises(ValueError):
            hsl_to_rgb(-1, 50, 50)  # h가 범위 밖
        
        with self.assertRaises(ValueError):
            hsl_to_rgb(361, 50, 50)  # h가 범위 밖
        
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, -1, 50)  # s가 범위 밖
        
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 101, 50)  # s가 범위 밖
        
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 50, -1)  # l가 범위 밖
        
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 50, 101)  # l가 범위 밖

    def test_main_hsl_to_rgb_conversion(self):
        # HSL에서 RGB로의 변환 테스트
        original_argv = sys.argv
        try:
            sys.argv = ["main.py", "--from", "hsl", "--to", "rgb", "0", "100", "50"]
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                main()
            except SystemExit:
                pass
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "255 0 0")
        finally:
            sys.argv = original_argv

if __name__ == "__main__":
    unittest.main()