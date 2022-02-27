def import_or_install(package):
    import pip
    try:
        __import__(package)
    except ImportError:
        print("Insalling",package)
        pip.main(['install', package])   
list_of_modules = ['mysql.connector',
                   'shutil',
                   'tabulate', 
                   'pwinput',
                   'time',
                   'os',
                   'pafy',
                   'vlc',
                   'tkinter',
                   'datetime',
                   'subprocess',
                   'youtube_search']
for package in list_of_modules:
    import_or_install(package)
