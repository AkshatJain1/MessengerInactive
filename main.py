from fbchat import Client
from fbchat.models import *
import time
import getpass

'''
Purpose: To see which people are inactive on the EECS group chat
'''

client = Client(input("Enter Facebook Phone/Email: "), getpass.getpass("Enter Facebook Password: "))
gcID = "2266484600080799"
activeIDs = set()

def updateActiveIds(targetedTimestamp):
    '''
    Query the group chat for which people read messages at targetedTimestamp
    Update Active IDs by taking the union
    '''
    global activeIDs
    msgs = client.fetchThreadMessages(thread_id=gcID, limit=100, before=targetedTimestamp)
    for message in msgs:
        messageRead = set(message.read_by)
        activeIDs = activeIDs.union(messageRead)

def updateWithTimestamps():
    '''
        Update the Active User Ids dated back 9 months.
        Moves 1 month at a time to account for newly added users.
    '''
    current = int(time.time()) * 1000
    for i in range(9):
        updateActiveIds(current)
        current -= 2592000000 # go back a month

def idsToNames(idDict):
    '''
    Convert a dictionary of user information to a list of names
    '''
    nameList = []
    for id in idDict:
        user = idDict[id]
        nameList.append(user.name)
    nameList.sort()

    return nameList


if __name__ == '__main__':
    updateWithTimestamps()

    totalParticipants = set(client.fetchGroupInfo(gcID)[gcID].participants)
    inactiveIDs = client.fetchUserInfo(*totalParticipants.difference(activeIDs))

    nameList = idsToNames(inactiveIDs)
    print(len(nameList), "people have not checked the chat in the last 9 months")
    print(nameList)
    client.logout()
