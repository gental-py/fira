# Functions: rename, open, edit?
# TODO: add ability to cancel action by :stop | write in <rprompt> how to cancel
# TODO: logs. (Maybe ability to undo.)
# chnglog: Changed shlex with argParse() function, added TUI, added ManualOperations option.


class Program:
    version = 0.3

# Import libaries.
from prompt_toolkit.completion import NestedCompleter, WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.formatted_text import HTML
import getpass as gp
import platform
import fnmatch
import shutil
import ctypes
import sys
import re
import os



# Minor functions.
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

def cls(): 
    os.system("cls || clear")

def argParse(string):
    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                             r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                             r'|\S+)\s*', string, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace') \
                .decode('unicode-escape')
        try:
            arg = type(string)(arg)
        except UnicodeError:
            pass
        rv.append(arg)
    return rv


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
    print(f"{red}You are not running FiraFiles on Windows.{end}")
    exit()



# Menus.
def DrawBanner():
    cls()
    print(f"""{red}⠀⠀⠀⠀⠀⠀⢱⣆⠀⠀⠀⠀⠀⠀ {orange}\n{red}⠀⠀⠀⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⠀ {orange}                           \n{red}⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣧⠀⠀⠀ {orange}                             \n{red}⠀⠀⠀⠀⡀⢠⣿⡟⣿⣿⣿⡇⠀⠀ {orange}     ███████╗██╗██████╗░░█████╗░███████╗██╗██╗░░░░░███████╗░██████╗\n{red}⠀⠀⠀⠀⣳⣼⣿⡏⢸⣿⣿⣿⢀⠀ {orange}     ██╔════╝██║██╔══██╗██╔══██╗██╔════╝██║██║░░░░░██╔════╝██╔════╝\n{red}⠀⠀⠀⣰⣿⣿⡿⠁⢸⣿⣿⡟⣼⡆ {orange}     █████╗░░██║██████╔╝███████║█████╗░░██║██║░░░░░█████╗░░╚█████╗░\n{red}⢰⢀⣾⣿⣿⠟⠀⠀⣾⢿⣿⣿⣿⣿ {orange}     ██╔══╝░░██║██╔══██╗██╔══██║██╔══╝░░██║██║░░░░░██╔══╝░░░╚═══██╗\n{red}⢸⣿⣿⣿⡏⠀⠀⠀⠃⠸⣿⣿⣿⡿ {orange}     ██║░░░░░██║██║░░██║██║░░██║██║░░░░░██║███████╗███████╗██████╔╝\n{red}⢳⣿⣿⣿⠀ {bold}{Program.version}{red}⠀ ⢹⣿⡿⡁{orange}     ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═════╝░\n{red}⠀⠹⣿⣿⡄⠀⠀⠀⠀⠀⢠⣿⡞⠁ {orange}                                                       {bold}@{underline}gental{end}\n{red}⠀⠀⠈⠛⢿⣄⠀⠀⠀⣠⠞⠋⠀⠀ {orange}                                                        \n{red}⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀{end}""")

def DrawMenu_Main():  
    print(f"""                    {orange}           [ {red}1 {orange}]  {bold}Manual operations.    \n                    {orange}           [ {red}2 {orange}]  {bold}Automatic operations. \n                    {orange}           [ {red}0 {orange}]  {red}Exit.{end}""")

def DrawMenu_Automatic():  
    print(f"""                    {orange}           [ {red}1 {orange}]  {bold}Find files.    \n                    {orange}           [ {red}2 {orange}]  {bold}Clean disks.\n                    {orange}           [ {red}3 {orange}]  {bold}Format disk.#  \n                    {orange}           [ {red}0 {orange}]  {red}Back.{end}""")



# Input validators.
class MenuInputValidator(Validator):
    MAX_RANGE = 0

    def validate(self, document):
        text = document.text

        if text == "":
            raise ValidationError(message="")

        if not text.isdigit():
            raise ValidationError(message='Input contains non-numeric characters!')

        if int(text) not in range(0, MenuInputValidator.MAX_RANGE):  
            raise ValidationError(message='Number is out of range!')                            

        if len(text) != 1:
            raise ValidationError(message='Input is too long!')

class PathInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if not os.path.exists(text) and text != "":
            raise ValidationError(message="This path does not exists!")

class TargetInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if text.replace(" ","") == "":
            raise ValidationError(message="Target cannot be blank!")

class DiskConfirmationInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if text.replace(" ","") == "":
            raise ValidationError(message="Input cannot be blank!")

        if text not in ("x", "no", "n", "0", "v", "yes", "y", "1"):
            raise ValidationError(message="Invalid input.")

class ManualInputValidator(Validator):
    FILE_SELECTED_NAME = ""
    FILE_SELECTED = False
    DIR_SELECTED_NAME = ""
    DIR_SELECTED = False
    ALL_DISKS = []
    PREFIXES = []
    FILES = []
    DIRS = []

    def validate(self, document):
        text = document.text
        parsed_text = argParse(text)

        if text.replace(" ","") == "":
            raise ValidationError(message="Input cannot be blank!")

        if not text.startswith(ManualInputValidator.PREFIXES):
            raise ValidationError(message="None command prefix!")

        if text.startswith(":disk"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No disk specifed!")

            if parsed_text[1]+"\\" not in ManualInputValidator.ALL_DISKS:
                raise ValidationError(message="Invalid disk!")
      
        if text.startswith(":goto"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No directory specifed!")

            if parsed_text[1] not in ManualInputValidator.DIRS:
                raise ValidationError(message="Invalid directory!")

        if text.startswith(":select"):
            if len(parsed_text) < 2:
                raise ValidationError(message=f"No file specifed!")

            if parsed_text[1] not in ManualInputValidator.FILES:
                raise ValidationError(message="Invalid file!")

        if text.startswith(":dirselect"):
            if len(parsed_text) < 2:
                raise ValidationError(message=f"No dir specifed!")

            if parsed_text[1] not in ManualInputValidator.DIRS:
                raise ValidationError(message="Invalid dirname!")

        if text.startswith(":unselect"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

        if text.startswith(":dirunselect"):
            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No dir selected!")

        if text.startswith(":move"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

        if text.startswith(":copy"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

            if ManualInputValidator.FILE_SELECTED_NAME in ManualInputValidator.FILES:
                raise ValidationError(message="File with this name actually exists in this location!")

        if text.startswith(":dircopy"):
            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No file selected!")

            if f"[{ManualInputValidator.DIR_SELECTED_NAME}]" in ManualInputValidator.DIRS:
                raise ValidationError(message="Dir with this name actually exists in this location!")


# Operations section.
class Manual:
    def Main():

        class Important:
            # :back // :..       Go to previous directory.
            # :goto <folder>     Go to folder.
            # :select <file>     Select file to operate on. 
            # :dirselect <dir>   Select dir to operate on.
            # :unselect          Clear selection.
            # :dirunselect       Clear dir selection.
            # :stop              Go back to main menu.
            # :disk <disk>       Set work disk.
            # :move              Move selected file to selected dir location.
            # :copy               Copy and paste selected file to selected dir location.
            # TODO: :refresh            Refresh filetree.
            # TODO: :dircopy            Copy and paste selected directory to current location.
            # TODO: :dirmove            Move selected dir to current location.
            # TODO: :edit               Edit selected file in multiline input.
            # TODO: :help               Print help page.


            current = os.getcwd()
            selected_fileLOC = None
            selected_fileNAME = None
            selected_dirNAME = None
            selected_dirLOC = None
            prompt_session = PromptSession()
            allDisks = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
            actions = (":back", ":goto", ":select", ":unselect", ":stop", ":..", ":disk", ":move", ":copy", ":dirselect", ":dirunselect", ":dircopy", ":dirmove")
            ManualInputValidator.PREFIXES = actions
            ManualInputValidator.ALL_DISKS = allDisks
    


        # Main loop
        while True:
            DrawBanner()
            
            # Fetch files and folders.
            wc_Dirs = []
            wc_Files = []

            for obj in os.listdir(Important.current):
                if not os.path.isdir(f"{Important.current}\\{obj}"): wc_Files.append(obj)
                else: wc_Dirs.append(f"[{obj}]")

            ManualInputValidator.DIRS = wc_Dirs
            ManualInputValidator.FILES = wc_Files


            # Draw file tree
            print(f"\n\n  {cyan}╭─< {bold}{Important.current} {cyan}>•{end}\n  {cyan}│{end}")
            for dir in wc_Dirs: 
                if dir.replace("[", "", 1)[:-1]+"\\" == Important.selected_dirNAME and Important.current+"\\"+Important.selected_dirNAME+"\\" == Important.selected_dirLOC+"\\": print(f"{purple}->{cyan}├ {blink}{bold}{dir}{end}")
                else: print(f"  {cyan}├ {bold}{dir}{end}")

            print(f"  {blue}⋮{end}")
            for file in wc_Files:
                if file == Important.selected_fileNAME and Important.current+"\\"+Important.selected_fileNAME == Important.selected_fileLOC: print(f"{orange}->{cyan}├ {blink}{bold}{file}{end}")
                else: print(f"  {cyan}├ {bold}{file}{end}")

            print(f"  {cyan}╰{red}•{end}")


            # Auto completer.
            Completer = NestedCompleter.from_nested_dict({
                ':back': None,
                ':stop': None,
                ':move': None,
                ':copy': None,
                ':dirmove': None,
                ':dircopy': None,
                ':unselect': None,
                ':dirunselect': None,
                ':goto': WordCompleter(wc_Dirs),
                ':select': WordCompleter(wc_Files),
                ':dirselect': WordCompleter(wc_Dirs),
                ':disk': WordCompleter(Important.allDisks)
            })
            

            # Bottom toolbar.
            def BottomToolbar(current, selectedfile, selecteddir):
                return HTML(f'Current:  <b><style bg="ansiblue">{current} </style></b>\nSelected file: <b><style bg="ansiblue">{selectedfile} </style></b>\nSelected dir:  <b><style bg="ansiblue">{selecteddir} </style></b>')


            # Get action
            action = Important.prompt_session.prompt(f'\n  ~  ', completer=Completer, validator=ManualInputValidator(), bottom_toolbar=BottomToolbar(Important.current, Important.selected_fileLOC, Important.selected_dirLOC), auto_suggest=AutoSuggestFromHistory())
            parsed_action = argParse(action)



            if parsed_action[0] == ":stop": break

            if parsed_action[0] == ":back" or parsed_action[0] == ":..":
                Important.current = os.path.dirname(Important.current)
                
            if parsed_action[0] == ":disk":
                Important.current = parsed_action[1] + "\\"

            if parsed_action[0] == ":goto":
                Important.current += "\\"+parsed_action[1].replace("[", "", 1)[:-1]

            if parsed_action[0] == ":select":
                Important.selected_fileLOC = Important.current+"\\"+parsed_action[1]
                Important.selected_fileNAME = parsed_action[1]
                ManualInputValidator.FILE_SELECTED = True
                ManualInputValidator.FILE_SELECTED_NAME = Important.selected_fileNAME

            if parsed_action[0] == ":unselect":
                Important.selected_fileLOC = None
                Important.selected_fileNAME = None
                ManualInputValidator.FILE_SELECTED = False
                ManualInputValidator.FILE_SELECTED_NAME = None

            if parsed_action[0] == ":dirselect":
                Important.selected_dirLOC = Important.current+"\\"+parsed_action[1].replace("[", "", 1)[:-1]+"\\"
                Important.selected_dirNAME = parsed_action[1].replace("[", "", 1)[:-1]+"\\"
                ManualInputValidator.DIR_SELECTED = True
                ManualInputValidator.DIR_SELECTED_NAME = parsed_action[1].replace("[", "", 1)[:-1]+"\\"

            if parsed_action[0] == ":dirunselect":
                Important.selected_dirLOC = None
                Important.selected_dirNAME = None
                ManualInputValidator.DIR_SELECTED = False
                ManualInputValidator.DIR_SELECTED_NAME = None

            # FIXME: copy/move not to current but to selected dir
            if parsed_action[0] == ":move":
                try:
                    shutil.move(Important.selected_fileLOC, Important.current+"//"+Important.selected_fileNAME)
                    Important.selected_fileLOC = Important.current+"\\"+Important.selected_fileNAME

                except Exception as e:
                    DrawBanner()
                    print(f"              {gray}[ {red}Error: {bold}Cannot move file. {e}{gray}]{end}")
                    WaitForEnter()

            if parsed_action[0] == ":copy":
                shutil.copyfile(Important.selected_fileLOC, Important.current+"\\"+Important.selected_fileNAME)

            # FIXME: Not working.
            if parsed_action[0] == ":dircopy":
                os.mkdir(Important.current+Important.selected_dirNAME)
                for file in os.walk(Important.selected_dirLOC):
                    shutil.copyfile(file, Important.current+Important.selected_dirNAME)
                


class Automatic:
    def Main():
        while True:

            # Menu.
            DrawBanner()
            DrawMenu_Automatic()


            # Get action.
            MenuInputValidator.MAX_RANGE = 4
            action = int(prompt('\n                               ~ ', validator=MenuInputValidator()))
            

            # Handle user action. 
            if action == 0: return
            if action == 1: Automatic.FindFile()
            if action == 2: Automatic.CleanDisks()


    def FindFile():
        DrawBanner()

        # Fetch data.
        target, location, allHits, allDisks = "", "", [], re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
             
        target = prompt('                         Target ~ ', validator=TargetInputValidator())
        location = prompt('                       Location ~ ', validator=PathInputValidator())
     

        # Find file(s).
        print(f"                          {bold}Searching . . .{end}")

        if location != "": allDisks = [location]
        for disk in allDisks:
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if fnmatch.fnmatch(file, target):
                        allHits.append(os.path.join(root, file))
        

        # Print results.
        DrawBanner()
        print(f"                          {red}• {bold}Found {orange}{len(allHits)} {bold}file(s).{end}\n")
        for hit in allHits: print(f"                 {orange}• {bold}{hit}{end}")
        WaitForEnter()


    def CleanDisks():
        allDisks = []
        disksStatus = []
        for disk in re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE):
            allDisks.append({"name": disk, "state": False})

        # Select disk(s)
        def DisplaySelection():
            DrawBanner()

            print(f"                      {bold}Select which disks you want to be cleaned.{end}\n\n")
            for disk in allDisks:
                print(f"                           {orange}• {bold}{disk['name']} {gray}: {f'{green}v{end}' if disk['state'] else f'{red}x{end}'}")

        def BottomToolbar():
            return HTML('<b><style bg="green">v, yes, y, 1</style></b> <style bg="gray">//</style> <b><style bg="red">x, no, n, 0</style></b>')

        for disk in allDisks:        
            DisplaySelection()

            state_input = prompt(f'\n                            {disk["name"]} ~ ', validator=DiskConfirmationInputValidator(), bottom_toolbar=BottomToolbar())
            if state_input in ("v", "yes", "y", "1"):
                disk["state"] = True
                disksStatus.append({"name": disk["name"], "TempFilesStatus": {"error": 0, "succes": 0, "total": 0}, "TempFoldersStatus": {"error": 0, "succes": 0, "total": 0}, "TempDirsStatus": {"error": 0, "succes": 0, "total": 0}})


        # Delete.
        DrawBanner()
        if not isAdmin():
            print(f"\n          {gray}[ {orange}Warning: {bold}Program is running without administrator permissions. May delete less files.{gray}]{end}")
        print(f"                                       {gray}[ {green}Info: {bold}Deleting process started.{gray}]{end}")

        for i, disk in enumerate(allDisks):
            if disk["state"] == False:
                continue

            # Delete .tmp files.
            for root, dirs, files in os.walk(disk["name"]):
                for file in files:
                    if file.endswith(".tmp"):
                        tmp_file_path = os.path.join(root, file)
                        disksStatus[i]["TempFilesStatus"]["total"] += 1

                        try:
                            os.remove(tmp_file_path)
                            disksStatus[i]["TempFilesStatus"]["succes"] += 1
                            
                        except:
                            disksStatus[i]["TempFilesStatus"]["error"] += 1

            # Delete files in Temp folder.
            if "c" in disk["name"].lower():
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
                    dirs = [f for f in os.listdir(temp_folder_path) if not os.path.isfile(os.path.join(temp_folder_path, f))]
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


# Main menu loop.
while True:

    # Draw main screen.
    DrawBanner()
    DrawMenu_Main()

    # Get user action.
    MenuInputValidator.MAX_RANGE = 3
    main_action = int(prompt('\n                               ~ ', validator=MenuInputValidator()))

    # Handle user action. 
    if main_action == 0:
        DrawBanner()
        exit()
    
    if main_action == 1:
        Manual.Main()

    if main_action == 2:
        Automatic.Main()


    


