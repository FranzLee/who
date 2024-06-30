import json
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

searchCompany = ["6152"]
# searchYear = [107, 108, 109, 110, 111, 112]
searchYear = [109]
searchSeason = [1, 2, 3, 4]
data_list = []
counter = 0
percentage = 0
money = 0
document = open('RCC.txt', 'w', encoding='utf8')

driver = webdriver.Chrome()
driver.get("https://mops.twse.com.tw/mops/web/t164sb03")

for k in range(len(searchCompany)):
    document.write(f"{searchCompany[k]}:\n")
    textInput = driver.find_element("id", "co_id")
    textInput.send_keys(searchCompany[k])
    selection = Select(driver.find_element("id", "isnew"))
    selection.select_by_index(1)
    for j in range(len(searchYear)):
        year = driver.find_element("id", "year")
        year.send_keys(searchYear[j])
        for m in range(len(searchSeason)):
            season = Select(driver.find_element("id", "season"))
            season.select_by_index(searchSeason[m])
            driver.execute_script("javascript:doAction();ajax1(document.form1,'table01');")
            time.sleep(1)
            elements = driver.find_elements(By.CLASS_NAME, "even")
                
            print(len(elements))
            if len(elements) >= 90:
                for i in range(40, len(elements)):
                    if counter > 0:
                        if counter == 2:
                            money = elements[i].text
                        elif counter == 1:
                            percentage = elements[i].text
                            document.write(f"{searchYear[j]}year {searchSeason[m]}season: money = {money}, percentage = {percentage}\n")
                        counter -= 1
                    if elements[i].text == "合約負債－流動":
                        print(f"Start from {i}")
                        counter = 2
            else:
                print(f"Warning: Expected at least 90 elements, but got {len(elements)}")
driver.quit()
