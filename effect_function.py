from PIL import Image, ImageStat, ImageDraw, ImageFont, ImageOps
import matplotlib.pyplot as plt
import numpy as np
from random import randint

Image.MAX_IMAGE_PIXELS = 10**10

def text_render(image,
                x,
                y, 
                text: str| None=None,
                text_size: int | None=200,
                text_font: str | None='fonts/Maji.ttf',
                straz_size: int | None=2,
                sample: int | None=19,
                threshold: int | None=30) -> Image:

    #Константы
    scale=1
    angle=90

    #Открытие изображения
    img=image.copy()
    if text:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(text_font, text_size)
        draw.text((0, 0),text,(0,0,0),font=font)

    #Конвертация изображения в чёрно белое
    img=img.convert('L')
    img=ImageOps.invert(img)
    img=img.point(lambda x: 255 if x > threshold else 0, "1")

    #Перебор пикселей
    channel = img.split()[0]
    channel = channel.rotate(angle, expand=1)
    size = channel.size[0]*scale, channel.size[1]*scale
    coordsx=[]
    coordsy=[]

    bitmap = Image.new('1', size,color='black')
    draw = ImageDraw.Draw(bitmap)
    for x in range(0, channel.size[0], sample):
        for y in range(0, channel.size[1], sample):
            box = channel.crop((x, y, x+sample, y+sample))
            mean = ImageStat.Stat(box).mean[0]
            diameter = (mean/255) ** 0.5
            x_pos, y_pos = (x+box.size[1]/2) * scale, (y+box.size[1]/2) * scale
            box_edge = straz_size
            if mean>5:
                draw.ellipse((x_pos-box_edge, y_pos-box_edge, x_pos+box_edge, y_pos+box_edge),fill=255)
                coordsx.append(x)
                coordsy.append(y)
    bitmap = bitmap.rotate(-angle, expand=1)
    width_half, height_half = bitmap.size
    xx = (width_half - img.size[0]*scale) / 2
    yy = (height_half - img.size[1]*scale) / 2
    bitmap = bitmap.crop((xx, yy, xx + img.size[0]*scale,yy + img.size[1]*scale))
    print((0,max(coordsx),0,max(coordsy)))
    return ImageOps.invert((Image.merge('1', [bitmap]))).crop((0,0,max(coordsy),max(coordsx)+10))

