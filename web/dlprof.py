#! python3
#MLDownloader.py - downloads all ML items in favourites


import requests, bs4, sys, webbrowser, time, os, pprint

#os.makedirs('D:\\Storage\\Internet Saves\\ML\\Pics', exist_ok=True)

#Connect to the page
url = 'http://instagram.com/pcscenes/'
print("Connecting to IG Server...")


try:
    res = requests.get(url)
    res.raise_for_status()
    print("Got page")
except Exception as e:
    print("Error: %s" %(e))
    sys.exit(1)


#Get number of items
soup = bs4.BeautifulSoup(res.text, "html.parser")
print(soup)
'''
numPics = soup.select('span[class="active"]')   #---> • Images [ 2,358 ] •
numPics = numPics[0].getText().split('[ ')      #---> '• Images', '2,358 ] •'
numPics = numPics[1].split(' ]')                #---> '2,358', ' •'
numPics = numPics[0]                            #---> 2,358


#Take out comma out of number of items          #---> 2358
if ',' in numPics:
    numPics = numPics.replace(',', '')
numPics = int(numPics)
print('Detected '+ str(numPics) + ' items.')


#Get all item divs
lis = soup.find_all("div", class_="col-md-12")
allDivs = lis[1]
picDivs = allDivs.div.div.div.div
picDivs = picDivs.contents
picDivs[:] = [x for x in picDivs if x != '\n'] # this removes all '\n' divs


#Get all urls from all pages
#TODO: Multiple pages
picURLs = []
for pic in picDivs:
    link = pic.a['href']
    picURLs.append(link)



#if len(picURLs) != numPics:
    #print('Not all image links retrieved')

numPicsDone = 0

#For loop to download all items
for item in picURLs:

    #Get 'pure' link with no extra subdomains
    link = 'http://com/'
    code = (item.split('/'))[-1]
    fileName = code
    link += code

    #Visit page and retrive pure file url
    try:
        res = requests.get(link)
        res.raise_for_status()
    except Exception as e:
        print("Error: %s" %(e))
        sys.exit(1)
    
    picSoup = bs4.BeautifulSoup(res.text, "html.parser")
    div = picSoup.find_all("div", id="media-media")
    div = div[0]
    finalPic = (div.div.a.img['src'].split('?'))[0]
    ext = (finalPic.split('.'))[-1]

    #Go to file url
    try:
        picRes = requests.get(finalPic)
        picRes.raise_for_status()
        picHead = requests.head(finalPic)
        picRes.raise_for_status()
        
        picHead = picHead.headers
        size = int(picHead['content-length'])
    except Exception as e:
        print("Error: %s" %(e))
        sys.exit(1)


    
    imgFile = open('D:\\Storage\\Internet Saves\\ML\\Pics\\' + fileName + "." + ext, 'wb')
    print('Downloading image ' + str(numPicsDone+1) + ' out of ' + str(numPics) + '.....', end='')
    
    for chunk in picRes.iter_content(100000):
        imgFile.write(chunk)
        #pctDone = int((count*100000)/size)        
        #print('Downloading image ' + str(numPicsDone+1) + ' out of ' + str(numPics) + '.....(' + str(pctDone) + '%)', end='\r')

    imgFile.close()
    print('Image Downloaded')
    numPicsDone+=1
    
sys.exit(0)

    

'''



