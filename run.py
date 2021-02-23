from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytesseract import image_to_string
import pytesseract
from time import sleep
import re
from PIL import Image
from io import BytesIO

options = Options()
options.headless = False

import os

import requests

def get_captcha_text(location, size):
    global extract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    im = Image.open(BytesIO(png))
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    
    im = im.crop((left, top, right, bottom)) # defines crop pointsdefines crop points
    im.save('ss.png')
    data = image_to_string(Image.open('ss.png'))
    dataList = re.split(r',|\.| ', data)
    for i in dataList:
        extract = i.strip()
        extract_second = extract.rstrip("\n")
    return extract_second

browser = webdriver.Chrome(options=options, executable_path=r"C:\Users\User\Downloads\chrome\chromedriver.exe")
url = 'https://portal.unri.ac.id'
browser.get(url)
def Login():
    global png
    global element
    global location
    global size
    sleep(5)
    element = browser.find_element_by_css_selector('#loginWrapper > #loginBox > #loginBox-body > #form-login > img')
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png() 
    username = browser.find_element_by_id("username")
    username.clear()
    username.send_keys("NIM")
    password = browser.find_element_by_id("password")
    password.clear()
    password.send_keys("password")
    captcha = browser.find_element_by_id("aid_captcha")
    captcha.clear()
    captcha_text = get_captcha_text(location, size)
    sleep(5)
    captcha.send_keys(captcha_text)
    login = browser.find_element_by_class_name("button").click()
    sleep(5)
    err_message = browser.find_element_by_css_selector('#loginBox > #loginBox-body > #login-box-info > a > b')
    if err_message :
        if err_message[0].text == 'The verification code is incorrect.':
            print(err_message[0].text)
            return False
    return True


while Login() == False:
    Login()