def calligraphy(image: Image,
                min_dot: int | None=1,
                max_dot: int | None=27,
                speed: int | None=100,
                margin: float | None=0.9):
    # read image into numpy array
    img = np.asarray(image)
    # binarize and coarse-graining
    img = (img[::2, ::2, 0] < 128).astype(int)

    def make_dots(
        img, # 2d np array of 1s and 0s
        spd=speed, # speed up factor
        marg=margin, # minimum spacing between dots relative to dot size,
        max_ds=max_dot, # maximum dot diameter in pixels
        min_ds=min_dot, # minimum dot diameter in pixels    
    ):

        # start with blank image
        img2 = np.zeros(img.shape)
        h, w = img.shape

        # keep track of areas occupied by dots
        occ = set()
        
        ofs = int(spd ** 0.5)

        # iterate over dot sizes, decreasing
        for t in np.arange(max_ds, min_ds, -5):
            # iterate over pixels
            for i in range(0, h, ofs):
                for j in range(0, w, ofs):
                    d = 0
                    # increase dot diameter while 1. within bounds, b. corners of bounding box are black and 3. not already occupied
                    while (
                        i + d < h and j + d < w
                    ) and all(
                        [img[i + d, j + d], img[i, j + d], img[i + d, j]]
                    ) and not any(
                        [(i + d1, j + d2) in occ for d1, d2 in [(0, d), (d, 0), (d, d)]]
                    ):
                        d += 1
                    # consider dot only if exceeding threshold
                    if d > t:
                        m = int(marg * d)
                        ci = i + d // 2
                        cj = j + d // 2
                        d2 = (d//2) ** 2
                        # iterate over pixels in bounding box of dot + margin
                        for a in range(i-m, i+d+m):
                            for b in range(j-m, j+d+m):
                                # mark pixel as occupied by dot
                                occ.add((a, b))
                                # if within radius, draw to image
                                if (ci - a) ** 2 + (cj - b) ** 2 < d2:
                                    img2[a, b] = 1
        return img2


    plt.imshow(make_dots(img), cmap='gray_r')
    plt.axis('off')
    idImage=randint(999999999999,9999999999999)
    plt.savefig(f'loggs/{idImage}.jpg')

    threshold=30
    return Image.open(f'loggs/{idImage}.jpg').convert('L').point(lambda x: 255 if x > threshold else 0, "1")

def dot_pattern(path,
                count: int,
                siz: int,
                pas: int,
                shadow: int,
                format_papers: tuple):
    def halftone_child(img, sample, scale,format_paper, angle=90):
        img=img.resize(format_paper)
        img_grey = img.convert('L')  # Convert to greyscale.
        channel = img_grey.split()[0]  # Get grey pixels.
        channel = channel.rotate(angle, expand=1)
        size = channel.size[0]*scale, channel.size[1]*scale

        bitmap = Image.new('RGB', size,color='white')
        #bitmap = bitmap.convert('RGB')
        draw = ImageDraw.Draw(bitmap)
        sizeses=[]
        count_straz=[0,0,0,0,0,0,0]
        for x in range(0, channel.size[0], sample):
            for y in range(0, channel.size[1], sample):
                box = channel.crop((x, y, x+sample, y+sample))
                mean = ImageStat.Stat(box).mean[0]
                diameter = (mean/255) ** 0.5
                edge = 0.5 * (1-diameter)
                x_pos, y_pos = (x+box.size[1]/2) * scale, (y+box.size[1]/2) * scale
                box_edge = (sample * diameter * scale)/2
                sizeses.append(int(box_edge))
                circle_size=pas
                color1 = (143,0,255)
                color2 = (75,0,130)
                color3 = (0,0,255)
                color4 = (0,255,0)
                color5 = (255,255,0)
                color6 = (255,127,0)
                color7 = (255,0,0)
                color=0
                #print(box_edge)
                porog=shadow
                shag=max(sizeses)/5
                if mean<shadow:
                    continue
                if mean>70-pas:
                    box_edge=7
                    straz=5
                    color=color1
                if mean>100-pas:
                    box_edge=8
                    straz=6
                    color=color2
                if mean>130-pas:
                    box_edge=9
                    straz=8
                    color=color3
                if mean>160-pas:
                    box_edge=11
                    straz=10
                    color=color4
                if mean>190-pas:
                    box_edge=12
                    straz=12
                    color=color5
                if mean>220-pas:
                    box_edge=15
                    straz=16
                    color=color6
                if mean>250-pas:
                    box_edge=19
                    straz=20
                    color=color7
                if color==0:
                    continue

                if box_edge==7:
                    count_straz[0]+=1
                elif box_edge==8:
                    count_straz[1]+=1
                elif box_edge==9:
                    count_straz[2]+=1
                elif box_edge==11:
                    count_straz[3]+=1
                elif box_edge==12:
                    count_straz[4]+=1
                elif box_edge==15:
                    count_straz[5]+=1
                elif box_edge==19:
                    count_straz[6]+=1
                draw.ellipse((x_pos-box_edge, y_pos-box_edge, x_pos+box_edge, y_pos+box_edge),
                            fill=color)
                draw.text((x_pos-box.size[1]/5,y_pos-box.size[1]/5),str(straz),fill=(255,255,255))


        print(f'{min(sizeses)} {sum(sizeses)/len(sizeses)} {max(sizeses)}')

        bitmap = bitmap.rotate(-angle, expand=1)
        width_half, height_half = bitmap.size
        xx = (width_half - img.size[0]*scale) / 2
        yy = (height_half - img.size[1]*scale) / 2
        bitmap = bitmap.crop((xx, yy, xx + img.size[0]*scale,
                                      yy + img.size[1]*scale))

        return bitmap
    
    img = path
    img_ht = halftone_child(img, int(count), int(siz),format_papers)
    return img_ht


if __name__=='__main__':
    #calligraphy(Image.open('test_ktext.jpg'))
    #dot_pattern(Image.open('test.png'), 19, 2.8, 30, 20, (3000,1000)).show()
    text_render(Image.open('10.10.10.jpg'),0,0).show()