#Exports lists of papers in each collection/folder (by title and DOI) from Papers3, and a list of all collection names
#see readme for notes on running
#see line 17 if script doesn't work

import subprocess
import json

#file paths
DOI_dict_path = './DOI_dict.txt'
title_dict_path = './title_dict.txt'
collection_names_path = './collection_names.txt'
missing_papers_path = './missing_papers.txt'

#get number of papers in library

#AppleScript command
#if script doesn't work, check and modify the name of the Papers3 app within the command
cmd = '''
tell application "Papers 3 (Legacy)"  
	get count of publication items
end tell
'''

#run command
result = subprocess.run(['osascript', '-e', cmd], capture_output=True)
paper_count = int(result.stdout.decode())

print('number papers = ' + str(paper_count))

#retreive collection names (directories), DOI and title of each paper

dict_papers_byDOI = {}
dict_papers_byTitle = {}
missing_papers = []

collectionNames = set() #holds complete set of collection names

for i in range(1, paper_count+1):

    #AppleScript commands
    cmd_doi = '''
    tell application "Papers 3 (Legacy)"
        get doi of item %d of publication items
    end tell
    ''' % i

    cmd_title = '''
    tell application "Papers 3 (Legacy)"
        get title of item %d of publication items
    end tell
    ''' % i

    cmd_collection = '''
    tell application "Papers 3 (Legacy)"
        get manual collection names of item %d of publication items
    end tell
    ''' % i

    #run commands
    result = subprocess.run(['osascript', '-e', cmd_doi], capture_output=True)
    doi = result.stdout.decode().strip()

    result = subprocess.run(['osascript', '-e', cmd_title], capture_output=True)
    title = result.stdout.decode().strip()

    result = subprocess.run(['osascript', '-e', cmd_collection], capture_output=True)
    collections = result.stdout.decode().strip()

    #clean up collection names
    collections = collections.split(",")  #split strings at ',' character
    collections = [s.strip() for s in collections] #remove outer whitespace from names
    collectionsSet = set(collections) #and add to a set to remove duplicates

    #update dictionaries with results
    if(doi != 'missing value'):
        #with doi as key
        print('adding paper ' + str(i) + ' by DOI')
        print('doi: ' + doi + '; title: ' + title)
        dict_papers_byDOI.update({doi: [x for x in collectionsSet]})
    if(title != 'missing value'):
        #with title as key
        print('adding paper ' + str(i) + ' by title')
        print('doi: ' + doi + '; title: ' + title)
        dict_papers_byTitle.update({title: [x for x in collectionsSet]})
    if(doi == 'missing value' and title == 'missing value'):
        print('excluding paper ' + str(i) + ' because no DOI or title attached.')
        #otherwise, exclude and count as a missing paper
        missing_papers.append(i)

    #add collection name to the set
    collectionNames.update(collectionsSet)

print('writing files')
with open(DOI_dict_path, "w") as f:
    f.write(json.dumps(dict_papers_byDOI))

with open(title_dict_path, "w") as f:
    f.write(json.dumps(dict_papers_byTitle))

with open(collection_names_path, "w") as f:
    for line in collectionNames:
        f.write(line + '\n')

with open(missing_papers_path, "w") as f:
    for item in missing_papers:
        f.write(str(item) + '\n')
