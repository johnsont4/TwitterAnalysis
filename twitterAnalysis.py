from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter

# Opens the text file with user's followers and returns all followers in a list
def createFollowersList(path, listOfFollowers):
    with open(path) as file:
        markup = file.read()

    for name in tqdm(markup.split()[10:20]):
        listOfFollowers.append(name[0:-1])
    return listOfFollowers

# Function that finds who a specific person follows
def getFollowing(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    #c.Output = "/Users/teaganjohnson/Desktop/TwitterFinalProject/Donald Trump Followers/{}.csv".format(username)

    twint.run.Following(c)
    listOfFollowing = twint.storage.panda.Follow_df

    #listOfFollowing = listOfFollowing.reindex(index=listOfFollowing.index[::-1])
    #print(listOfFollowing)
    #listOfFollowing.to_csv(r'/Users/teaganjohnson/Desktop/TwitterFinalProject/.csv', header=None, index=None, sep=' ', mode='a')
    try:
        print("Works")
        print()
        return listOfFollowing["following"][username]
    except Exception:
        print("Doesn't Work")
        print()
        return ""

# Function that returns the list of every single follower of a user.
# It will also include a dictionary where the keys are users and the values
# are lists of users that they follow.
def getTotalFollowerList(listOfFollowers):
    totalFollowerList = []
    for username in tqdm(listOfFollowers):
        try:
            listOfFollowers = getFollowing(username)
        except Exception:
            listOfFollowers = ""
        if listOfFollowers != "":
            totalFollowerList.append(listOfFollowers)
    return totalFollowerList

# Variable that stores list of all followers
listOfTrumpFollowers = createFollowersList("/Users/teaganjohnson/desktop/trumpFollowers", [])

# Gets a list of who followers are following (It will have duplicates)
totalFollowerList1 = getTotalFollowerList(listOfTrumpFollowers)
for x in totalFollowerList1:
    x = totalFollowerList1
#print((totalFollowerList))
# A dictionary that counts the most popular follows in the totalFollowerList
counterFollowers = Counter(totalFollowerList1)
print(counterFollowers.most_common(10))
