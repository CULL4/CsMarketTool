from selenium import webdriver
import time
import pickle

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get("https://buff.163.com/goods/857578")

# Here, you must login to steam from the automated browser. Wait for the browser to exit and the cookies will be saved in the specified location
selenium_cookie_file = 'selenium_cookie_file.txt'
time.sleep(50) # wait for manual login, save cookies
pickle.dump(pickle.dump(driver.get_cookies() , open("cookies.pkl","wb")))
driver.quit()