#Importing all the needed modules and packages.
import mysql.connector
from tabulate import tabulate
import time

user_id_open = open('user_id.txt','r')
user_id = str(user_id_open.read())

open_details = open("server_details.txt","r")
a = str(open_details.readline())
b = str(open_details.readline())
c = str(open_details.readline())
open_details.close()
AJA = mysql.connector.connect(
    host = a,
    user = b,
    passwd = c,
    database = "gostudy",
    )
db_cursor = AJA.cursor()

print_work_groups = ('''
            #     #  ####  ####  #  #       ####  ####   ####  #    # ####   #####
            #     # #    # #   # # #       #      #   # #    # #    # #   # #
            #  #  # #    # ####  ##        #  ### ####  #    # #    # ####   ####
            # # # # #    # #  #  # #       #    # #  #  #    # #    # #          #
             #   #   ####  #   # #  #       ####  #   #  ####   ####  #     #####
''')


#Dispays all work groups of the current user.
def display_all_work_groups():
    import os
    os.system('cls')
    print(print_work_groups)
    user_id_open = open('user_id.txt','r')
    user_id = user_id_open.read()
    db_cursor.execute("SELECT id, title FROM work_group WHERE user_id='"+user_id+"'")
    x = db_cursor.fetchall()
    print(tabulate(x, headers=['ID','WORK GROUP NAME'],tablefmt='grid'))
    print("\nEnter the id of the work group to OPEN it\n")
    print("Enter 00 to create new work group")
    print("Enter 000 to delete a work group")
    print("Enter 0000 to update a work group")
    print("Enter 0 if you want to go back to MAIN MENU\n")
    choice = str(input("Enter : "))
    if choice == "0":
        exit()
        # import os
        # os.system('main_menu.py')
    elif choice =="00":
        print('\n')
        name = str(input("Enter name for the new work group : "))
        add_new_work_group(name)
        display_all_work_groups()
    elif choice =="000":
        print('\n')
        id_to_delete = str(input("Enter the id of work group to be delete : "))
        delete_work_group(id_to_delete)
        display_all_work_groups()
    elif choice =="0000":
        print('\n')
        work_id_to_update = str(input("Enter the ID of the WORK GROUP TO BE UPDATED :"))
        print('\n')
        print("Enter 0 to change name of a work group")
        print("Enter 1 to add a new task to the work group")
        print("Enter 2 to delete a task from the work group")
        print('\n')
        choice = str(input("Enter the choice : "))
        if choice == '0':
            print('\n')
            new_name = str(input("Enter the new name for the Work group : "))
            update_work_group_name(work_id_to_update, new_name)
        elif choice =='1':
            create_new_task(work_id_to_update)
        elif choice =='2':
            print('\n')
            delete_task(work_id_to_update)
        display_all_work_groups()
                    
    else:
        import os
        os.system('cls')
        db_cursor.execute("SELECT title FROM work_group WHERE id ='"+choice+"'")
        wgn = db_cursor.fetchone()
        print("=========== WORK GROUP - "+ str(wgn)[2:-3] +" =============\n")
        db_cursor.execute("SELECT id, description, priority_lable, due_date, is_completed FROM tasks WHERE work_id ='"+choice+"'")
        x = db_cursor.fetchall()
        print(tabulate(x, headers=['ID','DESCRIPTION','PRIORITIY','DUE DATE','COMPLETION STATUS'],tablefmt='grid'))
        print("\nEnter 1 to add new task")
        print("Enter 2 to delete a task")
        print("Enter 3 to update a task")
        print("Enter 0 to go BACK")
        choice_task = str(input("Enter : "))
        if choice_task == "0":
            display_all_work_groups()
        elif choice_task == '2':
            wgtdf = str(choice)
            delete_task(wgtdf)
            display_all_work_groups()
        elif choice_task == '1':
            work_id = choice
            create_new_task(work_id)
            display_all_work_groups()
        elif choice_task =='3':
            to_update_from_work_group = choice
            update_task(to_update_from_work_group)
            display_all_work_groups()
        
#For deleting a work group
def delete_work_group(id_to_delete):
    delete = "DELETE FROM work_group WHERE id='"+id_to_delete+"'"
    db_cursor.execute(delete)   
    AJA.commit()
    print("\nWork group deleted successfully")
    import time
    time.sleep(3)
    
#Adds new work group
def add_new_work_group(name):
    c = "INSERT INTO work_group(title, user_id) VALUES(%s, %s)"
    x = (name, user_id)
    db_cursor.execute(c,x)
    AJA.commit()
    print("\nWork group ",name," added successfully")
    import time
    time.sleep(3)

#Updating a work groups name
def update_work_group_name(id_to_change, new_name):
    db_cursor.execute("UPDATE work_group SET title='"+ new_name +"' WHERE id='"+ id_to_change +"'")
    print("\nWork group name updated successfully")
    AJA.commit()
    import time
    time.sleep(3)

