# pip install prcode
import qrcode
from base64 import b64encode
from random import randrange
import argparse
from PIL import Image

 # Create the parser
parser = argparse.ArgumentParser(prog='qrcode_generator.py', description='QRCode Generator')

# Add the arguments
parser.add_argument('-n', '--number_of_qrs', action='store', help='How much QRs you want to generate?', required=True, type=int)

args = parser.parse_args()

W = 7
H = 5

def generate_id():
    return b64encode(str(randrange(10 ** 5)).encode())

def create_image(n, j):
    size = 290
    page = Image.new('RGB', (W * size + size, H * size + size))

    for i in range(n):
        qr_code = qrcode.make(data=generate_id()).get_image()
        x = int(size * ((i % W) * (1 + 1/(W-1))))
        y = int(size * ((i // W) * (1 + 1/(W-1))))
        page.paste(qr_code, (x, y))
    return page

def main():
    n = int(args.number_of_qrs)
    i = 0
    images = []
    while n > 0:
        current_image = min(H * W, n)
        images.append(create_image(current_image, i))
        n -= current_image
        i += 1
    images[0].save('qrcodes.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=images)

if __name__ == '__main__':
    main()

