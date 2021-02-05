#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:25:38 2021

@author: panda
"""

import sqlite3


connection=sqlite3.connect('plants.db')
print ("opened database successfully")

cursor=connection.cursor()
cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS plant_data (
                name TEXT, 
                location TEXT, 
                last_watered TEXT,nw
                water_frequency INTEGER 
                )
                ''')
             
connection.commit()            
         
             
def print_plant_data():
    cursor.execute("SELECT rowid, * FROM plant_data")
    readable_plants=cursor.fetchall()
    print("     1.name       2.location        3.last watered on:        4.days between watering")
    for plant in readable_plants:
        print(plant)
    
def update_plant(column, row, change ):
    cursor.execute("UPDATE plant_data SET [%s] = ? WHERE rowid = ? " % (column,),(change, row) )
    

def column_selection(col_id):
    if col_id== 1:
        column= 'name'
    elif col_id==2:
        column='location'
    elif col_id==3:
        column= 'last_watered'
    else:
        column= 'water_frequency'
    return column
def main ():
    print_plant_data()
    plant_id= int(input("what plant would you like to update?(enter the ID number)"))
    column_id= int(input("which column would you like to change?"))
    column=column_selection(column_id)
    update_item = input("Enter the updated information?")
    update_plant( column,plant_id,update_item)
    connection.commit()
    print_plant_data()

main()