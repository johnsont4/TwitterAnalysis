from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict

def createFollowersList():
    with open("/Users/teaganjohnson/Desktop/twint/trumpFollowers.rtf") as file:
        markup = file.read()

    listOfFollowers = []
    for name in tqdm(markup.split()[10:]):
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
    return listOfFollowing["following"][username]

def createDictAndList(listOfFollowers):
    followerDict = defaultdict(list)
    totalFollowerList = []
    for username in tqdm(listOfFollowers):
        listOfFollowers = getFollowing(username)
        totalFollowerList.append(listOfFollowers)
        followerDict['username'] = listOfFollowers

createDictAndList(listOfTrumpFollowers)
