from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter

def createFollowersList(path):
    with open(path) as file:
        markup = file.read()

    listOfFollowers = []
    for name in tqdm(markup.split()[10:20]):
        listOfFollowers.append(name[0:-1])
    return listOfFollowers
listOfTrumpFollowers = createFollowersList()

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
        return listOfFollowing["following"][username]
    except Exception:
        return ""

def createDictAndList(listOfFollowers):
    followerDict = defaultdict(list)
    totalFollowerList = []
    for username in tqdm(listOfFollowers):
        listOfFollowers = getFollowing(username)
        totalFollowerList.append(listOfFollowers)
        followerDict['username'] = listOfFollowers
    return followerDict, totalFollowerList

def getTotalFollowerList(listOfFollowers):
    #followerDict = defaultdict(list)
    totalFollowerList = []
    for username in tqdm(listOfFollowers):
        listOfFollowers = getFollowing(username)
        if listOfFollowers != "":
            for person in listOfFollowers:
                totalFollowerList.append(person)
        #followerDict['username'] = listOfFollowers
    return totalFollowerList

listOfTrumpFollowers = createFollowersList("/Users/teaganjohnson/Desktop/twint/trumpFollowers.rtf")
totalFollowerList = getTotalFollowerList(listOfTrumpFollowers)
counterFollowers = Counter(totalFollowerList)
print(counterFollowers.most_common(10))
