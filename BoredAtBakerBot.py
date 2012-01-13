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
        self.br.open(self.baseURL)
        html = self.br.response().read()
        soup = BeautifulSoup(html)

        feed = []
        for post in soup.findAll('div', 'post'):
            content = post.find('span', 'post_text')
            if content: feed.append((post['id'], content.renderContents()))
            
        return feed
    
    def post(self, message):
        self.br.open(self.baseURL)
        self.br.select_form(nr=1)
        self.br["post_text"] = message
        self.br.submit()
    
    def checkin(self, id):
        self.br.open(self.baseURL + "/actions/checkin_location.php?lid=" + str(id))
        html = self.br.response().read()
        if html.find('<div id="msg" class="grid_12 error center">You\'ve already checked-in recently! Try again later :)</div>') >= 0:
            print "YOU'VE ALREADY CHECKED IN RECENTLY!!"
        
                
# Enter username and password:
testBot = BoredAtBakerBot("eleazor", "qweasd")
testBot.checkin(178) # Check into AD
testBot.post("Unsteamy Nonhookup @ later")