#! python3
#Main profile checker to see the changes in numbers
import dlprof as prof


#load profile, check for diffs between last time checked

users = ['pcscenes']
output = '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\nUser: '

fle = 0
flo = 0
pos = 0


for user in users:

    global output, fle, flo, pos
    output += user

    oldFollowers = flo
    oldFollowing = fle
    oldNumPosts = pos

    newFollowers = prof.get_followers(user)
    newFollowing = prof.get_following(user)
    newNumPosts = prof.get_numPosts(user)

    diffFollowers = newFollowers - oldFollowers
    diffFollowing = newFollowing - oldFollowing
    diffPosts = newNumPosts - oldNumPosts


    output += '\n'

    if diffFollowers != 0:
        output += str(diffFollowers)+' new followers\n'

    if diffFollowing != 0:
        output += str(diffFollowing)+' pages followed\n'

    if diffFollowers != 0:
        output += str(diffPosts)+' new posts\n'

    

    print(output)


        
    
    
    


    
