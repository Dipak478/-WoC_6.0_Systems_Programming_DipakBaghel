import sys
import os 
import json 
import datetime
import hashlib
import base64
    
def hashfile(file):
    BUF_SIZE = 65536
    md5 = hashlib.md5()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def write_json(new_data, filename):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["emp_details"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


def status():
    currdir=os.getcwd()
    Files=os.listdir(currdir)
    filename=f"{currdir}/.VCS/branches/main/index.json"
    file_data=dict()

    check_file = os.stat(filename).st_size
    
    

    if(check_file == 0):
        for file in Files :
            file_extension = os.path.splitext(file)[1]
            temp = file_extension[1:]
            if(temp==''): continue
            print(file)
        return 
    

    with open(filename,'r+') as file:
        file_data = json.load(file)
    for file in Files:

        file_extension = os.path.splitext(file)[1]
        temp = file_extension[1:]
        if(temp==''): continue
        file_path = os.path.join(currdir, file)
        file_hash = hashfile(file_path)
        if file in file_data:
            if(file_data[file]!=file_hash):
                print(file)
        else:
             print(file)
    
   
       


        


def add():
   
     filename=sys.argv[2]
     currdir=os.getcwd()
     file_path = os.path.join(currdir, filename)
     if(os.path.exists(file_path)==0):
         print("File Not Exists")
         return
     file_hash = hashfile(file_path)


     jfilename=f"{currdir}/.VCS/branches/main/added.json"
     file_data=dict()
     check_file = os.stat(jfilename).st_size
     if(check_file != 0):
       with open(jfilename,'r+') as file:
        file_data = json.load(file)
     file_data[filename]=(file_hash)
   
     json_data = json.dumps(file_data, indent=4)
     added_file_path = f"{currdir}/.VCS/branches/main/added.json"
    
  
     with open(added_file_path, 'w') as json_file:
      json_file.write(json_data)

     jfilename = f"{currdir}/.VCS/branches/main/index.json"
     file_data=dict()
     check_file = os.stat(jfilename).st_size
     if(check_file != 0):
       with open(jfilename,'r+') as file:
        file_data = json.load(file)
     file_data[filename]=(file_hash)
   
     json_data = json.dumps(file_data, indent=4)
     index_file_path = f"{currdir}/.VCS/branches/main/index.json"
        
     with open(index_file_path, 'w') as json_file:
      json_file.write(json_data)

     print("added succesfully")
  



def init():
    # Step 1: Ask the user to set the username
    username = input("Enter your username: ")
    currdir=os.getcwd()

    if(os.path.exists(f"{currdir}/.VCS")==False):
        os.mkdir(".VCS")
        # if already exists then check
        branches_directory = os.path.join(".VCS", "branches")
        objects_directory = os.path.join(".VCS", "objects")
        os.mkdir(branches_directory)
        os.mkdir(objects_directory)

        main_branch_directory = os.path.join(branches_directory, "main")
        os.makedirs(main_branch_directory)

        added_json_path = os.path.join(main_branch_directory, "added.json")
        index_json_path = os.path.join(main_branch_directory, "index.json")
        users_txt_path = os.path.join(main_branch_directory, "users.txt")

        with open(added_json_path, 'w') as added_file:
            json.dump({}, added_file)

        with open(index_json_path, 'w') as index_file:
            json.dump({}, index_file)

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{currdir}/.VCS/branches/main/users.txt", 'w') as users_file:
        users_file.write(f"Date: {current_datetime}, Username: {username}\n")

def encode_file_content_to_base64(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return base64.b64encode(binary_data).decode('utf-8')


def commit():
 
    
   
    currdir=os.getcwd()
    fpath=f"{currdir}/.VCS/branches/main/added.json"
    check_file = os.stat(fpath).st_size

    if(check_file==0) :
       print("No changes available")
       return
 
    file_hash=hashfile(fpath)
    objectPath = f"{currdir}/.VCS/objects"

    cfiles=os.listdir(objectPath)

    match="0"
    last=""

    add_data={}
    with open(f"{fpath}", 'r') as file:
        add_data = json.load(file)
   
    if not cfiles:
        temp_data={}

        new_data={}
    
        for file in add_data:
            temp_path=f"{currdir}/{file}"
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

        # with open(new_file_path, 'w') as json_file:
        #  json_file.write(json_data)

        temp_data["changes"]=new_data
        temp_data["all"]=new_data
        temp_data["message"]=sys.argv[3]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        temp_data["timestamp"]=timestamp

        new_file_path = f"{objectPath}/{file_hash}.json" 
        json_data = json.dumps(temp_data, indent=4)

        with open(new_file_path, 'w') as json_file:
         json_file.write(json_data)

        # empty_dict={}
        # json_data = json.dumps(empty_dict)

        with open(fpath, 'w') as file:
          file.write("")
    
        # with open(fpath, 'w') as json_file:
        #     json_file.write(json_data)

        print("Done successfully")
        
        return 


    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file
    
    last_data={}
    with open(f"{objectPath}/{last}", 'r') as file:
        last_data = json.load(file)

    new_data={}
    
    for file in add_data:
            temp_path=f"{currdir}/{file}"
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

    temp_data={}
    temp_data["changes"]=new_data
    # new_data = {
    # "changes": add_data
    # } 
    
    for key in temp_data["changes"]:
        last_data["all"][key]=temp_data["changes"][key]
    
    last_data["changes"]=temp_data["changes"]
    last_data["message"]=sys.argv[3]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    last_data["timestamp"]=timestamp

    new_file_path = f"{objectPath}/{file_hash}.json" 
    json_data = json.dumps(last_data, indent=4)

    with open(new_file_path, 'w') as json_file:
      json_file.write(json_data)

    with open(fpath, 'w') as file:
           file.write("")

    print("Done successfully")

def rmcommit():

    match="0"
    last=""
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    os.remove(f"{objectPath}/{last}")

    match="0"
    last=""
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(currdir)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(currdir,file)
          if(os.path.isfile(os.path.join(currdir,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")


def log():
    log={}
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         log[creation_time_readable]=file
        
    myKeys = list(log.keys())
    myKeys.sort()
    sorted_log = {i: log[i] for i in myKeys}

    for x in sorted_log:
        fileName=sorted_log[x]
        filePath=f"{objectPath}/{fileName}"
        with open(f"{filePath}", 'r') as file:
         tempD = json.load(file)
        
        print("Author:The Great Dipak Baghel\n")
        print(f"Commit: {fileName[:-5]}\n")

        print("All files\n")

        for y in tempD["all"]:
            print(f"    {y}:{tempD["all"][y]}\n")

        print("Modified files\n")

        for y in tempD["changes"]:
            print(f"    {y}:{tempD["changes"][y]}\n")
    
        print(f"Message:{tempD["message"]}\n")
        print(f"Time Stamp:{tempD["timestamp"]}\n\n\n")

        

def checkout():
    hashvalue=f"{sys.argv[2]}.json"
    
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"

    creation_time = os.path.getctime(f"{objectPath}/{hashvalue}")
    hashtime = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cfiles=os.listdir(objectPath)

    for file in cfiles:
        creation_time = os.path.getctime(f"{objectPath}/{file}")
        creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if(creation_time_readable>hashtime):
            os.remove(f"{objectPath}/{file}")
   
    state={}

    with open(f"{objectPath}/{hashvalue}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(currdir)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(currdir,file)
          if(os.path.isfile(os.path.join(currdir,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")
    
def push():
    destPath=sys.argv[2]
    match="0"
    last=""
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)
    if(cfiles.st_size()==0):
         print("No commits yet")

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    for file in all:
        decodedContent=base64.b64decode(all[file])
        file_path = os.path.join(destPath, file)

        with open(file_path, 'wb') as f:
         f.write(decodedContent)
    print("Done Successfully")
  
def rmadd():

    currdir=os.getcwd()
    fpath=f"{currdir}/.VCS/branches/main/added.json"
    with open(fpath, 'w') as file:
           file.write("")

    print("Done successfully")

        


if __name__ == "__main__":

    if len(sys.argv) > 1:
        command=sys.argv[1]
        if command == "init":
                init()
        if command == "add":
                add()
        if command == "status":
                status()
        if command == "commit":
                commit()
        if command == "rmcommit":
                 rmcommit()
        if command == "log" :
                log()
        if command == "checkout" :
                checkout()
        if command == "push":
                push()
        if command == "rmadd":
                rmadd()

    else :
        print("VCS - A Version Control System \n\nVCS init - Initialize a new VCS repository \n\n\
VCS add <file> - Add a file to the index\n\nVCS commit -m <message> - Commit changes with a message\
        \n\nVCS rmadd <file> - remove a file from the index\n\nVCS rmcommit - remove last commit\n\n\
VCS log - Display commit log\n\nVCS checkout <commit> - Checkout a specific commit\n\n\
VCS help - to see this usage help\n\nVCS status - to see status\n\nVCS user show - to see present user\n\n\
VCS user set <username> - to change user\n\nVCS push <path> - to push your file to another folder\n\n\
Created by - Dipak Baghel")
