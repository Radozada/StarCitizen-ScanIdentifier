import pyautogui
from pytesseract import image_to_string
from PIL import Image

def capture_screen(region, save_path):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(save_path)
    return save_path

def process_image(image_path):
    image = Image.open(image_path)
    inverted_image = Image.eval(image, lambda x: 255 - x)
    inverted_image.save(image_path.replace(".png", "_inverted.png"))
    return image_to_string(image).strip()
