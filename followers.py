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
    

def get_followers(username, driver):
    followers = LinkedList()
    url = "https://www.instagram.com/" + username + "/following/"
    driver.get(url)

    #this shit loads dynamically, scroll to the bottom for this to work
    input("scroll to the bottom")
    # I will insert a script to do it for you eventually

    # Xpath to following container
    #x = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div"
    #follower_div = driver.find_element(By.XPATH, x)

    # iterate through followed accounts
    for div in driver.find_elements(By.XPATH, '//div[@class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"]'):
        #name div      /div/div/div/div[2]/div/div/div/div/div/a/div/div/span
        #full name div /div/div/div/div[2]/div/div/span/span
        name = div.find_element(By.XPATH, "./div/div/div/div[2]/div/div/div/div/div/a/div/div/span").text
        fullname = div.find_element(By.XPATH, "./div/div/div/div[2]/div/div/span/span").text

        followers.append((name, fullname))

    return followers


def printout(linked: LinkedList, file):
    file.write("scraped followers: \n")
    while linked.head is not None:
        text = linked.pop().value
        file.write(", ".join(text) + "\n")
    file.write("\n")
    

def main():
    with open("wanted_usernames.txt", "r", encoding="utf-8") as wanted:
        usernames_to_check = wanted.read().split(";")# WANTED usernames

    with open("pass.txt", "r") as cred_file:
        creds = cred_file.read().split(";")
    USERNAME, PASSWORD = creds

    # open browser & log in Instagram
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    log_in(USERNAME, PASSWORD, driver)
    time.sleep(10)
    print("logged in")

    with open ("followers.txt", "w", encoding = "utf-8") as res_file:
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