#Importing all the needed modules and packages.
import mysql.connector
from tabulate import tabulate


user_id_open = open('user_id.txt','r')
user_id = str(user_id_open.read())


open_details = open("server_details.txt","r")
a = str(open_details.readline())
b = str(open_details.readline())
c = str(open_details.readline())
open_details.close()
#Connecting to the database
#PLEASE CHANGE THE DATABASE CREDITIALS AS PER YOUR SYSTEM
AJA = mysql.connector.connect(
    host = a,
    user = b,
    passwd = c,
    database = "gostudy",
    )
db_cursor = AJA.cursor()

print_notes =('''
            #     #  ####  ####### ######  #####
            # #   # #    #    #    #      #
            #  #  # #    #    #    ####    ####
            #   # # #    #    #    #           #
            #     #  ####     #    ###### #####
''')

def display_all_notes():
    import  os
    os.system('cls')
    print(print_notes)
    db_cursor.execute("SELECT id, date, title FROM notes WHERE user_id= '" + user_id + "'")
    x = db_cursor.fetchall()
    print(tabulate(x, headers=['ID','DATE','NOTES NAME'],tablefmt='grid'))
    print("\nEnter the id of the NOTE to OPEN it\n")
    print("Enter 00 to create new NOTE")
    print("Enter 000 to delete a NOTE")
    print("Enter 0000 to update a NOTE title")
    print("Enter 0 if you want to go back to MAIN MENU\n")
    choice = str(input("Enter : "))
    if choice =='0':
        exit()
        # import os
        # os.system('main_menu.py')
    elif choice =="00":
        print("\nPlease make sure that you don't use a already used Name\n")
        title = str(input("Enter title for new NOTE : "))
        create_new_note(title)
        display_all_notes()
    elif choice == "000":
        print("\n")
        id_to_delete = str(input("Enter the ID of the NOTE to be deleted :"))
        delete_note(id_to_delete)
        display_all_notes()
    elif choice == "0000":
        print("\n")
        id_to_change = str(input("Enter the ID of the NOTE to be updated : "))
        new_title = str(input("Enter new title for the NOTE : "))
        update_note_name(id_to_change, new_title)
    else:
        db_cursor.execute("SELECT title FROM notes WHERE id ='"+choice+"'")
        title = str(db_cursor.fetchone())[2:-3]
        import os
        from os import path
        directory = os.getcwd()
        os.system(directory+"\\notes\\"+ title +".txt")
        display_all_notes()

#add new note
def create_new_note(title):
    import os
    from os import path
    directory = os.getcwd()
    f = open(directory+"\\notes\\"+ title +".txt", "w")
    x = "============= "+ title +" ==============="
    f.write(x)
    f.close()
    import time
    date = time.strftime("%Y:%m:%d")
    c = "INSERT INTO notes(date, title, user_id) VALUES(%s, %s, %s)"
    x = (date, title, user_id)
    db_cursor.execute(c,x)
    print("\nNOTE ",title," added successfully")
    AJA.commit()
    import time
    time.sleep(3)
    display_all_notes()

#Deleting a note    
def delete_note(id_to_delete):
    db_cursor.execute("SELECT title FROM notes WHERE id='"+id_to_delete+"'")
    title = db_cursor.fetchone()
    db_cursor.execute("SELECT title FROM notes WHERE id ='"+id_to_delete+"'")
    title = str(db_cursor.fetchone())[2:-3]
    db_cursor.execute("DELETE FROM notes WHERE id='"+id_to_delete+"'")
    AJA.commit()
    import os
    from os import path
    directory = os.getcwd()
    os.remove(directory+"\\notes\\"+ title +".txt")
    print("\nNOTE deleted successfully")
    import time
    time.sleep(3)
    display_all_notes()



#update playlist name
def update_note_name(id_to_change, new_title):
    db_cursor.execute("SELECT title FROM notes WHERE id='"+id_to_change+"'")
    title = str(db_cursor.fetchone())[2:-3]
    db_cursor.execute("UPDATE notes SET title='"+ new_title +"' WHERE id='"+ id_to_change +"'")
    AJA.commit()
    import os
    from os import path
    directory = os.getcwd()
    import shutil
    shutil.move(directory+"\\notes\\"+title+".txt", directory+"\\notes\\"+new_title+".txt")
    print("NOTE name changed from ",title," to ", new_title, " sucessfully")
    import time
    time.sleep(3)
    display_all_notes()







display_all_notes()
