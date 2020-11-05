
import os
import time
from time import sleep
from selenium import webdriver

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# driver.set_window_size(1120, 550)

s = input()
# dirr = input()

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
option.headless = True

############ change the below path to the chromedriver in your PC ####################
driver = webdriver.Chrome("/home/nightshade/bin/chromedriver", options=option)


driver.get("https://unsplash.com/s/photos/"+s)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(20)

photos = driver.find_elements_by_class_name('_2Mc8_')

images = [one_photo.get_attribute('href') + "/download?force=true" for one_photo in photos]
print("Found {} images".format(len(images)))

os.makedirs("photos/" + s)
os.chdir("photos/" + s)
# os.chdir(dirr)

def download_image(count, x):
	os.system("aria2c -o {:04d} {}".format(count, x))
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

