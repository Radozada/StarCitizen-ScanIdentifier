import pyautogui
from PIL import Image
import pytesseract
from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def capture_screen(region, save_path):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(save_path)
    return save_path

def process_image(image_path):
    image = Image.open(image_path)
    image_string = image_to_string(image)
    
    #TEMP - remove first digit since it is mistaken for a number when it is an icon
    #image_string = image_string[1:]

    return image_string