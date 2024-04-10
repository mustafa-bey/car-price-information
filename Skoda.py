import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(executable_path="C:/Users/mustafa/Desktop/chromedriver.exe")



url = "https://www.skoda.com.tr/fiyat-listesi"
driver.get(url)

for i in range(1, 12, 2):
    element_xpath = "//*[@id='__next']/div/div[1]/div[2]/div[2]/div[" + str(i) + "]/div[2]/button"
    element = driver.find_element(By.XPATH, element_xpath)
    driver.execute_script("arguments[0].click();", element)

driver.implicitly_wait(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')


car_elements = soup.find_all('table', class_='Tablestyle__StyledTable-sc-1hijn2x-2 jipqGn')

i = 0
grouped_data = []

tr_elements = soup.find_all('tr')
for tr_element in tr_elements:
    data_id_value = tr_element.get('data-id')
    if data_id_value:
        td_elements = tr_element.find_all('td')
        car_data = []
        for td_element in td_elements:
            div_elements = td_element.find_all('div')
            for div_element in div_elements:
                inner_text = div_element.get_text(strip=True)

                # "İncele", "Renk", "Emotion", "Panoramik", "Kişilik", fiyatları içeren verileri atla
                if any(keyword in inner_text for keyword in
                       ["İncele", "Renk", "Emotion", "Panoramik", "Kişilik", "₺75.000", "₺60.000", "₺41.667", "₺27.778",
                        "₺20.000", "₺30.000", "₺95.000", "₺100.000", "₺138.889"]):
                    continue

                car_data.append(inner_text)
                i += 1

                if i % 3 == 0:  # Her üç veride bir grup oluştur
                    # Boş veri içeren kısımları filtrele
                    filtered_car_data = [data for data in car_data if data.strip()]

                    # Eğer filtered_car_data'da üçten az veri varsa yazdırma
                    if len(filtered_car_data) >= 3:
                        grouped_data.append(tuple(filtered_car_data))

                    car_data = []

        i = 0


df = pd.DataFrame(grouped_data, columns=['Model', 'Paket', 'Fiyat'])
print(df)
"""# DataFrame'i 1 saniye arayla yazdır
for _, row in df.iterrows():
    print(row,"\n")
    time.sleep(0.5)
"""
driver.quit()
