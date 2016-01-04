
# Stdlib
import random
import urllib
import json as m_json
import re
import time
import sqlite3

# 3rd party
import discord
import requests
import traceback
import cleverbot
 
USERNAME = ''
PASSWORD = ''

client = discord.Client()
client.login(USERNAME, PASSWORD)

 
@client.event
def on_message(message):
    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello world!')
     
    m_suck = re.match(ur'!suckmy(?P<edible>\w+)', message.content)
    if m_suck:
        client.send_message(message.channel, 'mmmm {}... nomnomnom'.format(m_suck.group('edible')))
 
    #Searches DuckDuckGo for images after the "!orderdrink" keyword
    if message.content.startswith('!orderdrink'):
         find_drink(client, message)

    ##Makes a hangouts
    if message.content.startswith("!hangouts"):
        client.send_message(message.channel, 'https://talkgadget.google.com/hangouts/_/uf3oaihbt24csza5424mw7a7bua?authuser=0&hl=en')
    
    #Prints someone's avatar
    if message.content.startswith("!avatar"):
        printAvatar(message)
        
    #gets the numbe of users on the server
    if message.content.startswith('!8ball'):
        eightball(message)                

    #Sends a query to cleverbot.  Prints a responce
    if message.content.startswith('!cleverbot'):
        runCleverbot(message)
        
    #Use TTS to send a message
##    if message.content.startswith('!singsong'):
##        singSong(message)

##########################################################
## Housekeeping Functions ################################
##########################################################
##    #searches the bio database for the bio, prints bio
##    if message.content.startswith('!bio'):
##        printBio(client, message)
##
    #Set's a user's bio, limit is 256 chars
##    if message.content.startswith('!setbio'):
##        setBio(message)
##        
##    #Set's a user's gender and sexuality
##    if message.content.startwith('!setpreferences'):
##        setPreferences(message)
        
    if message.content.startswith('!register'):
        registerUser(message)
        
##########################################################
##########################################################
##########################################################
        
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


    
###################################################################
## Fun Functions ##################################################
###################################################################

def singSong(message):
    statement = message.content[len('!singsong'):].strip()
    client.send_message(message.channel, statement, 1, 1)


    
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

def eightball(message):
    if len(message.content) > 0:

        output_word_bank = ['It is certain', 'Yes, but you will be on your period', \
                            'Without a doubt', 'Yup, I\'ll suck your dick while it happens.', \
                            'You may rely on it', 'As I see it, yes', \
                            'Most likely', 'Outlook good', 'Yes', \
                            'Signs point to yes', 'Reply hazy try again' \
                            'Ask again later', 'Better not tell you now', \
                            'As If, Ask Me If I Care', \
                            'Don\'t count on it', 'My reply is no', 'You\'ve Got To Be Kidding...', \
                            'No, But At Least I Love You', 'Very doubtful', \
                            'Cocks, Your future is full of cocks.', 'Naaaaah Braaaaa', \
                            'Only if you do it with me <3', 'Why don\'t you forget about it and just cuddle me.',\
                            'Yes, but a genie will be the one deciding how it comes true.', \
                            'Yes, and you have beautiful nails :D', 'idk', \
                            'Error: 404 Future not found.' ]
        random_num = random.randint(0, len(output_word_bank)-1)
        client.send_message(message.channel, output_word_bank[random_num])
    else:
        client.send_message(message.channel, 'You didn\'t enter a question.')

def runCleverbot(message):      
    try:
        cb1 = cleverbot.Cleverbot()  
        statement = message.content[len('!cleverbot'):].strip()
        client.send_message(message.channel, '{} > '.format(message.author.mention()) + cb1.ask(statement))
        time.sleep(.1)
        return
    except Exception: #probably a unicode exception
        client.send_message(message.channel, "Oh no! You broke DommeBot. ;-;")
        
    else:
        client.send_message(message.channel, "Cleverbot/DommeBot is broke. ;-;")
        return
        

def printAvatar(message):
    if len(message.mentions) > 0:
        for user in message.mentions:
            if user.avatar_url() != "":
                client.send_message(message.channel, "<@" + user.id + ">'s avatar is " + user.avatar_url())
            else:
                client.send_message(message.channel, user.name + " doesn't have an avatar.")
    else:
        client.send_message(message.channel, message.author.mention() + " You need to mention the user you want to get avatar from.")

            
###################################################################
###################################################################
###################################################################

'''
Query SQL database, if there's no entry for that user, create a bio
entry, if there's an entry for that user, then delete that entry
and replace with a new entry
'''
##def setBio(message):
##

#The user needs to type !register gender sexualtiy pronouns
#   If this is the first time entering, update the date and time
#ex: !register purple cocks apple/oranges
#   will get gender = purple, sexualtiy = cocks, pronouns = apples/oranges
def registerUser(message):
    
    #used to cut the ends off the string if ends are attached
    check_format = message.content[len('!register'):].strip()
    print check_format
    #get the gender from the start of the string
    gender = re.match(r'(^[a-z]*)', check_format)
    print gender
    #replace gender with ''
    new_string = re.sub(r'(^[a-z]*)(\s{1,1})', '', check_format)
    print new_string
    #get sexualtiy
    sexualtiy = re.match(r'(^[a-z]*)', new_string)
    print sexualtiy
    new_string = re.sub(r'(^[a-z]*)(\s{1,1})', '', new_string)
    print new_string
    pronouns = re.match(r'^((([a-z]|(\/))*))', new_string)
    print pronouns

    client.send_message(message.channel, message.author.id)
    client.send_message(message.channel, gender.group(0))
    client.send_message(message.channel, sexualtiy.group(0))
    client.send_message(message.channel, pronouns.group(0))
    print str(gender.group(0))
    print type(sexualtiy.group(0))
    print type(pronouns.group(0))
    client.send_message(message.channel, "done")

    print type(message.author.name)
    print message.author.name
    name_insterted = (message.author.name).encode('ascii', 'ignore')


