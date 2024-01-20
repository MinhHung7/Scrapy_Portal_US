import requests
from config import password, user_name
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

class login():
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

        self.s = requests.session()
        headers = {
            'Accept-Language': 'en',
            'Referer': 'https://login.microsoftonline.com/40127cd4-45f3-49a3-b05d-315a43a9f033/oauth2/v2.0/authorize?client_id=9198f68e-537f-4bfa-afe6-205726c6d90e&scope=User.Read%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fstudent.hcmus.edu.vn%2Flogin&client-request-id=afa285b8-398c-4ad1-ac8b-539b7223f1af&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=3.2.0&client_info=1&code_challenge=l2qk6wY6PBGBWpl_kgC1Y5FYksbXF3D6GqGbbEOA_fc&code_challenge_method=S256&nonce=75d1da46-dc60-428c-acab-a487c475f88a&state=eyJpZCI6Ijg2MWQ2YWE3LTZmYWMtNGFlNS1iZTI0LTA0MjNkNWM1MjUwMiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&sso_reload=true',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform':"Android",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11.0; Surface Duo) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        }

        self.s.headers.update(headers)

        data = {
            'login': self.user_name,
            'loginfmt': self.user_name,
            'type': '11',
            'LoginOptions': '3',
            'passwd': self.password,
            'ps': '2',
        }
        login_in = self.s.post('https://login.microsoftonline.com/40127cd4-45f3-49a3-b05d-315a43a9f033/login', data = data, timeout=10)
        # self.s.trust_env == False
        self.s.cookies.update(login_in.cookies)

    def to_cookier(self):
        return self.s.cookies.get_dict()
    

    def checkInfo(self):   
        driver = webdriver.Chrome()

        driver.implicitly_wait(300)

        driver.get('https://student.hcmus.edu.vn/timetable')


        # Use WebDriverWait to wait for the page to finish loading
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'menu-item') and contains(@class,'active') and contains(@href,'/timetable?')]"))).click()

        # Print the page source
        html_content = driver.page_source
        html_content = html_content.split('<tbody>')[1].split('</tbody>')[0]

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Iterate through each row
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td')
            
            # Extract and print the content of each cell in separate lines
            for cell in cells:
                print(cell.get_text().strip())
            
            # Print a separator line between rows
            print('-' * 20)

        return html_content
    
user_name = '...'
password = '...'
test = login(user_name, password)

test.checkInfo()