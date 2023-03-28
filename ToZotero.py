#Imports the lists of papers in each collection into Zotero
#run this script after FromZotero
#see readme for notes on running
#make sure the paths to the Zotero database (line 9) and output files from FromZotero script (lines 13/14) are correct

import sqlite3
import json

con = sqlite3.connect("/Users/user/Zotero/zotero.sqlite")  #make sure the path to Zotero database is correct
cur = con.cursor()

dictPaths = [
    './title_dict.txt',       #path for title dictionary
    './DOI_dict.txt'          #path for DOI dictionary
]

importCollectionName = 'Import'     #name of collection that holds all imported papers
removeFromImportCollection = True   #set to True if you want papers to be removed from the import collection when they are transferred (recommended to keep track of which papers haven't transferred)

for dictPath in dictPaths:

    print('Now processing dictionary: %s' % dictPath)

    with open(dictPath, "r") as f:
        dict = json.loads(f.read())

    for key in dict: #for each key in dictionary
        collectionNames = dict[key] #extract collection names for this key

        for collectionName in collectionNames:

            if collectionName == "":
                collectionName = "Uncategorised" #add unlabeled items to 'uncategorised' collection
                print('Item %s has no collection name. Adding to Uncategorised.' % key)

            escaped_key = key.translate(str.maketrans({"'":  r"''"})) #escape the ' character to avoid error
            SQL_query = "SELECT valueID FROM itemDataValues WHERE value = '%s'" % escaped_key
            res = cur.execute(SQL_query)
            valueID_results = res.fetchall()

            if len(valueID_results) == 0:
                print('Item %s not found in database.' % key)
            elif len(valueID_results) > 1:
                print('Multiple records found for item %s in database; excluding this item.' % key)
            else:
                valueID = valueID_results[0][0]
                SQL_query = "SELECT itemID FROM itemData WHERE valueID = %d" % valueID
                res = cur.execute(SQL_query)
                itemID_results = res.fetchall()

                if len(itemID_results) == 0:
                    print('Item %s could not be associated with a paper in the database.' % key)
                else: #key is in the database
                    for i in range(len(itemID_results)): #in case there is more than one item, loop through the transfer

                        itemID = itemID_results[i][0]
                        SQL_query = "SELECT collectionID FROM collections WHERE collectionName = '%s'" % collectionName
                        res = cur.execute(SQL_query)
                        collectionID_results = res.fetchone()
                        if collectionID_results != None:
                            collectionID = collectionID_results[0]
                        else:
                            print('Collection name %s could not found in the database. Adding item to Uncategorised collection.' % collectionName)
                            collectionName = "Uncategorised"
                            SQL_query = "SELECT collectionID FROM collections WHERE collectionName = '%s'" % collectionName
                            res = cur.execute(SQL_query)
                            collectionID_results = res.fetchone()
                            collectionID = collectionID_results[0]

                        print('Processing item: %s' % key)

                        #add paper to collection
                        try:
                            SQL_query = "INSERT INTO collectionItems (collectionID, itemID) VALUES (%d, %d)" % (collectionID, itemID)
                            res = cur.execute(SQL_query)
                            con.commit()
                        except sqlite3.IntegrityError: #already in database
                            print("Item %s is already filed in collection %s)" % (key, collectionName))

                        #remove item from import collection
                        if removeFromImportCollection:
                            SQL_query = "SELECT collectionID FROM collections WHERE collectionName = '%s'" % importCollectionName
                            res = cur.execute(SQL_query)
                            collectionID_results = res.fetchone()
                            if collectionID_results != None:
                                collectionID = collectionID_results[0]
                                SQL_query = "DELETE FROM collectionItems WHERE collectionID = %d AND itemID = %d" % (collectionID, itemID)
                                res = cur.execute(SQL_query)
                                con.commit()


