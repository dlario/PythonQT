import gdata
import gdata.gauth
import gdata.contacts.client
import json
import requests

GOOGLE_CLIENT_ID = 'GOOGLE_CLIENT_ID'  # Provided in the APIs console
GOOGLE_CLIENT_SECRET = 'GOOGLE_CLIENT_SECRET'  # Provided in the APIs console
ACCESS_TOKEN = 'ACCESS_TOKEN' # given from a prior OAuth2 workflow, along with userID and refreshToken
REFRESH_TOKEN = 'REFRESH_TOKEN'

# GData with access token
token = gdata.gauth.OAuth2Token(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope='https://www.google.com/m8/feeds',
    user_agent='app.testing',
    access_token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN)

contact_client = gdata.contacts.client.ContactsClient()
token.authorize(contact_client)

feed = contact_client.GetContacts()

for entry in feed.entry:
  entry.title.text
  for e in entry.email:
    e.address

# JSON with access token
r = requests.get('https://www.google.com/m8/feeds/contacts/default/full?access_token=%s&alt=json&max-results=50&start-index=0' % (access_token))
data = json.loads(r.text)
print(data)