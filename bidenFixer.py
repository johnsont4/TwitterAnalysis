import shutil
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

def openFiles(path):
    addToBiden = []
    listOfTotalBidenFollowers = []
    listOfBidenFollowers = []
    listOfTrumpFollowers = []
    listOfTotalBothFollowers = []

    for user in os.listdir(path):
        if user[0] != ".":
            dataframe = pd.read_csv(path+'/'+user, usecols=[0])
            following = dataframe.username.tolist()
            print(following)

            if "realDonaldTrump" not in set(following):
                print("This is a biden follower")
                shutil.move("/Users/teaganjohnson/desktop/TwitterMaster/Both Followers/{}".format(user), "/Users/teaganjohnson/desktop/TwitterMaster/Joe Biden Followers")
                listOfBidenFollowers.append(user)
                listOfTotalBidenFollowers.append(following)
            elif "JoeBiden" not in set(following):
                print("This is a trump follower")
                shutil.move("/Users/teaganjohnson/desktop/TwitterMaster/Both Followers/{}".format(user), "/Users/teaganjohnson/desktop/TwitterMaster/Donald Trump Followers")
                listOfTrumpFollowers.append(user)
            else:
                print("This is a both follower")
                listOfTotalBothFollowers.append(following)
    return listOfBidenFollowers, listOfTrumpFollowers, listOfTotalBidenFollowers, listOfTotalBothFollowers

#bidenFollowers, newTrumpFollowers, listOfTotalBidenFollowers, listOfTotalBothFollowers = openFiles("{}/Both Followers".format(parent))

def createTop100(totalListOfFollowers, parent):
    print(type(totalListOfFollowers))
    counterFollowers = Counter(totalListOfFollowers)
    with open("{}/bothTop100.csv".format(parent), "w") as followerFile:
        csvwriter = csv.writer(followerFile)
        csvwriter.writerow(["username", "followers"])
        for thing in counterFollowers.most_common(100):
            add = [thing[0], thing[1]]
            csvwriter.writerow(zip(add))

def fixer():
    listOfTotalBidenFollowers = []
    count = 0
    for user in os.listdir("/Users/teaganjohnson/desktop/TwitterMaster/Both Followers"):
        count += 1
        if user[0] != ".":
            dataframe = pd.read_csv("/Users/teaganjohnson/desktop/TwitterMaster/Both Followers/"+user, usecols=[0])
            following = dataframe.username.tolist()
            for x in following:
                listOfTotalBidenFollowers.append(x)
                trump = 0
                '''if x == 'realDonaldTrump':
                    if 'JoeBiden' in set(following):
                        shutil.move("/Users/teaganjohnson/desktop/TwitterMaster/Biden Followers/{}".format(user), "/Users/teaganjohnson/desktop/TwitterMaster/Both Followers")
                    else:
                        shutil.move("/Users/teaganjohnson/desktop/TwitterMaster/Biden Followers/{}".format(user), "/Users/teaganjohnson/desktop/TwitterMaster/Donald Trump Followers")
                    trump += 1
                    print('NOOOOOO')'''
    return listOfTotalBidenFollowers, count
listOfTotalBidenFollowers, count = fixer()
print("BOTH: ",count)

createTop100(listOfTotalBidenFollowers, parent)

#createTop100(listOfTotalBothFollowers, "both", parent)
