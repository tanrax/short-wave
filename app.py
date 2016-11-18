#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_script import Manager
from News import News
import requests
import configparser
import os

config = configparser.ConfigParser()
config.read('.env')
for key, value in config.items('DEFAULT'):
    os.environ.setdefault(key.upper(), value)


app = Flask(__name__)
manager = Manager(app)


def generate_email():
    my_news = News()
    data = dict()
    data['static_url'] =  os.environ.get('STATIC_URL')
    max_news = int(os.environ.get('MAX_NEWS'))
    if os.environ.get('ENABLE_HACKER_NEWS') == 'yes':
        data['hacker_news'] = my_news.hacker_news(max_news)['hacker_news']
    if os.environ.get('ENABLE_REDDIT') == 'yes':
        subreddits = os.environ.get('REDDIT_SUBREDDITS').split(',')
        for key, subreddit in enumerate(subreddits):
            subreddits[key] = subreddit.strip()
        data['reddit'] = my_news.reddit(max_news, subreddits)['reddit']
    htmlEmail = render_template('email.html', data=data)
    return htmlEmail

@manager.command
def send():
    send_simple_message(generate_email())
    return 'OK'

@manager.command
def debug():
    return generate_email()

def send_simple_message(html):
    return requests.post(
        os.environ.get('GUNMAIL_URL'),
        auth=("api", os.environ.get('GUNMAIL_API') + '/messages'),
        data={"from": os.environ.get('EMAIL_FROM'),
              "to": [os.environ.get('EMAIL_TO')],
              "subject": os.environ.get('SUBJECT'),
              "html": html})


if __name__ == "__main__":
    manager.run()
