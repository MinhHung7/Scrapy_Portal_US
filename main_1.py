from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Event import Event
from datetime import datetime, timedelta

class login():
    def __init__(self, user_name, password, code, event_list = []):
        self.user_name = user_name
        self.password = password
        self.event_list = event_list
        self.code = code
    
        driver = webdriver.Chrome()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # To avoid an error message in some environments
        # driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(60)

        # Navigate to portal url
        driver.get('https://student.hcmus.edu.vn/login')

        self.driver = driver

    def to_cookier(self):
        return self.s.cookies.get_dict()
    
    def accessPortal(self):
        try:
            # Press Yes button
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@value,'Yes')]"))
            ).click()

            # Navigate to timetable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/timetable')]"))
            ).click()

            # Show tbody html
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tbody"))
            ).click()

            # Print the page source
            html_content = self.driver.page_source
            html_content = html_content.split('<tbody>')[1].split('</tbody>')[0]

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all rows in the table
            rows = soup.find_all('tr')

            # Iterate through each row
            for row in rows:
                # Find all cells in the row
                cells = row.find_all('td')

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
    
    def checkCode(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'idTxtBx_SAOTCC_OTC')]"))
            ).send_keys(self.code)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@id,'idChkBx_SAOTCC_TD')]"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@id,'idSubmit_SAOTCC_Continue')]"))
            ).click()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pass

            
    def postCode(self):
        try:
            # Choose send code to phone
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'table-cell text-left content')]"))
            ).click()  # Now click the element after it becomes clickable
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pass

    def checkInfo(self):   
        try:
            # Choose login by microsoft account
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'microsoft-button')]"))
            ).click()
            
            # Enter username
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'i0116')]"))
            ).send_keys(self.user_name)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@id,'idSIButton9')]"))
            ).click()
            
            # Enter password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'i0118')]"))
            ).send_keys(self.password)
            
            # Press Sign in button
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@value,'Sign in')]"))
            ).click()

            if EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'passwordError')]")):
                return False
        finally:
            return True


