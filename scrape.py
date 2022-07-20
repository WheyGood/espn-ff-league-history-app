import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Prompt user for ESPN log in information. Info will be passed to the site through Selenium
# Also prompt for file path and league id and year they would like the history downloaded
email = str(input('Please enter ESPN log in email or username: '))
email_pass = str(input('Please enter your password: '))
folder_path = input('Please enter folder path to store your files: ')
league_id = str(input('Please enter your League Id number found in the url on the ESPN fantasy site: '))
year = str(input('Please enter the year of league history you want to download: '))

# Setup the Selenium connection to the web driver by using its path in program files
driver_service = Service(executable_path=r'C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=driver_service)
driver.maximize_window()

# Website we will be connecting to for scraping from Beautiful Soup
driver.get(f'https://fantasy.espn.com/football/league/standings?seasonId={year}&leagueId={league_id}')
driver.implicitly_wait(5)

# Run a try block to catch a potential error
# Inside the try block we need to switch iFrames in order to select the log in input form
# We send the user and pass through to the site and then switch to the normal site iFrame for scraping
try:
    driver.switch_to.frame("disneyid-iframe")
    username = driver.find_element(By.XPATH, '//*[@id="did-ui-view"]/div/section/section/form/section/div[1]/div/label/span[2]/input' )
    username.send_keys(email)
    password = driver.find_element(By.XPATH, '//*[@id="did-ui-view"]/div/section/section/form/section/div[2]/div/label/span[2]/input')
    password.send_keys(email_pass)
    button = driver.find_element(By.XPATH, '//*[@id="did-ui-view"]/div/section/section/form/section/div[3]/button')
    button.click()

    time.sleep(3)

    # Successfully logged in now we can scrape the history table easily with Beautiful Soup
    # Switch the iFrame and collect the page source with the help of the driver
    driver.switch_to.default_content()
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', class_="Table")
    df = pd.read_html(str(table))[0]

    # History site contains two tables after 2018, need logic to correct for the issue
    if int(year) <= 2018:
        time.sleep(3)
        df.to_csv(fr'{folder_path}\{year}.csv')
        driver.quit()
    else:
        time.sleep(3)
        table2 = soup.find('table', class_="Table Table--align-right")
        df2 = pd.read_html(str(table2))[0]

        # Add the moves column to the original dataframe (was moved on the site after 2018)
        df.insert(8, 'MOVES', df2['MOVES'])
        df.to_csv(fr'{folder_path}\{year}.csv')
        driver.quit()

except:
    print('ERROR')

time.sleep(5)
driver.quit()