#for creating new tasks
def create_new_task(work_id):
    #description of the task ( newtask_description )
    print('\n')
    newtask_description = str(input("ENTER A NAME OR DESCRIPTION FOR NEW TASK : "))

    #slecting priority level( newtask_prioritylable )
    print("\nSELECT A PRIORITY LABLE -\n")
    print("ENTER 1 FOR - LOW PRIORITY")
    print("ENTER 2 FOR - MEDIUM PRORITY")
    print("ENTER 3 FOR - HIGH PRIORITY")
    print("ENTER 4 FOR - HIGHEST PRIORITY\n")
    priority_num = str(input("ENTER :"))
    if priority_num == "1":
        newtask_prioritylable = "LOW PRIORITY"
    elif priority_num == "2":
        newtask_prioritylable = "MEDIUM PRIORITY"
    elif priority_num == "3":
        newtask_prioritylable = "HIGH PRIORITY"
    elif priority_num == "4":
        newtask_prioritylable = "HIGHEST PRIORITY"
    else:
        newtask_prioritylable = "no priority level set"

    #asking if the task is completed or not ( completed_yes_no )
    print("\nIS THE TASK COMPLETE (Y for YES , N for NO) - \n")
    complete_not = str(input("ENTER (Y/N) : "))
    if complete_not == "Y" or complete_not == "y":
        completed_yes_no = "COMPLETED"
    if complete_not == "N" or complete_not == "n":
        completed_yes_no = "PENDING"    

    #selecting due date 
    print("\nSELECT THE DUE DATE -\n")
    year = str(input("Enter year : "))
    month = str(input("Enter month : "))
    date = str(input("Enter date : "))
    hour = str(input("Enter hours : "))
    minute = str(input("Enter minutes : "))
    second = str(input("Enter seconds : "))
    newtask_duedate = year +"-"+ month +"-"+ date +" "+ hour +":"+ minute +":"+ second
    #Selecting the work group to add in(work_id)
    c = "INSERT INTO tasks(description, priority_lable, due_date, is_completed, work_id) VALUES(%s, %s, %s, %s, %s)"
    x = (newtask_description ,newtask_prioritylable ,newtask_duedate, completed_yes_no, work_id)
    db_cursor.execute(c,x)
    AJA.commit()
    print("\nNew task",newtask_description,"created successfully")
    import time
    time.sleep(3)
    
#for deleting a task
def delete_task(wgtdf):
    print('\n')
    db_cursor.execute("SELECT description FROM tasks WHERE work_id ='"+ wgtdf +"'")
    tn = db_cursor.fetchall()
    task_to_delete = str(input("Enter the ID of the task you wish to delete : "))
    delete = "DELETE FROM tasks WHERE id = '" + task_to_delete + "'"
    db_cursor.execute(delete)   
    AJA.commit()
    print("Task "+ str(tn)[2:-3] + " deleted successfully")
    import time
    time.sleep(6)


    
#for updating a task
def update_task(to_update_from_work_group):
    print("\n")
    task_to_update = str(input("Enter the ID of the task to be updated : "))
    print("\nWhat do you want to update in task\n")
    print("\nEnter the serial numbers of detail you want to update\n")
    print("SELECT 1 for updating DESCRIPTION")
    print("SELECT 2 for updating PRIORITY")
    print("SELECT 3 for updating DUE DATE")
    print("SELECT 4 for updating COMPLETION STATUS")
    print("\nExample - Enter : 134 to update DESCRIPTION, DUE DATE AND COMPLETION STATUS\n")
    what_to_update = str(input("Enter : "))
    if '1' in what_to_update:
        print("\n")
        new_description = str(input("Enter new description : "))
        db_cursor.execute("UPDATE tasks SET description='"+ new_description +"' WHERE id='"+ task_to_update +"'")
        AJA.commit()
    if '2' in what_to_update:
        print("\nSELECT A PRIORITY LABLE -\n")
        print("ENTER 1 FOR - LOW PRIORITY")
        print("ENTER 2 FOR - MEDIUM PRIORITY")
        print("ENTER 3 FOR - HIGH PRIORITY")
        print("ENTER 4 FOR - HIGHEST PRIORITY\n")
        priority_num = str(input("ENTER :"))
        if priority_num == "1":
            new_prioritylable = "LOW PRIORITY"
        elif priority_num == "2":
            new_prioritylable = "MEDIUM PRIORITY"
        elif priority_num == "3":
            new_prioritylable = "HIGH PRIORITY"
        elif priority_num == "4":
            new_prioritylable = "HIGHEST PRIORITY"
        else:
            new_prioritylable = "no priority level set"
        db_cursor.execute("UPDATE tasks SET priority_lable='"+ new_prioritylable +"' WHERE id='"+ task_to_update +"'")
        AJA.commit()
    if '3' in what_to_update:
        print("SELECT THE DUE DATE -")
        year = str(input("Enter year : "))
        month = str(input("Enter month : "))
        date = str(input("Enter date : "))
        hour = str(input("Enter hours : "))
        minute = str(input("Enter minutes : "))
        second = str(input("Enter seconds : "))
        new_duedate = year +"-"+ month +"-"+ date +" "+ hour +":"+ minute +":"+ second
        x = "UPDATE tasks SET due_date='"+ new_duedate +"' WHERE id='"+ task_to_update +"'"
        db_cursor.execute(x)
        AJA.commit()
    if '4' in what_to_update:
        print("IS THE TASK COMPLETE (Y for YES , N for NO) - ")
        complete_not = str(input("ENTER (Y/N) : "))
        if complete_not == "Y" or complete_not == "y":
            new_completed_yes_no = "COMPLETED"
        if complete_not == "N" or complete_not == "n":
            new_completed_yes_no = "PENDING"        
        db_cursor.execute("UPDATE tasks SET is_completed='"+ new_completed_yes_no +"' WHERE id='"+ task_to_update +"'")
        AJA.commit()
    
    print('\n')
    print("The task was successfully updated")
    import time
    time.sleep(4)




display_all_work_groups()
