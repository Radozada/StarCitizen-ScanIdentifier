from scsi_main_window import show_popup
from scsi_ocr_scanner import capture_screen, process_image
from scsi_utils import get_google_sheet_data, find_all_headers_for_value, get_region_size

# Screen region settings
region = get_region_size() #960, 540, 200, 40)  # Adjust for your screen resolution
screenshot_path = "screenshot.png"

# Google Sheets settings
sheet_name = "Ground Mining Radar Reference"
worksheet_name = "RockDataWorksheet"

# Capture and process screen
captured_path = capture_screen(region, screenshot_path)
scanned_text = process_image(captured_path)

# Fetch data from Google Sheet
header, rows = get_google_sheet_data(sheet_name, worksheet_name)

# Find matching headers
headers = find_all_headers_for_value(scanned_text, header, rows)

# Show results in a popup
if headers:
    show_popup("Scan Result", f"Value '{scanned_text}' found under: {', '.join(headers)}")
else:
    show_popup("Scan Result", "No matching value found.")