from cx_Freeze import setup, Executable

base = None
executables = [Executable("main.py", base="Win32GUI")]
packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
setup(
    name = "Youtube",
    options = options,
    version = "1.0",
    description = 'Une application Youtube, pour les nerd qui ne veulent pas aller sur internet et taper "https://youtube.fr/"',
    executables = executables
)