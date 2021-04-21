"""
######################################################################################################################
Title: Onboard New Users
Description: This script allows you to easily onboard new users to your portal environment by generating usernames
cross-checked with existing users, randomized passwords (code excluded), and updating a CSV of credentials.
#######################################################################################################################
"""

# Libraries
from arcgis.gis import GIS, Item
from arcgis.env import active_gis
import pandas as pd
from random import *
import sys

# Portal login credentials (portal url, username, password). Credentials are only required for the portals you are interacting with.
por_dict = {'portal1':{'url':"",   'user':"", 'pass':""},
            'portal2':{'url':"",   'user':"", 'pass':""},
            'portal3':{'url':"",   'user':"", 'pass':""}}

# Attempts to login to the portals
def setPortal(name):
    print(f"\n* Attempting to login to {por_dict[name]['url']}")
    try:
        port = GIS(por_dict[name]['url'], por_dict[name]['user'], por_dict[name]['pass'], verify_cert=True)
        print(f"*** Logged into {por_dict[name]['url']} as: " + port.properties.user.username)
        return port
    except:
        print(f"*** Failed to login to {por_dict[name]['url']} as: " + port.properties.user.username)

# Generate a password. Code excluded.
def generatePassword():
    return 'fake_password'

# Generate a username based on first and last name, cross-checking with current usernames
def generateUsername(fn,ln,existing_users):
    print(f'\n* Generating username for {fn} {ln}.')
    uname = fn[0]+ln
    other_count = 1
    while len(uname) < 6:
        uname = fn[:other_count]+ln
        other_count += 1
    count = 2
    while uname in existing_users:
        print("Username taken. Generating new one.")
        uname = fn[0]+ln+str(count)
        count += 1
    print('*** Username generated.')
    return uname

# Main function
def main(users_file,gis_abr):

    # import user list, set environment, create list of existing users
    print('\n* Importing list of new users to add.')
    try:
        users = pd.read_csv(users_file)
        if {'Email','First Name','Last Name','Groups','Username', 'Password'}.issubset(users.columns):
            print('*** Imported file contains the necessary columns.')
        else:
            print('*** ERROR: Imported file has an invalid format. The required columns are: Email, First Name, Last Name, User Type, Role, Groups, Username, and Password.')
            sys.exit(1)
    except FileNotFoundError:
        print('*** Unable to import file.')
        sys.exit(1)
    else:
        print(f'*** {users_file} successfully imported.')
        
    # Set the portal environment and create list of existing users
    env = setPortal(gis_abr)
    existing_users = [user.username for user in env.users.search(max_users=2000)]
    
    # generate usernames and passwords for all users in the dataframe
    users['Username'] = users.apply(lambda x: generateUsername(x['First Name'],x['Last Name'],existing_users), axis=1)
    users['Password'] = users.apply(lambda x: generatePassword(x['First Name'],x['Last Name']), axis=1)

    # Update the new_users.csv file with the generated credentials
    users.to_csv(users_file, index=False)
    
    # Set user variables and create the user in the target portal
    for index, user in users.iterrows():
        
        # Set user variables
        email = user['Email']
        firstname = user['First Name']
        lastname = user['Last Name']
        user_type = user['User Type']
        role = user['Role']
        groups = user['Groups']
        username = user['Username']
        password = user['Password']

        # Create new user
        env.users.create(username = username,
                    password = password,
                    firstname = firstname,
                    lastname = lastname,
                    email = email,
                    role = role,
                    user_type = user_type)

if __name__ == "__main__":
    main('new_users.csv','portal1')
    #main('new_users.csv','portal2')
    #main('new_users.csv','portal3')