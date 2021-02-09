#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:02:33 2021

@author: panda

"""
#setting up OAuth2
#import google.oauth2.credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

"""other libraries"""
from datetime import datetime, timedelta
import json

"""my methods"""
#my sq file
#import sqlite


#credentials, 'plant-water-tracking' = google.auth.default(scopes='https://www.googleapis.com/auth/calendar', )
service= build('calendar', "v3")

class error(Exception):
    """base error"""
    pass

class invalid_menu_entry(error):
    """input not a valid menu option """
    pass

class plants():
    def __init__ (self, name, location, last_watered, water_frequency):
        
        self.name=name
        self.location=location
        self.last_watered=last_watered
        self.water_frequency= water_frequency
        
    #Request authorization to add/edit events to user's priamary Google Calendar
def oauth():
    
    flow= InstalledAppFlow.from_client_secrets_file('client_secret_799544582104-p7g4nv82mm0cr7v5ukph0rhee4fj7cae.apps.googleusercontent.com.json', scopes= ['https://www.googleapis.com/auth/calendar'])
    creds= flow.run_local_server()
    return build('calendar', 'v3', credentials=creds)
    
    #Use user input to create and add event to Calendar
def add_water_day(name, location, last_watered_date, water_days, service):
    #name of even includes plant's name
    event_summary= ('water {}'. format (name)) 
    #takes last day watered and adds the number of days from frequency to determine
    #date for next watering event. Converts to date only and then to string to make JSON compatiable
    
    plant_last_watered= datetime.strptime(last_watered_date,'%Y-%m-%d')
    water_date=str(datetime.date(plant_last_watered+timedelta(days= water_days)))  
    #creates reoccuring events based on number of days between watering
    frequency='RRULE:FREQ=DAILY;INTERVAL={};COUNT=10'. format (water_days)
    #event information for API calendar
    water_day={
        'summary': event_summary,
        'location': location,
        'start': {
            'date':water_date,
            'timeZone': 'America/Los_Angeles',
            },
        'end':{
            'date': water_date,
            'timeZone': 'America/Los_Angeles',
            },
        'recurrence': [frequency,]
        
        }
    #converts to json string and then json object. API won't correctly read json as string
    water_day= json.dumps(water_day,default=lambda o:o.__dict__)     
    json_wd=json.loads(water_day)
    #uses API calendar to add to user's calendar using event info above after converted to json readable
    service.events().insert(calendarId='primary', body=json_wd).execute()
    return event_summary

#check if user inputed date is valid:
    #1. date should be in correct format.
    #2. date should be actual date
    #3 date should not be in the future                **needs**
def check_input(prompt, condition, typ, except_message):
    while True:
        
        try:
            response=typ(input(prompt))
            condition(response)
            
            return response
        except:
            print(except_message)
            
def menu_selection_validation(prompt,allowable_responses):
    while True:
        response= input(prompt)
        try:
            if response in allowable_responses:
                return response
            else:
                raise invalid_menu_entry
            
        except invalid_menu_entry:
            print ("Enter a valid manu slection:{}".format(allowable_responses))
        
def main():
    #creaes dictionary to add plant data
    plant_index={}
    enter_plants= menu_selection_validation("do you have some plant children that need to be watered? Y or N",['y', 'Y', 'n', 'N'])
    index_number=0
   
    if enter_plants== "y" or enter_plants =="Y":
        add_plant="Y"
        while (add_plant=="y" or add_plant=="Y"):
            index_number+=1
            plant_name=input("what is your plant's name?")
            plant_location= input("where is your plant?")
            #Get input and check for valid date at the same time. Won't continue until valid date entered
            plant_last_watered= check_input("when did you last water your plant?(yyyy-mm-dd)", \
                                           lambda r: datetime.strptime(r, '%Y-%m-%d'), str,\
                                                "Try enterting again in yyyy-mm-dd format." )
           
            plant_water_frequency=check_input("how often (in days) do you water your plant?", lambda r: r>=1,\
                                              int, "Try entering a numeral equal to or higher then 1 for the number of days between watering")
            plants(plant_name, plant_location, plant_last_watered, plant_water_frequency)
            plant_index[index_number]= {'name':plant_name, 'location':plant_location, 'last_watered' :str(plant_last_watered), 'frequency(days)':plant_water_frequency}
            add_plant=menu_selection_validation("do you have more plants to add? Y or N",['y', 'Y', 'n', 'N'])
            
            #calls account authorization
            
            # calls function that adds event
            
            if add_plant== "n" or add_plant== "N":
                 #calls account authorization
                 print("Lets add your watering schdule to your Google calendar!")
                 service=oauth()
                 #iterates through dictionary to make events for each plant
                 #for plant_info in plant_index.values():   
                 index=1
                 for plant in plant_index:
                    
                    plant_info=plant_index[index]
                    
                    #sqlite.cursor.executemany('''INSERT INTO plant_data 
                                              # (name, location, last_watered, water_frequency) VALUES 
                                              # (:name, :location, :last_watered, :frequency(days))''', 
                                              # (plant_info,)
                                              # )    
                    index+=1
                    print("added to dictionary")
                    event_added=add_water_day(*plant_info.values(), service)
                    print ("'{}' has been added to your calendar" .format (event_added))
    else:
        print ("you should go get some plants and come back!")
       
  

main()


