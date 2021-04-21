"""
#######################################################################################################################
Title: Clone Hosted Items
Description: This script allows the user to clone hosted feature items between Portals. Portal login credentials are
required for a source portal and at least one target portal.
#######################################################################################################################
"""

# Libraries
from arcgis.gis import GIS

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
    
# Clone the items to the new portal
def clone_items(source, target, source_ids):
    for item in source_ids:
        try:
            # Clone the item to the target portal
            hosted_flyr = source.content.get(item)
            cloned_flyr = target.content.clone_items(items=[hosted_flyr], owner = target.properties.user.username)
        except:
            print(f"Item ID {item} failed to clone")
        else:
            # Print confirmation message in console listing the copied items
            print(f"Cloned item {item} to the target portal " + target.properties.portalHostname)

# Main
if __name__ == "__main__":

    # Item IDs list ex. ['itemid'] or ['itemid_1','itemid_2',....,'itemid_n']
    item_ids = ['']

    # Set the gis portal objects
    source = setPortal('portal1')
    target1 = setPortal('portal2')
    #target2 = setPortal('portal3')
    
    clone_items(source, target1, item_ids)
    #clone_items(source, target2, item_ids)
