import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://turkiye.toyota.com.tr/middle/fiyatl_aksesuar.html#YeniCorolla"

options = Options()
options.headless = True
s = Service("C:/Users/mustafa/Desktop/chromedriver.exe")

driver = webdriver.Chrome(service=s, options=options)

try:
    driver.get(url)

    # Wait until the table is present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "TableBody"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    carModels = ["Corolla","Yenilenen Corolla", "Corolla Hibrit", "Corolla Cross Hybrid", "Yaris Cross", "Yaris Cross Hybrid",
                 "Toyota C-HR Hybrid", "Yaris", "Yaris Hybrid", "Camry", "RAV4 Hybrid", "Land Cruiser Prado",
                 "Hilux", "Proace City", "Proace City Cargo"]

    i = 0
    for araba in soup.find_all('tbody', class_="TableBody"):
        rows = araba.find_all('tr')
        for row in rows:
            cols = [x.text.strip() for x in row.find_all('td')]
            print(carModels[i], cols[0] + " " + cols[1] + "TL")
        print("**************************************\n")
        time.sleep(0.3)
        i += 1

finally:
    # Close the WebDriver when done
    driver.quit()
