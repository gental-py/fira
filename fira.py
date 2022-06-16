# Functions: Find file, cleartmp, rename, open, edit?
class Program:
    version = 0.2

# Import libaries.
import getpass as gp
import time as t
import platform
import fnmatch
import ctypes
import sys
import re
import os

def WaitForEnter():
    print(bold)
    os.system('pause || read -s -p "Press any key to continue . . ."')
    print(end)
    
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


# Colors.
if not sys.stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    if platform.system() == "Windows":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32

underline = "\033[4m"
crossed = "\033[9m"
orange = "\033[0;33m"
purple = "\033[1;35m"
green = "\033[1;32m"
blink = "\033[5m"
bold = "\033[1;37m"
blue = "\033[1;34m"
gray = "\033[1;30m"
cyan = "\033[1;36m"
red = "\033[1;31m"
end = "\033[0m"


# Check if running on Windows.
if platform.system() != "Windows":
    print(f"{red}You are not running FiraFiles on Windows. It may cause some problems. Your platform: {__import__('platform').system()}{end}")
    WaitForEnter()


# Menus.
def DrawBanner():
    cls()
    print(f"""
{red}⠀⠀⠀⠀⠀⠀⢱⣆⠀⠀⠀⠀⠀⠀ {orange}
{red}⠀⠀⠀⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⠀ {orange}                           
{red}⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣧⠀⠀⠀ {orange}                             
{red}⠀⠀⠀⠀⡀⢠⣿⡟⣿⣿⣿⡇⠀⠀ {orange}     ███████╗██╗██████╗░░█████╗░███████╗██╗██╗░░░░░███████╗░██████╗
{red}⠀⠀⠀⠀⣳⣼⣿⡏⢸⣿⣿⣿⢀⠀ {orange}     ██╔════╝██║██╔══██╗██╔══██╗██╔════╝██║██║░░░░░██╔════╝██╔════╝
{red}⠀⠀⠀⣰⣿⣿⡿⠁⢸⣿⣿⡟⣼⡆ {orange}     █████╗░░██║██████╔╝███████║█████╗░░██║██║░░░░░█████╗░░╚█████╗░
{red}⢰⢀⣾⣿⣿⠟⠀⠀⣾⢿⣿⣿⣿⣿ {orange}     ██╔══╝░░██║██╔══██╗██╔══██║██╔══╝░░██║██║░░░░░██╔══╝░░░╚═══██╗
{red}⢸⣿⣿⣿⡏⠀⠀⠀⠃⠸⣿⣿⣿⡿ {orange}     ██║░░░░░██║██║░░██║██║░░██║██║░░░░░██║███████╗███████╗██████╔╝
{red}⢳⣿⣿⣿⠀ {bold}{Program.version}{red}⠀ ⢹⣿⡿⡁{orange}     ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═════╝░
{red}⠀⠹⣿⣿⡄⠀⠀⠀⠀⠀⢠⣿⡞⠁ {orange}                                                       {bold}@{underline}gental{end}
{red}⠀⠀⠈⠛⢿⣄⠀⠀⠀⣠⠞⠋⠀⠀ {orange}                                                        
{red}⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀{end}""")

def DrawMenu_Main():  
    print(f"""                    {orange}           [ {red}1 {orange}]  {bold}Manual operations.    
                    {orange}           [ {red}2 {orange}]  {bold}Automatic operations. 
                    {orange}           [ {red}0 {orange}]  {red}Exit.{end}""")

def DrawMenu_Automatic():  
    print(f"""                    {orange}           [ {red}1 {orange}]  {bold}Find files.    
                    {orange}           [ {red}2 {orange}]  {bold}Clean disks.
                    {orange}           [ {red}3 {orange}]  {bold}Format disk.#  
                    {orange}           [ {red}0 {orange}]  {red}Back.{end}""")


# Operations section.
class Manual:
    def Main():
        pass

