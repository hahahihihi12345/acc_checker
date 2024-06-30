from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def log_in(USERNAME, PASSWORD, driver):
    driver.get("https://www.instagram.com/accounts/login")

    # refuse cookies
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,\
        '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'))).click()
    
    time.sleep(4)
    
    # input name & password
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, \
        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'))).click()


def get_json(username, driver):
    # get the text from site
    url = "https://www.instagram.com/web/search/topsearch/?query=" + username
    driver.get(url)
    text = driver.find_element(By.XPATH, "/html/body").text

    # strip it from bullshit
    if "{" not in text or "users" not in text:
        return {}
    i = 0
    while text[i] != "{":
        i += 1
    text = text[i:]

    # repair if cut off
    depth = 0
    last_whole_index = 0

    for i in range(len(text)):
        char = text[i]
        match char:
            case "{":
                depth += 1
            case "}":
                depth -= 1
                if depth == 1:
                    last_whole_index = i
            case _:
                pass
    
    if depth != 0:
        text = text[:last_whole_index + 1] + "]}"

    # convert it to python and return
    try:
        return json.loads(text)
    except:
        with open("response.txt", "w")as resp_file:
            resp_file.write(text)
        return {}


def main():
    MAIN_USERNAME = "PLACEHOLDER_USERNAME" # YOUR username
    MAIN_PASSWORD = "PLACEHOLDER_PASSWORD"
    REC_FLAG = False

    usernames_to_check = ["lewd._.waifus._.v1", "sunny.video1","jojobeut1"] # WANTED usernames
    
    potential_alts = set()
    exists = {}

    # open browser & log in Instagram
    driver = webdriver.Edge()
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)
    time.sleep(20)

    # iterate through the wanted usernames

    for username in usernames_to_check:
        users_json = get_json(username, driver=driver)
        if users_json == {}:
            print("invalid JSON")
            continue

        for user in users_json['users']:
            exists[username] = False
            is_wanted = user['user']['full_name'] == username
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
