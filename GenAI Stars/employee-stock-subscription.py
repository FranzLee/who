from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
import re

data_list = []
companiesCode = []
market = [0, 1, 2, 3]
# market = [0]
counter = 0
document = open("employee-stock-subscription.txt", "w", encoding="utf8")
n = 1
year = int(time.strftime("%Y")) - 1911
document.write(f"資料抓取時間: {time.strftime(\"%Y-%m-%d %H:%M:%S\", time.localtime())}\n\n")
print(year) 
def regularExpression(txt):
    arr = re.findall("^\d{4}", txt)
    if len(arr) == 1:
        return True
    else:
        return False
    
def check(code):
    result = True
    for i in range(len(companiesCode)):
        if(companiesCode[i] == code):
            result = False
    return result

driver = webdriver.Chrome()
driver.get("https://mops.twse.com.tw/mops/web/t158sb06")
time.sleep(3)
searchStartYear = driver.find_element("id", "startYear")
searchStartYear.send_keys(f"{year}")
searchEndYear = driver.find_element(By.NAME, "endYear")
searchEndYear.send_keys(f"{year}")
for k in range(len(market)):
    marketSegment = Select(driver.find_elements(By.NAME, "TYPEK")[1])
    marketSegment.select_by_index(market[k])
    driver.execute_script("javascript:doAction();ajax1(document.form1,'table01');")
    time.sleep(5)
    oddElements = driver.find_elements(By.CLASS_NAME, "odd")
    print(len(oddElements))
    if (len(oddElements) >= 4):
        for i in range(len(oddElements)):
            if counter == 2:
                document.write(f"    公司名稱: {oddElements[i].text}\n")
                counter -= 1
            elif counter == 1:
                document.write(f"    審核日期: {oddElements[i].text}\n\n")
                counter -= 1
            elif regularExpression(oddElements[i].text):
                if(check(oddElements[i].text)):
                    if n >= 10:
                        document.write(f"{n}:")
                        document.write(f" 公司代碼: {oddElements[i].text}\n")
                        companiesCode.append(oddElements[i].text)
                        counter = 2
                        n +=1
                    else:
                        document.write(f"{n}:")
                        document.write(f"  公司代碼: {oddElements[i].text}\n")
                        companiesCode.append(oddElements[i].text)
                        counter = 2
                        n +=1
    else:
        print(f"Warning: Expected 4 and 5 elements, but got {len(oddElements)}")
    counter = 0
    
    evenElements = driver.find_elements(By.CLASS_NAME, "even")
    print(len(evenElements))
    if (len(evenElements) >= 4):
        for i in range(len(evenElements)):
            if counter == 2:
                document.write(f"    公司名稱: {evenElements[i].text}\n")
                counter -= 1               
            elif counter == 1:
                if n >= 10:
                    document.write(f"    審核日期: {evenElements[i].text}\n\n")
                    counter -= 1
            elif regularExpression(evenElements[i].text):
                if check(evenElements[i].text):
                    if n >= 10:
                        document.write(f"{n}:")
                        document.write(f" 公司代碼: {evenElements[i].text}\n")
                        companiesCode.append(evenElements[i].text)
                        counter = 2
                        n+=1
                    else:
                        document.write(f"{n}:")
                        document.write(f"  公司代碼: {evenElements[i].text}\n")
                        companiesCode.append(evenElements[i].text)
                        counter = 2
                        n+=1
        counter = 0
    else:
        print(f"Warning: Expected 4 and 5 elements, but got {len(evenElements)}")
