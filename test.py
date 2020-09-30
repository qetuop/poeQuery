import poeq
from time import sleep
import json

if __name__ == '__main__':
    config = json.loads(open('config.json').read())
    account = config['account']
    getStandard = config['getStandard']
    league = config['league']
    poesessid = config['poesessid']
    SLEEP = config['sleep']

    # print(poeq.getLeagues())
    poeq.setup(league, account, poesessid)
    # poeq.setup('Standard', poeq.ACCOUNT, poeq.POESESSID)
    # poeq.getAccount(poeq.ACCOUNT)

    out = poeq.getCharacterInventory('EwreckDefunct')
    charDict = poeq.readFromFile('EwreckDefunct')
    print(charDict)
    # poeq.dumpToFile('SalWrendMkII.json', out)

    # out = poeq.getAllCharacterInventory(poeq.ACCOUNT)
    # poeq.dumpToFile('allCharacters.json', out)

    #accountDict = poeq.getAccount(poeq.ACCOUNT)
    # poeq.getLeague(poeq.ACCOUNT,poeq.LEAGUE)
    #accountDict = poeq.readFromFile('qetuop.json')
    #print(accountDict['Account'])

    #leagues = list((map(lambda x: x['name'], accountDict['leagues'])))
    #print(leagues)

    #print(accountDict['leagues']['Standard'])
    #chars = list((map(lambda x: x['name'], accountDict['leagues'][0]['characters'])))
    #print(chars)

    # league = 'Blight'
    # out = poeq.getStash(league)
    # poeq.dumpToFile('%s.json'%league, out)

    # print(poeq.getNumTabs())
    # print(poeq.getCharacters())

    # print(poeq.getStashTab(1))
    # stash = poeq.getStashTabs()
    '''
    SLEEP = 1.0
    for i in range(1,100):
        #print("{}:{}".format(i,poeq.getNumTabs()))
        print(i,poeq.getStashTab(1))
        #sleep(SLEEP)
    '''
