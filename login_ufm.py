import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from Event import Event
from quickstart import main
import re
from datetime import datetime, timedelta

class login_ufm():
    def __init__(self, user_name, password, event_list = []):
        self.user_name = user_name
        self.password = password
        self.event_list = event_list
    
        driver = webdriver.Chrome()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # To avoid an error message in some environments
        # driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(60)

        # Navigate to portal url
        driver.get('https://uis.ufm.edu.vn/login')

        self.driver = driver

    def to_cookier(self):
        return self.s.cookies.get_dict()
    
    def accessPortal(self):
        try:
            try:
                WebDriverWait(self.driver, 0.01).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'MuiButtonBase-root') and contains(@class,'MuiIconButton-root') and contains(@class,'MuiIconButton-colorInherit') and contains(@class,'MuiIconButton-sizeMedium') and contains(@class,'css-r64moz-MuiButtonBase-root-MuiIconButton-root')]"))
                ).click()
                print("1")
            except Exception as e:
                print("Im here")
            finally:
                # Navigate to timetable
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/student/schedules')]"))
                ).click()
                print(2)

                html_content = self.driver.page_source
                pprint(html_content)

                # Print the page source
                # html_content = self.driver.page_source
                # html_content = html_content.split('<tbody>')[1].split('</tbody>')[0]
                # print(html_content)
                # Parse the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find all rows in the table
                rows = soup.find_all('tr')

                # Iterate through each row
                for row in rows:
                    # Find all cells in the row
                    cells = row.find_all('td')
                    print(cells)

                    event = Event()
                    # # Extract and print the content of each cell in separate lines
                    event.header = cells[4].get_text().strip()
                    event.content = "CÓ LỊCH THI LÚC " + cells[3].get_text().strip() + " TẠI "+ cells[5].get_text().strip()
                    event.date = datetime.strptime(cells[2].get_text().strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                    event.start_time = datetime.strptime(cells[3].get_text().strip().replace("g", "h"), "%Hh%M").strftime("%H:%M:%S")
                    event.end_time = (datetime.strptime(event.start_time, "%H:%M:%S") + timedelta(hours=1)).strftime("%H:%M:%S")

                    self.event_list.append(event)
                    # Print a separator line between rows

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()

    def checkInfo(self):   
        try:
            # Enter username
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'email')]"))
            ).send_keys(self.user_name)
            
            # Enter password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'password')]"))
            ).send_keys(self.password)
            
            # Press Sign in button
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@type,'submit')]"))
            ).click()
            print("Try")
            try:
                element_present = WebDriverWait(self.driver, 0.01).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(@class,'MuiFormHelperText-root') and contains(@class,'Mui-error') and contains(@class,'css-gg0pu9-MuiFormHelperText-root')]"))
                )
                print("OK")
                # If the element is present, do something
                return False
            except Exception as e:
                print("OK1")
                # If the element is not present within the timeout, do something else or raise an exception
                print("Timed out waiting for element to be present")
                        
        finally:
            print("OK2")
        
        return True
        
user_name = "2221000404"
password = 'dat147star'
event_list = []
t = login_ufm(user_name, password, event_list)
if t.checkInfo() == True:
    t.accessPortal()


