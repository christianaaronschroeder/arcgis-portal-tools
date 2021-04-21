"""
#######################################################################################################################
Title: Notify New Users of their Accounts
Description: This script sends pre-defined emails (through MS Outlook) to newly generated users from a CSV. The first
email contains their username, and the second contains their password. The imported CSV should follow the format required
by Esri's portal onboarding by file process: [Email, First Name, Last Name, User Type, Role, Username, Password].
This script is meant to be run AFTER running onboard-new-users.py to first create the accounts, and populate new_users.csv
#######################################################################################################################
"""

# Libaries
import win32com.client as win32
import pandas as pd

# Generates and sends the emails
def sendEmails(firstname, lastname, username, password, email):

    # email text
    email1_subject = "Email 1 Subject"
    email1_body = f'''Hello {firstname} {lastname}, 
    
    Email body text.
    Username: {username}

    '''
    email2_subject = "Email 2 Subject"
    email2_body = f'''Hello {firstname} {lastname}, 
    
    Email body text.
    Password: {password}

    '''

    try:
        # create email1
        outlook = win32.Dispatch('outlook.application')
        mail1 = outlook.CreateItem(0)
        mail1.To = email
        #mail1.CC = ""
        mail1.Subject = email1_subject
        mail1.Body = email1_body

        # create email2
        mail2 = outlook.CreateItem(0)
        mail2.To = email
        mail2.Subject = email2_subject
        mail2.Body = email2_body

        # Send the emails
        mail1.Send()
        mail2.Send()
    except:
        print(f"Failed to send emails to {email}.")
    else:
        print(f"{firstname} {lastname} has been notified at {email}.")


if __name__ == "__main__":

    # Import list of new user credentials (must include [Email, First Name, Last Name, Username, Password])
    user_list = 'new_users.csv'
    users = pd.read_csv(user_list)

    for index, user in users.iterrows():
        #set user variables
        firstname = user['First Name']
        lastname = user['Last Name']
        username = user['Username']
        password = user['Password']
        email = user['Email']

        # send emails
        sendEmails(firstname, lastname, username, password, email)