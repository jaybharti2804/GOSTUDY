#Importing all the needed modules and packages.
import mysql.connector
from tabulate import tabulate
import time
import pwinput

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


print_login_page = ('''
           #      ####   ####  ##### ##    #        ####    #    ####  #####
           #     #    # #        #   # #   #        #   #  # #  #      #
           #     #    # #  ###   #   #  #  #        ####  ##### #  ### ####
           #     #    # #    #   #   #   # #        #     #   # #    # #
           #####  ####   ####  ##### #    ##        #     #   #  ####  #####
''')

user_id = ""

def signup(newuser_name, newuser_email, newuser_passwd):
    c =("INSERT INTO user_credits(name, email, password) VALUES(%s, %s, %s)")
    x =(newuser_name, newuser_email, newuser_passwd)
    db_cursor.execute(c,x)
    AJA.commit()
    print("\nNew user with name", newuser_name ," added successfully.")
    db_cursor.execute("SELECT id FROM user_credits WHERE name='" + newuser_name + "'" )
    y = db_cursor.fetchall();
    a = str(y)
    user_id_open = open('user_id.txt','w')
    user_id_open.write(user_id)
    user_id_open.close()
    return a

def delete_user(name, password):
    x =("SELECT password FROM user_credits WHERE name='"+ name +"'")
    a = db_cursor.execute(x)
    a = db_cursor.fetchall();
    b = str(a)
    if password == b[slice(3,-4)]:
        print("\nCORRECT PASSWORD")
        print("ARE YOU SURE YOU WANT TO DELETE THE USER -",name)
        sure = str(input("Enter (y/n) : "))
        if sure in 'yY':
            db_cursor.execute("DELETE * FROM user_credits WHERE name='"+ name +"'")
            AJA.commit()
        else:
            print("\nUser not deleted")
            
    else :
        print("\nWRONG PASSWORD")

# Importing random to generate
# random string sequence
import random
	
# Importing string library function
import string
	
def rand_pass(size):
		
	# Takes random choices from
	# ascii_letters and digits
	generate_pass = ''.join([random.choice( string.ascii_uppercase +
											string.ascii_lowercase +
											string.digits)
											for n in range(size)])
							
	return generate_pass



def reset_password():
    print("\n==========PASSWORD RESET============\n")
    name = str(input("Enter your name : "))
    email = str(input("Enter your e-mail : "))
    otpgen = rand_pass(8)
    # Python code to illustrate Sending mail from
    # your Gmail account
    import smtplib

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("jaybharti5678@gmail.com", "jay_bharti420")

    # message to be sent
    message ='''
     ... From: GOSTUDY
     ... PASSWORD RESET OTP'...
     ...
     ... Your OTP for resetting your GOSTUDY accout password is: '''+ otpgen +''' '''
    #"Your OTP for resetting your GOSTUDY accout password is :" + str(otpgen)

    # sending the mail
    s.sendmail("jaybharti5678@gmail.com", email, message)

    # terminating the session
    s.quit()
    print("\nWe've sent an otp to your email id to verify that its you")
    otp = str(input("Enter the OTP :"))
    if otp == otpgen:
        while True:
            print("\n")
            new_password1 = pwinput.pwinput(prompt="Enter new password : ", mask="●")
            new_password2 = pwinput.pwinput(prompt="Confirm new password : ", mask="●")
            if new_password1 == new_password2:
                db_cursor.execute("UPDATE user_credits SET password='"+ new_password2 +"' WHERE name='"+ name +"'")
                AJA.commit()
                print("PASSWORD reset successful")
                break
            else:
                print("\nPassword did not match")
                print("Try Again")
                import time
                time.sleep(3)
                continue
    else:
        print("OTP did not match")
        import time
        time.sleep(3)


