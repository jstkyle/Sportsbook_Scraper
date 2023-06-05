from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from fuzzywuzzy import process


def getStakeOdds(driver):
    #print("Successfully opend browser")
    teams = []
    player1_odds = []
    player2_odds = []
    # Accept Cookie
    #accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/button')))
    #accept.click()

    grandparent = driver.find_element(By.CSS_SELECTOR, '.layout-spacing.variant-tournaments.svelte-1lhz8p6')
    parents = grandparent.find_elements(By.CSS_SELECTOR, '.secondary-accordion.level-2.svelte-7xs5kt.is-open')
    for parent in parents:
        children = parent.find_elements(By.CSS_SELECTOR, '[data-test="fixture-preview"]')
        for child in children:
            try:
                players = child.find_elements(By.CSS_SELECTOR, '.outcome-content.svelte-hktcf3')
                player1 = players[0].find_element(By.CSS_SELECTOR, '.name.svelte-hktcf3').text
                player2 = players[1].find_element(By.CSS_SELECTOR, '.name.svelte-hktcf3').text
                last, first = player1.split(', ')
                player1 = first + " " + last
                last, first = player2.split(', ')
                player2 = first + " " + last
                player1_odd = players[0].find_element(By.CSS_SELECTOR, '.weight-bold.line-height-default.align-left.size-default.text-size-default.variant-action.with-icon-space.svelte-1myjzud').text
                player2_odd = players[1].find_element(By.CSS_SELECTOR, '.weight-bold.line-height-default.align-left.size-default.text-size-default.variant-action.with-icon-space.svelte-1myjzud').text
                player1_odds.append(player1_odd)
                player2_odds.append(player2_odd)
                teams.append(player1 + '/' + player2)
                # print(player1, player2, player1_odd, player2_odd)
            except:
                pass
                # print("Match Locked!")

    dict_gambling = {'Teams': teams, 'Player1_Odds': player1_odds, 'Player2_Odds': player2_odds}
    df_Stake = pd.DataFrame.from_dict(dict_gambling)
    #print(df_Stake)
    return df_Stake


def getCloudbetOdds(driver):
    teams = []
    player1_odds = []
    player2_odds = []
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
                player1_odds.append(player1_odd)
                player2_odds.append(player2_odd)
                teams.append(player1 + '/' + player2)
                # print(player1, player2, player1_odd, player2_odd)
            except:
                pass
                # print("Match Locked!")
    dict_gambling = {'Teams': teams, 'Player1_Odds': player1_odds, 'Player2_Odds': player2_odds}
    df_CloudBet = pd.DataFrame.from_dict(dict_gambling)
    # print(df_CloudBet)
    return df_CloudBet

def get1xbitOdds(driver):
    teams = []
    player1_odds = []
    player2_odds = []

    grandparent = driver.find_element(By.CSS_SELECTOR, '.game_content_line.on_main.live-content ')
    parents = grandparent.find_elements(By.CSS_SELECTOR, '.dashboard-champ-content')
    for parent in parents:
        children = parent.find_elements(By.CSS_SELECTOR, '.c-events__item.c-events__item_col.dashboard-champ-content__event-item')
        for child in children:
            try:
                players = child.find_elements(By.CSS_SELECTOR, '.c-events-scoreboard__team-wrap')
                player1 = players[0].find_element(By.CSS_SELECTOR, '.c-events__team').text
                player2 = players[1].find_element(By.CSS_SELECTOR, '.c-events__team').text
                player1_odd = child.find_element(By.CSS_SELECTOR, '[title="1"]').find_element(By.CSS_SELECTOR, '.c-bets__inner').text
                player2_odd = child.find_element(By.CSS_SELECTOR, '[title="2"]').find_element(By.CSS_SELECTOR, '.c-bets__inner').text
                player1_odds.append(player1_odd)
                player2_odds.append(player2_odd)
                teams.append(player1 + '/' + player2)
                #print(player1, player2, player1_odd, player2_odd)
            except:
                pass
                #print("Match Locked!")

    dict_gambling = {'Teams': teams, 'Player1_Odds': player1_odds, 'Player2_Odds': player2_odds}
    df_1xbit = pd.DataFrame.from_dict(dict_gambling)
    #print(df_1xbit)
    return df_1xbit

