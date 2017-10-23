import requests
import json
import time
import sqlite3
from http.cookies import SimpleCookie


#get cookie from Chrome dev tools and paste here
#this converts the cookie into proper format for requests
raw = 'mid=WTDf5gAEAAGGqYWXwfqDvJkMmtn2; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC09664bc29d0b2773e5d943c2591b6399aa82008328f862aa7db1cf7e590205f8%3A3lsdrFuDhV1xBDrFyKPh8wr0G6FROifb%3A%7B%22_auth_user_id%22%3A239113428%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%22239113428%3AUxM49caO3zGJmKt0nmlhTttGHe6Sz4Gc%3A01127152e227cbc86cb7cc61d965c6be8764b7db489e0d845d4ebbfb325c963e%22%2C%22_platform%22%3A4%2C%22last_refreshed%22%3A1508644289.1435470581%7D; ig_or=landscape-primary; ig_vw=1920; ig_pr=1; ig_vh=949; fbsr_124024574287414=iO-ji_03oyKZ-GfIISFsJNnro6xxQDmyp11ZZYnxPtE.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFNbDktWHB6QlJ5MlR3YVhZOUN1ekMtX20welhFbkF6LUNwSDhsR2E0dkZpQ3loZUZlZDJWR2tBS0JCbWRlbnZuSXMyTWI4eWtBMjdLUFg4NWdia29HRmxHUzZPbWNlX0ZHOWZ1djh3MlhCUXRmSGhBN3pHa0p4akhzbUNYZUVhQzczcjJSZnhBREpqRHF5NmQ4UWlROUFfaE5XdDc3eHJHQXJuX0V6ZWhXY3NWQ2o1WE9DaDVvaEJMOGNKeGdSUERaZFpwUmtlRDZfQWFyMk9CeGlzbEJLVVNHYXZsMWdmeHFMX2R5VkFCXzFya1BIY2hSa0dqcW5qSEtvMTFIX1NXR3YtSzAwOUJGVWFhcjJQaE9iWlFOaHBvRHQ3a3FkbldoRGFtRjZGSUNYM0s2MHBLdWRFc00yeWxKbm9EdFpYYktQR0ZUSmdTUGRTci1ENTlwQ3VwSCIsImlzc3VlZF9hdCI6MTUwODcyMzE0MSwidXNlcl9pZCI6IjEwNzM0ODUxMjYifQ; csrftoken=nUn7FmmbxPTnOPhp4tN65SbEFtVCnFN3; rur=ASH; ds_user_id=239113428; urlgen="{\"time\": 1508644287}:1e6Rol:Y21KyiFNw5cOWaoTIxFG7ulgqOk"'
cookie = SimpleCookie()
cookie.load(raw)
cookies = {}
for k,v in cookie.items():
    cookies[k] = v.value




next_page = True
followersList = []
res = requests.get('https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables=%7B%22id%22%3A%22239113428%22%2C%22first%22%3A100%7D', cookies=cookies)

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
conn = sqlite3.connect('C:/Users/Igor/Desktop/New Folder/ex.db')
c = conn.cursor()
for user in followersList:
    user = user['node']
    toInsert = []
    for k,v in user.items():
        toInsert.append(str(v))

    c.execute("INSERT INTO following values(?,?,?,?,?,?,?)", toInsert)
conn.commit()
conn.close()

