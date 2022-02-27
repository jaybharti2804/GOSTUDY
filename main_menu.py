def main_menu():
    import os

    #Providing the optins to perform different tasks
    printHomePage = ('''
      #    #  ####  ##   ## #####      ####   ###   ####  #####
      #    # #    # # # # # #          #   # #   # #      #
      ###### #    # #  #  # ###        ####  ##### #  ### ###
      #    # #    # #     # #          #     #   # #    # #
      #    #  ####  #     # #####      #     #   #  ####  #####


|========MAIN MENU========|
|=========================|
|  WORK GROUPS   -   1    |
|  PLAYLISTS     -   2    |
|  NOTES         -   3    |
|  TIMER         -   4    |
|  STOPWATCH     -   5    |
|                         |
|  EXIT          -   0    |
|=========================|
         ''')
    #Selecting one of the above options
    while True:
            os.system('cls')
            print(printHomePage)
            selected = str(input("\nENTER THE SELECTED NUMBER :"))
            #Exit
            if selected =='0':
                exit()
                
            #MY WORK GROUPS
            elif selected == '1':
                import os
                os.system('work_groups.py')

            #PLAYLISTS
            elif selected =='2':
                import os
                os.system('playlists.py')
                

            #NOTES
            elif selected =='3':
                import os
                os.system('notes.py')
            
            #START THE TIMER
            elif selected =='4':
                import os
                os.system('timer.py')


            
            #START THE STOPWATCH
            elif selected =='5':
                import os
                os.system('stopwatch.py')

            elif selected =='0':
                print("Good bye :)")
                import time
                time.sleep(3)
                exit()
                
            else:
                print("\nWrong input")
                main_menu()
main_menu()
