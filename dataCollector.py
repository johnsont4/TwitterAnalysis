from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import csv

def openFiles(path, listOfFollowers):
    with open(path) as file:
        markup = file.read()

    for name in tqdm(markup.split()[1:2000]):
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
        return listOfFollowing["following"][username]
    except Exception:
        return ""


# Function that returns the list of every single follower of a user.
# It will also include a dictionary where the keys are users and the values
# are lists of users that they follow.
def getTotalFollowerStats(listOfFollowers):
    totalFollowerList = []
    followersDict = defaultdict(list)
    works = 0
    fails = 0
    for username in tqdm(listOfFollowers):
        listOfFollowing = getFollowing(username)

        if listOfFollowing != "":
            works+=1
            for user in listOfFollowing:
                totalFollowerList.append(user)
            followersDict[username] = listOfFollowing
        else:
            fails+=1
    return totalFollowerList, followersDict, works, fails

trumpFollowers = openFiles("trumpFollowers.csv", [])
bidenFollowers = openFiles("bidenFollowers.csv", [])
bothFollowers = openFiles("bothFollowers.csv", [])
def runStats(followers, name, folder):
    totalFollowerList, followersDict, works, fails = getTotalFollowerStats(followers)
    print(name)
    print()
    print("Length of list: ", len(totalFollowerList))
    print("works: ", works)
    print("doesn't work: ", fails)
    try:
        print("Proportion of followers that worked: ", works/(fails+works))
    except Exception:
        pass
    counterFollowers = Counter(totalFollowerList)

    with open("{}Top100.csv".format(name), "w") as followerFile:
        csvwriter = csv.writer(followerFile)
        csvwriter.writerows(zip(counterFollowers))

    for person in followersDict:
        with open("/Users/teaganjohnson/Desktop/TwitterAnalysis/{}/{}.csv".format(folder, person), "w") as personFile:
            csvwriter = csv.writer(personFile)
            csvwriter.writerows(zip(list(followersDict[person])))

    print("TOP 100: ", counterFollowers.most_common(100))
    print()


runStats(trumpFollowers, "trump", "Donald Trump Followers")
runStats(bidenFollowers, "biden", "Joe Biden Followers")
runStats(bothFollowers, "both", "Both Followers")
