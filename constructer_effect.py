import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import numpy as np
from effect_function import text_render
import threading

PIXEL=37
size_st={
    'ss5':7,
    'ss6':8,
    'ss8':9,
    'ss10':11,
    'ss12':12,
    'ss16':15,
    'ss20':20
}

class ConstructProgect:
    def __init__(self, width: int, height: int, userIP: str) -> None:
        self.size_real={
            'ширина': width,
            'высота': height
        }
        self.size={
            'ширина': (width*PIXEL)*2,
            'высота': (height*PIXEL)*2
        }

        self.objects=[]
        self.lays={}

        #Создание белой подложки
        img=np.zeros([100,100,3],dtype=np.uint8)
        img.fill(255)
        plt.imshow(img, cmap='gray_r')
        plt.axis('off')
        plt.savefig(f'static/projects/{userIP}.jpg')

        #Идентификация и изменение её размеров
        self.image=Image.open(f'static/projects/{userIP}.jpg').resize((self.size['ширина'], self.size['высота']))
        self.image.save(f'static/projects/{userIP}.jpg')
        self.lays['0']='Основной слой'

    def AppendObjectText(self,
                        x_pos: int | None=0,
                        y_pos: int | None=0,
                        text: str | None='Text',
                        font_size: int | None=500,
                        font: str | None='fonts/Maji.ttf',
                        straz_size: int | None=2,
                        sample: int | None=13
    ):  
        img=text_render(self.image, x_pos, y_pos, text, font_size, font, straz_size, sample)
        self.objects.append([img, 'TEXT', (x_pos, y_pos)])
        self.lays[f'{max([int(x) for x in self.lays])+1}']='Шрифт слой'

    def EditObjects(self,
                    index: int,
                    effect: str,
                    params: tuple
    ):
        match effect:
            case 'TEXT':
                self.objects[index][0]=text_render(*params)
            case _:
                pass

    def DeleteEffect(self, ids):
        print(ids)
        print(self.objects[ids-1])
        del self.objects[ids-1]

    def GetFullLayout(self, userIP):
        img=self.image.copy()
        for obj in self.objects:
            img.paste(obj[0], obj[2])
        img.save(f'static/projects/{userIP}.jpg')
    


if __name__=='__main__':
    a=ConstructProgect(21,29,'10.10.10')
    a.AppendObjectText(x_pos=0, y_pos=200, text='Hello teacherrsss', straz_size=20, sample=40, font_size=500)
    a.GetFullLayout(234833)