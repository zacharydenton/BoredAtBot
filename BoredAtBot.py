#!/usr/bin/env python

import os
import re
import time
import random
import pickle
import urllib
import urllib2
import mechanize
import lxml.html

class PandoraBot(object):
    def __init__(self, botid):
        self.api = "http://www.pandorabots.com/pandora/talk-xml"
        self.botid = botid

    def respond_to(self, words, conversation_id=None):
        params = urllib.urlencode({
            'botid': self.botid,
            'input': words,
            'custid': conversation_id
        })
        response = urllib2.urlopen(self.api, params).read()
        doc = lxml.html.fromstring(response)
        reply = doc.xpath('//that')[0].text_content()
        return reply

class BoredAtBakerBot(mechanize.Browser):

    base_url = "https://boredatbaker.com"

    def __init__(self, username, password):
        mechanize.Browser.__init__(self)
        cj = mechanize.LWPCookieJar()
        self.set_cookiejar(cj)
        self.set_handle_equiv(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        self.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.open(self.base_url)

        self.username = username
        self.password = password
        self.login()

        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
        mechanize.install_opener(opener)

    def goto(self, url, refresh=False):
        if self.geturl() != url or refresh:
            return self.open(url)
        else:
            return self._response
        
    def login(self):
        self.goto(self.base_url)
        self.select_form(name="d_q")
        self["d_x"] = self.username
        self["d_y"] = self.password
        self.submit()

    def feed(self):
        self.goto(self.base_url + "/page")
        doc = lxml.html.fromstring(self.response().read())
        for post in doc.cssselect(".post_text"):
            postid = post.getnext().getnext().get('id').replace('reply', '')
            yield postid, post.text_content()
    
    def post(self, message):
        self.goto(self.base_url)
        self.select_form(nr=1)
        self["post_text"] = message
        self.submit()

    def reply_to(self, postid, message):
        params = urllib.urlencode({
            'post_parent_id': postid,
            'snId': 0,
            'post_text': message
        })
        mechanize.urlopen(self.base_url + "/actions/post.php", params)
    
    def check_in(self, id):
        self.goto(self.base_url + "/actions/checkin_location.php?lid=" + str(id))
        html = self.response().read()
        return html.find('<div id="msg" class="grid_12 error center">You\'ve already checked-in recently! Try again later :)</div>') == -1

def main():
    bot = BoredAtBakerBot("eleazor", "qweasd")
    eve = PandoraBot("a9481f8c7e347656")

    # cache
    cache = os.path.expanduser("~/.boredcache")
    try:
        seen = pickle.load(open(cache))
    except:
        seen = set()
        pickle.dump(seen, open(cache, 'wb'))

    for postid, post in bot.feed():
        if postid in seen: continue
        response = eve.respond_to(post)
        bot.reply_to(postid, response)
        print "they said: " + post
        print "i said: " + response
        print
        seen.add(postid)
        pickle.dump(seen, open(cache, 'wb'))
        time.sleep(42)

if __name__ == "__main__": main()
