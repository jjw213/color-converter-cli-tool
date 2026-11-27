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

def hsl_to_rgb(h, s, l):
    """HSL 값을 RGB로 변환합니다."""
    # HSL 값 범위 검증
    if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100):
        raise ValueError("HSL 값은 유효한 범위 내여야 합니다. H: 0-360, S: 0-100, L: 0-100")

    # s와 l을 0-1로 변환
    s_decimal = s / 100.0
    l_decimal = l / 100.0

    # HSL에서 RGB로 변환
    if s_decimal == 0:
        r = g = b = int(l_decimal * 255)
    else:
        hue_2_rgb = lambda p, q, t: p + (q - p) * t if t < 1 else p + (q - p) * (t - 1)
        
        q = l_decimal * (1 + s_decimal) if l_decimal < 0.5 else l_decimal + s_decimal - l_decimal * s_decimal
        p = 2 * l_decimal - q
        
        t_h = h / 360.0
        r = int(255 * hue_2_rgb(p, q, t_h + 1/3))
        g = int(255 * hue_2_rgb(p, q, t_h))
        b = int(255 * hue_2_rgb(p, q, t_h - 1/3))

    return (r, g, b)

def rgb_to_hsl(r, g, b):
    """RGB 값을 HSL로 변환합니다."""
    # RGB 값 범위 검증
    if not all(0 <= x <= 255 for x in [r, g, b]):
        raise ValueError("RGB 값은 0에서 255 사이여야 합니다.")

    # RGB 값을 0-1로 정규화
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    diff = max_val - min_val

    # Luminance (명도)
    l = (max_val + min_val) / 2

    # Saturation (채도)
    if diff == 0:
        s = 0
    else:
        s = diff / (1 - abs(2 * l - 1))

    # Hue (색조)
    if diff == 0:
        h = 0
    elif max_val == r_norm:
        h = (g_norm - b_norm) / diff % 6
    elif max_val == g_norm:
        h = (b_norm - r_norm) / diff + 2
    else:  # max_val == b_norm
        h = (r_norm - g_norm) / diff + 4
    
    h = h * 60  # 각도로 변환

    return (int(h), int(s * 100), int(l * 100))

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
        elif from_format == "hsl" and to_format == "rgb":
            h = int(sys.argv[-3])
            s = int(sys.argv[-2])
            l = int(sys.argv[-1])
            r, g, b = hsl_to_rgb(h, s, l)
            print(f"{r} {g} {b}")
        elif from_format == "rgb" and to_format == "hsl":
            r = int(sys.argv[-3])
            g = int(sys.argv[-2])
            b = int(sys.argv[-1])
            h, s, l = rgb_to_hsl(r, g, b)
            print(f"{h} {s} {l}")
        else:
            print("지원되지 않는 변환 형식입니다.")
            sys.exit(1)
    except (ValueError, IndexError) as e:
        print(f"입력 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()