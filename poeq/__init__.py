import requests
import json
from time import sleep
import logging
from pathlib import Path


SLEEP = 1.1

league = None
account = None
poesessid = None
cookies = None

def setup(l, a, p):
    global league, account, poesessid, cookies
    league = l
    account = a
    poesessid = p

    cookies = dict(POESESSID='%s' % poesessid)

'''
Code	Text	Description
200	OK	The request succeeded.
400	Bad Request	The request was invalid. Check that all arguments are in the correct format.
404	Not Found	The requested resource was not found.
429	Too many requests	You are making too many API requests and have been rate limited.
500	Internal Server Error	We had a problem processing your request. Please try again later or post a bug report.
'''
def grabData( url ):
    wait = SLEEP

    #sleep(wait)
    r = requests.get(url, cookies=cookies)
    while (r.status_code == 429 ):
        print('RATE LIMTED....WAITING %s sec before retrying'%wait)
        r = requests.get(url, cookies=cookies)
        wait = wait*2
        sleep(wait)

    return r.json()


def checkForError(jresp):
    error = None
    print(jresp)
    if ( 'error' in jresp ):
        return(jresp['error']['code'], jresp['error']['message'])

'''
    [{"id":"Standard","realm":"pc","description":"The default game mode.","registerAt":"2019-09-06T19:00:00Z",
    "url":"http:\/\/pathofexile.com\/forum\/view-thread\/71278","startAt":"2013-01-23T21:00:00Z","endAt":null,
    "delveEvent":true,"rules":[]},...]
    '''
def getLeagues():
    r = requests.get('https://www.pathofexile.com/api/leagues')
    url = 'https://www.pathofexile.com/api/leagues'
    out = grabData(url)
    return out

# ["Standard", "Hardcore",...]
def getLeagueNames():
    allLeagues = getLeagues()

    leagues = []
    for league in allLeagues:
        leagues.append(league['id'])

    return leagues


def getNumTabs(league):
    url = 'https://pathofexile.com/character-window/get-stash-items?league=%s&accountName=%s' %(league,account)

    #cookies = dict(POESESSID='de4c695e9a693a94b563a1727233c7b7')
    #cookies = dict(POESESSID='d')  # error
    #print(url)
    r = requests.get(url, cookies=cookies)

    # checkForError(r.json())
    tabs = None
    try:
        tabs = r.json()['numTabs']
    except:
        tabs = 'error'

    #return (r.status_code, r.json()) #tabs
    return tabs

'''
    [{"name": "StrummBrand", "league": "Standard", "classId": 5, "ascendancyClass": 1, "class": "Inquisitor",
      "level": 94, "experience": 2660312216}, ... ]
      '''
def getCharacters(account):
    # can't do by league, at least don't know how
    url = ('http://pathofexile.com/character-window/get-characters?accountName=%s' %account) # requests.Response
    out = grabData(url)
    return out

'''
{"items":[{"verified":false,
...
"inventoryId":"MainInventory"}],
"character":{"name":"SalWrendMkII","league":"Blight","classId":6,"ascendancyClass":2,"class":"Trickster","level":91,"experience":2119008055,"lastActive":true}}
'''
def getCharacterInventory(charName):
    url = 'https://pathofexile.com/character-window/get-items?character=%s'%charName
    out = grabData(url)
    print(out)
    dumpToFile('%s.json' % charName, out)
    return out

def getAllCharacterInventory(account):
    out = []
    chars = getCharacters(account)
    for char in (map(lambda x: x['name'], chars)):
        out.append(getCharacterInventory(char))

    return out


def getStashTab(league, tabNum):
    url = 'https://pathofexile.com/character-window/get-stash-items?league=%s&accountName=%s&tabIndex=%s' \
          % (league, account, tabNum)
    out = grabData(url)
    print(tabNum,out)
    return out

def getStash(league):
    stash = []
    for i in range(0,getNumTabs(league)):
        stash.append(getStashTab(league, i))

    dumpToFile('%s.json' % league, stash)
    return stash

def getLeague(account, league):
    leagueDict = {'name': league, 'characters': [], 'stash': []}

    # only want the ones for this league
    chars = getCharacters(account)
    filteredChars = list(filter(lambda x: (x['league']==league), chars))
    for char in (map(lambda x: x['name'], filteredChars)):
        charDict = {}
        #print(char)
        charInv = getCharacterInventory(char)
        charDict[char] = charInv
        leagueDict['characters'].append(charDict)

    #print(leagueDict['characters'][1])

    # get all stash
    leagueDict['stash'] = getStash(league)
    return leagueDict



def getAccount(account):
    accountDict = {'account' : account, 'leagues' : []}

    leagues = getLeagues()
    for league in (map(lambda x: x['id'], leagues)):
        print(league)
        accountDict['leagues'].append(getLeague(account, league))

    dumpToFile('%s.json' % account, accountDict)
    return accountDict



def dumpToFile(fileName, data):
    p = Path('jsonData')
    p.mkdir(exist_ok=True)
    path = Path.cwd() / 'jsonData' / fileName

    with open(path, 'w') as file:
        json.dump(data, file, sort_keys=True, indent=4)

def readFromFile(fileName):
    path = Path.cwd() / 'jsonData' / (fileName +'.json')

    with open(path, 'r') as file:
        return json.load(file)
