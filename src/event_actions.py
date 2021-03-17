#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:02:33 2021

@author: panda

"""
#setting up OAuth2

from googleapiclient import errors

"""other libraries"""
from datetime import datetime, timedelta
import json

def update_event(event_id, event_info, update_info, service):
    OGevent = service.events().get(calendarId='primary', eventId= event_id).execute()
    # if OGevent['status']== 'cancelled':
    #     add_cancelled_event=menu_selection_validation("It looks like this event was deleted. Do you want to re add it to your calendar?", YN_menu)
    #     if add_cancelled_event== 'y' or add_cancelled_event =='Y':
    #         OGevent['status']= 'confirmed'
    #         db_data=sqlite.plant_db.get_plant_column_info('water_frequency', event_id)
    #         OGevent['recurrence']= ['RRULE:FREQ=DAILY;INTERVAL={};COUNT=10'. format (db_data)]
    #     if add_cancelled_event== 'n' or add_cancelled_event == 'N':
    #         return
    for field in event_info:
        i= event_info.index(field)
        
        if field == 'frequency':
            update_info=['RRULE:FREQ=DAILY;INTERVAL={};COUNT=10'. format(update_info[i])]
            OGevent['recurrence']= update_info
        if field ==('last_watered'):
            ##Datetime from form not working with format
            update_info= str(datetime.date(datetime.strptime(str(update_info[0]),'%Y-%m-%d')))
            update_info= {
                'date':update_info,
                'timeZone': 'America/Los_Angeles',
                },
            OGevent['start']= update_info
            OGevent['end']= update_info
        if field== 'name':

            OGevent['summary']= update_info[i]

        if field == 'location':
             OGevent['location']= update_info[i]
    OGevent= json.dumps(OGevent,default=lambda o:o.__dict__)     
    OGevent=json.loads(OGevent)
    
    service.events().update(calendarId='primary', eventId=event_id, body=OGevent).execute()
   
    print ("you have updated your plant's watering schedule")
    
def delete_event(event_id,service):
   try: 
    service.events().delete(calendarId='primary', eventId=event_id).execute()
   except errors.HttpError:
        print("it looks like that event was already deleted.")
        pass
    

    

    
    
    #Use user input to create and add event to Calendar
def create_event(name, location, last_watered_date, water_days, service):
    #name of event includes plant's name
    event_summary= ('Water {}'. format (name)) 
     #takes last day watered and adds the number of days from frequency to determine
     #date for next watering event. Converts to date only and then to string to make JSON compatiable
    
    
    plant_last_watered= datetime.strptime(str(last_watered_date),'%Y-%m-%d')
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








