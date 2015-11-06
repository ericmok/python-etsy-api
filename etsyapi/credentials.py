import os.path
from requests_oauthlib import OAuth1Session, OAuth1
import requests
import yaml
import json
from urlparse import parse_qs


from endpoints import ETSY_BASE, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL


def load_credentials_from_file():
    '''
    Loads YAML file with credentials: client_key, client_secret, resource_owner_key, resource_owner_secret.
    '''
    credentials = None

    if (os.path.isfile('credentials')):
        f = open('credentials')
        credentials = yaml.load(f)
        f.close()
        return credentials
    else:
        raise Exception("No credentials provided. Required client_key and client_secret")


def fetch_request_for_credentials(credentials):
    '''
    Takes credentials and populates with resource_owner_key, resource_owner_secret, and login_url
    '''
    oauth = OAuth1(credentials['client_key'], credentials['client_secret'])    
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    tokens = parse_qs(r.content)
    
    credentials['resource_owner_key'] = tokens.get('oauth_token')[0]
    credentials['resource_owner_secret'] = tokens.get('oauth_token_secret')[0]
    credentials['login_url'] = tokens.get('login_url')[0]

    return credentials


def verify_credentials(credentials, verifier):
    '''
    Take populated credentials with verifier and obtain access.
    '''
    credentials['verifier'] = verifier

    oauth = OAuth1(client_key=credentials['client_key'],
                   client_secret=credentials['client_secret'],
                   resource_owner_key=credentials['resource_owner_key'],
                   resource_owner_secret=credentials['resource_owner_secret'],
                   verifier=verifier)

    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)

    access = parse_qs(r.content)

    try:
        credentials['resource_owner_key'] = access.get('oauth_token')[0]
        credentials['resource_owner_secret'] = access.get('oauth_token_secret')[0]
        credentials['verfied'] = True
    except:
        raise Exception('There was a problem with verfication')

    return credentials


def create_oauth(credentials):
    return  OAuth1(client_key=credentials['client_key'],
                   client_secret=credentials['client_secret'],
                   resource_owner_key=credentials['resource_owner_key'],
                   resource_owner_secret=credentials['resource_owner_secret'])


def fetch_self(oauth):
    '''
    Makes a request to obtain UserID for SELF as implied by OAuth credentials.
    '''    
    r = requests.get(ETSY_BASE + 'users/__SELF__', auth=oauth)
    r = (json.loads(r.content))

    user_id = r['results'][0]['user_id']
    login_name = r['results'][0]['login_name']

    return user_id, login_name