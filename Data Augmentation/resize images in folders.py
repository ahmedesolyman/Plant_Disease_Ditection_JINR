
import cv2
import os
from PIL import Image
resize_method = Image.ANTIALIAS
    #Image.NEAREST)  # use nearest neighbour
    #Image.BILINEAR) # linear interpolation in a 2x2 environment
    #Image.BICUBIC) # cubic spline interpolation in a 4x4 environment
    #Image.ANTIALIAS) # best down-sizing filter


max_height= 256
max_width= 256
extensions= ['JPG']

path= os.path.abspath(".")

def adjusted_size(width,height):
    if width>max_width or height>max_height:
        if width>height:
            return max_width, int (max_width * height/ width)
        else:
            return int (max_height*width/height), max_height
    else:
        return width,height

	
if __name__ == "__main__":
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path,f)):
            f_text, f_ext= os.path.splitext(f)
            f_ext= f_ext[1:].upper()
            if f_ext in extensions:
                image = Image.open(os.path.join(path,f))
                width, height= image.size
                print (f, image.size)
                image = image.resize(adjusted_size(width, height))
                if image.size==(256,256):
                    print("Ok")
                if image.size!=(256,256):
                    print("Nooooooo, Please adjust me")
                image.save(os.path.join(path,f))


if __name__ == "__main__":
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path,f)):
            f_text, f_ext= os.path.splitext(f)
            f_ext= f_ext[1:].upper()
            if f_ext in extensions:
                image = Image.open(os.path.join(path,f))
                w, h= image.size[:2]
                center = (w / 2, h / 2)
                scale = 1.0
                M = cv2.getRotationMatrix2D(center, 90, scale)
                rotated90 = cv2.warpAffine(image, M, (h, w))
                cv2.imshow('Image rotated by 90 degrees',rotated90)
                image.save(os.path.join(path,f))

