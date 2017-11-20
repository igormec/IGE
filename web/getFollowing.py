import requests
import json
import time
import sqlite3
from http.cookies import SimpleCookie

'''
#get cookie from Chrome dev tools and paste here
#this converts the cookie into proper format for requests
raw = 'mid=tBf3a-Q"'
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

'''
