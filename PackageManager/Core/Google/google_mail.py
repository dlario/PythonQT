from __future__ import print_function
import pickle
import os.path
# from googleAPI.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
CLIENT_SECRET_FILE = 'credentials.json'
#https://developers.google.com/gmail/api/v1/reference/users/messages


import base64
import email
#from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GoogleMailSession():
    def __init__(self):
        super(GoogleMailSession, self).__init__()
        self.service = None
        self.loadSession()


    def loadSession(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)


    def getFolderLabels(self):
        # Call the Gmail API
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return None
        else:
            return labels


    def ListMessagesMatchingQuery(self, user_id, query=''):
      """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
      try:
        response = self.service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = self.service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages
      except (errors.HttpError):
        print('An error occurred: %s')


    def ListMessagesWithLabels(self, user_id, label_ids=[]):
      """List all Messages of the user's mailbox with label_ids applied.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

      Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
      """
      try:
        response = self.service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = self.service.users().messages().list(userId=user_id,
                                                     labelIds=label_ids,
                                                     pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages
      except (errors.HttpError):
        print ('An error occurred: %s')

    def GetMessage(self, user_id, msg_id):
        #https: // developers.google.com / gmail / api / v1 / reference / users / messages
      """Get a Message with given ID.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A Message.
      """
      try:
        message = self.service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()
        #print('Message snippet: %s' % message['snippet'])

        return message
      except (errors.HttpError):
        print('An error occurred:')

    def GetMimeMessage(self, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          msg_id: The ID of the Message required.

        Returns:
          A MIME Message, consisting of data from Message.
        """
        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id,
                                                     format='raw').execute()

            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)

            return mime_msg
        except errors.HttpError:
            print('An error occurred:')

    def GetAttachments(self, user_id, msg_id, store_dir):
      """Get and store attachment from Message with given id.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: ID of Message containing attachment.
        store_dir: The directory used to store attachments.
      """
      try:
        message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
          if part['filename']:

            file_data = base64.urlsafe_b64decode(part['body']['data']
                                                 .encode('UTF-8'))

            path = ''.join([store_dir, part['filename']])

            f = open(path, 'w')
            f.write(file_data)
            f.close()

      except (errors.HttpError):
        print ('An error occurred:')

    def PrintAllContacts(self, gd_client):
      feed = gd_client.GetContacts()
      for i, entry in enumerate(feed.entry):
        print('\n%s %s' % (i+1, entry.name.full_name.text))
        if entry.content:
          print('    %s' % (entry.content.text))
        # Display the primary email address for the contact.
        for email in entry.email:
          if email.primary and email.primary == 'true':
            print('    %s' % (email.address))
        # Show the contact groups that this contact is a member of.
        for group in entry.group_membership_info:
          print('    Member of group: %s' % (group.href))
        # Display extended properties.
        for extended_property in entry.extended_property:
          if extended_property.value:
            value = extended_property.value
          else:
            value = extended_property.GetXmlBlob()
          print('    Extended Property - %s: %s' % (extended_property.name, value))
