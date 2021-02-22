#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:02:33 2021

@author: panda

"""
#setting up OAuth2
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

"""other libraries"""
from datetime import datetime, timedelta
import json

"""my methods"""
#my sq file
import sqlite
import exceptions





class error(Exception):
    """base error"""
    pass

class invalid_menu_entry(error):
    """input not a valid menu option """
    pass
def update_event(event_id,event_info, update_info, service):
    
    OGevent = service.events().get(calendarId='primary', eventId= event_id).execute()
    OGevent[event_info]= update_info
    service.events().update(calendarId='primary', eventId=event_id, body=OGevent).execute()
    print ("you have updated your plant's watering schedule")
    
def delete_event(event_id,service):
   try: 
    service.events().delete(calendarId='primary', eventId=event_id).execute()
   except errors.HttpError:
        print("it looks like that event was already deleted.")
        pass
    
def column_event(column):
    if column== '1':
        event_info= 'summary'
    if column == '2':
        event_info= 'location'
        ##work on/test these
    if column== '3':
        event_info= ('start', 'end')
        
    if column== '4':
        event_info=='recurrence'
    return event_info
    
class plants():
    plant_id=1
    plant_index={}
   
    def __init__ (self, name, location, last_watered, water_frequency):
        
        self.plant_id=plants.plant_id
        self.name=name
        self.location=location
        self.last_watered=last_watered
        self.water_frequency= water_frequency    
    #def add_event_id(self,event_id):
       # self.event_id=event_id
        
    def plant_dict(self):
        plants.plant_index[plants.plant_id]= {'name':self.name, 'location':self.location, 'last_watered' :self.last_watered, 'frequency(days)':self.water_frequency}
        plants.plant_id+=1
        
    def add_plant(service):
        add_plant='y'
        while (add_plant=="y" or add_plant=="Y"):
            plant_name=input("what is your plant's name?")
            plant_location= input("where is your plant?")
            #Get input and check for valid date at the same time. Won't continue until valid date entered   
            plant_last_watered= exceptions.check_input(exceptions.date_error)
            plant_water_frequency=exceptions.check_input(exceptions.days_error)
            plant_entry= plants(plant_name, plant_location, plant_last_watered, plant_water_frequency)
            plant_entry.plant_dict()
            add_plant=menu_selection_validation(str, "do you have more plants to add? Y or N",('y', 'Y', 'n', 'N') )
            if add_plant== "n" or add_plant== "N":
                  
                 #calls account authorization
                  print("Lets add your watering schdule to your Google calendar!")
                 
                 #iterates through dictionary to make events for each plant
                  for plant in plants.plant_index:
                     event_added=add_water_day(*plants.plant_index[plant].values(), service)
                     
                     
                     plants.plant_index[plant]['event_id']=event_added['id']
                     print ("'{}' has been added to your calendar" .format (event_added['summary']))
                     
                  sqlite.plant_db.add_to_database(plants.plant_index)
            
    def update_plant(service):
       update_plant='y'
       while (update_plant== 'y' or update_plant== 'Y'): 
           sqlite.plant_db.print_plant_data()
           plant_id= menu_selection_validation(int,"what plant would you like to update?(enter the ID number)", sqlite.plant_db.get_db_column_info('rowid'))
           column_id= menu_selection_validation(int,"which column would you like to change?", (1, 2, 3, 4))
           
           column=sqlite.plant_db.column_selection(column_id)
           if column_id== 1 or column_id ==2:
               update_item = input("Enter the updated information.")
           if column_id == 3:
               update_item= exceptions.check_input(exceptions.date_error)
           if column_id == 4:
               update_item = exceptions.check_input(exceptions.days_error)
           sqlite.plant_db.update_plant( column,plant_id,update_item)
           event_id=sqlite.plant_db.get_event_id(plant_id)
           
           update_event(event_id, column, update_item, service)
           print ("Your updates have been made to database and calendar")
           update_plant= menu_selection_validation(str,'Do you want to update another plant?', ('y', 'Y', 'n', 'N'))
           
    def delete_plant(service):
        delete_plant='y'
        while (delete_plant== 'y' or delete_plant== 'Y'): 
           sqlite.plant_db.print_plant_data()
           plant_id= menu_selection_validation(int,"what plant would you like to update?(enter the ID number)", sqlite.plant_db.get_db_column_info('rowid'))
           event_id=sqlite.plant_db.get_event_id(plant_id)
           sqlite.plant_db.delete_plant(plant_id)
           delete_event(event_id, service)
           delete_plant= menu_selection_validation(str,'Do you want to delete another plant?', ('y', 'Y', 'n', 'N'))
   
def main_menu(service):   

     menu_selec= menu_selection_validation(str,'would you like to \n 1) Add new plant \n 2) View your current plants \n 3) Update your plants \n 4) Delete a plant \n 5) Exit', ('1', '2', '3', '4', '5'))
     if menu_selec=='1':
         plants.add_plant(service)
         main_menu(service)
     if menu_selec=='2':
         sqlite.plant_db.print_plant_data()
         main_menu(service)
     if menu_selec=='3':
         plants.update_plant(service)
         main_menu(service)
     if menu_selec =='4':
         plants.delete_plant(service)
         main_menu(service)
     if menu_selec== '5':
         sqlite.plant_db.connection.close()
         print("take care of those plant babies!")
        
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
    plant_added= service.events().insert(calendarId='primary', body=json_wd).execute()
   
    return plant_added


    ##### Not being used currently        
def menu_selection_validation(value_type, prompt,allowable_responses):
    while True:
        try:
            response= value_type(input(prompt))
            try:
                if response in allowable_responses:
                    return response
                else:
                    raise invalid_menu_entry
            
            except invalid_menu_entry:
                print ("Enter a valid manu slection:{}".format(allowable_responses))
        except:
            print ("Enter a valid manu slection:{}".format(allowable_responses))
        
            

        
def main():
    
    service=oauth()
    main_menu(service)
    
    
       
  

main()


