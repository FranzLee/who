from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select

currentYear = int(time.strftime("%Y")) - 1911
currentMonth = int(time.strftime("%m"))
currentDay = int(time.strftime("%d"))
searchCompany = ["6152"]
searchYear = [currentYear-1, currentYear]
searchMonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
data_list = []
counter = 0
percentage = 0
money = 0
document = open('revenue.txt', 'w', encoding='utf8')
driver = webdriver.Chrome()
driver.get("https://mops.twse.com.tw/mops/web/t05st10_ifrs")
document.write(f"資料抓取時間: {time.strftime(\"%Y-%m-%d %H:%M:%S\", time.localtime())}\n")
document.write("單位: 新台幣仟元\n\n")
for k in range(len(searchCompany)):
    document.write(f"公司代號 {searchCompany[k]}:\n")
    selection = Select(driver.find_element("id", "isnew"))
    selection.select_by_index(1)
    textInput = driver.find_element("id", "co_id")
    textInput.send_keys(searchCompany[k])
    for j in range(len(searchYear)):
        year = driver.find_element("id", "year")
        year.send_keys(searchYear[j])
        time.sleep(2)
        for m in range(len(searchMonth)):
            month = Select(driver.find_element("id", "month"))
            month.select_by_index(searchMonth[m])
            driver.execute_script("javascript:doAction();ajax1(document.form1,'table01');")
            time.sleep(2)
            oddElements = driver.find_elements(By.CLASS_NAME, "odd")
            evenElements = driver.find_elements(By.CLASS_NAME, "even")
            
            if (len(oddElements) >= 4) and (len(evenElements) >= 5):
                document.write(f"{searchYear[j]}年 {searchMonth[m]}月:\n")
                document.write(f"本月營收:{oddElements[0].text}\n")
                document.write(f"較去年同期增減金額:{oddElements[1].text}\n")
                document.write(f"較去年同期增減百分比:{evenElements[1].text}%\n")
                document.write(f"本年度至本月累積營收:{oddElements[2].text}\n")
                document.write(f"較去年同期增減金額:{oddElements[3].text}\n")
                document.write(f"較去年同期增減百分比:{evenElements[3].text}%\n\n")
            else:
                print(f"Warning: Expected 4 and 5 elements, but got {len(oddElements)} and {len(evenElements)}")
            if searchYear[j] == currentYear and searchMonth[m] >= currentMonth-2 and currentDay <= 10:
                
                break
            if searchYear[j] == currentYear and searchMonth[m] >= currentMonth-1 and currentDay > 10:
                break
        time.sleep(5)
        year.clear()
driver.quit()
