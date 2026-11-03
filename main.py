import sys

def main():
    print("Color Converter CLI Tool")
    print("사용 가능한 색상 형식: RGB, HEX, HSL")
    print("예시: python main.py --from rgb --to hex 255 0 0")
    sys.exit(1)

if __name__ == "__main__":
    main()