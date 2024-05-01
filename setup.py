import cx_Freeze
import sys
import os 

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"/Users/ritikbansal/Documents/GitHub/Text-Editor/setup.py"
os.environ['TK_LIBRARY'] = r"/Users/ritikbansal/Documents/GitHub/Text-Editor/setup.py"

executables = [cx_Freeze.Executable("vpad.py", base=base, icon="icon.ico")]

cx_Freeze.setup(
    name = "Vpad Text Editor",
    options = {
        "build_exe": {
            "packages":["tkinter", "os", "distutils"],
            "include_files":["icon.ico",'tcl86t.dll','tk86t.dll', 'icons2']
        }
    },
    version = "0.01",
    description = "Tkinter Application",
    executables = executables
)