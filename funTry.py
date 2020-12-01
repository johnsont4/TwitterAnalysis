from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import csv
from sklearn.naive_bayes import BernoulliNB

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
        print("Something went wrong. User may not exist")
        return ""


def createVector(person, columnsVector):
    followerVector = []
    followTrump = False
    followBiden = False
    listOfFollowing = getFollowing(person)
    totalCount = 0
    if "realDonaldTrump" in set(listOfFollowing):
        followTrump = True
    if "JoeBiden" in set(listOfFollowing):
        followBiden = True
    for account in columnsVector:
        if account in listOfFollowing:
            totalCount+=1
            followerVector.append(1)
        else:
            followerVector.append(0)
    return followerVector, followTrump, followBiden, totalCount

topTeamsListMessy = np.load('topTeamsList.npy')

def cleanTeamsList(teamsList):
    cleanList = []
    for user in teamsList:
        cleanUser = user[2:-3]
        cleanList.append(cleanUser)
    return cleanList

topTeamsList = cleanTeamsList(topTeamsListMessy)

matrix = np.load('matrix.npy')
targetArray = np.load('targetArray.npy')

model = BernoulliNB()
model.fit(matrix, targetArray)

personVector, followTrump, followBiden, totalCount = createVector(input("What's your username?: "), topTeamsList)
predictionProba = model.predict_proba(np.array(personVector).reshape(1, -1))

for num in predictionProba:
    predictionProb = num

predictionProb = list(predictionProb)

print()
print()
print("Preface: You  follow ", totalCount, "of our top users")
print()
print()
print("You have a ", predictionProb[0], "chance of following Biden's Twitter account!")
print("You have a ", predictionProb[1], "chance of following Trump's Twitter account!")
print()
print("Do you follow Trump? ", followTrump)
print("Do you follow Biden? ", followBiden)
print()
print()
