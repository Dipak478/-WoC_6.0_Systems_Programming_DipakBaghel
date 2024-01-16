import os 
import sys
import hashlib
import json 

Fpath=input("Please enter the folder path\n")
Files=os.listdir(Fpath)

my_dictionary = dict()
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
 
 

for file in Files:
    file_path = os.path.join(Fpath, file)
    file_hash = hashfile(file_path)
    file_size = os.path.getsize(file_path)
    my_dictionary[file] = (file_size, file_hash)

for dict in my_dictionary:
    print(my_dictionary[dict])

file_path = f"{Fpath}/output.json"
json_data = json.dumps(my_dictionary, indent=4)

# Write the JSON string to a file
with open(file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON data has been written to {file_path}")

  
 
