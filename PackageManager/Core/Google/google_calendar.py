from __future__ import print_function
import httplib2
import os
import settings

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow()
    date2 = now - datetime.timedelta(days=7)
    eventsResult = service.events().list(
        calendarId='0usu2st0ea98o9olut3ntus8eo@group.calendar.google.com', timeMin=date2.isoformat() + 'Z', maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        eventdict = {}

        eventdict["SentDateTime"] = event['start'].get('dateTime', event['start'].get('date'))

        eventdatalist = event['description'].split(chr(10))
        #Outgoing Call: Phone Number, Name, Duration, Location Accuracy
        #Incoming Call: Phone Number, Name, Duration
        #Outgoing SMS: Address/Number, Message
        #Incoming SMS: Address/Number, Message

        for column, items in enumerate(eventdatalist):
            itemlist = items.split(":")
            if len(itemlist) == 2:
                if itemlist[0] == "Duration":
                    durations = itemlist[1].split(" ")
                    etime = 0
                    for column, idur in enumerate(durations):

                        if idur == "hours": etime += int(durations[column - 1])*3600
                        if idur == "minutes": etime += int(durations[column -  1])*60
                        if idur == "seconds": etime += int(durations[column - 1])

                    eventdict[itemlist[0]] = etime
                if itemlist[0] == "Message":
                    eventdict["Message"] = eventdatalist[column+1]
                else:
                    eventdict[itemlist[0]] = itemlist[1]

            if len(itemlist) == 1 and column ==0:
                eventdict["Event Type"] = itemlist[0]

            try:
                eventdict["Location"] = event['location']
            except:
                pass

        print(eventdict)
        CommunicationDict = {}
        CommunicationDict["Outgoing SMS"] = 1
        CommunicationDict["Incoming SMS'"] = 2
        CommunicationDict["Outgoing call"] = 3
        CommunicationDict["Incoming call"] = 4



        newcommunication = esession.query(CommunicationData).filter_by(SentDataTime=now).first()
        if newcommunication is None:
            esession.begin()
            newcommunicationtext = CommunicationBodyText(BodyText=eventdict["Message"])
            esession.add(newcommunicationtext)
            esession.commit()

            esession.begin()
            newcommunication = CommunicationData(CommunicationType=CommunicationDict[eventdict["Event Type"]],
                                                 From_name=eventdict["Address/Number"],
                                                 To_name="",
                                                 SentDateTime=eventdict["SentDateTime"],
                                                 Duration=eventdict["Duration"],
                                                 ReceivedDateTime="",
                                                BodyText_id="",
                                                Comments="",
                                                Tags="")
        esession.add(newcommunication)
        esession.commit()

if __name__ == '__main__':
    main()