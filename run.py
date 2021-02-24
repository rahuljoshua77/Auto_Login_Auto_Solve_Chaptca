from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pytesseract import image_to_string
import pytesseract
from time import sleep
import re
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
import pandas as pd
from timeit import default_timer as timer
from selenium.webdriver.common.keys import Keys

start = timer()

options = Options()
options.headless = True
options.add_argument('log-level=3')
import os

import requests

def cek_ip():
    click_submit12 =  wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#sidebar > #navigation > ul > li:nth-child(12) > a'))).send_keys(Keys.ENTER)
    print("[*] Menu Cek IP Semester")
    print("[*] 1. Genap 2018/2019")
    print("[*] 2. Ganjil 2018/2019")
    print("[*] 3. Genap 2019/2020")
    print("[*] 4. Ganjil 2020/2021")
    print("[*] 5. Genap 2021/2021 (belum tersedia)")
    pilihan = int(input("[*] Masukin pilihan: "))
    print("[*] Trying to Get  your IP")
    #click_submit1 =  wait(browser,10).until(EC.element_to_be_clickable((By.NAME,'lstSemester'))).click
    click_smster1 =  Select(wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.table-form > tbody > tr > td > select'))))
    #print("Trying to Select")
    index = pilihan - 1 
    click_smster1.select_by_index(index)
    #print("Trying to Submit")
    click_submit =  wait(browser,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'input-disclaimer'))).send_keys(Keys.ENTER)

    ip_element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#content > table:nth-child(10) > tbody > tr:nth-child(3) > td:nth-child(2)')))
    #print("Trying to Extract IPK")
    ip_hasil = ip_element.text
    print("[*] IP Semester Anda", ip_hasil)
    print("[*] Check another Semester? (y/t)")
    pilih = input("[*] Masukin pilihan: ")
    if pilih == "y" or pilih == "Y":
        cek_ip()
    else:
        print("Bye!")

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

print("[*] Auto Login + Auto Solve Captcha by RJD")
print("[*] Trying to access ",url)

def Login():
    global png
    global element
    global location
    global size
    global username
    element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#loginWrapper > #loginBox > #loginBox-body > #form-login > img')))
    print("[*] Success Open URL")
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png() 
    username = wait(browser,20).until(EC.presence_of_element_located((By.ID, "username")))
    username.clear()
    print("[*] Trying to Fill Username")
    usernames = "YOUR NIM"
    passwords = "YOUR PASSWORD"
    username.send_keys(usernames)
    password = wait(browser,20).until(EC.presence_of_element_located((By.ID,"password")))
    password.clear()
    print("[*] Trying to Fill Password")
    password.send_keys(passwords)
    captcha = wait(browser,20).until(EC.presence_of_element_located((By.ID,"aid_captcha")))
    captcha.clear()
    print("[*] Trying to Solve Captcha")
    captcha_text = get_captcha_text(location, size)
    print("[*] Captcha Solved: ", captcha_text)
    captcha.send_keys(captcha_text)
    print("[*] Trying to Login")
    login = wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#loginWrapper > #loginBox > #loginBox-body > #form-login > .button'))).click()

    nim_checking = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#page > #main-content > #sidebar > #user-info > h4:nth-child(4)')))
    nim = nim_checking.text
    if nim == usernames:
        print("[*] Login Succes")
        userinfo_element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#main-content > #content > #front-content-full > .front-content-full-left > h4')))
        user_info = userinfo_element.text
        print("[*]", user_info)
        cek_ip()
    else:
        print("Login Gagal")

Login()
