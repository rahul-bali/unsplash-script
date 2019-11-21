
import os
from time import sleep
from selenium import webdriver
# driver.set_window_size(1120, 550)

s = "cry"

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
option.headless = True

driver = webdriver.Chrome("D:\libtools\chromedriver\chromedriver.exe", options=option)


driver.get("https://unsplash.com/s/photos/"+s)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(20)

photos = driver.find_elements_by_class_name('_2Mc8_')

images = [one_photo.get_attribute('href') + "/download?force=true" for one_photo in photos]
print("Found {} images".format(len(images)))

os.makedirs("photos/" + s)
os.chdir("photos/" + s)

for count, x in enumerate(images):
    os.system("aria2c -o {:04d} {}".format(count, x))
    print("Downloaded {}".format(x))

files = os.listdir(".")
for f in files:
    if not f.endswith(".jpg"):
        os.rename(f, f + ".jpg")

print("\nFiles downloaded into photos/{}".format(s))

