from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class Instagram:

    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.url = 'https://instagram.com'
        self.username = username
        self.password = password
        self.followers = []
        self.following = []

    def run(self):
        self.driver.get(self.url)
        if "Instagram" in self.driver.title:
            print(f"----- Logging in {self.username} -----")
            self.login()
            print(f'----- Processing haters -----')
            self.find_haters()

    def login(self):
        username_text_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_text_field.send_keys(self.username)
        password_text_field = self.driver.find_element_by_name('password')
        password_text_field.send_keys(self.password)
        login_btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
        login_btn.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(text(), "Not Now")]'))
            ).click()
        except NoSuchElementException:
            pass
        # Click on profile picture to go to profile page
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img').click()

    def find_haters(self):

        def _get_users(users_box, context):
            limit = 50
            while True:
                old_height = self.driver.execute_script('return document.getElementsByClassName("isgrP")[0].scrollHeight;')
                sleep(0.25)
                self.driver.execute_script('document.getElementsByClassName("isgrP")[0].scrollTop = document.getElementsByClassName("isgrP")[0].scrollHeight;')
                if old_height == self.driver.execute_script('return document.getElementsByClassName("isgrP")[0].scrollHeight;'):
                    if limit == 0:
                        print(f'Done proccessing {context}')
                        break
                    limit -= 1
                else:
                    limit = 50
            unfiltered_users = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul').find_elements_by_tag_name('a')
            users = [name.text for name in unfiltered_users if name.text != '']
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()

            return users



        def _get_followers():
            # Click on Followers to show <ul> of followers
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))
            ).click()
            followers_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[4]/div/div[2]'))
            )
            self.followers = _get_users(followers_div, "followers")

        def _get_following():
            # Click on Followers to show <ul> of followers
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'))
            ).click()
            following_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[4]/div/div[2]'))
            )
            self.following = _get_users(following_div, "following")

        _get_followers()
        _get_following()

        for num, username in enumerate([username for username in self.following if username not in self.followers], 1):
            print(f'{num} {username}')
        
        


instagram = Instagram('<USERNAME>', '<PASSWORD>')
instagram.run()