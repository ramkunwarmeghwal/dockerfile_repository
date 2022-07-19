from copy import error
import logging

import azure.functions as func
from selenium import webdriver
from concurrent.futures.thread import ThreadPoolExecutor
#from azure.identity import DefaultAzureCredential, ClientSecretCredential
#from azure.storage.blob import BlobServiceClient
#from datetime import datetime
import warnings
import sys
from PIL import Image
import base64
from io import BytesIO
import numpy as np
#import urllib.request
import cv2
import pytesseract
#import csv
import json
import os
import asyncio

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def captcha(data):
    print("captcha start")
    def ocr_core(img):
        try:
            text = pytesseract.image_to_string(img) 
            return text
        except Exception as e:
            print(e)


        #data='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G9UmHWO0lb8kJoA+W/hhaeJPEHi/V4/Dt9Hp7XsLrd3xGXghaQMTHznecAD69R1H0P4G+HWkfD9L5dKuL6YXhQyfanRsbN2MbVX+8a8g/ZqTOu68/pbRj82P+FfRtABRRRQAUUUUAFFFFABRRRQAUUUUAFNkjSaNo5EV0YYKsMg/hTqKAK9pYWenxvHZWkFsjtvZYYwgZvUgdTwOafcW8F3bS21zCk0EqlJI5FDK6nggg9RUtFAHi8vwv8UeCNdn1b4d6hA0N1kTafdjCqvVRknDclsZwR75rV0i4+MmpazYwarZaPpWnQ3Ec11cRsrNPEGG6IDc+CQSc4Xp94d/U6KAPOPip8MG8fRWd1Y3q2up2nyxtKT5bITkg4BII6g/h7iPRvhFbPo99D4v1GbXtQvI1g+1OzKbeFSGVIyScYcbuwPTHXPpdFAGN4Y8K6R4P0k6bots0Fs0hlYNIzlnIALEk+ijpxxWolvBHI0iQxq7HLMFAJPualooAKintbe6UrcQRSqe0iBh+tS0UAULPQ9I06QyWOl2Vq5YuWgt0Q7iME8DrjjNO1exOp6Lf6esgjN1byQhyM7dylc4/GrtFAHlfwm+GWrfD/VdWkv7uzuYLqKNYngLZypOdwIGOvYmvVKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/9k='
        #img = Image.open(BytesIO(base64.b64decode(data)))
        #img = cv2.imread('/Users/vishwanathmk/Downloads/cbimage (3).png')
        #print("cv2_read",img)
        #img = cv2.imread('captcha.png')
    nparr = np.frombuffer(base64.b64decode(data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def get_grayscale(image):
                return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    def remove_noice(image):
                return cv2.medianBlur(image, 5)

    def thresholding(image):
                #return cv2.threshold(image,0,225,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                return cv2.threshold(cv2.GaussianBlur(image, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    img = get_grayscale(img)
        #img= thresholding(img)
        #img = remove_noice(img)
    img_text = ocr_core(img).rstrip()
    return img_text

async def scrape(cin, max_attempt, result, errCins, executor,  loop):#(url, driver, executor, *, loop):
    await loop.run_in_executor(executor, scraper, cin, max_attempt, result, errCins)

def  scraper(cin, max_attempt, result, errCins):
    try:
        print(cin)
        lists = get_directors_info(cin,  max_attempt)
        
        result.append({cin:lists})
    except:
        errCins.append(cin)

def get_or_create_eventloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    cinList  = req_body.get('cins')
    max_attempt  = req_body.get('max_attempt',20)
    errCins=[]
    result =[]
    executor = ThreadPoolExecutor(len(cinList))

    for cin in cinList:
        executor.submit(scraper,cin, max_attempt, result, errCins)
        #await scrape(cin, max_attempt, result, errCins, executor,  loop=loop)

    executor.shutdown(wait=True) 
    #loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))
    resp ={
        "result": result,
        "errCins":errCins,
        "status_code":200
    }
    print(json.dumps(resp))
    return func.HttpResponse(
        json.dumps(resp),
        mimetype="application/json",
    )

def test():
    cinList  = ["U01110AN2016PTC005317","U65921AP1996PTC025131"]
    max_attempt  = 3
    errCins=[]
    result =[]
    executor = ThreadPoolExecutor(len(cinList))

    for cin in cinList:
        executor.submit(scraper,cin, max_attempt, result, errCins)
        #await scrape(cin, max_attempt, result, errCins, executor,  loop=loop)

    executor.shutdown(wait=True) 
    #loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))
    resp ={
        "result": result,
        "errCins":errCins,
        "status_code":200
    }
    print(json.dumps(resp))
    return func.HttpResponse(
        json.dumps(resp),
        mimetype="application/json",
    )
    
    
def get_directors_info(cin, max_attempt = 20):
    my_list = []
    print("cin:",cin)
    print("tttttttttttttttt")
    i=0
    while True:
            if i == max_attempt: #100:
                print("Not able to get the response even after"+str()+" attempt")
                return #sys.exit()
            
            #driver = webdriver.Chrome("/Users/vishwanathmk/Downloads/chromedriver", chrome_options=chrome_options)
            #driver.get('http://www.ubuntu.com/')
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            print("XXXXXXXXXXXXXXXXXXXX")
            chrome_driver_path= "/usr/local/bin/chromedriver"
            #chrome_driver_path= "C:\\legitquest\\chromedriver.exe"
            #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
            print("XXXXXXXXXXXXXXXXXXXX2")
            url = 'https://www.mca.gov.in/content/mca/global/en/mca/master-data/view-compnay-or-llp-master-data.html'
            
            driver.get(url) #scrape(url, driver, executor,  loop)
            print("XXXXXXXXXXXXXXXXXXXX3")
            #driver.get()
            print(driver.title)

            #print(driver.title)
            element = driver.find_element_by_xpath('//*[@id="captcha"]') # find part of the page you want image of
            location = element.location
            size = element.size
            png = driver.get_screenshot_as_png() # saves screenshot of entire page


            im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']


            im = im.crop((left, top, right, bottom)) # defines crop points
            buffered = BytesIO()
            im.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue())
            encoded_string = str(img_str).lstrip("b'")
                                    
            encoded_string = str(encoded_string).rstrip("'")
            #print(encoded_string)

            response_captcha_text = captcha(encoded_string)
            print("rrrrrrrrrrrrrrrrrrr")
            print(response_captcha_text.lower())


            ent_cin = driver.find_element_by_xpath('//*[@id="companyID"]')
            ent_cin.send_keys(cin)

            ent_captcha = driver.find_element_by_xpath('//*[@id="userEnteredCaptcha"]')
            ent_captcha.send_keys(response_captcha_text.lower())

            submit = driver.find_element_by_xpath('//*[@id="companyLLPMasterData_0"]')
            driver.execute_script("arguments[0].click();", submit)
            try:
                element = driver.find_element_by_xpath('//*[@id="msg_overlay"]/p') #this element is visible
                i =+1
                print("Wrong Captcha")
                continue

            except:
                print("Correct Captcha")
                break
            
            #//*[@id="resultTab6"]/tbody/tr[2]/td[2]  //*[@id="resultTab6"]/tbody/tr[2]/td[2]
    no_rows = len(driver.find_elements_by_xpath('//*[@id="resultTab6"]/tbody/tr'))
    no_col = len(driver.find_elements_by_xpath('//*[@id="resultTab6"]/tbody/tr'))

    print("no of rows",no_rows-1)
    print("no of cols",no_col)
    dicts = {}
    lists = []

    keys = ('din', 'DirectorName', 'Begining date','End date','surrender din')
    print(keys)
    for r in range (1, no_rows+1):
            print (cin)
            #print("r",r)
            #//*[@id="resultTab1"]/tbody/tr[2]/td[2]
            companyname = driver.find_elements_by_xpath('//*[@id="resultTab1"]/tbody/tr[2]/td[2]')
            for values in companyname:
                companyname = values.text
            
            for c in range(0,no_col+1):
                #print("c",c)
                #print_details = options.find_elements_by_xpath("//*[@id='block-system-main']/div/div/div[2]/table/tbody/tr["+str(r)+"]/td["+str(c)+"]")
                print_details = driver.find_elements_by_xpath("//*[@id='resultTab6']/tbody/tr["+str(r)+"]/td["+str(c)+"]")
                for values in print_details:
                    val = values.text
                    my_list.append(val)
            #print (my_list)
            if r !=1:
                for i in range(len(keys)):
                    dicts[keys[i]] = my_list[i]
                #print(dicts)
                dicts1 = {'cin': cin, 'CompanyName': companyname}
                
                dict3 = Merge(dicts1, dicts)
                y = json.dumps(dict3)
                print("This is json",y)
                lists.append(y)
                my_list.clear()
    return lists
            #driver.close()

#test()
            

            
