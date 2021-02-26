from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pytesseract import image_to_string
import pytesseract
from texttable import Texttable
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
table_krs= Texttable()

#Input your username dan password here
usernames = "NIM"
passwords = "PASSWORD"

def cek_krs():
    print("[*] Trying to Extract KRS")
    click_krs =  wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#navigation > ul > li:nth-child(13) > a'))).send_keys(Keys.ENTER)
    row = browser.find_elements_by_xpath('//*[@id="content"]/form/div/table[2]/tbody/tr')
    cols = browser.find_elements_by_xpath('//*[@id="content"]/form/div/table[2]/tbody/tr/th')
    row_idx = len(row)
    cols_idx = len(cols)

    row_element = []
    for i in range(3, 14):
        for j in range(1, cols_idx): 
            d=browser.find_element_by_xpath('//*[@id="content"]/form/div/table[2]/tbody/tr['+str(i)+']/td['+str(j)+']').text
            row_element.append(d)
                
    print(row_element)
    n = 5 

    # using list comprehension 
    final = [row_element[i * n:(i + 1) * n] for i in range((len(row_element) + n - 1) // n )]  
    x = 0
    nomor = []
    kode = []
    matkul = []
    kelas = []
    jadwal = []
    for i in final:
        nomor.append(i[0])
        kode.append(i[1])
        matkul.append(i[2])
        kelas.append(i[3])
        jadwal.append(i[4])

    for i in range(len(final)):
        table_krs.add_rows([[
                'No',
                'Kode',
                'Mata Kuliah',
                'Kelas',
                'Jadwal',
            ], [nomor[i], kode[i], matkul[i], kelas[i], jadwal[i]]])

    print(table_krs.draw())


    print("[*] Success Extract")
    print("[*] All Job is Done, Boss!")
     
def cek_ip():
    click_submit12 =  wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#sidebar > #navigation > ul > li:nth-child(14) > a'))).send_keys(Keys.ENTER)
    print("[*] =====================================")
     
    print("[*] Trying to Get Your Indeks Prestasi (IP)") 
    click_smster1 =  Select(wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.table-form > tbody > tr > td > select'))))

    element = wait(browser,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="content"]/form[1]/table/tbody/tr/td[1]/select')))
    all_options =element.find_elements_by_tag_name("option")
    dot = '.'
    collect_ip = []
    jumlah = 0
    for i in range(0, len(all_options)-1):
        click_smster1 =  Select(wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.table-form > tbody > tr > td > select'))))
        click_smster1.select_by_index(i)
        click_submit =  wait(browser,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/form[1]/table/tbody/tr/td[2]/input'))).send_keys(Keys.ENTER)
        ip_element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#content > table:nth-child(10) > tbody > tr:nth-child(3) > td:nth-child(2)')))
        #print("Trying to Extract IPK")
        ip_hasil = ip_element.text
        total = re.findall(r'[0-9]+', ip_hasil)
        join = total[0] + dot + total[1]
        collect_ip.append(join)
        print(f"[*] IP Semester {i+1}: {join}")

    for x in collect_ip:
        jumlah = jumlah + float(x)

    jumlah_index = len(all_options) - 1
    your_ipk = jumlah/jumlah_index
    formatted_float = "{:.2f}".format(your_ipk)
    print("[*] IP Kumulatif:", formatted_float)
    cek_krs()

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

def login():
    url = 'https://portal.unri.ac.id'
    browser.get(url)

    print("[*] Auto Login + Auto Solve Captcha by RJD")
    print("[*] Trying to access ", url)

    global png
    global element
    global location
    global size
    global usernames
    global passwords
    global user_info
    element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#loginWrapper > #loginBox > #loginBox-body > #form-login > img')))
    print("[*] Success Open ", url)
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png() 
    username = wait(browser,20).until(EC.presence_of_element_located((By.ID, "username")))
    username.clear()
    print("[*] Trying to Fill Username")
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
    userinfo_element = wait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#main-content > #content > #front-content-full > .front-content-full-left > h4')))
    user_info = userinfo_element.text
    print("[*]", user_info)
    cek_ip()
    

login()