import twint

# Function that saves a list of 50,000 users that follow a given account
def getFollowers(username):
    c = twint.Config()
    c.Username = username
    c.Limit = 50000
    c.Store_csv = True
    c.Output = "../{}Followers.csv".format(username)

    twint.run.Followers(c)

getFollowers("realDonaldTrump")
getFollowers("JoeBiden")
