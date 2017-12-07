import praw
import pymysql
import smtplib
from ffclass import ff
from email.mime.text import MIMEText
from datetime import datetime






#YAHOO API STUFF

#http://tech.thejoestory.com/2014/12/yahoo-fantasy-football-api-using-python.html
#^^^^^^DIRECTIONS^^^^^^^

# import yql
# from yql.storage import FileTokenStore
# import os
#
#
# y3 = yql.ThreeLegged('dj0yJmk9b0twbjZaTm5FbHprJmQ9WVdrOVJVSjRPVzFoTkRJbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD00OQ--', '7a0fdb386b42b7e685f1591c401762f0ece7d64a')
#
# _cache_dir = 'c:\\python36\\projects\\YahooFF'
#
# if not os.access(_cache_dir, os.R_OK):
#     os.mkdir(_cache_dir)
#
# token_store = FileTokenStore(_cache_dir, secret='7a0fdb386b42b7e685f1591c401762f0ece7d64a')
#
# stored_token = token_store.get('foo')







#constats
subreddit = 'fantasyfootball'
team1 = ["Kirk Cousins", "Antonio Brown", "Adam Thielen", "Alfred Morris", "Carlos Hyde", "Vernon Davis", "JuJu", "Anderson", "Rex Burkhead", "Robby Anderson", "Bilal Powell", "Jordy Nelson", "Rod Smith", "Josh Gordon", "Graham Gano", "Cincinnati"]
team2 = ["Andy Dalton", "Doug Baldwin", "JuJu", "Alvin Kamara", "Mark Ingram", "Jack Doyle", "Alex Collins", "Isaiah Crowell", "Tyler Kroft", "Kenny Stills", "Andre Ellington", "Jonathan Stewart", "Rod Smith", "Kai Forbath", "Los Angeles", "Cincinnati"]

#authentic with redit through praw
def praw_reddit_auth(clientid,secret,bot):
    reddit = praw.Reddit(client_id=clientid,
                     client_secret=secret,
                     user_agent=bot)
    return reddit


def dbconnect(host, user, password, db):
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

    # try:
    #     with connection.cursor() as cursor:
    #         sql = "DESCRIBE ff"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         print(result)
    # finally:
    #     connection.close()


#loop through new submission in subreddit and see if any matches with playes names
def get_news(reddit, subredditname, teams):
    message = []
    sub = reddit.subreddit(subredditname)

    for submission in sub.new(limit=50):
       # print(submission.title)
        for player in teams:
            if(player.lower() in (submission.title).lower()):
                message.append(submission.title)
                #message += submission.url

    return message


#send text
def send_text(msg, comefrom, to, passwrd):

    for mes in msg:
        if(len(mes) > 0):
            print(mes)
            # s = smtplib.SMTP('smtp.gmail.com:587')
            # s.ehlo()
            # s.starttls()
            # s.login(comefrom, passwrd)
            # s.sendmail(comefrom, to, msg)
            # s.quit()


def update_ff_table(reddit):
    sub = reddit.subreddit('fantasyfootball')
    fobjs = []

    for submission in sub.new(limit=5):
        url = None
        flair = None
        datecreated = utc_to_datetime(submission.created_utc)

        if "https://www.reddit.com/r/fantasyfootball/comments/" not in submission.url:
            url = submission.url

        if (submission.link_flair_text != None):
            flair = submission.link_flair_text

        f = ff(submission.title, submission.selftext, url, flair, datecreated)
        fobjs.append(f)

    return fobjs


def add_ff_to_db(fs,connection):
    for f in fs:
            with connection.cursor() as cursor:
                #CLENSE
                sql = "Insert INTO fftest.ff (title,link,body,flair,date_posted) VALUES (%s,%s,%s,%s,%s);"
                cursor.execute(sql,(f.title, f.link, f.body, f.flair, f.date))
                connection.commit()

    connection.close()


def utc_to_datetime(utcc):
    return datetime.fromtimestamp(utcc)


def main():
    print("sensetive data goes here")

if __name__ == "__main__":
    main()


