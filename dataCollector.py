from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import csv

currPath = os.getcwd()
parent = os.path.abspath(os.path.join(currPath, os.pardir))

def openFiles(path, listOfFollowers):
    with open(path) as file:
        markup = file.read()
        print(markup)

    for name in tqdm(markup.split()[0:499]):
        listOfFollowers.append(name)
    return listOfFollowers

# Function that finds who a specific person follows
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
        print("WAIT", username)
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

trumpFollowers = openFiles("{}/TrumpFollowers.csv".format(parent), [])
bidenFollowers = openFiles("{}/BidenFollowers.csv".format(parent), [])
bothFollowers = openFiles("{}/BothFollowers.csv".format(parent), [])

print('Trump', len(trumpFollowers))
print('biden', len(bidenFollowers))
print('both', len(bothFollowers))
def runStats(followers, name, folder, parent):
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


runStats(trumpFollowers, "trump", "Donald Trump Followers", parent)
runStats(bidenFollowers, "biden", "Joe Biden Followers", parent)
runStats(bothFollowers, "both", "Both Followers", parent)
