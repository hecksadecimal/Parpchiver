# Parpchiver
A tool for archiving chats on msparp locally.
Requirements: Python 2.7

## Usage
```
python msparp_archive.py <chatname> [datecode]
```
### Archiving an entire chat log
You can archive an entire chat by providing the script the name of the chat. 
The example used here is http://msparp.com/featuretesting

Note that this works exactly the same for searched chats with one caveat. It will save the entire searced chat log in one file, datecodes do not apply.

The script will automatically attempt to resume from the latest saved log if it exists.

Example input:
```
python msparp_archive.py featuretesting
```
Example output:
```
$ python msparp_archive.py featuretesting
Getting logs for featuretesting
featuretesting: 2017-06-17
featuretesting: 2017-05-28
featuretesting: 2017-05-27
featuretesting: 2017-05-19
featuretesting: 2017-05-17
featuretesting: 2017-05-15
featuretesting: 2017-05-13
featuretesting: 2017-05-12
```
### Archiving specific page of chat log
Example input:
```
python msparp_archive.py featuretesting 2017-05-28
```
Example output:
```
$ python msparp_archive.py featuretesting 2017-05-28
Getting 2017-05-28 for featuretesting
featuretesting: 2017-05-28
```
### Starting archival from specific page of chat log
Example input, first command:
```
python msparp_archive.py featuretesting 2017-05-19
```
Example output, first command:
```
$ python msparp_archive.py featuretesting 2017-05-19
Getting 2017-05-19 for featuretesting
featuretesting: 2017-05-19
```
Example input, second command:
```
python msparp_archive.py featuretesting
```
Example output, second command:
```
$ python msparp_archive.py featuretesting
Getting logs for featuretesting
Resuming from 2017-05-19
featuretesting: 2017-05-17
featuretesting: 2017-05-15
featuretesting: 2017-05-13
featuretesting: 2017-05-12
```
