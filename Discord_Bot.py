# Stdlib
import random
import urllib
import re
import json as m_json
 
# 3rd party
import discord
import requests
 
 
client = discord.Client()
client.login('mycutebot@yandex.com', 'pasword_goes_here')
 
@client.event
def on_message(message):
    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello world!')
 
    m_suck = re.match(ur'!suckmy(?P<edible>\w+)', message.content)
    if m_suck:
        client.send_message(message.channel, 'mmmm {}... nomnomnom'.format(m_suck.group('edible')))
 
    ##This will search google image for some alchoholic drink name,
    ## then display that image.
    if message.content.startswith('!orderdrink'):
        #client.send_message(message.channel, 'nomnomnom')
        find_drink(client, message)
   
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
 
             
def find_drink(client, message):
    """
   Use duckduckgo to get image and abstract
   """
    #name = message[len('!orderdrink'):].strip()
    name = message.content[len('!orderdrink'):].strip()
    name = name + " drink"
    #print name
    url = "http://api.duckduckgo.com"
    params = {
        #"q": "{} drink".format(name),
        "q": u"{}".format(name),
        "format": "json",
        "pretty": 1,
    }
    #print params
    resp = requests.get(url, params=params)
    # Did it succeed? If so, parse the json and extract the data.
    # Finally, send the data to the client.
    try:
        resp.raise_for_status()
    except Exception as e:
        print u"Error searching: {}".format(e).encode('utf-8')
    else:
        try:
            doc = resp.json()
        except Exception as e:
            print u"Error decoding json: {}".format(e).encode('utf-8')
        else:
            img = doc.get('Image') or ''
            if img:
                msg = u'Your *{}* is served: {}\n'.format(name, img).encode('utf-8')
                #print msg
                client.send_message(message.channel, msg)
            else:
                msg = u"I can't find *{}* anywhere. So sad...\n".format(name).encode('utf-8')
                #print msg
                client.send_message(message.channel, msg)
            abstract = doc.get('Abstract')
            if abstract:
                msg = u'Did you know this about a *{}*?\n\n{}'.format(name, abstract).encode('utf-8')
                #print msg
                client.send_message(message.channel, msg)
            else:
                msg = u'I know nothing about *{}*. So sad...'.format(name).encode('utf-8')
                #print msg
                client.send_message(message.channel, msg)
 
           

client.run()
