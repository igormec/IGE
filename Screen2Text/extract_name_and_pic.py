import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import ndimage as ndi
from PIL import Image as pil

from skimage import data
from skimage.measure import structural_similarity as ssim
from skimage.filters import threshold_otsu, gaussian
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb
from skimage.segmentation import random_walker
from skimage.data import binary_blobs
from skimage.transform import rescale

import skimage as sk
import sys
import pytesseract
from PIL import ImageChops
from math import ceil


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


#trim method takes out white borders on top and bottom of image
def trim(im):
    bg = pil.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def allRegions(regions, im=None, draw=False, drawAll=False):

    #draw makes box around name and pic
    #drawAll makes box around all found regions
    #both false = return name and pic regions
    if draw or drawAll:
        fig, ax = plt.subplots(ncols=1, nrows=1)
        ax.imshow(im, cmap='gray', interpolation='nearest')

    nameRegs=[]
    for reg in regions:
        minr, minc, maxr, maxc = reg.bbox

        #Expand region a little bit. Avoids text pixel clipping
        minr -= 1
        minc -= 1
        maxr += 2
        maxc += 5

        #Scale region by 4 (original image downsized by 4)
        minr *= 4
        minc *= 4
        maxr *= 4
        maxc *= 4

        blen = maxc - minc
        bhigh = maxr - minr

        #drawAll switch draws all regions, exits
        if drawAll:
            print(str(minr)+ ', '+str(minc)+ ', '+str(maxr)+ ', '+str(maxc))
            print('Dim: ' + str(blen) + ' x ' + str(bhigh))
            rect = mpatches.Rectangle((minc,minr), blen, bhigh, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
        else:
            #This will find the the name region (will be long and not very tall
            if bhigh >= 45 and bhigh <=100 and blen >=150 and blen <= 450 and regions.index(reg) < 10:
                nameRegs.append(reg)
                if draw:
                    rect = mpatches.Rectangle((minc,minr), blen, bhigh, fill=False, edgecolor='red', linewidth=2)
                    ax.add_patch(rect)
            #This will find the picture region
            #TODO - Images could be shorter than 750
            if blen >= 750 and bhigh >= 750:
                picReg = reg
                if draw:
                    rect = mpatches.Rectangle((minc,minr), blen, bhigh, fill=False, edgecolor='red', linewidth=2)
                    ax.add_patch(rect)
  
    if drawAll or draw:
        plt.show()
        sys.exit(0)
        
    return nameRegs[0], picReg



def check_SSIM(img1, img2):

    im1 = ndi.imread(img1, flatten=True)
    im2 = ndi.imread(img2, flatten=True)

    #Convert from float(0.0 - 255.0) to float(0.0 - 1.0)
    im1 = im1/255
    im1 = sk.img_as_float(im1)

    #Convert from float(0.0 - 255.0) to float(0.0 - 1.0)
    im2 = im2/255
    im2 = sk.img_as_float(im2)

#================MAIN==================#

def getNameAndPic(src='', dest='', savePic=False, saveAll=False, drawAll=False):
    
    try:
        if src == '':
            print('No image given.')
            return None
        
        im = ndi.imread(src, flatten=True)

        #Convert from float(0.0 - 255.0) to float(0.0 - 1.0)
        im = im/255
        im = sk.img_as_float(im)

        #Downsize to reduce number of pixels (helps gaussian + otsu)
        ims = rescale(im, 0.5)
        ims = rescale(ims, 0.5)
        
        #Otsu, blur to spread pixels, otsu once more to create larger 'blobs'
        imss = ims > 0.85
        imss = gaussian(imss, 2)
        imss = imss > 0.85

        #Create and store all regions of black
        labelImage = label(imss, connectivity=2, background=1)
        regions = regionprops(labelImage)

        #Extract name and picture regions
        if drawAll == True:
            nameRegion, picRegion = allRegions(regions, im=im, drawAll=True)
        else:
            nameRegion, picRegion = allRegions(regions)
        nameRegion = nameRegion.bbox
        picRegion = picRegion.bbox

        #Regions' bbox is ((y,x)(y,x)). Switch to ((x,y)(x,y)).*4 to resize bbox to proper resolution
        nameRegion = (nameRegion[1]*4,nameRegion[0]*4,nameRegion[3]*4,nameRegion[2]*4)
        picRegion = (picRegion[1]*4,picRegion[0]*4,picRegion[3]*4,picRegion[2]*4)

        #Open and crop out name and pic as new images
        toCrop = pil.open(src)
        name = toCrop.crop(nameRegion)
        pic = toCrop.crop(picRegion)
        picNoBord = trim(pic)

        #Calculate new icon resolution and make icon
        iconW, iconH = picNoBord.size
        iconH = ceil(iconH/9)
        iconW = ceil(iconW/9)
        picIcon = picNoBord.resize((iconW,iconH), pil.ANTIALIAS)
        
        #saves picture, name image and icon
        if savePic or saveAll:
            if dest == '':
                print('Cannot save without destination directory')
            else:
                picFile = dest + 'Pic - ' + src.split('\\')[-1]
                picNoBord.save(picFile)
                if saveAll:
                    nameFile = dest + 'Name - ' + src.split('\\')[-1]
                    name.save(nameFile)
                    picIcon.save(dest + 'Icon - ' + src.split('\\')[-1])

        #OCR will parse name image and return name string 
        nametxt = pytesseract.image_to_string(name)
        nametxt = nametxt.replace('|','l')
        nametxt = nametxt.split('\n')[0]
        print(nametxt)
        return ([nametxt,picIcon])
        
    except Exception as e:
        print('Error ocurred: %s' %e)
        return None
        

#======================================#

if __name__ == '__main__':

    #src = 'C:\\Users\\Igor\\Desktop\\sc.png'
    #dest = 'C:\\Users\\Igor\\Desktop\\'
    #namet, pic = getNameAndPic(src, dest, saveAll=True)
    print('hello')

'''
-----PLAN-----

X - extract from screenshot: name and picture regions
X - bounding box coords serve as crop markers for pic and name
X - crop the name out of the screenshot (will only work for one format of screenshot)
X - crop the pic out of the screenshot
X - if there is a location in name, divide further (OCR will divide separate lines with \n)
X - convert the name to text using OCR
X - downsize image to smaller resolution (get icon size of insta pics)

 - make above work for all formats
 - top bar to be cropped (wifi, time etc)

 - Visit profile using name
 - Get date modified of original pic
 - Go down insta profile until reaching date
 - Search +/- several days, comparing thumbnails
 - if not found with date method, keep going until end of pics
 - if not found again, throw error
 - if found, collect all data and store in a database

--------------
'''
