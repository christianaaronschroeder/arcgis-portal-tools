# ArcGIS API for Python Tools
Various tools for managing users and content within an ArcGIS Enterprise Portal environment.

## Scripts
- clone-hosted-items.py
    - clone hosted feature items between Portals.
- clone-service-items.py
    - Clone non-hosted, REST service-based items between Portals, along with any internal configurations including symbology, thumbnails, and metadata.
- onboard-new-users.py
    - Easily onboard new users to your portal environment by generating usernames cross-checked with existing users, randomized passwords (code excluded), and updating a CSV of credentials.
- notify-new-users.py
    - Sends pre-defined emails (through MS Outlook) to newly generated users from a CSV. The first email contains their username, and the second contains their password. The imported CSV should follow the format required by Esri's portal onboarding by file process: [Email, First Name, Last Name, User Type, Role, Username, Password]. This script is meant to be run AFTER running onboard-new-users.py to first create the accounts, and populate new_users.csv.