from fuzzywuzzy import process
import pandas as pd

def match_name(name, list_names, min_score=0):
    max_score = -1
    max_name = ""
    for name2 in list_names:
        score = process.extractOne(name, [name2], score_cutoff=min_score)
        if score is not None and score[1] > max_score:
            max_name = name2
            max_score = score[1]
    return max_name, max_score


def combine_dfs(df1, df2):
    print(df1)
    print(df2)
    names_df1 = df1['Teams'].tolist()
    names_df2 = df2['Teams'].tolist()

    names = []
    for name in names_df2:
        match = match_name(name, names_df1, 70)  # 80 is the score cutoff
        if match[1] >= 70:
            names.append(match[0])
        else:
            names.append(None)

    df2['matched_name'] = names

    merged_df = pd.merge(df1, df2, left_on='Teams', right_on='matched_name', how='outer')

    # Rename columns for clarity
    merged_df = merged_df.rename(columns={'Player1_Odds_x': 'player1_odds_stake',
                                          'Player2_Odds_x': 'player2_odds_stake',
                                          'Player1_Odds_y': 'player1_odds_cloudbet',
                                          'Player2_Odds_y': 'player2_odds_cloudbet'})

    # Remove the temporary 'matched_name' column
    merged_df = merged_df.drop(columns=['matched_name'])
    merged_df = merged_df.drop(columns=['Teams_y'])
    merged_df = merged_df.rename(columns={'Teams_x': 'Teams'})
    merged_df = merged_df.dropna()
    return merged_df

def calculate_surebets(df):
    df['player1_odd_max'] = df[['player1_odds_cloudbet', 'player1_odds_stake']].max(axis=1)
    df['player2_odd_max'] = df[['player2_odds_cloudbet', 'player2_odds_stake']].max(axis=1)
    df['probability'] = 1/df['player1_odd_max'] + 1/df['player2_odd_max']
    df['surebets'] = df['probability'] < 1

    return df


def run_live_bets():
    #changing chromedriver default options
    options = Options()
    options.add_argument('window-size=1920x1080')
    path = '/Users/.../chromedriver'  # replace with your chromedriver path

    stake_live_tennis = 'https://stake.com/sports/live/tennis'
    cloudbet_live_tennis = 'https://www.cloudbet.com/en/sports/tennis/inPlay'
    tennis_1xbit = 'https://1xbit1.com/live/tennis'

    # create a Service object
    s1 = Service(path)
    s2 = Service(path)

    onexbit_driver = webdriver.Chrome(service=s1, options=options)
    cloudbet_driver = webdriver.Chrome(service=s2, options=options)
    onexbit_driver.get(tennis_1xbit)
    cloudbet_driver.get(cloudbet_live_tennis)
    
    while(True):
        df_1xbit = get1xbitOdds(onexbit_driver)
        df_cloudbet = getCloudbetOdds(cloudbet_driver)
        combined_df = combine_dfs(df_1xbit, df_cloudbet)
        final_df = calculate_surebets(combined_df)
        # set to None to display all columns in the dataframe
        pd.set_option('display.max_columns', None)

        # set to None to display all rows in the dataframe
        pd.set_option('display.max_rows', None)
        print(final_df)
        time.sleep(2)

    
def test_run():
    #changing chromedriver default options
    options = Options()
    options.add_argument('window-size=1920x1080')
    path = '/Users/.../chromedriver'  # replace with your chromedriver path

    stake_live_tennis = 'https://stake.com/sports/live/tennis'
    cloudbet_live_tennis = 'https://www.cloudbet.com/en/sports/tennis/inPlay'
    tennis_1xbit = 'https://1xbit1.com/live/tennis'

    # create a Service object
    s = Service(path)

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(tennis_1xbit)
    get1xbitOdds(driver)


run_live_bets()
#test_run()