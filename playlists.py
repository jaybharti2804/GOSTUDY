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
#Connecting to the database
#PLEASE CHANGE THE DATABASE CREDITIALS AS PER YOUR SYSTEM
AJA = mysql.connector.connect(
    host = a,
    user = b,
    passwd = c,
    database = "gostudy",
    )
db_cursor = AJA.cursor()

print_playlists =('''
                    #####  #       #   #     #  #     ####### #     #######  #####  #######  #####
                    #    # #      # #   #   #   #        #    #        #    #          #    #
                    #####  #     #####   # #    #        #    #        #     #####     #     #####
                    #      #     #   #    #     #        #    #        #          #    #          #
                    #      ##### #   #    #     ##### ####### ##### #######  #####     #     #####
''')


def display_all_playlists():
    import  os
    os.system('cls')
    print(print_playlists)
    db_cursor.execute("SELECT id, name FROM playlist WHERE user_id= '" + user_id + "'")
    x = db_cursor.fetchall()
    print(tabulate(x, headers=['ID','PLAYLIST NAME'],tablefmt='grid'))
    print("\nEnter the id of the playlist to OPEN it\n")
    print("Enter 00 to create new playlist")
    print("Enter 000 to delete a playlist")
    print("Enter 0000 to update a playlist")
    print("Enter 0 if you want to go back to MAIN MENU\n")
    choice = str(input("Enter : "))
    if choice =='0':
        #exit()
        import os
        os.system('main_menu.py')
    elif choice == '00':
        print('\n')
        name = str(input("Enter name for new playlist : "))
        add_new_playlist(name)
        display_all_playlists()
    elif choice =='000':
        print('\n')
        id_to_delete = str(input("Enter the ID of the playlist to be deleted :"))
        delete_playlist(id_to_delete)
        display_all_playlists()
    elif choice =='0000':
        print('\n')
        id_to_change = str(input("Enter the id of the playlist to be updated : "))
        print('\n')
        new_name = str(input("Enter new name for the playlist : "))
        update_playlist(id_to_change, new_name)
        display_all_playlists()
    else:
        db_cursor.execute("SELECT name FROM playlist WHERE id ='"+choice+"'")
        pln = str(db_cursor.fetchall())
        import os
        os.system('cls')
        print("############## "+pln[3:-4]+" ##################")
        db_cursor.execute("SELECT id, name, artist FROM song WHERE playlist_id ='"+choice+"'")
        x = db_cursor.fetchall()
        print(tabulate(x, headers=['ID','SONG NAME','ARTIST'],tablefmt='grid'))
        print("\nEnter 00 to play the PLAYLIST")
        print("Enter 000 to add new song")
        print("Enter 0000 to delete a song")
        print("Enter the id of the song to played")
        print("Enter 0 for PLAYLISTS\n")
        choice_song = str(input("Enter : "))
        if choice_song == "0":
            display_all_playlists()
        elif choice_song =='00':
            #import subprocess
            #subprocess.Popen(play_playlist, choice)
            db_cursor.execute("SELECT name FROM playlist WHERE id ='"+choice+"'")
            pln = str(db_cursor.fetchall())
            print("\nPLAYING PLAYLIST - ",pln[2:-3],"\n")
            play_playlist(choice)
            display_all_playlists()
        
        elif choice_song == '0000':
            delete_song(choice)
            display_all_playlists()
        elif choice_song == '000':
            print('\n')
            search_text = str(input("Enter song name to search : "))
            print("\nDownloading song. Please wait..........\n")
            url = search_song(search_text)
            if url in ("SELECT url, COUNT(*) FROM song WHERE url='{url}'"):
                name,artist,location,duration = name_artist_location(url)
                a = "INSERT INTO song(name, artist, url, location, duration, playlist_id) VALUES(%s, %s, %s, %s, %s, %s)"
                b = (name, artist, url, location, duration, choice)
                db_cursor.execute(a,b)
                AJA.commit()
                db_cursor.execute("SELECT name FROM playlist WHERE id='"+ choice +"'")
                y = db_cursor.fetchone()
                print(name,"added to playlist",y,"successfully")
                import time
                time.sleep(3)
                display_all_playlists()
            else:
                name,artist,location,duration = download_song(url)
                a = "INSERT INTO song(name, artist, url, location, duration, playlist_id) VALUES(%s, %s, %s, %s, %s, %s) "
                b = (name, artist, url, location, duration, choice)
                db_cursor.execute(a,b)
                AJA.commit()
                db_cursor.execute("SELECT name FROM playlist WHERE id='"+ choice +"'")
                y = db_cursor.fetchone()
                print(name,"added to playlist",y,"successfully")
                display_all_playlists()
        else:
            print('\n')
            play_song(choice_song)
            display_all_playlists()

           
