import sys
import os 
import json 
import datetime
import hashlib



    
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
     file_hash = hashfile(file_path)

     jfilename=f"{currdir}/.VCS/branches/main/index.json"
     file_data=dict()
     check_file = os.stat(jfilename).st_size
     if(check_file != 0):
       with open(jfilename,'r+') as file:
        file_data = json.load(file)
     file_data[filename]=(file_hash)
   
     json_data = json.dumps(file_data, indent=4)
     added_file_path = f"{currdir}/.VCS/branches/main/added.json"
     index_file_path = f"{currdir}/.VCS/branches/main/index.json"

     with open(added_file_path, 'w') as json_file:
      json_file.write(json_data)
     with open(index_file_path, 'w') as json_file:
      json_file.write(json_data)
  



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





if __name__ == "__main__":

    if len(sys.argv) > 1:
        command=sys.argv[1]
        if command == "init":
                init()
        if command == "add":
                add()
        if command == "status":
                status()

    else :
        print("VCS - A Version Control System \n\nVCS init - Initialize a new VCS repository \n\n\
VCS add <file> - Add a file to the index\n\nVCS commit -m <message> - Commit changes with a message\
        \n\nVCS rmadd <file> - remove a file from the index\n\nVCS rmcommit - remove last commit\n\n\
VCS log - Display commit log\n\nVCS checkout <commit> - Checkout a specific commit\n\n\
VCS help - to see this usage help\n\nVCS status - to see status\n\nVCS user show - to see present user\n\n\
VCS user set <username> - to change user\n\nVCS push <path> - to push your file to another folder\n\n\
Created by - Dipak Baghel")
