from time import time

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url="https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(by=By.ID, value="cookie")

t_end_2 = time() + (5 * 60)


def store_buy(sc):
    target_price = 0
    store = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
    for s in store:
        print(s.text, end=" ")
    print()
    price_list = []
    for item in store:
        try:
            price = item.text.split("-")[1].strip()
        except IndexError:
            print(f"Index error for: {item.text}")
            continue
        price_list.append(int(price.replace(',', '')))
    price_list.sort(reverse=True)
    print(price_list)
    for price in price_list:
        if price <= sc:
            target_price = price
            print(f"Score: {sc}\tTarget Price:{target_price}\tCP: {price}")
            break

    price_list.sort()
    for item in store:
        try:
            price = int(item.text.split("-")[1].strip().replace(',', ''))
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException for: {item.text}")
            continue
        print(price, end=" ")
        if price == target_price:
            item.click()
            try:
                print("Bought " + item.text.split("-")[0].strip())
            except StaleElementReferenceException:
                continue
            break


def find_score():
    return int(driver.find_element(by=By.ID, value="money").text.replace(',', ''))


score = find_score()
print(f"Score: {score}")

for i in range(0, (1 * 60), 5):
    print(f"\n----iteration {(i/5)+1}----")
    start_t = time()
    while time() <= start_t + 5:
        cookie.click()
    end_t = time()
    store_buy(find_score())
    print(f"Time taken for this iteration: {end_t - start_t}")

cps = driver.find_element(by=By.ID, value="cps")
print(f"Cookies per second: {cps.text}")
# driver.quit()
