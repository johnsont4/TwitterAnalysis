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




def followerMatrix(faction, columnsVector):
    matrix = []
    array = []

    for person in os.listdir("/Users/teaganjohnson/Desktop/TwitterAnalysis/{}".format(faction)):
        if person[0] != ".":
            followerVector = makeFollowerVector(person, faction, columnsVector)
            matrix.append(followerVector)
            if faction == 'Donald Trump Followers':
                array.append('1')
            elif faction == 'Joe Biden Followers':
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

trumpMatrix, trumpArray = followerMatrix("Donald Trump Followers", columnsVector)
bidenMatrix, bidenArray = followerMatrix("Joe Biden Followers", columnsVector)
bothMatrix, bothArray = followerMatrix("Both Followers", columnsVector)

print(trumpArray)
