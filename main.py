from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pandas as pd
from pandas import DataFrame


def get_name_by_id(id: str):

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(
        #     "--user-data-dir=" + os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data")
        # chromedriver = "./chromedriver"
        # driver = webdriver.Chrome(executable_path=chromedriver,
        #                         chrome_options=chrome_options)
        try:
            driver = webdriver.Chrome()
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            
            driver.get("https://www.manpower.gov.kw/Pages/Services/TrainingRegister.aspx")

            driver.execute_script("document.body.style.zoom='100%'")
            
            id_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ContentPlaceHolder1_TrainingRegisterUC_txtCivilID")))
            action = ActionChains(driver) 
            action.move_to_element(id_element).click().perform()
            # print("id = ", id)
            id_element.send_keys(id)
            time.sleep(1)
            action.send_keys(Keys.ENTER).perform()

            name_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ContentPlaceHolder1_TrainingRegisterUC_lblName")))
            name = name_element.text
            # print("name = ", name)
            driver.close()
            driver.quit()
            return name
        except:
            os.system("taskkill /im chrome.exe /f")
            return "repeat"

if __name__ == "__main__":
    df = pd.read_excel("id.xlsx", sheet_name="Sheet1")
    list_id = []
    list_name = []
    id = 0
    while id < len(df):
        name = get_name_by_id(str(df.at[id, 'ID']))
        if 'repeat' in name:
            print("{0} : error in chrome driver!".format(id + 1))
        else:
            time.sleep(3)
            list_id.append(str(df.at[id, 'ID']))
            list_name.append(str(name))
            df1 = DataFrame(list(zip(list_id, list_name)), columns=['ID', 'NAME'])
            df1.to_excel("name.xlsx", sheet_name='Sheet1')
            print("{0} : success!".format(id + 1))
        id += 1
    # df = DataFrame(list(zip(list_id, list_name)), columns=['ID', 'NAME'])
    # df.to_excel("name.xlsx", sheet_name='Sheet1')
