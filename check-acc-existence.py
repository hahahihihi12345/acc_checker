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
        print("trying")
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
    text = text[text.index("{"):]
    text = text[:text.index("<")]

    # convert it to python and return
    try:
        return json.loads(text)
    except:
        with open("response.txt", "w",encoding="utf-8")as resp_file:
            resp_file.write(text)
        return {}


def encode(string):
    return "".join([char for char in string if char.isnumeric()])


def get_most_likely(usernames, alts):
    return [alt for alt in list(alts) if encode(alt) in set([encode(name) for name in usernames])]


def print_out_txt(exists, alts):
    with open("results.txt", "w", encoding="utf-8") as res_file:
        most_likely = get_most_likely(exists.keys(), alts)
        for user in exists.keys():
            res_file.write(user + " is still up\n" if exists[user][0] else user + " is gone, good work!\n")
        res_file.write("\nmost likely alts:\n")
        for alt in list(most_likely):
            res_file.write(" - " + alt + "\n")

        res_file.write("\npotential alts:\n")
        for alt in list(alts):
            res_file.write(" - " + alt + "\n")


def print_out_csv(exists):
    par = lambda val: f'"{val}"'
    with open("username-ID.csv", "w", encoding="utf-8") as res_file:
        res_file.write('"username";"user ID";"exists"\n')
        for user in exists.keys():
            res_file.write(";".join((par(user), par(exists[user][1] if exists[user][0] else ""), par("True" if exists[user][0] else "False"))))


def check_username(driver, username, potential_alts):
    users_json = get_json(username, driver=driver)
    if users_json == {}:
        print("invalid JSON")
        return False

    exists = (False,)
    for user in users_json['users']:
        is_wanted = user['user']['full_name'] == username or user['user']['username'] == username
        if not is_wanted:
            potential_alts.add(user['user']['full_name'])
        else:
            exists = (True, user['user']['pk_id'])


    return exists


def status_check(username: str, driver) -> list[bool, str, bool]:
    '''
    checks if account exists, its id and if its private (returned in this order)
    '''
    # get the text from site
    url = "https://www.instagram.com/web/search/topsearch/?query=" + username
    driver.get(url)
    text = driver.page_source
    res = [False, "", False]
    text = text[text.index("{"):]

    first_name_index = text.index('"username":"') + len('"username":"')
    first_id_index = text.index('"pk_id":"') + len('"pk_id":"')
    first_private_index = text.index('"is_private":') + len('"is_private":')
    
    res[0] = text[first_name_index:first_name_index + len(username)] == username # is the first match our username?
    if res[0]:
        res[1] = text[first_id_index:text.index('"', first_id_index)]
        res[2] = not text[first_private_index:text.index('"', first_private_index)] == "false"

    return res


def main():
    with open("wanted_usernames.txt", "r", encoding="utf-8") as wanted:
        usernames_to_check = wanted.read().split(";")# WANTED usernames
    
    with open("pass.txt", "r") as pass_file:
        creds = pass_file.read().split(";")

    MAIN_USERNAME = creds[0] # YOUR username
    MAIN_PASSWORD = creds[1]

    mode = ""
    accepted_modes = {"txt", "csv"}
    while mode not in accepted_modes:
        mode = input("Input mode: ")

    potential_alts = set()
    exists = {}

    # open browser & log in Instagram
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    log_in(MAIN_USERNAME, MAIN_PASSWORD, driver)
    time.sleep(15)

    # iterate through the wanted usernames
    for username in usernames_to_check:
        exists[username] = check_username(driver, username, potential_alts)
        time.sleep(1)

    match mode:
        case "txt":
            print_out_txt(exists, potential_alts)
        case "csv":
            print_out_csv(exists)


if __name__ == '__main__':
    main()
