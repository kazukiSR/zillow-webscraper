import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd2lRZjalibE2bRJRNaGVuBvIYzbrdh3NfjTsLQSFaPS9A9iw/viewform?usp=sf_link"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Accept-Language": "en-US"
}

response = requests.get(ZILLOW_URL, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

listOfListings = soup.find(name="ul", class_="photo-cards")
listings = listOfListings.find_all(name="li")

propertyDict = {}

for n in range(len(listings)):
    addressElement = listings[n].find(class_="list-card-addr")
    if addressElement:
        address = addressElement.text
        price = listings[n].find(name="div", class_="list-card-price").text
        link = listings[n].a['href']
        propertyDict[n] = {
            "address": address,
            "price": price,
            "link": link,
        }


service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)

for n in propertyDict:
    driver.get(FORM_URL)
    addressForm = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    )
    priceForm = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    linkForm = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submitButton = driver.find_element(By.CSS_SELECTOR, ".NPEfkd")

    addressForm.send_keys(propertyDict[n]["address"])
    priceForm.send_keys(propertyDict[n]["price"])
    linkForm.send_keys(propertyDict[n]["link"])

    submitButton.click()
