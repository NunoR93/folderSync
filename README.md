# Python folder syncing script

This is a python script that syncs two folders provided by the user, in a interval also provided by the user, and it logs every change in the interval to a file named `log.txt` to a directory of the user choosing and the terminal.

**Usage**
`python sync.py -interval -sourceFolder -destinationFolder -destinationOfLog`

**Example**
`python sync.py 10 /User/Nuno/Desktop/ImportantFolder /User/Nuno/Documents/Backup /User/Nuno/Documents`

This usage will sync the folder `ImportantFolder` located in the Desktop, with a folder called `Backup` located in Documents, and log all the changes made to them while the script is running to the `log.txt` file that will be located in the `Documents` folder
