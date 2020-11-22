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

    for name in tqdm(markup.split()[1:20]):
        listOfFollowers.append(name)
    return listOfFollowers

# Function that finds who a specific person follows
def getFollowing(username):
    works = 0
    fails = 0
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
    works = 0
    fails = 0
    for username in tqdm(listOfFollowers):
        listOfFollowing = getFollowing(username)

        if listOfFollowing != "":
            works+=1
            for user in listOfFollowing:
                totalFollowerList.append(user)
        else:
            fails+=1
    return totalFollowerList, works, fails

# Variable that stores list of all followers
listOfTrumpFollowers = createFollowersList("/Users/teaganjohnson/desktop/trumpFollowersYuh.csv", [])

# Gets a list of who followers are following (It will have duplicates)
totalFollowerList1, works, fails = getTotalFollowerList(listOfTrumpFollowers)
print("works: ", works)
print("doesn't work: ", fails)
print("Proportion of followers that worked: ", works/(fails+works))

# A dictionary that counts the most popular follows in the totalFollowerList
counterFollowers = Counter(totalFollowerList1)
print(counterFollowers.most_common(10))
