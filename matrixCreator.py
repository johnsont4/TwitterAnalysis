import numpy as np
import os
import pandas as pd

def makeFollowerVector(person, faction, columnsVector):
    followerVector = []
    with open("/Users/teaganjohnson/desktop/TwitterAnalysis/{}/{}".format(faction, person)) as user:
        dataframe = pd.read_csv(user, usecols=[0])
        dataframe = dataframe.username.tolist()
        for account in columnsVector:
            if account[2:-3] in dataframe:
                followerVector.append(1)
            else:
                followerVector.append(0)
    return followerVector




def followerMatrix(faction, path):
    matrix = []
    array = []
    with open(path) as mostPopular:
        for person in mostPopular:
            if nameOfFile[0] != ".":
                followerVector = makeFollowerVector(person, faction)
                matrix.append(followersVector)
                if faction == 'trump':
                    array.append('1')
                elif faction == 'biden':
                    array.append('0')
    matrix = np.array(matrix)
    return matrix, array

def createTop50List(path):
    top100 = []
    with open(path) as mostPopularFile:
        dataframe = pd.read_csv(mostPopularFile, usecols=[0], nrows=60)
        top50 = dataframe.username.tolist()
        if "('JoeBiden',)" in top50:
            top50.remove("('JoeBiden',)")
        if "('realDonaldTrump',)" in top50:
            top50.remove("('realDonaldTrump',)")
        return top50

trumpTop50 = createTop50List("/Users/teaganjohnson/Desktop/TwitterAnalysis/trumpTop100.csv")
bidenTop50 = createTop50List("/Users/teaganjohnson/Desktop/TwitterAnalysis/bidenTop100.csv")

top100 = trumpTop50 + bidenTop50
columnsVector = list(dict.fromkeys(top100))
print(columnsVector)

x = makeFollowerVector('evie29192940.csv', "Donald Trump Followers", columnsVector)
#print(x)
#DTMatrix,DTArray = followerMatrix('trump', "/Users/teaganjohnson/Desktop/TwitterAnalysis/Donald Trump Followers")
#JBMatrix,JBArray = followerMatrix('biden', "/Users/teaganjohnson/Desktop/TwitterAnalysis/Joe Biden Followers")
#BMatrix, BArray = followerMatrix('BothFollowers')
#if listType == 'BidenFollowers'
#    array.append('2')
