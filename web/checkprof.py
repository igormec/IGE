#! python3
#Main profile checker to see the changes in numbers
import dlprof as prof


#load profile, check for diffs between last time checked

users = ['pcscenes']
output = '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\nUser: '

followerCount = 4
followingCount = 9
poss = 0

for user in users:

    global output, followerCount, followingCount, poss
    output += user

    oldFollowers = followerCount
    oldFollowing = followingCount
    oldNumPosts = poss

    newFollowers = prof.get_followers(user)
    newFollowing = prof.get_following(user)
    newNumPosts = prof.get_numPosts(user)

    diffFollowers = newFollowers - oldFollowers
    diffFollowing = newFollowing - oldFollowing
    diffPosts = newNumPosts - oldNumPosts


    output += '\n'
    changed = False
    
    if diffFollowers != 0:
        output += str(diffFollowers)+' new followers\n'
        changed = True

    if diffFollowing != 0:
        output += str(diffFollowing)+' pages followed\n'
        changed = True

    if diffFollowers != 0:
        output += str(diffPosts)+' new posts\n'
        changed = True

    if not changed:
        output += "No changes for user\n"
        
    print(output)


        
    
    
    


    
