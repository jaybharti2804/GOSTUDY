import os
import pwinput

os.system('cls')
print_setup_page = ('''
                 ##### ##### ##### #    # ####        ####    #    ####  #####
                #      #       #   #    # #   #       #   #  # #  #      #
                 ####  ###     #   #    # ####        ####  ##### #  ### ####
                     # #       #   #    # #           #     #   # #    # #
                #####  #####   #    ####  #           #     #   #  ####  #####
''')
x = open("new=0,old=1.txt","r")
y = x.read()
x.close()
if y=='1':
    import os
    os.system('user_authentification.py')
else:
    import os
    print("\nINSTALLING ALL THE NEEDED MODULES AND PACKAGES IF NOT INSTALLED ALREADY\n")
    print("This may take some time.......\n")
    os.system('install_modules_needed.py')
    print("\nAll MODULES AND PACKAGES NEEDED INSTALLED SUCCESSFULLY")
    print("\nPLEASE GO THROUGH THE GUIDE")
    import time
    time.sleep(3)
    os.system('GUIDE.txt')
    os.system('cls')
    print(print_setup_page)
    print("\nPLEASE ENTER THE DETAILS OF YOUR MySQL server to be used :\n")
    a = str(input("Enter name of the host : "))
    b = str(input("Enter name of the user : "))
    c = pwinput.pwinput(prompt="Enter the password : ", mask="●")
    open_details = open("server_details.txt","w")
    L = [a, b, c]
    open_details.write(a+"\n"+ b +"\n" +c)
    open_details.close()
    import mysql.connector
    AJA = mysql.connector.connect(
    host = a,
    user = b,
    passwd = c,
    )

    #Cursor
    db_cursor = AJA.cursor()
    print('CREATING DATABSE AND TABLES NEEDED')
    sql = "CREATE DATABASE IF NOT EXISTS gostudy"
    db_cursor.execute(sql)
    #creating the needed tables if they do not exist
    import os
    os.system('create_tables_needed.py')
    g = "1"
    x = open("new=0,old=1.txt","w")
    x.write(g)
    x.close()
    import os
    os.system('user_authentification.py')