#Adding new playlist
def add_new_playlist(name):
    c = "INSERT INTO playlist(name, user_id) VALUES(%s, %s)"
    x = (name, user_id)
    db_cursor.execute(c,x)
    print("\nPlaylist ",name," added successfully")
    AJA.commit()
    import time
    time.sleep(3)
    
#Deleting a playlist    
def delete_playlist(id_to_delete):
    db_cursor.execute("DELETE FROM playlist WHERE id='"+id_to_delete+"'")
    AJA.commit()
    print("Playlist deleted successfully")
    time.sleep(3)

#Updating a playlist
def update_playlist(id_to_change, new_name):
    db_cursor.execute("UPDATE playlist SET name='"+ new_name +"' WHERE id='"+ id_to_change +"'")
    print("Name of the playlist updated")
    AJA.commit()
    time.sleep(3)

#searching for song in youtube
def search_song(search_text):
    from youtube_search import YoutubeSearch
    results = YoutubeSearch(search_text, max_results=10).to_dict()
    link_suffix = str(results[0])[slice(-13,-2)]
    url = "https://www.youtube.com/watch?v=" + link_suffix
    return url



def download_song(url):
    import pafy
    video = pafy.new(url)
    import os
    from os import path
    directory = os.getcwd()
    destination = directory+"\\songs" 
    name = video.title
    artist = video.author
    duration = str(video.length)
    new_name =name
    if "|" in name:
        new_name = new_name.replace('|','_')
    if "/" in name:
        new_name = new_name.replace('/','_')
    if ":" in name:
        new_name = new_name.replace(':','_')
    if "*" in name:
        new_name = new_name.replace('*','_')
    if '"' in name:
        new_name = new_name.replace('"','_')
    if "?" in name:
        new_name = new_name.replace('?','_')
    if '\\' in name:
        new_name = new_name.replace('\\','_')
    if "<" in name:
        new_name = new_name.replace('<','_')
    if ">" in name:
        new_name = new_name.replace('>','_')
    import os
    if path.exists(destination+"\\"+ new_name +".webm"):
        print("SONG ALREADY DOWNLOADED")
        print("Added to playlist")
    else:
        bestaudio = video.getbestaudio()
        bestaudio.download()
        file_name_list = os.listdir(directory)
        for i in file_name_list:
            if i[-3:]=="m4a":
                import shutil
                shutil.move(directory+"\\"+new_name+".m4a",new_name+".webm")
        pre_location = (directory +"\\"+ new_name +".webm")
        import shutil
        shutil.move(pre_location, destination+"\\"+new_name+".webm")
        print("SONG DOWNLOADED")
        print("Added to playlist")
    location = (destination+"\\"+new_name+".webm")
    return name,artist,location,duration


def name_artist_location(url):
    import pafy
    video = pafy.new(url)
    import os
    directory = os.getcwd()
    name = video.title
    artist = video.author
    location = (directory +"\\songs\\" + name + ".webm")
    return name,artist,location


def delete_song(id_to_delete_from):
    print('\n')
    delete = str(input("Enter ID of song to be deleted : "))
    db_cursor.execute("DELETE FROM song WHERE id='"+ delete +"'")
    AJA.commit()
    print("The song was deleted succesfully")
    import time
    time.sleep(3)

#def play_playlist(pid_to_play):
def play_playlist(pid_to_play):
    print("PLAYING PLEASE WAIT............")
    db_cursor.execute("SELECT id FROM song WHERE playlist_id='"+ pid_to_play +"' GROUP BY id")
    x = db_cursor.fetchall()
    for i in range(len(x)):
        sid_to_play = (str(x[i])[1:-2])
        play_song(sid_to_play)
        db_cursor.execute("SELECT duration FROM song WHERE id='"+ sid_to_play +"'")
        duration_str = db_cursor.fetchone()
        duration = str(duration_str[0])
        import time
        time.sleep(int(duration)-10)
    


    
#play a song
def play_song(sid_to_play):
    import os
    import vlc
    location = os.getcwdb()
    len_location = len(location)
    db_cursor.execute("SELECT location FROM song WHERE id = '"+ sid_to_play +"'");
    x = db_cursor.fetchone()
    a =str(x)[slice(len_location+8,-3)]
    db_cursor.execute("SELECT name FROM song WHERE id = '"+ sid_to_play +"'")
    n = db_cursor.fetchone()
    print('\n')
    print("Playing -",str(n)[slice(2,-3)])
    media = vlc.MediaPlayer(a)
    media.play()
    import time
    time.sleep(4)





display_all_playlists()
