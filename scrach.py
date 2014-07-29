from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



browser = webdriver.Chrome(executable_path='/home/enki/Projects/freelance/hangout_api/chromedriver')
wait = WebDriverWait(browser, 10)

browser.get('https://plus.google.com/hangouts/active')

element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'opd')))
# element = browser.find_element_by_xpath('//div[@class="opd"]')
element.click()

sleep(10)  # TODO: add waiting for second window to open
browser.close()
browser.switch_to_window(browser.window_handles[-1])  # 'Google+' title

name = "DoeJohnBot"
password = "fwjfklsmdflkjdsklfjklsdj"


element = wait.until(EC.element_to_be_clickable((By.ID, 'Email')))
element.send_keys(name)
element = wait.until(EC.element_to_be_clickable((By.ID, 'Passwd')))
element.send_keys(password)
element = wait.until(EC.element_to_be_clickable((By.ID, 'signIn')))
element.click()

import pdb; pdb.set_trace()

injection = """
    var scriptElt = document.createElement('script');
    scriptElt.type = 'text/javascript';
    scriptElt.src = '//plus.google.com/hangouts/_/api/v1/hangout.js';
    document.getElementsByTagName('head')[0].appendChild(scriptElt)"""

browser.execute_script(injection)
browser.execute_script('gapi.hangout.av.getCameraMute()')
