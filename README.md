# Star Citizen Scan Identifier
A Python application for scanning and identifying Radar Signatures in Star Citizen. This project reads data from an on-screen capture and identifies related details from a packaged database.

![SC_ScanID_Screenshot](https://github.com/user-attachments/assets/3737c054-3b01-4206-8e88-feb804a4c802)


# Features
- Screen Capture & OCR: Captures a region of your screen and processes it using OCR.
- Database Integration: Identifies and maps the captured data to stored values in a packaged SQLite database.
- History Tracking: Maintains a searchable history of previous scans.
- Customizable Scan Areas: Allows users to set and adjust scan areas dynamically.
- User-Friendly Interface: Built using PyQt for an intuitive GUI experience.

# Requirements
This project requires the following dependencies:
- Python 3.10+
- PyQt6
- pytesseract
- Pillow
- pyautogui
- SQLite (packaged database)
- Tesseract-OCR 64bit (Included)

# How to use

## Launch SC Scan ID Executable
 1. Once you launch if you get a blank command console just hit the Enter Key and it should launch the window
 2. Set the database to search depending on what kind of mining you are doing
![Options Section](https://github.com/user-attachments/assets/984f4d47-79be-4a26-b86d-c3598447d6ef)

## Manual Search
1. Enter a number into the search box

![Search Section](https://github.com/user-attachments/assets/c2d0af9a-11f3-4ca1-b90f-bee3f813594e)

2. Perform a Search
   - Click on "Search" to query a search based on the Radar Signature number inputted.
   - The system processes the input and identifies corresponding values in the database.

## Setup (for scanning)
   1. If you want to do Scans, not just Manual Searches, you must install and setup Tesseract-OCR 64bit which is included in the downloads
   2. You can include more languages in the installation which will increase its footprint, this improves the Scan accuracy.

      ![Languages to include](https://github.com/user-attachments/assets/a87040a0-3c05-4185-97c5-dc1dbf686e60)
   3. Make sure to install in the default directly to ensure it works correctly. `C:\Program Files\Tesseract-OCR`

## Scan Search
1. Customize Scan Area
   - Click on the Red Rectangle Icon in the upper right corner of the "Scan Area of Screen" section.
     
   ![Red Rectangle Icon](https://github.com/user-attachments/assets/00ccc9bb-77d2-472e-876d-57d837490162)
   - Drag and resize the rectangle dynamically
     
   ![Drag and Resize Scan Area](https://github.com/user-attachments/assets/924da0f5-99bb-4cb7-bc42-6bcbffff22cf)
   - Move the Scan Area preview over the screen where the Radar Signature pops up
   - This section moves depending on the ship so you want to make sure if the scans aren't working, that it's in the right location
  
     ![Scan Area in Position](https://github.com/user-attachments/assets/b0e2ac18-fcb1-40b8-8513-73c46cee7d53)
   - Click on the Faded out Rectangle Icon in the upper right corner of the "Scan Area of Screen" section to hide the Scan Area preview.

3. Perform a Scan
   - Click on "Start Scan" to capture data from the predefined screen area.
   - The system processes the input and identifies corresponding values in the database.

## View Results
   - Identified elements are displayed in the Results section.
   - Number of Nodes is the number of rocks calculated

![Results Section](https://github.com/user-attachments/assets/12e5f88d-c64b-4cd5-9858-5d18d5234b08)

   - The application also saves search history for future reference.

![History Section](https://github.com/user-attachments/assets/402167c8-2c43-48a4-9082-e0516b36936a)


# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Credits
Developer: Jonathan Alvarado

Special Thanks: Stardads
