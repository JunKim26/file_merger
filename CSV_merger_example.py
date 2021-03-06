# Title : CSV Files Merger
# Author: Jun Kim
# Date: 09/24/2021
# Description: In this program, all the csv files in a directory will be merged into one csv file.


import os
import glob
import pandas as pd
import numpy as np
from datetime import date                                                                   
from datetime import datetime      
import tkinter as tk                                                                        
from tkinter.filedialog import askdirectory                                                 
from tkinter import StringVar                                                           
from tkinter import *

def main():


    window = tk.Tk()                                                                        
    window.geometry('200x200')                                                              

    label = tk.Label(text='CSV Merger')                                                     
    label.pack()

    def csv_opener():
        """ this function is used for the button to open the csv file """

        global csv_folder
        csv_folder = askdirectory()                                                         
        end_button = Button(window, text = 'Create', command =window.destroy).pack()        
                                                                    
    csv_button = Button(window, text = 'Open Folder', command = csv_opener).pack()

    window.mainloop()                                                                       


    def rename_column(rename_df):
        
        rename_df.rename(columns={
                        'cs_hid' : 'Household ID', 
                        'profile_url': 'Linkedin Link', 
                        'email':"Email",
                        'full_name':"Household Name",
                        'first_name':"First Name",
                        'last_name':"Last Name",
                        'avatar':"LinkedIn Profile Picture URL",
                        'location_name':"Location",
                        'industry':"Industry",
                        'address':"Address",
                        'birthday':"Birthdate",
                        'organization_1':"Employed By",
                        'organization_title_1':"Title",
                        'organization_start_1':"Hire Date",
##                      'organization_2':"",
##                      'organization_title_2':"",
##                      'organization_3':"",
##                      'organization_title_3':"",
                        'education_1':"Education",
##                      'education_degree_1':"",
##                      'education_fos_1':"",
                        'education_start_1':"Education Start Date",
                        'education_end_1':"Education End Date",
##                      'education_2':"",
##                      'education_degree_2':"",
##                      'education_fos_2':"",
##                      'education_start_2':"",
##                      'education_end_2':"",
##                      'education_3':"",
##                      'education_degree_3':"",
##                      'education_fos_3':"",
##                      'education_start_3':"",
##                      'education_end_3':"",
##                      'language_1':"Language",
##                      'language_proficiency_1':"",
##                      'language_2':"",
##                      'language_proficiency_2':"",
##                      'language_3':"",
##                      'language_proficiency_3':"",
                        'languages':"Languages",
                        'phone_1':"Phone",
                        'phone_type_1':"Phone Type",
##                      'phone_2':"",
##                      'phone_type_2':"",
##                      'mutual_first_fullname':"",
##                      'mutual_second_fullname':""
                        'address': 'location',
                        'City': 'Billing City', 
                        'State': 'Billing State/Province'
                            }, inplace=True
                        )


    def csv_merge():
        os.chdir(csv_folder)
        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        
        # combine all files in the list                                                                            
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])                  
        csv_df = pd.DataFrame(combined_csv)    
        
        # year_month_day-hours_minutes_seconds_AM/PM ; used in Title
        dt = datetime.now().strftime('%Y.%m.%d-%I%M%S%p')                                   
        dt_string = str(dt)                                                                 
        file_name = dt_string +" combined.csv"

        script_dir = os.path.dirname(__file__)                                              
        rel_path = 'Output'
        
        # this joins the absolute path of current script with wanted relative path
        abs_file_path = os.path.join(script_dir, rel_path)                                  
        
        # this drops all columns without any values
        csv_df = csv_df.dropna(axis=1, how='all')                                           
 
        # clean up Phone Numbers           
        csv_df['phone_1'] = csv_df['phone_1'].str.replace(' ','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('(','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace(')','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('-','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('#','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('+','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('.','',regex=True)
        csv_df['phone_1'] = csv_df['phone_1'].astype(str)
        csv_df['phone_1'] = csv_df['phone_1'].str.strip()
        csv_df['phone_1'] = csv_df['phone_1'].str.replace('nan','',regex=True)
        

        # change Location to City, State

        df2 = pd.read_csv('../../MASTER Locations.csv', encoding = "ISO-8859-1")

        locationList = csv_df['location_name'].tolist()
        searchLocationList = df2['Location'].tolist()
        cityList = df2['City'].tolist()
        stateList = df2['State'].tolist()
        finalCity = []
        finalState = []
        noLocationData = []

        i = 0
        while i < len(locationList):
            try:
                j = searchLocationList.index(locationList[i])
                finalCity.append(cityList[j])
                finalState.append(stateList[j])
            except:
                finalCity.append('')
                finalState.append('')
                noLocationData.append(locationList[i])
            i += 1
            
        csv_df['City'] = finalCity
        csv_df['State'] = finalState

        # clean up Company Names 

        companyNamer = pd.read_csv('../../MASTER Company Replacers.csv')
        DSNames = companyNamer['Duxsoup Company'].tolist()
        SFNames = companyNamer['Sales Force Company'].tolist()

        z = 0
        while z < len(DSNames):
            csv_df = csv_df.replace(DSNames[z], SFNames[z])
            z += 1
            
        
         # creates a separate dataframe that contains rows with houshold ids
        hid_csv = csv_df[(csv_df.cs_hid.str.len() > 5)]                                     
        hid_csv = hid_csv.dropna(axis=1, how='all')
        
        # creates a separate dataframe that contains rows without household ids
        nohid_csv = csv_df[~(csv_df.cs_hid.str.len() > 5)]                                  
        nohid_csv = nohid_csv.dropna(axis=1, how='all')
        
        # these are the columns to keep in the final csv files
        wanted_columns = [                                                                  
            'cs_hid', 
            'profile_url', 
            'email',
            'full_name',
            'first_name',
            'last_name',
            'avatar',
            'industry',
            'address',
            'birthday',
            'organization_1',
            'organization_title_1',
            'organization_start_1',
##          'organization_2',
##          'organization_title_2',
##          'organization_3',
##          'organization_title_3',
            'education_1',
##          'education_degree_1',
##          'education_fos_1',
            'education_start_1',
            'education_end_1',
##          'education_2',
##          'education_degree_2',
##          'education_fos_2',
##          'education_start_2',
##          'education_end_2',
##          'education_3',
##          'education_degree_3',
##          'education_fos_3',
##          'education_start_3',
##          'education_end_3',
##          'language_1',
##          'language_proficiency_1',
##          'language_2',
##          'language_proficiency_2',
##          'language_3',
##          'language_proficiency_3',
            'languages',
            'phone_1',
            'phone_type_1',
##          'phone_2',
##          'phone_type_2',
##          'mutual_first_fullname',
##          'mutual_second_fullname',
            'City',
            'State'
            ]

        
        # keeps columns in the wanted columns array
        hid_csv = hid_csv[hid_csv.columns.intersection(wanted_columns)]                                             
        nohid_csv = nohid_csv[nohid_csv.columns.intersection(wanted_columns)]
        csv_df =csv_df[csv_df.columns.intersection(wanted_columns)]

        rename_column(hid_csv)
        rename_column(nohid_csv)
        rename_column(csv_df)

        last_path = os.path.basename(os.path.normpath(csv_folder))    
        
        # exports csv to folder
        hid_csv.to_csv("../../Output/Update/" + dt_string +" "+ last_path + " hid exists.csv", index=False, encoding='utf-8-sig')       
        nohid_csv.to_csv("../../Output/Insert/" + dt_string +" "+ last_path + " nohid.csv", index=False, encoding='utf-8-sig')           
        csv_df.to_csv("../../Output/Combined/"+ dt_string +" "+ last_path + " combined.csv", index=False, encoding='utf-8-sig')            


    csv_merge()

if __name__ == '__main__':
    main()
