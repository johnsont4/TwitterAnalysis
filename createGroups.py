from tqdm import tqdm
import os
import twint
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import csv

def createFollowersList(path, listOfFollowers, previousLists=None):
    with open(path) as file:
        markup = file.read()

    for name in tqdm(markup.split()[1:10]):
        listOfFollowers.append(name)
    return listOfFollowers


listOfTrumpFollowers = createFollowersList("realDonaldTrumpFollowers.csv", [])
listOfBidenFollowers = createFollowersList("JoeBidenFollowers.csv", [])

listOfTrumpFollowers = findAllFollowers(listOfTrumpFollowers, listOfBidenFollowers, "JoeBidenFollowers.csv")
listOfBidenFollowers = findAllFollowers(listOfBidenFollowers, listOfTrumpFollowers, "realDonaldTrumpFollowers.csv")

both = set(listOfTrumpFollowers).intersection(set(listOfBidenFollowers))


print("Total length!: ", len(listOfTrumpFollowers)+len(listOfBidenFollowers)-len(both))

print("Trump: ", len(listOfTrumpFollowers))
print(listOfTrumpFollowers)
print()
print("Biden: ", len(listOfBidenFollowers))
print(listOfBidenFollowers)
print()
print(len(both))
print(both)
print()

def removeDuplicates(listOfFollowers, both):
    for user in both:
        if user in listOfFollowers:
            listOfFollowers.remove(user)
    return listOfFollowers

uniqueTrump = set(removeDuplicates(listOfTrumpFollowers, both))
uniqueBiden = set(removeDuplicates(listOfBidenFollowers, both))

print("Trump: ", len(uniqueTrump))
print("Biden: ", len(uniqueBiden))
print("Both: ", len(both))

def saveToComp(file, faction):
    with open("{}.csv".format(faction), "w") as followerFile:
        csvwriter = csv.writer(followerFile)

        csvwriter.writerows(zip(file))


saveToComp(uniqueTrump, "TrumpFollowers")
saveToComp(uniqueBiden, "BidenFollowers")
saveToComp(both, "BothFollowers")
