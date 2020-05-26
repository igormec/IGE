'''
-----PLAN-----

X - extract from screenshot: name and picture regions
X - bounding box coords serve as crop markers for pic and name
X - crop the name out of the screenshot (will only work for one format of screenshot)
X - crop the pic out of the screenshot
X - if there is a location in name, divide further (OCR will divide separate lines with \n)
X - convert the name to text using OCR
X - downsize image to smaller resolution (get icon size of insta pics)

X - make above work for all formats
X - top bar to be cropped (wifi, time etc)

 - Visit profile using name
 - Get date modified of original pic
 - Go down insta profile until reaching date
 - Search +/- several days, comparing thumbnails
 - if not found with date method, keep going until end of pics
 - if not found again, throw error
 - if found, collect all data and store in a database


5/25/2020 PLAN
 - Determine if image is instagram screenshot
 - get name from screenshot
 - place in folder of that same name
 
--------------
'''

import warnings
import sys, os, time, shutil, threading, pprint
import numpy as np                                  #https://docs.scipy.org/doc/numpy-1.11.0/reference/
from math import ceil
from scipy import ndimage as ndi                    #https://docs.scipy.org/doc/scipy-0.19.0/reference/ndimage.html

import matplotlib.pyplot as plt                     #https://matplotlib.org/3.2.1/api/pyplot_summary.html
import matplotlib.patches as mpatches               #https://matplotlib.org/3.2.1/api/patches_api.html

from PIL import Image as pil                        #- Python Imaging Library
from PIL import ImageChops                          #http://omz-software.com/pythonista/docs/ios/ImageChops.html

import skimage as sk                                #https://scikit-image.org/docs/0.11.x/api/api.html
from skimage.measure import compare_ssim as ssim
from skimage.filters import gaussian
from skimage.measure import label
from skimage.measure import regionprops
from skimage.transform import rescale, resize

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#trim method takes out white borders on top and bottom of passed in image
#returns the cropped version of the image
def trim(img, showSteps=False, returnArr=False):

    #convert from float32 ndarray to uint8 ndarray to PIL Image
    if type(img) == np.ndarray:
        img = pil.fromarray(np.uint8(img))

    #open image as PIL Image if img is a path string
    elif type(img) == type('abc'):
        im = pil.open(img)
        if showSteps:
            show(img)

    #bg is an image of the same size as img but in one colour,
    #using the top-left pixel of img as the background colour
    bg = pil.new(img.mode, img.size, img.getpixel((0,0)))

    #diff will be a darkened version of the image on a black background.
    #bbox is the bounding box of all non-background-coloured pixels
    #crop image using bbox and return ndarray of cropped image
    diff = ImageChops.difference(img, bg)
    if showSteps:
        show(diff)
    diff = ImageChops.add(diff, diff, 2.0, -50)
    if showSteps:
        show(diff)
    bbox = diff.getbbox()
    if bbox:
        if showSteps:
            show(img.crop(bbox))
        #.covert('L') - coverting to a greyscale image
        return np.array(img.crop(bbox).convert('L')) if returnArr else img.crop(bbox)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#show function will display the image array passed to it in greyscale
def show(im, flat=True):
    plt.clf() #Clear current figure
    plt.imshow(readImage(im, greyscale=flat), cmap='gray', interpolation='nearest') #Display data as image
    plt.show() #Display the data


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#thresh_otsu method takes an ndarray image (pic) and returns binary image array where
#all pixels above thresh value are white and below/equal to thresh are black
def thresh_otsu(pic, thresh):
    pic = pic > thresh          #iterates through every value, sets it to True/False (ndarray now all bools)
    pic = sk.img_as_ubyte(pic)  #converts bool values to 0 or 255.
    return pic                  #return ndarray of binary image


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#readImage returns 
#img - string path of image or image object (ndarray)
#greyscale - If True, flattens the color layers into a single gray-scale layer.
#returns an ndarray of the image:
#   3D array if colour, [height/rows][width][R,G,B(ints)]
#   2D array if greyscale [height/rows][width(floats)]

