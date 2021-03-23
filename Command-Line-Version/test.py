#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 20:31:55 2021

@author: panda
"""
from datetime import datetime

import sqlite

def check_valid_date(date_entered):
    try:
        datetime.strptime(date_entered, "%y-%m-%d")
        return True
    except ValueError:
        print ("Try enterting again in yyy-mm-dd format.")
        return False
            
def check_days(days):
    try: 
        days<=1
        return True
    except ValueError:
        return False
    
def check_input(prompt, condition, typ, except_message):
    while True:
        
        try:
            response=typ(input(prompt))
            condition(response)
            
            return response
        except:
            print(except_message)
            
class plants():
    def __init__ (self, name, location, last_watered, water_frequency):
        
        self.name=name
        self.location=location
        self.last_watered=last_watered
        self.water_frequency= water_frequency    

    
def add_to_database(plant_input):
    index=1
    for plant in plant_input:
        
        plant_info=plant_input[index]
        
        sqlite.cursor.executemany('''INSERT INTO plant_data 
                                   (name, location, last_watered, water_frequency) VALUES 
                                   (:name, :location, :last_watered, :frequency(days))''', 
                                   (plant_info,)
                                   )    
        index+=1
        print("added to dictionary")
        sqlite.connection.commit()
            
    sqlite.cursor.execute("SELECT * FROM plant_data")
    print(sqlite.cursor.fetchall())
    
    sqlite.connection.close()
            
def main():
    #creaes dictionary to add plant data
    plant_index={}
    enter_plants=str(input("do you have some plant children that need to be watered? Y or N"))
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
            plant_index[index_number]= {'name':plant_name, 'location':plant_location, 'last_watered' :plant_last_watered, 'frequency(days)':plant_water_frequency}
            add_plant=str(input("do you have more plants to add? Y or N"))
            
           
            
            if add_plant== "n" or add_plant== "N":
                 #calls account authorization
                 print("Lets add your watering schdule to your Google calendar!")
                 
                 add_to_database(plant_index)
            
       
  

main()