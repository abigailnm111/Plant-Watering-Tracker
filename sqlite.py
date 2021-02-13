#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:25:38 2021

@author: panda
"""

import sqlite3

class plant_db():
    connection=sqlite3.connect('plants.db')
    cursor=connection.cursor()
    def __init__(self):
        pass

    def open_plant_db():
        print ("opened database successfully")
        
        cursor=plant_db.connection.cursor()
        cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS plant_data (
                    name TEXT, 
                    location TEXT, 
                    last_watered TEXT,nw
                    water_frequency INTEGER 
                    )
                    ''')
                 
        plant_db.connection.commit()  
        
    def add_to_database(plant_input):
        
        index=1
        plant_db.open_plant_db()
        for plant in plant_input:
            
            plant_info=plant_input[index]
            
            plant_db.cursor.executemany('''INSERT INTO plant_data 
                                        (name, location, last_watered, water_frequency) VALUES 
                                        (:name, :location, :last_watered, :frequency(days))''', 
                                        (plant_info,)
                                        )    
            index+=1
            print("added to dictionary")
            plant_db.connection.commit()
                
        plant_db.cursor.execute("SELECT * FROM plant_data")
        print(plant_db.cursor.fetchall())
        
        plant_db.connection.close()
 
class login_db:
    
        connection=sqlite3.connect('login.db')
        cursor= connection.cursor()
        def __init__(self, *logon):
            self.UN=logon[0]
            self.PW=logon[1]
        def open_login_db():
            login_db.cursor.execute('''
                           CREATE TABLE IF NOT EXISTS login_ids(
                               username TEXT,
                               password TEXT
                               
                               )
                
                            ''')
            login_db.connection.commit()
            print ("database connected")
            
        def create_login_id(self):
            
            login_db.cursor.execute('''INSERT INTO login_ids
                                    (username, password ) VALUES
                                     (?, ?)''', (self.UN, self.PW,)
                                    
                                    
                                    )
            login_db.connection.commit()
            print("login id added")
        def user_login(self):
           login_db.cursor.execute('''SELECT *
                                    FROM login_ids
                                    WHERE username= ? and password = ?
                                    
                                    ''', (self.UN, self.PW) )
           UN_valid= login_db.cursor.fetchall()
           print (UN_valid)
           if UN_valid != []: 
               return True
           else:
                return False
            
            
#integrate into main file and add validation           
def main():
    menu=input ('do you already have an account?')
    if menu == 'y' or menu== "Y":
        UN_attempt= input ('enter your username')
        PW_attempt= input ('enter your password')
        user=login_db(UN_attempt, PW_attempt)
        login_db.open_login_db()
        validate=user.user_login()
        print (validate)
        if validate== True:
               print ("valid login id")
        else:
               print ("faild login id")
        
    elif menu == 'n' or menu == "N":   
           create_UN= input ('enter username')
           ''' add validation to check if username exists'''
           create_PW= input ('enter password')
           user=login_db(create_UN, create_PW)
           login_db.open_login_db()
           user.create_login_id()
           
 
       
main()       
             
# def print_plant_data():
#     cursor.execute("SELECT rowid, * FROM plant_data")
#     readable_plants=cursor.fetchall()
#     print("     1.name       2.location        3.last watered on:        4.days between watering")
#     for plant in readable_plants:
#         print(plant)
    
# def update_plant(column, row, change ):
#     cursor.execute("UPDATE plant_data SET [%s] = ? WHERE rowid = ? " % (column,),(change, row) )
    

# def column_selection(col_id):
#     if col_id== 1:
#         column= 'name'
#     elif col_id==2:
#         column='location'
#     elif col_id==3:
#         column= 'last_watered'
#     else:
#         column= 'water_frequency'
#     return column




# """practice calling and updating database"""
# def main ():
#     print_plant_data()
#     plant_id= int(input("what plant would you like to update?(enter the ID number)"))
#     column_id= int(input("which column would you like to change?"))
#     column=column_selection(column_id)
#     update_item = input("Enter the updated information?")
#     update_plant( column,plant_id,update_item)
#     connection.commit()
#     print_plant_data()
