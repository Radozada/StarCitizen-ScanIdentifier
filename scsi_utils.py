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

    return region

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
                nodes = value // first_value
                results.append((str(header), str(nodes)))

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

    #Remove any Gems and convert them into a single entry
    results = replace_gems_with_single_entry(results)

    return results

def replace_gems_with_single_entry(results):
    gem_found = False

    strings_to_remove = ["Aphorite", "Dolivine", "Hadanite", "Janalite"]

    filtered_results = []
    
    for header, nodes in results:      
        if any(string in header for string in strings_to_remove):
            gem_found = True
            if "(N)" in header:
                gem_size = "(N)"
                gem_nodes = nodes
            elif "(L)" in header:
                gem_size = "(L)"
                gem_nodes = nodes
        else:
            filtered_results.append((header,nodes))
    
    if gem_found:
        s_gem = "Gems " 
        filtered_results.append((str(s_gem + gem_size), str(gem_nodes)))
    
    filtered_results.sort()

    results = filtered_results    
    return results

from datetime import datetime

def hour_to_meridien():
    hour = int(datetime.now().strftime("%H"))

    if hour == 0:
        return 12, "AM"
    elif 1 <= hour <= 11:
        return str(hour), "AM"
    elif hour == 12:
        return str(hour), "PM"
    else:
        return str(hour - 12), "PM"

def results_to_widget(scanned_text, matches):
    # Get the current datetime object
    time_h, meridian = hour_to_meridien()
    time_m = datetime.now().strftime("%M")
    time_s = datetime.now().strftime("%S")

    # Format the datetime object as a string
    time = (f'{time_h}:{time_m}:{time_s} {meridian}')  
    widget_item = get_widget_item(time, scanned_text, matches)    
    results = {
        "widget_item": widget_item,
        "time": time,
        "scanned_text": scanned_text,
        "matches": matches
        }

    return results

def get_widget_item(time, scanned_text, matches):
    radar_search_widget = RadarSignatureListItem(time, scanned_text, matches)

    return radar_search_widget

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt

GEM_APHORITE_ICON = "resources/gemstone_aphorite.png" #ground mining
GEM_DOLIVINE_ICON = "resources/gemstone_dolivine.png" #ground mining
GEM_HADANITE_ICON = "resources/gemstone_hadanite.png" #ground mining
GEM_JANALITE_ICON = "resources/gemstone_janalite.png" #ground mining
DEPOSIT_ICON = "resources/stone.png"                  #ground mining

ASTEROID_TYPE_ICON = "resources/asteroid.png"         #asteroid mining
SALVAGE_ICON = "resources/vulture.png"                #asteroid mining

# Goal = 12:30:15PM GEM_ICON GEM_NAME [X Nodes] 
class RadarSignatureListItem(QWidget):
    def __init__(self, time, search, matches):
        super().__init__()

        no_matches_string = "No results"
        
        # Set up layout
        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(1, 1, 1, 1)
        main_h_layout.setSpacing(0)#for debugging set to 1

        # Time Label
        if time:
            self.time_label = QLabel(time)
            self.time_label.setStyleSheet("color: #0055ff; font-weight: underline;")
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.time_label.setFixedWidth(QFontMetrics(self.time_label.font()).horizontalAdvance(time) + 15)
            main_h_layout.addWidget(self.time_label)

        # Search Label
        self.search_label = QLabel(search) 
        self.search_label.setWordWrap(True)
        self.search_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_label.setStyleSheet("color: #00d0d0; font-weight: bold;")  # Cyan color   
        self.search_label.setFixedWidth(QFontMetrics(self.search_label.font()).horizontalAdvance(search) + 15)
        main_h_layout.addWidget(self.search_label)

        match_v_wrapper_layout = QVBoxLayout()
        match_v_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        main_h_layout.addLayout(match_v_wrapper_layout)   
        if matches:
            for header, nodes in matches:
                # Horizontal Layout
                match_h_wrapper_layout = QHBoxLayout()

                # Icon Label
                icon_path = self.assign_icon(header)
                if icon_path:
                    self.icon_label = QLabel()
                    self.icon_label.setFixedWidth(24)
                    self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.icon_label.setPixmap(QPixmap(icon_path).scaled(16, 16))  # Adjust size as needed

                # Mineral Name Label (custom color)
                self.mineral_label = QLabel(header)
                self.mineral_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.mineral_label.setStyleSheet("color: #FFD700;")  # Gold color
                self.mineral_label.setFixedWidth(QFontMetrics(self.mineral_label.font()).horizontalAdvance(header) + 15)
                self.mineral_label.adjustSize()

                # Nodes Label (custom color)
                self.nodes_label = QLabel(nodes + " Nodes")
                self.nodes_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.nodes_label.setStyleSheet("color: #00FF00;")  # Green color
                #self.nodes_label.adjustSize()

                # Horizontal Layout Setup
                if icon_path:
                    match_h_wrapper_layout.addWidget(self.icon_label)
                match_h_wrapper_layout.addWidget(self.mineral_label)
                match_h_wrapper_layout.addWidget(self.nodes_label)

                # Add each Match as a row to the vertical wrapper
                match_v_wrapper_layout.addLayout(match_h_wrapper_layout)
        else:
            self.nothing_found_label = QLabel(no_matches_string)
            self.nothing_found_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.nothing_found_label.setStyleSheet("color: #00FF00;")  # Green color
            match_v_wrapper_layout.addWidget(self.nothing_found_label)

    def assign_icon( self, header ):
        '''Determines what icon to assign based on the result'''
        icon_path = None

        # Set icon based on the result text
        if "Aphorite" in header:
            icon_path = GEM_APHORITE_ICON
            #print("gemstone_aphorite")
        elif "Dolivine" in header:
            icon_path = GEM_DOLIVINE_ICON
            #print("gemstone_dolivine")
        elif "Hadanite" in header:
            icon_path = GEM_HADANITE_ICON
            #print("gemstone_hadanite")
        elif "Janalite" in header:
            icon_path = GEM_JANALITE_ICON
            #print("gemstone_janalite") 
        elif "Gems" in header:
            icon_path = GEM_APHORITE_ICON
            #print("gemstone_janalite") 
        elif "Type" in header:
            icon_path = ASTEROID_TYPE_ICON
            #print("asteroid") 
        elif "Salvage" in header:
            icon_path = SALVAGE_ICON
            #print("salvage")
        else:
            icon_path = DEPOSIT_ICON
            #print("salvage")

        return icon_path