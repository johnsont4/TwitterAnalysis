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

    for name in tqdm(markup.split()[10:200]):
        listOfFollowers.append(name[0:-1])
    return listOfFollowers

# Function that finds who a specific person follows
def getFollowing(username):
    count = 0
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    #c.Output = "/Users/teaganjohnson/Desktop/TwitterFinalProject/Donald Trump Followers/{}.csv".format(username)

    try:
        twint.run.Following(c)
        listOfFollowing = twint.storage.panda.Follow_df

        #listOfFollowing = listOfFollowing.reindex(index=listOfFollowing.index[::-1])
        #print(listOfFollowing)
        #listOfFollowing.to_csv(r'/Users/teaganjohnson/Desktop/TwitterFinalProject/.csv', header=None, index=None, sep=' ', mode='a')

        print(username)
        print("Works")
        print()
        return listOfFollowing["following"][username]
    except Exception:
        print(username)
        print("Doesn't Work")
        print()
        return ""

# Function that returns the list of every single follower of a user.
# It will also include a dictionary where the keys are users and the values
# are lists of users that they follow.
def getTotalFollowerList(listOfFollowers):
    totalFollowerList = []
    for username in tqdm(listOfFollowers):
        listOfFollowing = getFollowing(username)

        if listOfFollowing != "":
            for user in listOfFollowing:
                totalFollowerList.append(user)
    return totalFollowerList

# Variable that stores list of all followers
listOfTrumpFollowers = createFollowersList("/Users/teaganjohnson/desktop/bidenFollowers", [])

# Gets a list of who followers are following (It will have duplicates)
totalFollowerList1 = getTotalFollowerList(listOfTrumpFollowers)
print(totalFollowerList1)

# A dictionary that counts the most popular follows in the totalFollowerList
counterFollowers = Counter(totalFollowerList1)
print(counterFollowers.most_common(10))
