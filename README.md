# Radar Scan ID
A Python application for scanning and identifying Radar Signatures in Star Citizen. This project reads data from an on-screen capture and identifies related details from a packaged database.

![Radar_Scan_ID_Screenshot](https://github.com/user-attachments/assets/e32d1ee3-437b-4582-9cf2-0b458ff6e420)

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
 ### 1. Once you launch if you get a blank command console just hit the Enter Key and it should launch the window
 ### 2. Set the database to search depending on what kind of mining you are doing
![Options Section](https://github.com/user-attachments/assets/984f4d47-79be-4a26-b86d-c3598447d6ef)

## Manual Search
### 1. Enter a number into the search box

![Search Section](https://github.com/user-attachments/assets/c2d0af9a-11f3-4ca1-b90f-bee3f813594e)

### 2. Perform a Search
   - Click on "Search" to start a search based on the value in the search box.
   - The system processes the input and identifies corresponding values in the database.

## Setup (for scanning)
   1. If you want to do Scans, not just Manual Searches, you must install and setup Tesseract-OCR 64bit which is included in the downloads
   2. You can include more languages in the installation which will increase its footprint, this improves the Scan accuracy.

      ![Languages to include](https://github.com/user-attachments/assets/a87040a0-3c05-4185-97c5-dc1dbf686e60)
   3. Make sure to install in the default directly to ensure it works correctly. `C:\Program Files\Tesseract-OCR`

## Scan Search
### 1. Customize Scan Area
   - Click on the Scan Area Preview Icon in the upper right corner of the "Scan Area of Screen" section.
   
     ![Scan Area Preview Icon](https://github.com/user-attachments/assets/00ccc9bb-77d2-472e-876d-57d837490162)
   - Click on the center of the rectangle and drag it around to move it.
   - Click on any edge to resize it like a window.
   
     ![Drag and Resize Scan Area](https://github.com/user-attachments/assets/924da0f5-99bb-4cb7-bc42-6bcbffff22cf)
   - Move the Scan Area preview over the screen where the Radar Signature pops up.

     ![Scan Area in Position](https://github.com/user-attachments/assets/d6a436f2-e90b-417c-b38a-8d3c718fba77)
   - This section moves depending on the ship so you want to make sure if the scans aren't working, that it's in the right location.
   - Click on the Faded Scan Area Preview Icon in the upper right corner of the "Scan Area of Screen" section to hide the Scan Area preview.

     ![Faded out Scan Area Preview Icon](https://github.com/user-attachments/assets/17ff8f14-57a6-493c-a3d0-ff557608b909)


### 2. Perform a Scan
   - Click on "Start Scan" to capture data from the predefined screen area.
   - The system processes the input and identifies corresponding values in the database.

## View Results
   - Identified elements are displayed in the Results section.
   - Previous searches are saved for future reference.
     
     ![Results Section](https://github.com/user-attachments/assets/31849708-c15b-4ea7-b6c8-35c60b405f2f)   

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/Radozada/StarCitizen-ScanIdentifier/blob/main/LICENSE) file for details.

## Credits
Developer: Jonathan Alvarado

Special Thanks: Josh Norton for feedback during the creation

## Attributions
- <a href="https://www.flaticon.com/free-icons/gem" title="gem icons">Gem icons created by Freepik - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/rock" title="rock icons">Rock icons created by Icongeek26 - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/asteroid" title="asteroid icon">Asteroid icons created by VectorPortal - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/vulture" title="vulture icons">Vulture icons created by Freepik - Flaticon</a>
