import requests, secrets, os, json, time, base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class pinterest():

    def __init__(self):

        if not os.path.exists("./data"):
            os.makedirs("./data")

    def get_token(self, code: str, client_id: str, client_secret: str):
        
        headers = {
            'Authorization': f'Basic {base64.b64encode((f"{client_id}:{client_secret}").encode()).decode()}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost/'
        }

        response = requests.post('https://api.pinterest.com/v5/oauth/token', headers=headers, data=data)

        return response.json()

    def get_code(self, url: str):

        cookies = json.loads(open("./data/cookies.json", "r+").read())["cookies"]
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://{cookies[0]['domain']}/login/")
        
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get(url)
        page_state = driver.execute_script('return document.readyState;')
        
        if page_state == 'complete':
            time.sleep(3)
            if "/oauth" in driver.current_url:
                driver.find_element(By.XPATH, "//div[contains(text(),'Give access')]").click()
            
            else: print("Refreshing cookies..."); pinterest()
        
        while ("code=" not in driver.current_url):
            pass

        code = driver.current_url.split("code=")[1].split("&")[0]
        driver.close()

        return code

    def get_cookies(self, email: str, password: str):

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pinterest.com/login/")

        driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

        driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/form[1]/div[5]/button[1]/div[1]").click()
        
        while ('/business/hub/' not in driver.current_url):
            pass
        
        cookies = driver.get_cookies()
        driver.close()

        return cookies

    def auth(self, client_id: str, client_secret: str, redirect_uri: str,  scope: str):

            if not os.path.exists("./data/cookies.json"):

                if not os.path.exists("./data/credentials.txt"):
                    print("No cookies found or expired, you need relogin.\n")
                    email, password = input("Enter your Email Address: "), input("Enter your Password: ")

                    os.system("cls")

                    save_credentials = input("Would you like to save your credentials? (y/n): ")
                    if save_credentials.lower() == "y":
                        open("./data/credentials.txt", "w+").write(f"{email}:{password}")

                else: 
                    credentials = (open("./data/credentials.txt", "r+").read()).split(":")
                    email, password = credentials[0], credentials[1]

                open("./data/cookies.json", "w+").write(json.dumps({"cookies": self.get_cookies(email, password)}))
                
            oauth_state = secrets.token_hex()

            params = {
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': scope,
                'state': oauth_state,
            }

            response = requests.get('https://www.pinterest.com/oauth/', params=params, allow_redirects=True)

            if response.status_code != 200:
                return response.json()

            try:
                result = self.get_token(self.get_code(response.url), client_id, client_secret)
            except Exception as E: print(f"Error: {E}! Restarting..."); time.sleep(3); pinterest()

            return result
