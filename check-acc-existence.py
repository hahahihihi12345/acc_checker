from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

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


def get_json(username, driver):
    # get the text from site
    url = "https://www.instagram.com/web/search/topsearch/?query=" + username
    driver.get(url)
    text = driver.page_source

    # strip it from bullshit
    if "{" not in text or "users" not in text:
        return {}

    # cut off html part

    text = text[:text.index("<")]

    # convert it to python and return
    try:
        return json.loads(text)
    except:
        with open("response.txt", "w",encoding="utf-8")as resp_file:
            resp_file.write(text)
        return {}


def main():

    with open("pass.txt", "r") as pass_file:
        creds = pass_file.read().split(",")
    MAIN_USERNAME = creds[0]#"PLACEHOLDER_USERNAME" # YOUR username
    MAIN_PASSWORD = creds[1]#"PLACEHOLDER_PASSWORD"

    REC_FLAG = False

    usernames_to_check = ["sunny.video1"] # WANTED usernames
    
    potential_alts = set()
    exists = {}

    # open browser & log in Instagram
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)

    time.sleep(15)

    # iterate through the wanted usernames

    for username in usernames_to_check:
        users_json = get_json(username, driver=driver)
        if users_json == {}:
            print("invalid JSON")
            continue

        exists[username] = False
        for user in users_json['users']:

            is_wanted = user['user']['full_name'] == username or user['user']['username'] == username
            exists[username] = exists[username] or is_wanted

            if not is_wanted:
                if REC_FLAG:
                    pass
                else:
                    potential_alts.add(user['user']['full_name'])
            
            time.sleep(1)



    with open("results.txt", "w", encoding="utf-8") as res_file:
        for user in exists.keys():
            res_file.write(user + " is still up\n" if exists[user] else user + " is gone, good work!\n")
        res_file.write("potential alts:\n")

        for alt in list(potential_alts):
            res_file.write(" - " + alt + "\n")


if '__main__':
    main()