##    #########
##    #update stuff in database
##    sqlite_file = 'C://Users//Rawr//Desktop//Discord_Bot//TransSexDB.sqlite'
##    table_name = "main_table"
##    name_column = "Names"
##    id_column = "ID_Number"
##    gender_column = "Gender"
##    pronoun_column = "pronouns"
##    sexualtiy_column = "sexuality"
##    
##
##    # Connecting to the database file
##    conn = sqlite3.connect(sqlite_file)
##    c = conn.cursor()
##    #check and see if the user is already registered.  If registered,
##    #use the 'update' command, else, use the 'INSERT OR IGNORE INTO'
##    #command.
##    c.execute(u"SELECT * FROM {tn} WHERE {idf}={my_id}".\
##              format(tn=table_name, idf=id_column, my_id=message.author.id))
##    id_exists = c.fetchone()
##    print id_exists
##    if id_exists:
##        client.send_message(message.channel, "ERROR 1")
##        #if the ID exists, use the UPDATE command
##    else:
##        #if the ID doesn't exist, use the INSERT OR IGNORE INTO command
##        client.send_message(message.channel, "This thing doesn't exist, adding to db")
##        name_insterted = (message.author.name).encode('ascii', 'ignore') #strips unicode
####        
####        apple = u"INSERT INTO {tn} ({idf}, {cn}) VALUES ({uniID}, {bbb})".\
####            format(tn=table_name, idf=id_column, cn=name_column, uniID=message.author.id, bbb=name_insterted)
####       
##        cocks = (message.author.id, name_insterted, gender.group(0), sexualtiy.group(0), pronouns.group(0))
##        c.execute("INSERT INTO main_table (ID_Number, Names, Gender, sexuality, pronouns) VALUES(?, ?, ?, ?, ?)", cocks)
##        
##
####    client.send_message(message.channel, "Should exist now")
####    c.execute(u'SELECT ({coi}) FROM {tn} WHERE {cn}={uniID}'.\
####            format(coi=name_column, tn=table_name, cn=id_column, uniID=message.author.id))
####    all_rows = c.fetchall()
####    print('2):', all_rows)
##    client.send_message(message.channel, "done")
##    
##    conn.commit()
##    conn.close()
###################################################################
###################################################################
###################################################################


 
client.run()      



##
##def send_unicode_message(self, destination, content, mentions=True, tts=False):
##        """Sends a message to the destination given with the content given.
##
##        The destination could be a :class:`Channel`, :class:`PrivateChannel` or :class:`Server`.
##        For convenience it could also be a :class:`User`. If it's a :class:`User` or :class:`PrivateChannel`
##        then it sends the message via private message, otherwise it sends the message to the channel.
##        If the destination is a :class:`Server` then it's equivalent to calling
##        :meth:`Server.get_default_channel` and sending it there. If it is a :class:`Object`
##        instance then it is assumed to be the destination ID.
##
##        .. versionchanged:: 0.9.0
##            ``str`` being allowed was removed and replaced with :class:`Object`.
##
##        The content must be a type that can convert to a string through ``str(content)``.
##
##        The mentions must be either an array of :class:`User` to mention or a boolean. If
##        ``mentions`` is ``True`` then all the users mentioned in the content are mentioned, otherwise
##        no one is mentioned. Note that to mention someone in the content, you should use :meth:`User.mention`.
##
##        If the destination parameter is invalid, then this function raises :exc:`InvalidArgument`.
##        This function raises :exc:`HTTPException` if the request failed.
##
##        :param destination: The location to send the message.
##        :param content: The content of the message to send.
##        :param mentions: A list of :class:`User` to mention in the message or a boolean. Ignored for private messages.
##        :param tts: If ``True``, sends tries to send the message using text-to-speech.
##        :return: The :class:`Message` sent.
##        """
##
##        channel_id = self._resolve_destination(destination)
##
##        #content = str(content)
##        content = unicode(content)
##        mentions = self._resolve_mentions(content, mentions)
##
##        url = '{base}/{id}/messages'.format(base=endpoints.CHANNELS, id=channel_id)
##        payload = {
##            'content': content,
##            'mentions': mentions
##        }
##
##        if tts:
##            payload['tts'] = True
##
##        response = requests.post(url, json=payload, headers=self.headers)
##        log.debug(request_logging_format.format(response=response))
##        utils._verify_successful_response(response)
##        data = response.json()
##        log.debug(request_success_log.format(response=response, json=payload, data=data))
##        channel = self.get_channel(data.get('channel_id'))
##        message = Message(channel=channel, **data)
##        return message
##
##