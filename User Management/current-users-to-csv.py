"""
#######################################################################################################################
Title: CSV List of Current Portal Users
Description: Generate CSV file of all current users of the portal environment.
#######################################################################################################################
"""

# Libaries
from arcgis.gis import GIS
import csv

# Set portal
gis = GIS("", "", "")
users = gis.users.search(max_users=2000)

# Generate CSV file
with open('current_users.csv', 'w', newline='') as ResultFile:
    wr = csv.writer(ResultFile)
    header = 'First Name', 'Last Name', 'Username', 'Role', 'Email'
    wr.writerow(header)
    for user in users:
        UserRow = user.firstName, user.lastName, user.username, user.role, user.email
        wr.writerow(UserRow)