#ndi.imread ndarray image returns:
#   JPEG, coloured - uint8 (int 0-255)
#   JPEG, greyscale - float32 (0.00000000-1.00000000)
#   PNG, coloured - uint8 (int 0-255)
#   PNG, greyscale - float32 (0.00000000-1.00000000)
def readImage(img, greyscale=True):
    try:
        return ndi.imread(img, flatten=greyscale) if type(img) == type('str') else img
    except Exception as e:
        print('readImage Error: %s' %e)
        return None

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#makes a folder in the path directory if one doesn't already exist
def makeFolder(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path+'\\'


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#this function takes all the folder names that have been read and finds the most
#common strings of different lengths, then displays the strings in order
def collect_terms():
    allNames = 'D:\\Screenshots - Copy\\IG\\filtered\\NONE\\'
    allNames = os.listdir(allNames)
    allNames = ' '.join(allNames)

    terms = []
    termTups = []
    
    for termLen in range(10,2,-1):
        terms = []
        termTups = []
        print('\n\n--------------------LENGTH:'+str(termLen)+'------------------------\n')
        for sub in range((len(allNames)-termLen)+1):
            term = allNames[sub:sub+termLen]
            if term not in terms:
                terms.append(term)
                termTups.append((term,1))
            else:
                for x in range(len(termTups)):
                    if (termTups[x])[0] == term:
                        termTups[x] = (term, (termTups[x])[1]+1)
                        break
    
        newSort = sorted(termTups, key=lambda tup: tup[1], reverse=True)
        newSort = newSort[:75]
        pprint.pprint(newSort)
    
                
    



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def filter_db():

    terms = {}
    terms['dogs'] = ['dog', 'pup', 'canine']
    terms['golden'] = ['gold', 'retriev']
    terms['lab'] = ['lab', 'choc']
    terms['bulldog'] = ['bull','english', 'bulldog', 'bully', 'bullie', 'french', 'wrink', 'wrinck']
    terms['corgi'] = ['corgi', 'corg']
    terms['husky'] = ['husk']
    terms['shiba'] = ['shiba', 'inu']
    terms['bernese'] = ['bern']

    terms['cats'] = ['cat']
    
    terms['props'] = ['arch', 'tecture','lux', 'listing', 'home', 'house', 'room']
    
    terms['photog'] = ['photog', 'travel', 'visu']
    
    terms['cars'] = ['car', 'auto', 'perform']
    terms['audi'] = ['audi', 'quattro']
    terms['bmw'] = ['bmw', 'm3', 'm6']
    terms['camaro'] = ['camaro', 'chev']
    
    terms['cities'] = ['t.o', 'york', 'toro', '6ix', 'six']

    '''
    terms[''] =
    terms[''] =
    terms[''] =
    terms[''] =
    terms[''] =
    terms[''] =

    '''
    
    src = 'E:\\Sample\\Screenshots\\Sort\\'
    dest = 'E:\\Sample\\((CATEGORIZED))\\'
    #src = dest+'NONE\\'
    
    anyFunc = lambda folder,terms : any(i in folder for i in terms)
    
    dirs = os.listdir(src)
    for folderName in dirs:
        #-------------------------DOGS-------------------------
        #Dogs
        dogs = makeFolder(dest+'Dogs')
        
            #Golden
        golden = makeFolder(dogs+'Golden') 
        if anyFunc(folderName,terms['golden']):
            shutil.move(src+folderName,golden)
            continue
        
            #Labs
        lab = makeFolder(dogs+'Lab')
        if anyFunc(folderName,terms['lab']):
            shutil.move(src+folderName,lab)
            continue
                      
            #Bulldog
        bulldog = makeFolder(dogs+'Bulldog')
        if anyFunc(folderName,terms['bulldog']):
            shutil.move(src+folderName,bulldog)
            continue
                       
            #Corgi
        corgi = makeFolder(dogs+'Corgi')
        if anyFunc(folderName,terms['corgi']):
            shutil.move(src+folderName,corgi)
            continue
                       
            #Husky
        husky = makeFolder(dogs+'Husky')
        if anyFunc(folderName,terms['husky']):
            shutil.move(src+folderName,husky)
            continue

            #Shiba
        shiba = makeFolder(dogs+'Shiba')
        if anyFunc(folderName,terms['shiba']):
            shutil.move(src+folderName,shiba)
            continue

            #Bernese
        bernese = makeFolder(dogs+'Bernese')
        if anyFunc(folderName,terms['bernese']):
            shutil.move(src+folderName,bernese)
            continue
        

        if anyFunc(folderName,terms['dogs']):
            shutil.move(src+folderName,makeFolder(dogs+'Other'))
            continue

        #-------------------------CATS-------------------------
        cats = makeFolder(dest+'Cats')
        if anyFunc(folderName, terms['cats']):
            shutil.move(src+folderName, cats)
            continue


        #-------------------------PROPERTIES-------------------------
        #Properties
        props = makeFolder(dest+'Properties')
        if anyFunc(folderName,terms['props']):
            shutil.move(src+folderName,props)
            continue


        #-------------------------PHOTOGRAPHY-------------------------
        #Photography
        photog = makeFolder(dest+'Photography')
        if anyFunc(folderName,terms['photog']):
            shutil.move(src+folderName,photog)
            continue

        
        #-------------------------CARS-------------------------
        #Cars
        cars = makeFolder(dest+'Cars')

            #Audi
        audi = makeFolder(cars+'Audi')
        if anyFunc(folderName,terms['audi']):
            shutil.move(src+folderName,audi)
            continue

            #BMW
        bmw = makeFolder(cars+'BMW')
        if anyFunc(folderName,terms['bmw']):
            shutil.move(src+folderName,bmw)
            continue

            #Camaro
        camaro = makeFolder(cars+'Camaro')
        if anyFunc(folderName,terms['camaro']):
            shutil.move(src+folderName,camaro)
            continue

            #MISC
        if anyFunc(folderName,terms['cars']):
            shutil.move(src+folderName,makeFolder(cars+'Other'))
            continue

        
        #-------------------------CITIES-------------------------
        #Cities
        cities = makeFolder(dest+'Cities')
        if anyFunc(folderName,terms['cities']):
            shutil.move(src+folderName,cities)
            continue


        if not os.path.isdir(dest+'NONE\\'+folderName):
            shutil.move(src+folderName, makeFolder(dest+'NONE'))


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def sort_by_name(src='', dest='', named=False):
    unreadNames = 'E:\\Sample\\Sample\\Sort\\((Not Read))\\' 
    allPics = os.listdir(src)
    startTime = int(time.time())
    nowTime = int(time.time())
    endTime = int(time.time())
    remaining = 0
    remainMin = 0
    remainSec = 0
    
    print('Processed: 0 out of '+ str(len(allPics)))
    
    for x, p in enumerate(allPics):
        #print('-----------------------------')
        try:
            name = get_name(src+p)
            
            if name == '':
                name = '((ERROR))'

            if not os.path.isdir(dest+name):
                os.makedirs(dest+name)
                
            shutil.copy(src+p, dest+name+'\\'+p)

        except UnicodeDecodeError as e:
            print("Can't read!")
            namepic = get_name(src+p, returnStr=False, returnPNG=True)
            d = unreadNames
            
            if len(os.listdir(d)) > 0:
                flag = True
                for nn in os.listdir(d):
                    i1 = readImage(d+nn)
                    i2 = np.array(namepic.convert('L'))
                    
                    i1 = trim(i1, returnArr=True)
                    i2 = trim(i2, returnArr=True)

                    if i2.shape != i1.shape:
                        i2 = resize(i2,i1.shape)*255
                    
                    ss = get_ssim(i1, i2)
                    #print('SSIM: '+str(ss)+'\twith: '+nn)
                    if ss > 0.885:
                        if named:
                            unnamed = dest+('.'.join(nn.split('.')[:-1]))
                            if not os.path.isdir(unnamed):
                                os.makedirs(unnamed)
                            shutil.copy(src+p, unnamed+'\\'+p)
                        #print(nn+" is already here! SSIM: "+str(ss))
                        flag = False
                        break
                    
                
            if (len(os.listdir(d)) < 1 or ss <= 0.885) and not named:
                nameInput = (str(x)+' - '+str(int(time.time())))
                namepic.save(d+nameInput+'.png')
                #print('Not here. Saved '+nameInput+'\nCLOSE WINDOW!')

            if not named or flag:
                if not os.path.isdir(dest+'((ERROR))'):
                    os.makedirs(dest+'((ERROR))')
                shutil.copy(src+p, dest+'((ERROR))\\'+p)

            
        except Exception as e:
            if not os.path.isdir(dest+'((ERROR))'):
                os.makedirs(dest+'((ERROR))')

            shutil.copy(src+p, dest+'((ERROR))\\'+p)

        #if x%10==0 or x%(len(allPics)-1)==0:
        #print('Processed: '+str(x+1)+' out of '+ str(len(allPics)))
        if x%5==0:
            if(x>0):
                nowTime = int(time.time())
                #print(str(nowTime-startTime) + " " + str(num))
                remaining = int((nowTime - startTime)/x*(len(allPics)-x))
                remainMin = remaining//60
                remainSec = remaining%60
                #remaining = ((nowTime-startTime)/(num/len(allPics)*100))*((len(allPics)-num)/len(allPics)*100)
                print('Processed: '+str(x)+' out of '+str(len(allPics))+' ('+str(int(x/len(allPics)*100))+'%)'+
                      '---Remaining: '+str(remainMin)+' min '+str(remainSec)+
                      ' sec (sec/pic: '+str((nowTime-startTime)/x)+")")

    endTime = int(time.time())
    endMin = (endTime - startTime)//60
    endSec = (endTime - startTime)%60                      
                      
    print("COMPLETE - Elapsed Time: "+str(endMin)+" mins "+str(endSec)+" secs.")
    return None

    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#separate_instas function will separate all(99.9%) the instagram screenshots 
#from non-instagram screenshots. Further into old and new instagram formats
def separate_instas():
    src = 'E:\\Sample\\Screenshots\\'
    dest = src+'IG\\'
    non = src+'non\\'
    
    dirs = [dest, non, dest+'old', dest+'new', dest+'latest']
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)

    allPics = os.listdir(src)
    startTime = int(time.time())
    nowTime = int(time.time())
    endTime = int(time.time())
    remaining = 0
    remainMin = 0
    remainSec = 0
    
    for x, pic in enumerate(allPics):
        if os.path.isfile(src+pic):
            if is_insta_screenshot(src+pic) == 1:
                shutil.copy(src+pic, dest+'old\\'+pic)
            elif is_insta_screenshot(src+pic) == 2:
                shutil.copy(src+pic, dest+'new\\'+pic)
            elif is_insta_screenshot(src+pic) == 3:
                shutil.copy(src+pic, dest+'latest\\'+pic)
            elif is_insta_screenshot(src+pic) == 0:
                shutil.copy(src+pic, non+pic)
        
        if x%5==0:
            if(x>0):
                nowTime = int(time.time())
                #print(str(nowTime-startTime) + " " + str(num))
                remaining = int((nowTime - startTime)/x*(len(allPics)-x))
                remainMin = remaining//60
                remainSec = remaining%60
                #remaining = ((nowTime-startTime)/(num/len(allPics)*100))*((len(allPics)-num)/len(allPics)*100)
                print('Processed: '+str(x)+' out of '+str(len(allPics))+' ('+str(int(x/len(allPics)*100))+'%)'+
                      '---Remaining: '+str(remainMin)+' min '+str(remainSec)+
                      ' sec (sec/pic: '+str((nowTime-startTime)/x)+")")
    endTime = int(time.time())
    endMin = (endTime - startTime)//60
    endSec = (endTime - startTime)%60
                      
                      
    print("COMPLETE - Elapsed Time: "+str(endMin)+" mins "+str(endSec)+" secs.")

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#get_formats iterates through the path and based on the bottom portion of
#the screenshot, collects the most common "formats". Instagram screenshots all
#have a utility bar at the bottom. All variations of bar are saved for later use
def get_formats():

    startTime = int(time.time())
    nowTime = int(time.time())
    endTime = int(time.time())
    remaining = 0
    remainMin = 0
    remainSec = 0
    
    #switch will change the otsu threshold and the crop size of bottom 
    switch = 'Screenshot_2016-05-11-17-36-20.png'
    switch2 = 'Screenshot_20161121-192038.png'
    switch3 = 'Screenshot_20180607-202442.png'
    path = 'E:\\Sample\\Screenshots\\'
    allPics = os.listdir(path)
    formats = []
    amounts = []
    botSize = 168
    otsu = 100
    
    
    for num, pic in enumerate(allPics):
        if pic == switch:
            botSize = 144
            otsu = 204

        #read image as array, crop out bottom
        im = ndi.imread(path+pic, flatten=True)
        imm = im[im.shape[0]-botSize:][:]
        imm = thresh_otsu(imm,otsu)
        
        #add the first format into empty list
        if len(formats) == 0:
            formats.append(imm)
            amounts.append(1)
        else:
            #for loop will iterate through all formats to check if imm is in the list
            for idx, f in enumerate(formats):
                f = thresh_otsu(f,otsu)
                inList = False
                
                #resize smaller crop, need same dimmensions to compare
                if imm.shape != f.shape:
                    imm = (resize(imm/255,f.shape))*255
                #must match any format in the list by at least 93%
                if get_ssim(f,imm) > 0.93:
                    inList = True                    
                    amounts[idx] += 1
                    break

            #if imm was not matched to a format, add it as a new one
            #limit of 10 (except switches) different formats or else VERY SLOW
            if ((not inList) and (len(formats)<10)) or pic == switch or pic == switch2 or pic == switch3:
                formats.append(imm)
                amounts.append(1)

        #print progress every 10 pics
        if(num%100==0):
            if(num>0):
                nowTime = int(time.time())
                #print(str(nowTime-startTime) + " " + str(num))
                remaining = int((nowTime - startTime)/num*(len(allPics)-num))
                remainMin = remaining//60
                remainSec = remaining%60
                #remaining = ((nowTime-startTime)/(num/len(allPics)*100))*((len(allPics)-num)/len(allPics)*100)
            print('Complete: '+str(num)+' out of '+str(len(allPics))+' - LEN: '+str(len(formats))+'---Remaining: '+str(remainMin)+' min '+str(remainSec)+' sec')
        elif(num%10==0):
            if(num>0):
                nowTime = int(time.time())
                #print(str(nowTime-startTime) + " " + str(num))
                remaining = int((nowTime - startTime)/num*(len(allPics)-num))
                remainMin = remaining//60
                remainSec = remaining%60
                #remaining = ((nowTime-startTime)/(num/len(allPics)*100))*((len(allPics)-num)/len(allPics)*100)
            print('Complete: '+str(num)+' out of '+str(len(allPics))+'---Remaining: '+str(remainMin)+' min '+str(remainSec)+' sec')
            
    for idx, f in enumerate(formats):
        if amounts[idx] > 1:
            i = pil.fromarray(np.uint8(f))
            i.save('E:\\Sample\\Formats2\\'+str(amounts[idx])+' - '+str(int(time.time())+idx)+'.png')

    return formats
  

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#is_insta_screenshot method will return True if the screenshot passed to it
#has the bottom instagram toolbar. This indicates that the screenshot is of IG
#boolean switches between returning True/False or actual image type, 1,2 or 3
def is_insta_screenshot(img,readPath=True, boolean=False):

    #0 - NOT INSTA
    #1 - OLD FORMAT
    #2 - NEW FORMAT
    format1 = 'E:\\Sample\\Formats2\\1-859.png'
    format2 = 'E:\\Sample\\Formats2\\2-3452.png'
    format3 = 'E:\\Sample\\Formats2\\3-372.png'

    #Read in image as im and both formats, all greyscale
    im = ndi.imread(img, flatten=True)
    format1 = ndi.imread(format1, flatten=True)
    format2 = ndi.imread(format2, flatten=True)
    format3 = ndi.imread(format3, flatten=True)

    #Try to match im to format 1
    imm = im[im.shape[0]-168:][:]
    imm = thresh_otsu(imm,100)
    if get_ssim(format1,imm) > 0.93:
        return True if boolean else 1

    #Try to match format 2
    imm = im[im.shape[0]-144:][:]
    imm = thresh_otsu(imm,204)
    imm = (resize(imm/255,format1.shape))*255
    if get_ssim(format2,imm) > 0.93:
        return True if boolean else 2

    #Try to match format 3
    imm = im[im.shape[0]-144:][:]
    imm = thresh_otsu(imm,204)
    imm = (resize(imm/255,format1.shape))*255
    if get_ssim(format3,imm) > 0.93:
        return True if boolean else 3

    return False if boolean else 0


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#get_ssim will return a float value (0.0-1.0)indicating how similar img1 and img2 are
#otsu takes -1 for inactive or 0-255 for an otsu threshold
#assist will gaussian blur and scale image in order to get a better match
#gauss and rs(rescale) can be set to specific values for better precision
def get_ssim(img1, img2, otsu=-1, assist=False, gauss=0, rs=0):

    im1 = readImage(img1)
    im2 = readImage(img2)

    if otsu > 0:
        im1 = thresh_otsu(im1,otsu)
        im2 = thresh_otsu(im2,otsu)
    
    im1 = im1/255
    im1 = sk.img_as_float(im1)
    im2 = im2/255
    im2 = sk.img_as_float(im2)

    if assist==True:
        gauss = 1
        rs = 0.5
    
    if rs > 0:
        im1 = rescale(im1, rs)
        im2 = rescale(im2, rs)
    if gauss > 0:
        im1 = gaussian(im1, gauss)
        im2 = gaussian(im2, gauss)
    
    label = '{0:.2f}'.format(ssim(im1, im2)*100)
    #print('SSIM: ' + label +'%')

    return ssim(im1,im2)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#DON'T pass in src if you are passing in a regList.
