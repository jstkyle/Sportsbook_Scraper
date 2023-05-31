from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getStakeOdds():
    #changing chromedriver default options
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    web = 'https://stake.com/'
    live_tennis = 'https://stake.com/sports/live/tennis'
    path = '/Users/.../chromedriver'  # replace with your chromedriver path

    # create a Service object
    s = Service(path)

    #execute chromedriver with edited options
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(live_tennis)


    # Accept Cookie
    accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/button')))
    accept.click()

    grandparent = driver.find_element(By.CSS_SELECTOR, '.layout-spacing.variant-tournaments.svelte-1lhz8p6')
    parents = grandparent.find_elements(By.CSS_SELECTOR, '.secondary-accordion.level-2.svelte-7xs5kt.is-open')

    for parent in parents:
        children = parent.find_elements(By.CSS_SELECTOR, '[data-test="fixture-preview"]')
        print(len(children))
        for child in children:
            players = child.find_elements(By.CSS_SELECTOR, '.outcome-content.svelte-hktcf3')
            for player in players:
                name = player.find_element(By.CSS_SELECTOR, '.name.svelte-hktcf3').text
                odd = player.find_element(By.CSS_SELECTOR, '.weight-bold.line-height-default.align-left.size-default.text-size-default.variant-action.with-icon-space.svelte-1myjzud').text
                print(name, odd)
    time.sleep(5)

getStakeOdds()

def getCloudbetOdds():
    #changing chromedriver default options
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    live_tennis = 'https://www.cloudbet.com/en/sports/tennis/inPlay'
    today_tennis = 'https://www.cloudbet.com/en/sports/tennis/today'
    path = '/Users/.../chromedriver'  # replace with your chromedriver path

    # create a Service object
    s = Service(path)

    #execute chromedriver with edited options
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(today_tennis)


    # Accept Cookie
    # accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/button')))
    # accept.click()

    grandparent = driver.find_element(By.CSS_SELECTOR, '.MuiBox-root.css-hpgf8j')
    parents = grandparent.find_elements(By.CSS_SELECTOR, '[data-component="competition-accordion"]')
    for parent in parents:
        children = parent.find_elements(By.CSS_SELECTOR, '[data-component="event-list-item"]')
        for idx, child in enumerate(children):
            try:
                players = child.find_elements(By.CSS_SELECTOR, '.css-vb6e92')
                player1 = players[0].find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body2.css-dfdar3').text
                player2 = players[1].find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body2.css-dfdar3').text
                odds = child.find_elements(By.CSS_SELECTOR, '[class$="css-68o8xu"]')
                player1_odd = odds[0].text
                player2_odd = odds[1].text
                #print(player1_odd, player2_odd)
                print(player1, player2, player1_odd, player2_odd)
            except:
                print("Match Locked!")
            
    time.sleep(600)
