import numpy as np
import os
import pandas as pd

currPath = os.getcwd()
parent = os.path.abspath(os.path.join(currPath, os.pardir))

def makeFollowerVector(person, faction, columnsVector, parent):
    followerVector = []
    with open("{}/{}/{}".format(parent, faction, person)) as user:
        dataframe = pd.read_csv(user, usecols=[0])
        dataframe = dataframe.username.tolist()
        for account in columnsVector:
            if account[2:-3] in dataframe:
                followerVector.append(1)
            else:
                followerVector.append(0)
    return followerVector




def followerMatrix(faction, columnsVector, parent):
    matrix = []
    array = []

    for person in os.listdir("{}/{}".format(parent, faction)):
        if person[0] != ".":
            followerVector = makeFollowerVector(person, faction, columnsVector, parent)
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

trumpTop50 = createTop50List("{}/trumpTop100.csv".format(parent))
bidenTop50 = createTop50List("{}/bidenTop100.csv".format(parent))

top100 = trumpTop50 + bidenTop50
columnsVector = list(dict.fromkeys(top100))

trumpMatrix, trumpArray = followerMatrix("Donald Trump Followers", columnsVector, parent)
bidenMatrix, bidenArray = followerMatrix("Joe Biden Followers", columnsVector, parent)
bothMatrix, bothArray = followerMatrix("Both Followers", columnsVector, parent)


matrix_list = np.concatenate((trumpMatrix, bidenMatrix), axis = 0)
matrix = np.array(matrix_list)
np.save('/{}/matrix.npy'.format(parent), matrix)

np.save('/{}/bothMatrix.npy'.format(parent), bothMatrix)

targetArray_list = np.concatenate((trumpArray, bidenArray), axis = 0)
targetArray = np.array(targetArray_list)
np.save('/{}/tagetArray.npy'.format(parent), targetArray)

np.save('/{}/topTeamsList.npy'.format(parent), top100)
