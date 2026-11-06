import sys
import re

def rgb_to_hex(r, g, b):
    """RGB 값을 HEX로 변환합니다."""
    if not all(0 <= x <= 255 for x in [r, g, b]):
        raise ValueError("RGB 값은 0에서 255 사이여야 합니다.")
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_value):
    """HEX 값을 RGB로 변환합니다."""
    # HEX 값이 #으로 시작하지 않으면 추가
    if not hex_value.startswith('#'):
        hex_value = '#' + hex_value

    # 6자리 HEX 값인지 확인
    if len(hex_value) != 7:
        raise ValueError("HEX 값은 6자리여야 합니다.")

    try:
        r = int(hex_value[1:3], 16)
        g = int(hex_value[3:5], 16)
        b = int(hex_value[5:7], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError("유효하지 않은 HEX 값입니다.")

def main():
    if len(sys.argv) < 2:
        print("Color Converter CLI Tool")
        print("사용 가능한 색상 형식: RGB, HEX, HSL")
        print("예시: python main.py --from rgb --to hex 255 0 0")
        sys.exit(1)

    try:
        from_format = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None
        to_format = sys.argv[sys.argv.index("--to") + 1] if "--to" in sys.argv else None

        if from_format == "rgb" and to_format == "hex":
            r = int(sys.argv[-3])
            g = int(sys.argv[-2])
            b = int(sys.argv[-1])
            hex_value = rgb_to_hex(r, g, b)
            print(hex_value)
        elif from_format == "hex" and to_format == "rgb":
            hex_value = sys.argv[-1]
            r, g, b = hex_to_rgb(hex_value)
            print(f"{r} {g} {b}")
        else:
            print("지원되지 않는 변환 형식입니다.")
            sys.exit(1)
    except (ValueError, IndexError) as e:
        print(f"입력 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()