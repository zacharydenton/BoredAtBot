#!/usr/bin/env python

import urllib, urllib2, re, mechanize
from BeautifulSoup import BeautifulSoup

class BoredAtBakerBot:

    baseURL = "https://boredatbaker.com"
    br = mechanize.Browser()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logIn()
        
    def logIn(self):
        self.br.open(self.baseURL)
        self.br.select_form(name="d_q")
        self.br["d_x"] = self.username
        self.br["d_y"] = self.password
        self.br.submit()
    
    def feed(self):
        feed = []
        html = self.br.response().read()
        soup = BeautifulSoup(html)

        for post in soup.findAll('div', 'post'):
            content = post.find('span', 'post_text')
            if content: feed.append((post['id'], content.renderContents()))
            
        return feed
    
    def post(self, message):
        self.br.select_form(nr=1)
        print self.br.form
        self.br["post_text"] = message
        self.br.submit()
                
# Enter username and password:
testBot = BoredAtBakerBot("eleazor", "qweasd")
print testBot.feed()
testBot.post("I'm BORED AT HACKER CLUB!")