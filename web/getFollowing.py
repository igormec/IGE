import requests
import json
import time
import sqlite3
from http.cookies import SimpleCookie


#get cookie from Chrome dev tools and paste here
#this converts the cookie into proper format for requests
raw = 'mid=Wj-AuAAEAAH1VCWP6a6plRHXSb-Y; fbm_124024574287414=base_domain=.instagram.com; csrftoken=x225iit3aHCMiOwcCdek9eLuzxMQFVQB; ds_user_id=239113428; rur=ASH; sessionid=IGSCdc22d28459fa880bc35be0d77492bb90fdc794556c0ab8e0c6501670e19bd33d%3ARyLgyHSqTt8TQVtRcqiPc6NQeIJD2Ikk%3A%7B%22_auth_user_id%22%3A239113428%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%22239113428%3A0qe9V2bzXuKYEIHHFAQdjj0V0y9TORd2%3Ad4506e6d38da67a7a80b52296893625ed3787c2fc4a2e7b21158a99a3be19715%22%2C%22last_refreshed%22%3A1515041065.4881484509%7D; ig_pr=1; ig_or=landscape-primary; ig_vw=944; ig_vh=922; fbsr_124024574287414=LkYoWVtr9aIqwBZg1FNBFDWRholz6YXHeVGKZanGZKU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURFUlFNWDh1LVdoZjhPYXZqMGFLLWhKVkthUE1PU19vOFpDaGZoQ3NmVXpXelhnaW5UWUdUREJMRnVUX1FOR0htNEc4MWdCRlM1U0xpd3pRTk1uZXJIZzdpd1YzNFlkcTVuVWNsZEo0dXNSY205aUkzVEx0Rmp5UTNheFdUYktIYVpvLUZFMlp2MG1JUG03RlN3RXlHOEVCejhzQWRVUUdkelF5ZzhEVXJEMkxoVmlCc2UyS3pMTmZqbkNPWENDSDVqUl92c0s2bmhwZVlsNFAwUl8yUXFVRWlwV0tuYmFEUFJXSW5GZnhsU25ybG1QQzdqNEZBeUllX2dtQUNCb3Q3VVRtN2JEdVoxVFAzMVJxOEx1X09EUGt2emxkMjlfcVZMYVNxZG1hdnZEdTl5TUJ2SFpKVVloTEVaeEFQTXkwcDBmekVHbUxVYkxScFVEMFBTbkt0QyIsImlzc3VlZF9hdCI6MTUxNTA0MTE4MCwidXNlcl9pZCI6IjEwNzM0ODUxMjYifQ; urlgen="{\"time\": 1515041064}:1eWxQl:VHfH4qMc_9axVrLpkMThozoVmKU"'
cookie = SimpleCookie()
cookie.load(raw)
cookies = {}
for k,v in cookie.items():
    cookies[k] = v.value




next_page = True
followersList = []
res = requests.get('https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables=%7B%22id%22%3A%22239113428%22%2C%22first%22%3A20%7D', cookies=cookies)

while next_page == True:
    print(res)
    resp_json = json.loads(res.text)

    next_page = bool(resp_json['data']['user']['edge_follow']['page_info']['has_next_page'])
    end_cursor = resp_json['data']['user']['edge_follow']['page_info']['end_cursor']
    followersList += resp_json['data']['user']['edge_follow']['edges']
    print(len(followersList))
    time.sleep(1)
    #res = requests.get('https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B%22id%22%3A%22239113428%22%2C%22first%22%3A50%2C%22after%22%3A%22'+str(end_cursor)+'%22%7D', cookies=cookies)
    res = requests.get('https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables=%7B%22id%22%3A%22239113428%22%2C%22first%22%3A100%2C%22after%22%3A%22'+str(end_cursor)+'%22%7D', cookies=cookies)



#Store the list from above in the database ex.db
conn = sqlite3.connect('C:/Users/Igor/Documents/Dev/projects/IGE/db/MAIN.db')
c = conn.cursor()
for user in followersList:
    user = user['node']
    toInsert = []
    for k,v in user.items():
        toInsert.append(str(v))

    c.execute("INSERT INTO following values(?,?,?,?,?,?,?)", toInsert)
conn.commit()
conn.close()