#src is the path to the image to process
#dest is the path to save ONLY IF save=True
#src not required if a regList is passed to this function
def get_name(src, dest='', regList=[], save=False, returnStr=True, showSteps=False, returnPNG=False, draw=False):
    
    if regList == []:
        regions = get_regions(src, showSteps=showSteps, draw=draw)
    else:
        regions = regList
    
    if draw:
        fig, ax = plt.subplots(ncols=1, nrows=1)
        ax.imshow(readImage(src), cmap='gray', interpolation='nearest')
    
    nameRegs = []
    for reg in regions:
        minc, minr, maxc, maxr = reg
        wide = maxc - minc
        high = maxr - minr
        
        #This will find the the name region based on approximation of height and position
        if  minc > 125 and minc < 165 and minr < 500 and high >= 45 and wide >= 80 and wide <= 830 and regions.index(reg) < 10:
            nameRegs.append(reg)
            if draw:
                print('('+str(minr)+ ', '+str(minc)+ '), ('+str(maxr)+ ', '+str(maxc)+')')
                print('Dim: ' + str(wide) + ' x ' + str(high))
                print('------------------------')
                rect = mpatches.Rectangle((minc,minr), wide, high, fill=False, edgecolor='red', linewidth=2)
                ax.add_patch(rect)
    
    if draw:
        plt.show()


    if type(src) == type('abc'):
        toCrop = pil.open(src)
    else:
        toCrop = pil.fromarray(np.uint8(src))

    #Crop the name region out from original screenshot, convert to array i        
    name = toCrop.crop(nameRegs[0])
    i = np.array(name.convert('L'))
    

    #Check height of region, crop out location if present
    if i.shape[0] > 75 and returnPNG and not returnStr:
        regs = get_regions(i,draw=draw, showSteps=showSteps, scale=False, gauss=1.6)
        i = name.crop(regs[0])
        name = pil.fromarray(np.uint8(i))
    #saves name image
    if save:
        if dest == '':
            print('Cannot save without destination directory')
        else:
            name.save(dest + 'Name - ' + src.split('\\')[-1])

    if returnPNG and not returnStr:
        return name
    
    #OCR will parse name image and return name string 
    nametxt = pytesseract.image_to_string(name)
    nametxt = nametxt.replace('|','l')
    nametxt = nametxt.replace(' ','')
    nametxt = nametxt.split('\n')[0]

    errorOCR = ['Photo', 'Video', 'FOLLOWING', 'Expl']

    if nametxt in errorOCR:
        im = readImage(src)
        im = im[219:][:]
        
        if returnPNG and returnStr:
            nametxt, name = get_name(im, dest=dest, regList=get_regions(im, showSteps=showSteps, draw=draw), returnPNG=True, save=False,draw=draw, showSteps=showSteps)
        elif returnPNG:
            name = get_name(im, dest=dest, regList=get_regions(im, showSteps=showSteps, draw=draw), returnPNG=True, returnStr=False, save=False,draw=draw, showSteps=showSteps)
        else:
            nametxt = name = get_name(im, dest=dest, regList=get_regions(im, showSteps=showSteps, draw=draw), save=False,draw=draw, showSteps=showSteps)
    
    if save:
        if dest == '':
            print('Cannot save without destination directory')
        else:
            name.save(dest + 'Name - ' + src.split('\\')[-1])
    
    #print(nametxt)
    if returnPNG and returnStr:
        return [nametxt,name]
    elif returnStr:
        return nametxt
    elif returnPNG:
        return name
    else:
        print('Nothing to return from get_name!')
        return None


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def get_pic(src, dest='', regList=[], saveThumb=False, saveFull=False, draw=False):

    if regList == []:
        regions = get_regions(src)
    else:
        regions = regList
    
    if draw:
        fig, ax = plt.subplots(ncols=1, nrows=1)
        ax.imshow(readImage(src), cmap='gray', interpolation='nearest')
        
    picRegs = []
    for reg in regions:
        minc, minr, maxc, maxr = reg
        if minc < 0:
            minc = 0
        if minr < 0:
            minr = 0
        if maxc > 1080:
            maxc = 1080
        if maxr > 1920:
            maxr = 1920
        
        wide = maxc - minc
        high = maxr - minr
    
        #This will find the picture region
        #TODO - Images could be shorter than 750
        if wide >= 500 and high >= 500:
            picRegs.append((minc, minr, maxc, maxr))
            if draw:
                rect = mpatches.Rectangle((minc,minr), wide, high, fill=False, edgecolor='red', linewidth=2)
                ax.add_patch(rect)
                
    if draw:
        plt.show()
    
    if type(src) == type('abc'):
        toCrop = pil.open(src)
    else:
        toCrop = pil.fromarray(np.uint8(src))
    pic = toCrop.crop(picRegs[0])
    
    picNoBord = trim(pic)

    if not((saveFull or saveThumb) and dest == ''):
        if saveFull:
            picFile = dest + 'Pic - ' + src.split('\\')[-1]
            picNoBord.save(picFile)
        
        if saveThumb:
            #Calculate new icon resolution and make icon
            iconW, iconH = picNoBord.size
            iconH = ceil(iconH/9)
            iconW = ceil(iconW/9)
            picIcon = picNoBord.resize((iconW,iconH), pil.ANTIALIAS)
            picIcon.save(dest + 'Icon - ' + src.split('\\')[-1])
    else:
        print('No destination to save to.')

    return picNoBord
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#get_both is a method to get the name string and PIL image
#this method is faster than doing both get_name and get_pic as they
#make separate calls to get_regions. get-both makes one call
def get_both(src, dest, saveName=False, saveAll=False, draw=False):
    regions = get_regions(src)
    name = get_name(src, dest=dest, regList=regions, draw=draw, save=True if (saveName or saveAll) else False)
    pic = get_pic(src, dest, regList=regions, saveFull=saveAll, saveThumb=saveAll, draw=draw)
    
    return [name,pic]


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def get_regions(src, draw=False, showSteps=False, scale=True, ots=0.96, gauss=1):
    
    #this allows 0-255 values for otsu instead of just 0.0-1.0
    if ots > 1:
        ots = ots/255
    
    try:
        im = readImage(src)
    except Exception as e:
        print('get_regions Error Reading Image: %s' %e)
        return None

    #Convert from float(0.0 - 255.0) to float(0.0 - 1.0)
    im = im/255
    im = sk.img_as_float(im)

    #Show original image
    if showSteps:
        show(im)

    #Scale to quarter size but scale down twice by half each time (better result)
    if scale:
        ims = rescale(im, 0.5)
        ims = rescale(ims, 0.5)
    else:
        ims = im
    
    #Show scaled img, Otsu , otsu once more to create larger 'blobs'
    if showSteps:
        show(ims)
    imss = ims > ots

    #show Otsu 
    if showSteps:
        show(imss)

    #blur to spread pixels for better patches (default=1)
    if gauss != 0:
        imss = gaussian(imss, gauss)
        #show blurred
        if showSteps:
            show(imss)

        #Otsu again after blur
        imss = imss > ots
        if showSteps:
            show(imss)

    
    if draw:
        fig, ax = plt.subplots(ncols=1, nrows=1)
        ax.imshow(readImage(src), cmap='gray', interpolation='nearest')

    #Create and store all regions of black, regionList stores tuples of regions ((x,y),(x,y))
    labelImage = label(imss, connectivity=2, background=1)
    regions = regionprops(labelImage)
    regionList = []
    for reg in regions:
        minr, minc, maxr, maxc = reg.bbox

        #Expand region a little bit. Avoids text pixel clipping
        minr -= 1 
        minc -= 1
        maxr += 2
        maxc += 3

        #Scale region by 4 (original image downsized by 4)
        if scale:
            minr *= 4
            minc *= 4
            maxr *= 4
            maxc *= 4

        regionList.append((minc, minr, maxc, maxr))
        if draw:
            wide = maxc - minc
            high = maxr - minr
            rect = mpatches.Rectangle((minc,minr), wide, high, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    if draw:
        plt.show()
           
    return regionList



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-MAIN=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

if __name__ == '__main__':

    startTime = int(time.time())
    warnings.filterwarnings("ignore")

    srcOld = 'E:\\Sample\\Sample\\'
    srcNew = 'D:\\Screenshots - Copy\\IG\\new\\'
    dest = 'D:\\FULL FINAL SORT\\'
    
    switch = 0

    if switch == 1:
        sort_by_name(srcOld, dest, named=True)
        sort_by_name(srcNew, dest, named=True)

        

    elif switch == 2:
        p = 'D:\\Screenshots - Copy\\IG\\new\\Screenshot_20160912-032757.png'
        i = readImage(p)
        n=get_name(i,showSteps=True,draw=True)
        #namepic = get_name(i, returnStr=False, returnPNG=True,showSteps=True, draw=True)
        print(n)

    elif switch == 3:
        
        filter_db()        
                
    else:

    #if not os.path.isdir(dest+'ERROR\\ERR\\'):
     #   os.makedirs(dest+'ERROR\\ERR\\')

        #sort_by_name(src=dest+'ERROR\\', dest='D:\\Screenshots - Copy\\IG\\2Err\\', named=True)
        print("quitting")

    endTime = int(time.time())

    processDuration = endTime - startTime
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('Process Duration: '+str(processDuration//60)+ ' mins    ' +str(processDuration%60)+ ' secs')