class Automatic:
    def Main():
        while True:
            DrawBanner()
            DrawMenu_Automatic()
            automatic_action = input(f"\n                               {orange}~{bold} ").lower().replace(" ", "")

            # Check user input correction.
            if not isNumber(automatic_action):
                continue

            else:
                automatic_action = int(automatic_action)

                if automatic_action not in range(0, 3):
                    continue 

            # Handle user choose. 
            if automatic_action == 0:
                return

            if automatic_action == 1:
                Automatic.FindFile()

            if automatic_action == 2:
                Automatic.CleanDisks()


    def FindFile():
        DrawBanner()

        def ShowData(t,l,i):
            DrawBanner()
            print(f"                            {orange}Target {red}:{bold} {t}")
            print(f"                          {orange}Location {red}:{bold} {l}")
            print(f"\n{i}")

        # Take data.
        target, location, info, allDisks, allHits = "", "", "", re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE), []
        while True:
            ShowData(target, location, info)
            info = ""

            if target == "":              
                target = input(f"\n                      {orange}Target {red}~{bold} ")
                continue

            if location == "":
                location = input(f"\n                    {orange}Location {red}~{bold} ")
                if location == "":
                    location = f"{gray}Everywhere{end}"

                else:
                    if not os.path.exists(location):
                        info = f"                                     {gray}[ {red}Error: {bold}Path does not exists! {gray}]{end}"
                        location = ""
                continue

            else:
                break
        if location == f"{gray}Everywhere{end}":
            location = ""


        # Find file(s).
        print(f"                          {bold}Searching . . .{end}")

        if location != "":
            allDisks = [location]

        for disk in allDisks:
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if fnmatch.fnmatch(file, target):
                        allHits.append(os.path.join(root, file))
        

        # Print founded files.
        DrawBanner()
        print(f"                          {red}• {bold}Found {orange}{len(allHits)} {bold}file(s).{end}\n")
        for hit in allHits:
            print(f"                 {orange}• {bold}{hit}{end}")

        WaitForEnter()

    def CleanDisks():
        allDisks = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
        tempAllDisks = []
        
        for disk in allDisks:
            tempAllDisks.append({"name": disk, "state": False})

        allDisks = tempAllDisks
        selectedDisks = []
        disksStatus = []

        # Select disk(s)
        def DisplaySelection():
            DrawBanner()

            print(f"                      {bold}Select which disks you want to be cleaned.{end}\n\n")
            for disk in allDisks:
                print(f"                           {orange}• {bold}{disk['name']} {gray}: {f'{green}v{end}' if disk['state'] else f'{red}x{end}'}")


        for disk in allDisks:        
            DisplaySelection()

            state_input = input(f"\n                           {red}• {bold}{disk['name']} {gray}~ {bold}").lower().replace(" ","")
            while state_input not in ("x", "no", "n", "0", "v", "yes", "y", "1"):
                DisplaySelection()
                state_input = input(f"\n           {gray}[{red}Y{gray}]es / [{red}N{gray}]o    {red}• {bold}{disk['name']} {gray}~ {bold}").lower().replace(" ","")
        
            if state_input in ("v", "yes", "y", "1"):
                disk["state"] = True
                selectedDisks.append(disk["name"])
                disksStatus.append({"name": disk["name"], "TempFilesStatus": {"error": 0, "succes": 0, "total": 0}, "TempFoldersStatus": {"error": 0, "succes": 0, "total": 0}, "TempDirsStatus": {"error": 0, "succes": 0, "total": 0}})


        if len(selectedDisks) == 0:
            return


        # Delete.

        DrawBanner()
        if not isAdmin():
            print(f"\n          {gray}[ {orange}Warning: {bold}Program is running without administrator permissions. May delete less files.{gray}]{end}")

        print(f"                                       {gray}[ {green}Info: {bold}Deleting process started.{gray}]{end}")

        for i, disk in enumerate(selectedDisks):
            
            # Delete .tmp files.
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if file.endswith(".tmp"):
                        tmp_file_path = os.path.join(root, file)
                        disksStatus[i]["TempFilesStatus"]["total"] += 1

                        try:
                            os.remove(tmp_file_path)
                            disksStatus[i]["TempFilesStatus"]["succes"] += 1
                            
                        except:
                            disksStatus[i]["TempFilesStatus"]["error"] += 1

            if "c" in disk.lower() and platform.system() == "Windows":
                # Delete files in Temp folder.
                temp_folder_path = f"C:\\Users\\{gp.getuser()}\\AppData\\Local\\Temp\\"

                try:
                    for root, dirs, files in os.walk(temp_folder_path):
                        for file in files:
                            folder_file_path = os.path.join(root, file)
                            disksStatus[i]["TempFoldersStatus"]["total"] += 1

                            try:
                                os.remove(folder_file_path)
                                disksStatus[i]["TempFoldersStatus"]["succes"] += 1

                            except:
                                disksStatus[i]["TempFoldersStatus"]["error"] += 1

                except Exception as TempFoldersStatusERROR:
                    disksStatus[i]["TempFoldersStatus"]["error"] = -1


                # Delete dirs in Temp folder
                try:
                    dirs  = [f for f in os.listdir(temp_folder_path) if not os.path.isfile(os.path.join(temp_folder_path, f))]
                    for dir in dirs:
                        disksStatus[i]["TempDirsStatus"]["total"] += 1

                        try:
                            os.rmdir(temp_folder_path+dir)
                            disksStatus[i]["TempDirsStatus"]["succes"] += 1

                        except:
                            disksStatus[i]["TempDirsStatus"]["error"] += 1

                except Exception as TempDirsStatusERROR:
                    disksStatus[i]["TempDirsStatus"]["error"] = -1
                

        # Print results.
        DrawBanner()
        for disk in disksStatus:
            print(f"\n\n                {orange}• {bold}{disk['name']}{end}")
            print(f"                        {orange}╰• {bold}.tmp files:{end}")
            print(f"                            {blue}╰• Total: {disk['TempFilesStatus']['total']}{end}")
            print(f"                            {green}╰• Succes: {disk['TempFilesStatus']['succes']}{end}")
            print(f"                            {red}╰• Errors: {disk['TempFilesStatus']['error']}{end}")


            if "c" in disk["name"].lower():
                print(f"\n                        {orange}╰• {bold}Files in /Temp folder:{end}")
                print(f"                            {blue}╰• Total: {disk['TempFoldersStatus']['total']}{end}")
                print(f"                            {green}╰• Succes: {disk['TempFoldersStatus']['succes']}{end}")
                print(f"                            {red}╰• Errors: {f'Fatal error: {TempFoldersStatusERROR}' if disk['TempFoldersStatus']['error'] == -1 else disk['TempFilesStatus']['error']}{end}")

                print(f"\n                        {orange}╰• {bold}Dirs in /Temp folder:{end}")
                print(f"                            {blue}╰• Total: {disk['TempDirsStatus']['total']}{end}")
                print(f"                            {green}╰• Succes: {disk['TempDirsStatus']['succes']}{end}")
                print(f"                            {red}╰• Errors: {f'Fatal error: {TempDirsStatusERROR}' if disk['TempDirsStatus']['error'] == -1 else disk['TempDirsStatus']['error']}{end}")

        WaitForEnter()


# Clear screen function.
def cls(): os.system("cls || clear")

# Check if character is number.
def isNumber(n):
    try:
        int(n)
        return True
    except:
        return False
    

# Main loop.
while True:

    # Draw main screen.
    DrawBanner()
    DrawMenu_Main()
    main_action = input(f"\n                               {orange}~{bold} ").lower().replace(" ", "")

    # Check user input correction.
    if not isNumber(main_action):
        continue

    else:
        main_action = int(main_action)

        if main_action not in range(0, 3):
            continue 

    # Handle user choose. 
    if main_action == 0:
        cls()
        print(f"{red}Good{orange}bye{bold}!{end}")
        exit()
    
    if main_action == 1:
        Manual.Main()

    if main_action == 2:
        Automatic.Main()


    


