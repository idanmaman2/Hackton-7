import qrcode
from PIL import Image, ImageDraw, ImageFont
from supabase import create_client, Client 

URL = "https://lifxuidjisbluwwautjd.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh1aWRqaXNibHV3d2F1dGpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE1NDUwNDksImV4cCI6MTk4NzEyMTA0OX0.u0vX3jzEiFoFSoCMGUoPj-oloJAOvUXo_wUEFMB3Zl0"
W = 6 
H = 4
font_path = "/usr/share/fonts/truetype/fonts-yrsa-rasa/Yrsa-SemiBold.ttf"  # for unix
# font_path = "arial.ttf"  # should work for windows

font = ImageFont.truetype(font_path, 48)
text_color = 0

def create_image(ids):
    size = 290
    page = Image.new('RGB', (W * size + size, H * size + size))

    for i in range(len(ids)):
        qr_code = qrcode.make(data=ids[i]).get_image()
        ImageDraw.Draw(qr_code).text((50, 0), ids[i], font=font, fill=text_color)        
        x = int(size * ((i % W) * (1 + 1/(W-1))))
        y = int(size * ((i // W) * (1 + 1/(W-1))))
        page.paste(qr_code, (x, y))
    return page

def main():
    supabase = create_client(URL, KEY)
    ids = [i['id'] for i in supabase.table("patients").select("id").execute().data]

    images = []
    while ids:
        n = min(H * W, len(ids))
        images.append(create_image(ids[:n]))
        ids = ids[n:] 
    images[0].save('qrcodes.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])


if __name__ == '__main__':
    main()

