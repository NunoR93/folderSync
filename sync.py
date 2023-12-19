import os
import hashlib
import shutil
import sys
import datetime
import time

args = sys.argv

log_path = args[4]
src_folder = args[2]
dst_folder = args[3]
sync_time = args[1]

deleted_files = []
created_files = []
modified_files = []

print("Ctrl-c to end the program ")
for i in range(3):
  time.sleep(1)
  print(".")

#This function gets the folder path and returns all it's contents in a list with a relative path for every item in the folder
def getFolderStructure(path):
  files_paths = []

  for root, dirs, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      relative_path = os.path.relpath(file_path, path)
      files_paths.append(relative_path)
    for d in dirs:
      dir_path = os.path.join(root, d)
      relative_path = os.path.relpath(dir_path, path)
      files_paths.append(relative_path)
  return files_paths

#Checks if item was deleted by cheking if the destination folder has files or folders that the source folder doesn't, if it was a file simply removes it, if it was a folder removes the entire tree
def checkDeleted(item, src, dst):
  if(not os.path.exists(os.path.join(src,item))):
    if(os.path.isfile(os.path.join(dst,item))):
      os.remove(os.path.join(dst,item))
    else:
      shutil.rmtree(os.path.join(dst,item))
    return True
  return False

#Checks the md5 hash of two files, if they're not equal it means the file in the source folder was modified, so it copies it to the destination folder
def checkModified(file_src, file_dst):
  file_from_src = open(file_src, "rb").read()
  src_md5 = hashlib.md5(file_from_src).hexdigest()
  file_from_dst = open(file_dst, "rb").read()
  dst_md5 = hashlib.md5(file_from_dst).hexdigest()

  if(src_md5 != dst_md5):
    shutil.copy2(file_src, file_dst)
    #modified_files.append(file_src)
    return True
  return False
  #return src_md5!=dst_md5

#This fucntion checks if the item exists in the destination folder, if it's a file and it doesn't exist, it copies it, if it's a folder, copies it and it's entire contents
def checkItem(item, src, dst):
  dst_path = os.path.join(dst,item)
  src_path = os.path.join(src,item)

  if(not os.path.exists(dst_path)):
    if(os.path.isfile(src_path)):
      shutil.copy2(src_path, dst_path)
      #created_files.append(src_path)
      creation_time = datetime.datetime.fromtimestamp(os.path.getctime(src_path))
      log = str(creation_time)+" Created: "+src_path+" -> "+str(datetime.datetime.now())+" Copied to: "+dst_path+"\n"
      print(log)
      file.write(log)
    else:
      shutil.copytree(src_path, dst_path)
      for i in getFolderStructure(src_path):
        #created_files.append(os.path.join(src_path,i))
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(src_path))
        log = str(creation_time)+" Created: "+os.path.join(src_path,i)+" -> "+str(datetime.datetime.now())+" Copied to: "+os.path.join(dst_path,i)+"\n"
        print(log)
        file.write(log)
      #created_files.append(src_path)
      creation_time = datetime.datetime.fromtimestamp(os.path.getctime(src_path))
      log = str(creation_time)+" Created: "+src_path+" -> "+str(datetime.datetime.now())+" Copied to: "+dst_path+"\n"
      print(log)
      file.write(log)
  else: #If the path already exists, check if it's a file, and if it was modified
    if(os.path.isfile(src_path)):
      if(checkModified(src_path, dst_path)):
        modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(src_path))
        log = str(modification_time)+" Modified: "+dst_path+"\n"
        print(log)
        file.write(log)

while(1):
  #Fetch the structure of both the source folder and the destination folder
  src_filesPathList = getFolderStructure(src_folder)
  dst_filesPathList = getFolderStructure(dst_folder)

  file = open(log_path+"/log.txt", "a")
  #Iterate through the destination folder to check if there was any deleted files or folders
  for i in dst_filesPathList:
    try:
      if(checkDeleted(i, src_folder, dst_folder)):
        #deleted_files.append(os.path.join(src_folder,i))
        log = str(datetime.datetime.now())+" Deleted: "+os.path.join(dst_folder,i)+"\n"
        print(log)
        file.write(log)
    except:
      #deleted_files.append(os.path.join(src_folder,i))
      log = str(datetime.datetime.now())+" Deleted: "+os.path.join(dst_folder,i)+"\n"
      print(log)
      file.write(log)
      

  #Iterate through the source folder to check if files were created or modified
  for i in src_filesPathList:
    checkItem(i, src_folder, dst_folder)

  file.close()
  time.sleep(int(sync_time))