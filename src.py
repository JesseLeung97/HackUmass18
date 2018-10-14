import os
import praw
import re
import time
import random

# A Reddit bot based on Skeleseer from The Last of Us.  Designed by /u/generic_panda as a HackUMass VI project.


# List to contain possible skeleseer answers
from praw import reddit, Reddit

ans_list = ['Seems dreadfully unlikely.',
            'I feel it in my bones.',
            'Your chances are dismal.',
            'The spirits are quiet.',
            'The answer is in limbo.',
            'I am dead certain it is true.',
            'The spirit nods yes.',
            'The signs aren\'t clear.',
            'Not in this existence.']


# List to contain IDs for comments which have already been replied to


# Number of total replies
numreplies = 0

# create a list
if not os.path.isfile("replied_to.txt"):
    replied_to = []

else:
    with open("replied_to.txt", "r") as f:
        replied_to = f.read()
        replied_to = replied_to.split("\n")
        replied_to = list(filter(None, replied_to))


# Authenticates the Reddit bot using given credentials
def authenticate():
    print('authentication in progress...')
    reddit = praw.Reddit(client_id='XXXXXXXX',
                         client_secret='XXXXXXXX',
                         password='XXXXXXXX',
                         user_agent='<terminal:generic_panda_bot:0.0.1 (by: /u/generic_panda)>',
                         username='generic_panda_bot')
    botname = str(reddit.user.me())
    print('successfully authenticated: ' + botname)
    return reddit


# Keeps track of the number of replies the bot has posted
def num_replies():
    global numreplies
    numreplies += 1
    return numreplies


# Generates a random integer then selects the corresponding answer from the list
def ans_generator():
    rand = random.randint(0, 7)
    ans = ans_list[rand]
    return ans


# Check's if an ID has already been replied to
def check_replied(comment):
    global replied_to
    if comment.id in replied_to:
        return True
    else:
        return False


# Recognizes a given string to summon skeleseer
def summon_skeleseer(commentbody):
    if 'Skeleseer:' in commentbody:
        return True
    else:
        return False


# Posts a reply randomly chosen from the list
def post_reply(comment):
    ans = ans_generator()
    comment.reply(ans)
    return


# Checks for new comments and then responds appropriately
def run_gpb(reddit):
    print('Generic_panda_bot is currently running...')
    for comment in reddit.subreddit('GenericPandaTest').stream.comments():
        if comment.id not in replied_to:
            text = comment.body
            if summon_skeleseer(text):
                post_reply(comment)
                num_replies()
                replied_to.append(comment.id)
                for x in range(len(replied_to)):
                    print('List of comment IDs that have been replied to: ' + replied_to[x])
                print('Number of comments that have been replied to: ', num_replies())
        else:
            continue


with open("replied_to.txt", "w") as f:
    for comment_id in replied_to:
        f.write(comment_id + "\n")


# Runs the authentication process, the monitoring process, and posts comments
def main():
    bot = authenticate()
    while True:
        run_gpb(bot)


