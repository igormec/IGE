#! python3
#MLDownloader.py - downloads all ML items in favourites


import json, requests, bs4, time, pprint

DEBUG = True
CURRENT_USER = ''
USER_SOUP = ''
#==================PRIVATE FUNCTIONS==================#

#Connect to user's profile and get full DOM of page
def get_soup(username):

    global CURRENT_USER
    global USER_SOUP
    
    if username == '':
        print("No username")
    else:

        #If checking for same user as last function call, use same soup
        #This will connect to IG only once reducing IG calls
        if CURRENT_USER == username:
            if DEBUG: print("Return same soup")
            return USER_SOUP

        else:
            CURRENT_USER = username
            #Connect to the page
            url = 'http://instagram.com/'+username+'/'
            if DEBUG:
                print("Connecting to IG Server...")

            try:
                res = requests.get(url)
                res.raise_for_status()
                if DEBUG:
                    print("Got page")
            except Exception as e:
                print("Error: %s" %(e))
                sys.exit(1)


            #Get profile page
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            USER_SOUP = soup
            if DEBUG:
                print(soup)
            return soup
        

def get_main_json(user):

    jsn = get_soup(user)
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn.find_all('script')
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn[1]
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn.contents
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn[0].split('._sharedData = ')
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn[1]
    if DEBUG:
        print(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn[:-1]
    if DEBUG:
        pprint.pprint(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = json.loads(jsn)
    if DEBUG:
        pprint.pprint(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')

    jsn = jsn['entry_data']['ProfilePage'][0]['user']
    if DEBUG:
        pprint.pprint(jsn)
        print('\n\n\n\n========================\n\n\n\n\n')
        
    return jsn
    



#This gets the tag 
def get_profile_numbers(user):
    soup = get_soup(user)
    numbers = soup.find("meta", attrs={"property":"og:description"})
    if DEBUG:
        print(numbers)

    output = numbers['content']
    if DEBUG:
        print(output)
    return output




#==================PUBLIC FUNCTIONS==================#


def get_followers(user):
    out = get_profile_numbers(user).split(' ')[0]
    if DEBUG:
        print(out)
    return int(out)

def get_following(user):
    out = get_profile_numbers(user).split(' ')[2]
    if DEBUG:
        print(out)
    return int(out)

def get_numPosts(user):
    out = get_profile_numbers(user).split(' ')[4]
    if DEBUG:
        print(out)
    return int(out)

def get_username(user):
    out = get_profile_numbers(user).split('(')[1]
    out = out[1:-1]
    if DEBUG:
        print(out)
    return out


def get_last_pic(user, num=1):
    s = get_soup(user)
    
    



if __name__ == '__main__':
    print('RUNNING')

    mainjson = get_main_json('pcscenes')







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



