import os 
import shutil

Fpath=input("Please enter the folder path\n")


os.chdir(Fpath)

DFE = set()

Files=os.listdir(Fpath)

print(Files)

for file in Files:
    file_extension = os.path.splitext(file)[1]
    temp = file_extension[1:]
    if(temp==''): continue
    DFE.add(temp)

for x in DFE:
    if(os.path.exists(f"{Fpath}/{x}")):continue
    os.mkdir(x)

for file in Files:
    file_extension = os.path.splitext(file)[1]
    temp = file_extension[1:]
    if(temp==''): continue
    shutil.move(f"{Fpath}/{file}", f"{Fpath}/{temp}")

