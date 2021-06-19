import constants
import oauth2
import urllib.parse as urlparse
import json

# Create a consumer, which uses CONSUMER_KEY AND CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# Use the client to perform a request for the request token
# Note: The request we perform with the REQUEST_TOKEN tells the Twitter API that we have...
# ...obtained user approval to authenticate. Later, it will be used with the Oauth verifier, for the access token.
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')  # Client.request() will return a response and some content.
if response.status != 200:
    print('An error occurred getting the request token from Twitter!')

# Get the REQUEST_TOKEN parsing the query string returned.
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
# parse_qsl = parse_querystring and convert it into a dictionary.
#decode('utf-8') converts bytes into strings

# Ask the user to authorize our app and give us the pin code.
print("Go to the following site in your browser:")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_TOKEN_URL, request_token['oauth_token']))

# {}?oauth_token={}.format() -> {constants.AUTHORIZATION_TOKEN_URL}?oauth_token={request_token['oauth_token']}
# www.ourwebsite.com "log in with twitter button"
# user presses "sign in" or "authorize"
# Twitter sends them back to e.g. www.ourwebsite.com/auth
# We get that auth code + request token -> send the codes to twitter -> twitter gives us an access token

oauth_verify = input("What is the PIN?")

# Create a Token object which contains the request token, and the verifier
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verify)

# Create a client with our consumer (our app) and the newly created (and verified) token
client = oauth2.Client(consumer, token)

# Ask Twitter for an access token, and Twitter knows it should give it to us because weve verified the request token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)

# Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
# Client represents the user that logged in and gave our app access to their Twitter account
authorized_client = oauth2.Client(consumer, authorized_token)

# Make Twitter API calls!
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
if response.status != 200:
    print('An error occured when searching!')
tweets = json.loads(content.decode('utf-8'))

statuses = tweets['statuses'] #list of dictionaries
for item in statuses:
    print(item['text'])

