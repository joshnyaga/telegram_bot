from telethon.sync import TelegramClient
import os
import csv
import time
import sys
import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import PeerFloodError
from decouple import config
from telethon.tl.types import InputPeerUser
os.system('cls||clear')
SLEEP_TIME = 10
print("Welcome "+os.getlogin()+" to Api Bot.Created by JoshNyaga")
print("==================================\n")



api_id = int(config('API_ID'))
api_hash = config('API_HASH')
phone = config('PHONE_NUMBER')
client = TelegramClient(phone, api_id, api_hash)
	
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('\nEnter the code: '))

#let the user choose if he wants to scrap messages	
running = 1   
while running == 1:
    print("==================MENU========================")
    print("1. Get all groups")
    print("2. Send message to scraped group members")
    print("3. Exit the application")


    mode = int(input("Choose an option: "))

    if mode ==1:
        chats = []
        last_date = None
        chunk_size = 200
        groups=[]
        
        result = client(GetDialogsRequest(
                    offset_date=last_date,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=chunk_size,
                    hash = 0
                ))
        chats.extend(result.chats)
            
        for chat in chats:
            try:
                #get only megagroups
                if chat.megagroup== True:
                    groups.append(chat)
            except:
                continue
        
        #print group names starting with a number
        print('Choose a group to scrape members from:')
        i=0
        for g in groups:
            print(str(i) + '- ' + g.title)
            
            target_group=groups[int(i)]

            print('Fetching Members...')
            all_participants = []
            all_participants = client.get_participants(target_group, aggressive=True)

            #stroring scapped memmbers in a csv	
            print('Saving group members for '+g.title+' In file...')
            with open("members.csv","a",encoding='UTF-8') as f:
                writer = csv.writer(f,delimiter=",",lineterminator="\n")
                writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
                for user in all_participants:
                    if user.username:
                        username= user.username
                    else:
                        username= ""
                    if user.first_name:
                        first_name= user.first_name
                    else:
                        first_name= ""
                    if user.last_name:
                        last_name= user.last_name
                    else:
                        last_name= ""
                    name= (first_name + ' ' + last_name).strip()
                    writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])   
            i+=1   
            print('Group '+ g.title+' members saved successfully')
        toclean = pd.read_csv('members.csv')
        deduped = toclean.drop_duplicates(["access hash"])
        deduped.to_csv('memberswithoutduplicates.csv')
        print("Number of records = ", len(pd.read_csv('members.csv')))
    
        
    elif mode ==2:
        #choose to send a message only to the scrapped members

        #message = input("Enter a message to send to the user: ")
        print("Starting the sending service...")
       

        with open("memberswithoutduplicates.csv", encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                if row[1] == "":
                    continue
                receiver = client.get_input_entity(row[1])
                try:
                    print("Sending Message to:", row[4])
                    client.send_message(receiver, "JOIN OVER 13.1 K INTERNATIONAL STUDENTS\n\nhttps://t.me/studenthelpcenter945\n\nLet's Connect!")
                    print("Waiting {} seconds".format(SLEEP_TIME))
                    time.sleep(SLEEP_TIME)
                except PeerFloodError:
                    print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                    client.disconnect()
                    sys.exit()
                except Exception as e:
                    print("Error:", e)
                    print("Trying to continue...")
    elif mode == 3:
        print("GoodBye. The application is exiting...")
        sys.exit()
    else:
        print("Invalid option. Please try again")
print("Done sending messages. The application will now exit.")



 
