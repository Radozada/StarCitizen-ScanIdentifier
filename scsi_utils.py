import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet_data(sheet_name, worksheet_name):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    service_account_file = load_json( "starcitizenscanidentifier-dd7bf0006208.json" )    
    credentials = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    data = sheet.get_all_values()
    return data[0], data[1:]

def find_all_headers_for_value(value, header, rows):
    headers = []
    for row in rows:
        for col_index, cell in enumerate(row):
            if cell == value:
                headers.append(header[col_index])
    return headers

import pyautogui

def get_region_size():
    #Need this to be dynamic based on screen resolution
    region_width  = 200           #           0.078125 % of 2560
    region_height = 40            # 0.0277777777777778 % of 1440
    region_height_offset = 190    # 0.1319444444444444 % of 1440

    screensize = pyautogui.size()

    #Gets the center point of the screen
    half_screensize_x = int(screensize[0] / 2)
    half_screensize_y = int(screensize[1] / 2)

    #Dividing the region width before adding the offset makes sure it's equally distant
    #From the center of the screen
    #Adding more offset to desired location for text reading
    x_offset = ( region_width / 2 )
    #y_offset = ( region_height / 2 ) + 173   #works for drake cutlass only
    y_offset = ( region_height / 2 ) + region_height_offset # 190 works for drake cutlass only
    #y_offset = ( region_height / 2 ) + 240 #works for drake cutlass only
    #y_offset = ( region_height / 2 ) + 225 #works for anvil arrow only

    #Sets the desired location incorporating the offset
    desired_location_x = int(half_screensize_x - x_offset )
    desired_location_y = int(half_screensize_y - y_offset )

    #Sets the region we want to be screenshotted
    region = ( desired_location_x, desired_location_y, region_width,region_height ) # Adjust this based on your screen area || left, top, width, and height

    debug_show_area_with_mouse( region )

    return region

def debug_show_area_with_mouse( region,  speed = 0.5 ):
    #-------------------------------------------------------------------------DEBUGGING
    # Point 1: Move to starting point
    pyautogui.moveTo( region[0],region[1], speed )

    # Point 2: Add the width to the starting point X to get to the second point
    pyautogui.moveTo( region[0] + region[2], region[1], speed) 

    # Point 3: Add the height to the starting point Y to get to the third point
    pyautogui.moveTo(None, region[1] + region[3], speed)

    # Point 4: Move to starting point X but keep the height of the third point
    pyautogui.moveTo( region[0],region[1] + region[3], speed )

    # Point 5: Move back to starting point
    pyautogui.moveTo( region[0],region[1], speed )
    #-------------------------------------------------------------------------DEBUGGING

import json
import os

# Handles loading JSON credentials file
def load_json(filename):
    # Get the path to the JSON file inside the 'resources' directory
    file_path = os.path.join('resources', filename)

    # Open the JSON file and load its contents
#    with open(file_path, 'r') as file:
#        data = json.load(file)

    return file_path #data