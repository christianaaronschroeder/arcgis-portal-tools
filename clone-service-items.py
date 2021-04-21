"""
#######################################################################################################################
Title: Clone Service Items
Description: This script allows the user to clone non-hosted, REST service-based items between Portals, along with any
internal configurations including symbology, thumbnails, and metadata. Portal login credentials are required for a
source portal and at least one target portal.
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

    # Create temp folder to hold the thumbnail and metadata files; folder is deleted when script finishes running
    with tempfile.TemporaryDirectory() as temp:
        target.content.create_folder(folder=target_folder)
        target_ids = []
        
        # Clone each item listed in item_ids
        for item in source_ids:
            layer = source.content.get(item)
            layer_properties = {}
            
            # Copy the item's properties
            for property_name in properties_list:
                layer_properties[property_name] = layer[property_name]
            
            # Temp download the thumbnail and metadata
            thumbnail = layer.download_thumbnail(temp)
            metadata = layer.download_metadata(temp)

            # Create the cloned item, applying the copied properties, thumbnail, and metadata
            copied_item = target.content.add(item_properties=layer_properties, thumbnail=thumbnail, metadata=metadata)
            
            # Update the drawing info (transparency included) of the new item in the target portal
            item_properties = {'text': json.dumps(layer.get_data())}
            copied_item.update(item_properties=item_properties)
            target_ids.append(copied_item.id)
        
        # Print confirmation message in console listing the copied items
        print("Copied the item to the target portal " + target.properties.portalHostname + " with new ID:")
        for target_id in target_ids:
            newlayer = target.content.get(target_id)
            print('\t- ' + newlayer.title + " : " + newlayer.id)

# Main
if __name__ == "__main__":
    # format: clone_tiems(source_portal, target_portal, item_ids)

    # Item IDs list ex. ['itemid'] or ['itemid_1','itemid_2',....,'itemid_n']
    item_ids = ['']

    # List of the properties to be copied between portals
    properties_list = ['title', 'type', 'description', 'snippet', 'extent', 'tags', 'accessInformation', 'url']

    # Set the gis portal objects
    source = setPortal('portal1')
    target1 = setPortal('portal2')
    #target2 = setPortal('portal3')
    
    clone_items(source, target1, item_ids)
    #clone_items(source, target2, item_ids)

