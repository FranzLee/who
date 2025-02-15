from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select

currentYear = int(time.strftime("%Y")) - 1911
searchCompany = ["6152"]
searchYear = [currentYear-1, currentYear]
searchSeason = [1, 2, 3, 4]
data_list = []
counter = 0
money = 0
document = open('RCC.txt', 'w', encoding='utf8')

driver = webdriver.Chrome()
driver.get("https://mops.twse.com.tw/mops/web/t164sb03")
document.write(f"資料抓取時間: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n")
document.write("單位: 新台幣仟元\n\n")
for k in range(len(searchCompany)):
    document.write(f"公司代碼: {searchCompany[k]}\n")
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
                    for i in range(40, len(elements)):
                    if elements[i].text == "合約負債－流動":
                        print(f"Start from {i}")
                        counter = 2
                        money = elements[i+1].text
                        document.write(f"{searchYear[j]}年 第{searchSeason[m]}季\n金額: {money}\n\n")
            else:
                print(f"Warning: Expected at least 90 elements, but got {len(elements)}")
        year.clear()
driver.quit()
