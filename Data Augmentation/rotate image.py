import os

from PIL import Image
path= os.path.abspath(".")
extensions= ['JPG']
angle=30
#read the image
##im = Image.open("1.jpg")
##
###rotate image by 90 degrees
##angle = 270
##out = im.rotate(angle, expand=True)
##out.save('rotate-output1.jpg')
if __name__ == "__main__":
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path,f)):
            f_text, f_ext= os.path.splitext(f)
            f_ext= f_ext[1:].upper()
            if f_ext in extensions:
                image = Image.open(os.path.join(path,f))
                width, height= image.size
                print (f, image.size)
                image = image.rotate(angle, expand=True)
                image.save(os.path.join(path,f))
