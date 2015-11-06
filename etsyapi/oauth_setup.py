import json
from credentials import *


credentials = load_credentials_from_file()

if (credentials.get('verified', False)):

    print('Welcome to First Time Setup\n')
    fetch_request_for_credentials(credentials)

    print('Visit the following address to verify this application:\n%s\n' % credentials['login_url'])

    verifier = raw_input('Input the verifier: ')
    verify_credentials(credentials, verifier)


    oauth = create_oauth(credentials)

    user_id, login_name = fetch_self(oauth)

    # Write credentials
    f = open('credentials', 'w')
    credentials['user_id'] = user_id
    credentials['login_name'] = login_name
    f.write(yaml.dump(credentials, default_flow_style=False))
    f.close()

    print('\nSetup Successful!\n')
    print(' login_name: %s\n user_id: %s\n' % (login_name, user_id))

else: 
    print('\nSetup has already run\n')
    print('Credentials are already populated')
    print('To reset, erase all keys except for client_key and client_secret\n')

    print(' login_name: %s\n user_id: %s\n' % (credentials['login_name'], credentials['user_id']))