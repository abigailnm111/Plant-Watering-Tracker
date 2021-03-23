#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 12:15:25 2021

@author: panda
"""
from datetime import datetime
"""
All exceptions for program
"""



class date_error:
# """invalid date"""
# def __init__ (self, message="Try enterting again in yyyy-mm-dd format."):
#     self.message=message
#     super().__init__(message)
# def __str__(self):
#     return '{self.message}'
    def __init__ (self):
        self.message="Try entering the date in yyy-mm-dd format."
        self.prompt= "when did you last water your plant?(yyyy-mm-dd)"
                    
        
    def validation_check(self, response):
        self.response=response
        self.validation_check=datetime.strptime(self.response, '%Y-%m-%d')
        return self.response

class days_error:
    """ not a valid integer to describe number of days"""
    def __init__ (self ):
        self.message= "Try entering a numeral equal to or higher then 1 for the number of days between watering."
        self.prompt= "how often (in days) do you water your plant?"
   
    def validation_check(self, response):
        self.response= int(response)
        self.validation_check= self.response >=1
        return self.response
        
def check_input(error):
    
   
    while True:
        
        try:
            valid= error()
            response= input(valid.prompt)
            
            valid_entry=valid.validation_check(response)
        
            return valid_entry
        except:
            
            print(valid.message)

    
