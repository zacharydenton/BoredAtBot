#!/usr/bin/env python

import urllib, urllib2, re, mechanize
from BeautifulSoup import BeautifulSoup

class BoredAtBakerBot:

    baseURL = "https://boredatbaker.com"
    loginForm = "d_q"
    br = mechanize.Browser()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logIn()
        
    def logIn(self):
        self.br.open(self.baseURL)
        self.br.select_form(name=self.loginForm)
        self.br["d_x"] = self.username
        self.br["d_y"] = self.password
        self.br.submit()
    
    def printFeed(self):
        html = self.br.response().read()
        soup = BeautifulSoup(html)

        for post in soup.findAll('div', 'post'):
            print post['id']
            content = post.find('span', 'post_text')
            if content: print content.renderContents()
        
# Enter username and password:
testBot = BoredAtBakerBot("username", "password")
testBot.printFeed()