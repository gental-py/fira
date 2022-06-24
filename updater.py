import requests as r
import os


os.system("cls")
print("[start] Updater.py.")


# Change fira.py to fira.py.old
try:
    if os.path.exists('./fira.py.old'):
        print("[WARRNING] File <fira.py.old> actually exists! After pressing ENTER, it will be deleted.")
        os.system("pause")
        try:
            os.remove("./fira.py.old")
            print("[done]  .old file has been deleted.")

        except Exception as e:
            print(f"[error] Cannot delete .old file: {e}")
            exit()

    os.rename("./fira.py", "./fira.py.old")
    print("[done]  Rename process: OK.")

except Exception as e:
    print(f"[error] Rename process: ERROR: {e}.")
    exit()


# Create fira.py
try:
    open("./fira.py", "a+").close()
    print("[done]  Creating file: OK.")

except Exception as e:
    print(f"[error] Creating file: ERROR: {e}.")
    exit() 


# Get code.
try:
    mainCodeURL = "https://raw.githubusercontent.com/gental-py/fira/main/fira.py"
    mainCodeREQ = r.get(mainCodeURL).text
    print("[done]  Get code: OK.")

except Exception as e:
    print(f"[error] Get code: ERROR: {e}.")
    exit()


# Write to file.
try:
    with open("./fira.py", "w", encoding="utf-8", newline="") as file:
        file.write(mainCodeREQ)
    print("[done]  Write code: OK.")

except Exception as e:
    print(f"[error] Write code: ERROR: {e}.")
    exit()


# "autodestruction" Delete this file and run fira.py
try:
    print("[info] This file will be deleted and Fira.py will be runed.")
    os.system('pause')
    os.remove("./updater.py")
    os.system("py fira.py || python fira.py || python3 fira.py")
    exit()

except Exception as e:
    print(f"[error] {e}.")
 
