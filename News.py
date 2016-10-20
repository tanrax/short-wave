#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import requests
import praw


class News(object):

    def __init__(self):
        self.data = dict()
        # Statics
        self.URL_API_HACKER_NEWS_TOP = 'https://hacker-news.firebaseio.com' \
                                       '/v0/topstories.json?print=pretty'
        self.URL_API_HACKER_NEWS_ITEM = 'https://hacker-news.firebaseio.com' \
                                        '/v0/item/%s.json?print=pretty'

    def hacker_news(self, max_news):
        '''
        Hacker News
        '''
        # Get all the items
        responseIds = requests.get(self.URL_API_HACKER_NEWS_TOP).json()
        self.data['hacker_news'] = list()

        # Get data
        if responseIds:
            for key, value in enumerate(responseIds[:max_news]):
                # Get the item information
                responseItem = requests.get(
                    self.URL_API_HACKER_NEWS_ITEM % value).json()
                item = dict()
                item['title'] = responseItem['title']
                item['url'] = responseItem['url']
                self.data['hacker_news'].append(item)
        return self.data

    def reddit(self, max_news, subreddits):
        self.data['reddit'] = dict()
        r = praw.Reddit(user_agent='top_news')
        for item_sub in subreddits:
            # Title
            self.data['reddit'][item_sub] = dict()
            submissions = r.get_subreddit(item_sub).get_hot(limit=max_news)
            # Subreddits
            for key_j, submission in enumerate(submissions):
                self.data['reddit'][item_sub][key_j] = {
                    'title': submission.title,
                    'url': submission.url
                    }
        return self.data
