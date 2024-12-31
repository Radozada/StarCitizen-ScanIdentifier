import time

#-------CAPTURE THE SCREEN

from asyncio import sleep
import pyautogui

#Need this to be dynamic based on screen resolution
region_width = 200
region_height = 40

screensize = pyautogui.size()

#Gets the center point of the screen
half_screensize_x = int(screensize[0] / 2)
half_screensize_y = int(screensize[1] / 2)

#Dividing the region width before adding the offset makes sure it's equally distant
#From the center of the screen
#Adding more offset to desired location for text reading
x_offset = ( region_width / 2 )
y_offset = ( region_height / 2 ) + 190

#Sets the desired location incorporating the offset
desired_location_x = int(half_screensize_x - x_offset )
desired_location_y = int(half_screensize_y - y_offset )

#Sets the region we want to be screenshotted
region = ( desired_location_x,desired_location_y,region_width,region_height ) # Adjust this based on your screen area || left, top, width, and height

screenshot = pyautogui.screenshot(region=region)

#Save or analyze the screenshot
screenshot.save("G:\My Drive\_Projects\Python\StarCitizen_ScanIdentifier\captured_area.png")

#------ANALYZE THE IMAGE CONTENT
from pytesseract import image_to_string
from PIL import Image

# Load the screenshot
screenshot = Image.open ("G:\My Drive\_Projects\Python\StarCitizen_ScanIdentifier\captured_area.png")
text = image_to_string(screenshot)

#remove first letter since the icon is mistaken for a 2
screen_text_found = text[1:]
##print("Detected text:", screen_text_found)

#-------------------------------------------------------------------------DEBUGGING
# Point 1: Move to starting point
##pyautogui.moveTo( region[0],region[1], 0.1 )

# Point 2: Add the width to the starting point X to get to the second point
##pyautogui.moveTo( region[0] + region[2], region[1], 0.1) 

# Point 3: Add the height to the starting point Y to get to the third point
##pyautogui.moveTo(None, region[1] + region[3], 0.1)

# Point 4: Move to starting point X but keep the height of the third point
##pyautogui.moveTo( region[0],region[1] + region[3], 0.1 )

# Point 5: Move back to starting point
##pyautogui.moveTo( region[0],region[1], 0.1 )

#pyautogui.alert(text='HEY HEY HEY', title='THIS ROCK BE THE SHIT YO', button='OK')
#-------------------------------------------------------------------------DEBUGGING

#Compare scanned text with information on sheet

import gspread
from google.oauth2.service_account import Credentials

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = 'G:\My Drive\_Projects\Python\StarCitizen_ScanIdentifier\Google Cloud Stuff\JSON Key File\starcitizenscanidentifier-dd7bf0006208.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']

# Authenticate and create a client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# Open the Google Sheet by name
sheet = client.open("Ground Mining Radar Reference")

rockdata_worksheet = sheet.worksheet("RockDataWorksheet")

# Read data from the sheet
data = rockdata_worksheet.get_all_values()
#print("Data from sheet:", data)
header = data[0]  # Extract the header row (column names)
rows = data[1:]   # Extract the rows of data

#-------------------------------------------------------------------------DEBUGGING
# Write data to the sheet
#testworksheet = sheet.add_worksheet("Test",1,3)

#print("I sleep.")
#time.sleep( 1 )
#print("I wake.")

#second_testworksheet_ref = sheet.worksheet("Test")

#sheet.del_worksheet(second_testworksheet_ref)
#-------------------------------------------------------------------------DEBUGGING

#value to check, remove spaces
search_value = screen_text_found.strip()

# Function to find all headers for a given value
def find_all_headers_for_value(value):
    headers = []
    for row_index, row in enumerate(rows):  # Iterate through rows
        for col_index, cell in enumerate(row):  # Check each cell
            if cell == value:  # Match found
                headers.append(header[col_index])  # Add corresponding header
    return headers

#from win10toast import ToastNotifier
#toaster = ToastNotifier()

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

def show_popup(title_text, message_text):
    # Create a PyQt application
    app = QApplication(sys.argv)

    # Create a window
    window = QWidget()
    window.setWindowTitle("Star Citizen Scan Identifier")
    window.setGeometry(100, 100, 350, 150)
    window.setFixedSize(350,150)
    window.setWindowFlags( Qt.WindowType.WindowStaysOnTopHint )  # Always on top & no border
    screen = app.primaryScreen().geometry()
    window_width = 350
    window_height = 150
    x = (screen.width() - window_width) // 2
    y = (screen.height() - window_height) // 2
    window.move(x, y)

    # Set the window icon
    window.setWindowIcon(QIcon("C:/Users/Administrator/Documents/_Python/mining_text_icon_217240.ico"))  # Path to your icon file (e.g., 'icon.png')

    # Create a title label to display the message
    title_label = QLabel(title_text, window)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet("font-size: 24px; padding: 10px;")

    # Create a message label to display the message
    message_label = QLabel(message_text, window)
    message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    message_label.setStyleSheet("font-size: 14px; padding: 10px;")

    # Create a "Dismiss" button to close the pop-up
    dismiss_button = QPushButton("Dismiss", window)
    dismiss_button.clicked.connect(window.close)  # Close the window when clicked

    # Arrange the label and button in a layout
    layout = QVBoxLayout()
    layout.addWidget(title_label)
    layout.addWidget(message_label)
    layout.addWidget(dismiss_button)
    window.setLayout(layout)

    # Show the window
    window.show()
    sys.exit(app.exec())

    # Center the window on the screen


# Example usage
#show_popup("Your Python script found the value 620 under the header HADENITE!")


# Find all headers for the given value
headers = find_all_headers_for_value(search_value)
if headers:
    print(f"Value '{search_value}' is found under the headers: {', '.join(headers)}") 
    #toaster.show_toast(f'Potential Rock Identified: {search_value}',f"{', '.join(headers)}","G:\My Drive\_Projects\Python\StarCitizen_ScanIdentifier\applier_mining_text_icon_217281.ico",None,True )
    show_popup(f'Potential Rock Identified: {search_value}',f"{', '.join(headers)}" )
    #pyautogui.alert(text=f"{', '.join(headers)}", title=f'Potential Rock Identified: {search_value}', button='Rock On')

else:
    print(f"Value '{search_value}' not found in the table.")
    #toaster.show_toast(f'No Potential Rock Identified',f"Try again :)","G:\My Drive\_Projects\Python\StarCitizen_ScanIdentifier\applier_mining_text_icon_217281.ico",5,True )
    show_popup("Scan Empty", f'{search_value}')
    #pyautogui.alert(text='Nada', title='NOTHING IDENTIFIED', button='OK')