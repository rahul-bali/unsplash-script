
import os
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# driver.set_window_size(1120, 550)

s = input("type your search term and hit enter: ")

chrome_options = Options()
# chrome_options.add_argument(f"--user-data-dir=./chrome-data")
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.headless = True

service = Service('D:\\libtools\\chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://unsplash.com/s/photos/"+s)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(20)

photos = driver.find_elements(by=By.CLASS_NAME, value='NP4SP')

print(len(photos), photos[0].tag_name)


images = [one_photo.get_attribute('href') + "/download?force=true" for one_photo in photos]
print("Found {} images".format(len(images)))

os.makedirs("photos/" + s)
os.chdir("photos/" + s)
# os.chdir(dirr)

def download_image(count, x):
	os.system("D:\\libtools\\aria2c -o {:04d} {}".format(count, x))
	print("Downloaded {}".format(x))

with ThreadPoolExecutor() as executor:
	futures = [executor.submit(download_image, count, x) for count, x in enumerate(images)]
	for f in as_completed(futures):
		print(f.result())

'''
for count, x in enumerate(images):
    os.system("aria2c -o {:04d} {}".format(count, x))
    print("Downloaded {}".format(x))

'''

files = os.listdir(".")
for f in files:
    if not f.endswith(".jpg"):
        os.rename(f, f + ".jpg")

print(f"\nFiles downloaded into photos/{s}")

