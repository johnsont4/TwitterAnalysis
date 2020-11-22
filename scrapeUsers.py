import twint

c = twint.Config()
c.Username = "realDonaldTrump"
c.Limit = 20
c.Store_csv = True
c.Output = "trumpFollowersYuh.csv"

twint.run.Followers(c)
