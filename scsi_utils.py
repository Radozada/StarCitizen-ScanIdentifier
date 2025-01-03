RECTANGLE_BOUNDS_FILE = "data/rectangle_bounds.json"

import pyautogui

def get_region_size():
    #Need this to be dynamic based on screen resolution
    region_width  = 200           # 0.0781250000000000 % of 2560
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

    #debug_show_area_with_mouse( region )

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

# Handles getting the JSON credentials file path
def load_json(filename):
    # Get the path to the JSON file inside the 'resources' directory
    file_path = os.path.join('data', filename)

    return file_path #data

def load_rectangle_bounds():
    """
    Load the saved rectangle bounds from the file.
    :return: A tuple (left, top, width, height) or None if no bounds are saved
    """
    try:
        with open(RECTANGLE_BOUNDS_FILE, "r") as file:
            bounds_data = json.load(file)
            return (bounds_data["x"], bounds_data["y"], bounds_data["width"], bounds_data["height"])
    except FileNotFoundError:
        return None  # Return None if no saved bounds exist

import re

def remove_non_numeric(value):
    # Use regular expression to keep only digits
    return ''.join(re.findall(r'\d', value))

def format_number_remove_comma(value):
    try:
        # Try converting to an integer
        number = int(value.replace(",", ""))  # Remove commas if present
        return str(number)
    except ValueError:
        # Handle the case where the value is not a valid number
        return "Invalid number"
    
def clean_input_text(value):
    value = value.strip() #strip spaces
    value = remove_non_numeric(value)
    value = format_number_remove_comma(value)    
    return value

def check_table_values( s_table ):
    print(s_table)


import sqlite3

def find_matching_headers(database_file, table_name, value):
    results = []
    conn = None  # Initialize conn to None
    try:
        # Convert value to integer if needed
        value = int(value)

        # Connect to the SQLite database
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Get the column headers
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = [column[1] for column in cursor.fetchall()]

        # Get the first row of the table
        cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 1")
        first_row = cursor.fetchone()

        if not first_row:
            raise ValueError("The table is empty or does not exist.")

        # Check divisibility for each column
        for header, first_value in zip(columns, first_row):
            if isinstance(first_value, (int, float)) and first_value != 0 and value % first_value == 0:
                result = value // first_value
                results.append((str(header), str(result)))

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

    return results

from datetime import datetime

def format_new_results(scanned_text, matches):    
    # Get the current datetime object
    local_time = datetime.now()

    # Format the datetime object as a string
    formatted_time = local_time.strftime("%H:%M:%S ")

    if matches:
        formatted_matches = ' OR '.join([f"{header} [{result} Nodes]" for header, result in matches])
        result_string = get_history_format(formatted_time, scanned_text, formatted_matches)
    else:
        formatted_matches = "No matches found."
        result_string = "Did not find any results."

    return [result_string, formatted_time, scanned_text, formatted_matches]

def get_history_format(formatted_time,scanned_text, formatted_matches ):
    history_format_string = f"{formatted_time} Search: '{scanned_text}' | Signature: {formatted_matches}"
    return history_format_string