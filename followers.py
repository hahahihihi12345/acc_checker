from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def pop(self):
        head = self.head
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        return head

    def append(self,val):
        if self.head is None:
            self.head = Node(val)
            self.tail = self.head
        else:
            self.tail.next = Node(val)
            self.tail = self.tail.next

class Node:
    def __init__(self, val):
        self.value = val
        self.next = None


def get_names() -> list[str]:
    with open("wanted_usernames.txt", "r", encoding="utf-8") as wanted:
        return wanted.read().split(";")# WANTED usernames


def get_creds() -> list[str]:
    with open("pass.txt", "r") as cred_file:
        return cred_file.read().split(";")


def get_filter() -> list[str]:
    keywords = []
    with open("keywords.txt", "r") as keywords_file:
        keywords = [keyword.strip() for keyword in keywords_file.read().split(";")]
    return keywords


def scroll_down(driver):
    # xpath /html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]
    x = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]"
    scrollable_element = driver.find_element(By.XPATH, x)
    driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scrollable_element)


def log_in(USERNAME, PASSWORD, driver):
    driver.get("https://www.instagram.com/accounts/login")

    # refuse cookies
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,\
            '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'))).click()
    except:
        pass

    time.sleep(4)
    
    # input name & password
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, \
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'))).click()
    

def get_followers(username, driver) -> LinkedList:
    followers = LinkedList()
    url = "https://www.instagram.com/" + username + "/following/"
    driver.get(url)
    
    # Xpath to following container
    x = '//div[@class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"]'
    loaded = driver.find_elements(By.XPATH, x)
    new_loaded = None
    while new_loaded != loaded:
        loaded = new_loaded
        scroll_down(driver)
        time.sleep(4)
        new_loaded = driver.find_elements(By.XPATH, x)
        


    # iterate through followed accounts
    for div in loaded:
        #name div      /div/div/div/div[2]/div/div/div/div/div/a/div/div/span
        #full name div /div/div/div/div[2]/div/div/span/span
        name = div.find_element(By.XPATH, "./div/div/div/div[2]/div/div/div/div/div/a/div/div/span").text
        fullname = div.find_element(By.XPATH, "./div/div/div/div[2]/div/div/span/span").text

        followers.append((name, fullname))

    return followers


def has_keyword(name: str, keywords: list[str]) -> bool:
    #interchangeable numbers: 0-o, 1-i, 3-e, 4-a, 5-s, 7-t
    change = {"0":"o", "1":"i", "2":"", "3":"e", "4":"a", "5":"s", "6":"", "7":"t", "8":"", "9":""}
    name = name.lower()
    enc_name = "".join([char for char in name if char.isalpha()])
    num_enc_name = "".join([change[char] if char.isnumeric() else char for char in name if char.isalnum()])
    for keyword in keywords:
        if keyword in name or keyword in enc_name or keyword in num_enc_name:
            return True
    return False


def printout(linked: LinkedList, file):
    keywords = get_filter()
    file.write("scraped followers: \n")
    while linked.head is not None:
        text = linked.pop().value
        for name in text:
            if has_keyword(name, keywords):
                file.write(", ".join(text) + "\n")
                break
    file.write("\n")


def main():
    usernames_to_check = get_names()
    USERNAME, PASSWORD = get_creds()

    # open browser & log in Instagram
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    log_in(USERNAME, PASSWORD, driver)
    time.sleep(10)
    print("logged in")

    with open("followers.txt", "w", encoding = "utf-8") as res_file:
        for username in usernames_to_check:
            #try:
                print("trying username: " + username)
                followers = get_followers(username, driver)
                res_file.write("Root username: " + username + "\n")
                printout(followers, res_file)
                print("attempt successful")
            #except:
                #print("failed")


if "__main__":
    main()
