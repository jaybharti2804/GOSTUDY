import mysql.connector
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
db_cursor  = AJA.cursor()


db_cursor.execute('''CREATE TABLE IF NOT EXISTS user_credits(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(45), email VARCHAR(45), password VARCHAR(45))''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS work_group(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(45), user_id INT NOT NULL, FOREIGN KEY(user_id) REFERENCES user_credits(id))''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
description VARCHAR(45), priority_lable VARCHAR(45), due_date DATETIME, is_completed VARCHAR(45),
work_id INT NOT NULL, FOREIGN KEY(work_id) REFERENCES work_group(id))''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS playlist(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(45), user_id INT NOT NULL, FOREIGN KEY(user_id) REFERENCES user_credits(id))''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS song(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100),artist VARCHAR(45), url VARCHAR(45),location VARCHAR(300),duration VARCHAR(200),
playlist_id INT NOT NULL, FOREIGN KEY(playlist_id) REFERENCES playlist(id))''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS notes(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
date DATE, title VARCHAR(100),user_id INT NOT NULL, FOREIGN KEY(user_id) REFERENCES user_credits(id))''')