def update_user():
    print("\nUSER CREDITIALS CAN ONLY BE UPDATED FOR EXISTING USERS")
    name = str(input("\nENTER YOUR NAME : "))
    password = pwinput.pwinput(prompt="ENTER NEW PASSWORD : ", mask="●")
    x =("SELECT password FROM user_credits WHERE name='"+ name +"'")
    a = db_cursor.execute(x)
    a = db_cursor.fetchall();
    b = str(a)
    c = db_cursor.execute("SELECT id FROM user_credits WHERE name='"+ name +"'")
    e = db_cursor.fetchall();
    d = str(e)
    if password == b[slice(3,-4)]:
        print("\nCORRECT PASSWORD")
        print("\nWhat details do you want to update??")
        print("\nWhat do you want to update for the user")
        print("\nEnter the serial numbers of detail you want to update")
        print("\nSELECT 1 for updating NAME")
        print("SELECT 2 for updating E-MAIL")
        print("SELECT 3 for updating PASSWORD")
        print("\nExample - Enter : 13 to update NAME and PASSWORD\n")
        what_to_update = str(input("Enter : "))
        if '1' == what_to_update:
            print("\n")
            new_name = str(input("Enter new name : "))
            db_cursor.execute("UPDATE user_credits SET name ='"+ new_name +"' WHERE id ='"+ d[slice(2,-3)] +"'")
            AJA.commit()
        if '2' in what_to_update:
            print("\n")
            new_email = str(input("Enter new E-mail : "))
            db_cursor.execute("UPDATE user_credits SET email='"+ new_email +"' WHERE id='"+ d[slice(2,-3)] +"'")
            AJA.commit()
        if '3' in what_to_update:
            print("\n")
            new_passwd = str(input("Enter new password : "))
            db_cursor.execute("UPDATE user_credits SET password='"+ new_passwd +"' WHERE id='"+ d[slice(2,-3)] +"'")
            AJA.commit()
        print("\nUser credits updated successfully")
        import time
        time.sleep(3)
    else:
        print("\nWrong Password")
        import time
        time.sleep(3)



while True:
    import os
    os.system('cls')
    print(print_login_page)

    #Checking if the user is new or old
    print("\n|========LOG IN PAGE=========|")
    print("|LOG IN                 - 0  |")
    print("|SIGN UP                - 1  |")
    print("|DELETE A USER          - 2  |")
    print("|UPDATE USER CREDITIALS - 3  |")
    print("|============================|")
    neworold_user = str(input("\nENTER : "))
    #(Sign up)Creating new user by adding to table- user_credits
    if neworold_user == "1":
        while True:
            newuser_name = str(input("ENTER YOUR NAME : "))
            x =("SELECT name FROM user_credits")
            db_cursor.execute(x)
            a = db_cursor.fetchall()
            if newuser_name in a:
                print("\nThe Username is already taken please Enter a new Username\n")
                continue
            else:
                break
        newuser_email = str(input("ENTER YOUR E-MAIL ID : "))
        newuser_passwd = pwinput.pwinput(prompt="CREATE A PASSWORD : ", mask="●")
        a = signup(newuser_name, newuser_email, newuser_passwd)
        user_id = user_id + a[2]
    #Delete a user
    elif neworold_user == "2":
        name = str(input("ENTER YOUR NAME : "))
        password = pwinput.pwinput(prompt="ENTER YOUR PASSWORD : ", mask="●")
        delete_user(name, password)    


    #Update user_credits
    elif neworold_user == "3":
        update_user()


    elif neworold_user == "0":
        name = str(input("\nENTER YOUR NAME : "))
        # password = str(input("ENTER YOUR PASSWORD : "))
        password = pwinput.pwinput(prompt="ENTER YOUR PASSWORD : ", mask="●")

        x =("SELECT password FROM user_credits WHERE name='"+ name +"'")
        a = db_cursor.execute(x)
        a = db_cursor.fetchall();
        b = str(a)
        if password == b[slice(3,-4)]:
            print("\nCORRECT PASSWORD")
            print("LOGGING IN......")
            import time
            time.sleep(4)
            db_cursor.execute("SELECT id FROM user_credits WHERE name='" + name + "'" )
            y = db_cursor.fetchall();
            a = str(y)
            user_id = a[2]
            user_id_open = open('user_id.txt','w')
            user_id_open.write(user_id)
            user_id_open.close()
            #Telling the user_id of user
            print("\nYOUR USER ID IS ", user_id)
            import os
            os.system('main_menu.py')
        else :
            print("\nINCORRECT USERNAME or PASSWORD\n")
            print("1 - Re-try")
            print("0 - Forgot password(RESET)\n")
            reorre = str(input("Enter : "))
            if reorre == '1':
                continue
            elif reorre == '0':
                reset_password()
                continue



    else:
        print("\nINCORRECT INPUT")
        print("\nPlease try again")
        time.sleep(3)
        continue
