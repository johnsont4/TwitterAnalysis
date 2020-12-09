from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import csv

# Find the parent function for future reference
currPath = os.getcwd()
parent = os.path.abspath(os.path.join(currPath, os.pardir))

# Function that reads a csv and returns a list of users given a path
def openFiles(path):
    listOfFollowers = []
    with open(path) as file:
        markup = file.read()

    for name in tqdm(markup.split()[1:2000]):
        listOfFollowers.append(name)
    return listOfFollowers

# Function that returns a list of who a user follows given a Twitter username
def getFollowing(username):
    works = 0
    fails = 0
    c = twint.Config()
    c.Username = username
    c.Pandas = True

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
def getTotalFollowerStats(listOfFollowers, name):
    totalFollowerList = []
    listOfPeopleFollowingBoth = []
    followersDict = defaultdict(list)
    bothFollowersDict = defaultdict(list)
    works = 0
    fails = 0
    for username in tqdm(listOfFollowers):
        listOfFollowing = getFollowing(username)
        if listOfFollowing != "":
            works+=1
            if "realDonaldTrump" and "JoeBiden" not in listOfFollowing:
                for user in listOfFollowing:
                    totalFollowerList.append(user)
                followersDict[username] = listOfFollowing
            else:
                print("THIS PERSON FOLLOWS BOTH: ", username)
                listOfPeopleFollowingBoth.append(username)
                bothFollowersDict[username] = listOfFollowing
        else:
            fails+=1
    return totalFollowerList, followersDict, works, fails, bothFollowersDict

# Function that writes the top 100ish column accounts to a directiry
# It also writes each user's following list to a directory
# Lastly, it returns the dictionary containing information about the users following both
def runStats(followers, name, folder, parent):
    totalFollowerList, followersDict, works, fails, bothFollowersDict = getTotalFollowerStats(followers, name)
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

    with open("{}/{}Top100.csv".format(parent, name), "w") as followerFile:
        csvwriter = csv.writer(followerFile)
        csvwriter.writerow(["username", "followers"])
        for thing in counterFollowers.most_common(100):
            add = [thing[0], thing[1]]
            csvwriter.writerow(zip(add))

    for person in followersDict:
        with open("{}/{}/{}.csv".format(parent, folder, person), "w") as personFile:
            csvwriter = csv.writer(personFile)
            csvwriter.writerow(["username"])
            csvwriter.writerows(zip(list(followersDict[person])))

    print("TOP 100: ", counterFollowers.most_common(100))
    print()
    return bothFollowersDict

# Function that merges to dictionaries based on keys
def mergeDicts(dict1, dict2):
    both = dict1.copy()
    both.update(dict2)
    return both

# Function that writes each user following both's following list given a list of bothFollowers
def writeBothFolder(bothFollowers, parent):
    for person in bothFollowers.keys():
        with open("{}/Both Followers/{}.csv".format(parent, person), "w") as personFile:
            csvwriter = csv.writer(personFile)
            csvwriter.writerow(["username"])
            csvwriter.writerows(zip(list(bothFollowersDict[person])))


trumpFollowers = openFiles("{}/realDonaldTrumpFollowers.csv".format(parent))
bidenFollowers = openFiles("{}/JoeBidenFollowers.csv".format(parent))
bothFollowersTrump = runStats(trumpFollowers, "trump", "Donald Trump Followers", parent)
bothFollowersBiden = runStats(bidenFollowers, "biden", "Joe Biden Followers", parent)
bothFollowersDict = mergeDicts(bothFollowersTrump, bothFollowersBiden)
writeBothFolder(bothFollowersDict, parent)
