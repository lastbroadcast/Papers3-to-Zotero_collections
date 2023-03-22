# Papers3-to-Zotero_collections

These scripts transfer the collections/folders from Papers3 to Zotero.

Run these scripts after transfering your library (by doing an XML export and using the Papers3-to-Zotero script). Note that only papers that have a title or a DOI will be captured by these scripts.

How to use:

1. Backup your Zotero library database before running the scripts! The database is named 'zotero.sqlite' and is in the Zotero folder. Simply create a copy of this file and name it something else. If the script damages the database, delete the file and restore the original.

2. Export collections from Papers3:

-Make sure all collections in Papers3 have UNIQUE names. This may require renaming some of them. I suggest doing this before you export the library as XML.

-Run FromPapers.py script. If script doesn't work, you may need to modify the name of the Papers 3 app in the script. See comment at top of script about this.

3. Import collections into Zotero:

-Open the 'collection_names.txt' file that was created by the FromPapers script. This is the complete list of collection names in your Papers3 library.

-In Zotero, create your collections with the EXACT names as in the file. It is important that the names are exactly the same. I found it easiest to copy and paste directly from the file. You can nest the collections in sub-folders if you want - the import script will still work.

-Create a collection called 'Uncategorised'. Any papers that could not be filed will be added to this collection.

-Open the ToZotero.py script (don't run it yet).

-If you want the papers to be removed from their current Zotero collection (i.e. the library import folder) when they are moved to their new collection(s) (I recommend doing this to keep track of which papers have been transfered), do the following: 
   
   On line 11, add the exact name of the current collection. For example:
    importCollectionName = "Import"
    
   On line 12, set flag as True:
    removeFromImportCollection = True
  
-If you want the papers to remain in their current collection, set flag as Flase:
   removeFromImportCollection = False. 

-Make sure the paths to 'title_dict.txt' and 'DOI_dict.txt' (the output files from the previous script) are correct.

-Make sure the path to the Zotero database ('zotero.sqlite') is correct.

-Make sure Zotero is closed.

-Run script.

-Check Uncategorised collection for any papers that could not be filed.

4. After filing of the library into the collections, if you want to remove items from parent collections (and only have them appear in nested child collections), run the script Zotero_RemoveParents.
