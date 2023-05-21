from selenium import webdriver
import time


def download(urls, path):
    driver = webdriver.Chrome()

    i = 0
    for url in urls:

        driver.get(url)

        if i == 0:
            time.sleep(2)
        driver.add_cookie({'name': 'cookieconsent_status', 'value': 'allow'})

        time.sleep(1)
        driver.save_screenshot(f"{path}/screenshot_{i}.png")
        i += 1

    driver.quit()
