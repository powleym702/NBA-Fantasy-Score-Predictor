from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

CHROME_DRIVER_PATH = r'C:\Users\matth\OneDrive\Documents\chromedriver-win32\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
 
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Initiates all the lists that will hold the projection values for each player
player_stats = {}
point_calcs = []
reb_calcs = []
assist_calcs = []
steal_calcs = []
block_calcs = []
turnover_calcs = []

# Opens draftkings website to begin scraping the points projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-points&subcategory=points-o%2Fu"
    driver.get(url)
    time.sleep(5) 

    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0,0,0,0,0,0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-') 
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)
# Approximates the projection for the player using known limits and values for draftkings for points projections
                if over_odds == under_odds:
                    point_calc = line_value
                elif over_odds < under_odds:
                    if line_value < 12:
                        if over_odds == -120:
                            point_calc = line_value + .125
                        elif over_odds == -125:
                            point_calc = line_value + .25
                        elif over_odds == -130:
                            point_calc = line_value + .375
                        elif over_odds == -135:
                            point_calc = line_value + .5 
                        else:
                            print(f"error: odds not correct for {player_name}") 
                    elif line_value > 12:
                        if over_odds == -120:
                            point_calc = line_value + .17
                        elif over_odds == -125:
                            point_calc = line_value + .33
                        elif over_odds == -130:
                            point_calc =  line_value + .5 
                        else:
                            print(f"error: odds not correct for {player_name}")                        
                elif under_odds < over_odds:
                    if line_value < 12:
                        if under_odds == -120:
                            point_calc = line_value - .125
                        elif under_odds == -125:
                            point_calc = line_value - .25
                        elif under_odds == -130:
                            point_calc = line_value - .375
                        elif under_odds == -135:
                            point_calc = line_value - .5 
                        else:
                            print(f"error: odds not correct for {player_name}") 
                    elif line_value > 12:
                        if under_odds == -120:
                            point_calc = line_value - .17
                        elif under_odds == -125:
                            point_calc = line_value - .33
                        elif under_odds == -130:
                            point_calc =  line_value - .5
                        else:
                            print(f"error: odds not correct for {player_name}")     
                else:
                    print(f"odds error for {player_name}")  
# Adds the point calculation for each player                
                point_calc = round(point_calc,3)
                player_stats[player_name][1] = point_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

finally:
    print("")

# Opens draftkings website to begin scraping the rebounds projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-rebounds&subcategory=rebounds-o%2Fu"
    driver.get(url)
    time.sleep(5) 

    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0, 0, 0, 0, 0, 0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-')  
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)

                if under_odds < over_odds:
                    Q20 = "u"
                elif over_odds < under_odds:
                    Q20 = "o"
                else:
                    Q20 = "u"  

# Approximates the projection for the player using known limits and values for draftkings for rebounds projections

                R20 = line_value
                S20 = min(over_odds, under_odds)

                if R20 <= 15 and R20 % 1 == 0.5:
                    if R20 == 1.5:
                        Q21 = 250 if Q20 == "u" else 200
                    elif R20 == 2.5:
                        Q21 = 200 if Q20 == "u" else 175
                    elif R20 == 3.5:
                        Q21 = 175 if Q20 == "u" else 160
                    elif R20 == 4.5:
                        Q21 = 166 if Q20 == "u" else 160
                    elif R20 == 5.5:
                        Q21 = 160
                    elif R20 == 6.5:
                        Q21 = 160 if Q20 == "u" else 154
                    elif R20 == 7.5:
                        Q21 = 154
                    elif R20 == 8.5:
                        Q21 = 145
                    elif R20 == 9.5:
                        Q21 = 145
                    elif R20 == 10.5:
                        Q21 = 145
                    elif R20 == 11.5:
                        Q21 = 140 if Q20 == "u" else 135
                    elif R20 == 12.5:
                        Q21 = 135 if Q20 == "u" else 130
                    elif R20 >= 13.5:
                        Q21 = 130
                    else:
                        Q21 = None  
                else:
                    Q21 = None  

                if S20 > -115 and S20 < 115:
                    reb_calc = line_value  
                else:
                    if Q20 == "u":
                        reb_calc = (R20 - 0.5) + (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None
                    else:
                        reb_calc = (R20 + 0.5) - (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None

# Adds the rebound calculation for each player                
                reb_calc = round(reb_calc,3)
                player_stats[player_name][2] = reb_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue
finally:
    print("")

# Opens draftkings website to begin scraping the assists projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-assists&subcategory=assists-o%2Fu"
    driver.get(url)
    time.sleep(5)  

    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0, 0, 0, 0, 0, 0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-') 
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)


                if under_odds < over_odds:
                    Q20 = "u"
                elif over_odds < under_odds:
                    Q20 = "o"
                else:
                    Q20 = "u"  

# Approximates the projection for the player using known limits and values for draftkings for assists projections
                R20 = line_value
                S20 = min(over_odds, under_odds)

                if R20 <= 15 and R20 % 1 == 0.5:
                    if R20 == 1.5:
                        Q21 = 250 if Q20 == "u" else 200
                    elif R20 == 2.5:
                        Q21 = 200 if Q20 == "u" else 175
                    elif R20 == 3.5:
                        Q21 = 175 if Q20 == "u" else 160
                    elif R20 == 4.5:
                        Q21 = 166 if Q20 == "u" else 160
                    elif R20 == 5.5:
                        Q21 = 160
                    elif R20 == 6.5:
                        Q21 = 160 if Q20 == "u" else 154
                    elif R20 == 7.5:
                        Q21 = 154
                    elif R20 == 8.5:
                        Q21 = 145
                    elif R20 == 9.5:
                        Q21 = 145
                    elif R20 == 10.5:
                        Q21 = 145
                    elif R20 == 11.5:
                        Q21 = 140 if Q20 == "u" else 135
                    elif R20 == 12.5:
                        Q21 = 135 if Q20 == "u" else 130
                    elif R20 >= 13.5:
                        Q21 = 130
                    elif R20 == 0.5:
                        Q4 = max(over_odds,under_odds)
                        P4 = min(over_odds,under_odds)
                        if Q20 == "o":
                            Q21 = 250
                       
                    else:
                        Q21 = None  
                else:
                    Q21 = None  

                if S20 > -115 and S20 < 115:
                    assist_calc = line_value 
                else:
                    if Q20 == "u":
                        if R20 == 0.5:
                            assist_calc = Q21 = (abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) / \
                   ((abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) + 
                    (abs(P4) / (abs(P4) + 100) if P4 < 0 else 100 / (P4 + 100)))
                        else:
                            assist_calc = (R20 - 0.5) + (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None
                    else:
                        assist_calc = (R20 + 0.5) - (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None

# Adds the assists calculation for each player                
                assist_calc = round(assist_calc,3)
                player_stats[player_name][3] = assist_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

finally:
    print("")

# Opens draftkings website to begin scraping the steals projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-defense&subcategory=steals-o%2Fu"
    driver.get(url)
    time.sleep(5) 
    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0, 0, 0, 0, 0, 0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-')  
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)


                if under_odds < over_odds:
                    Q20 = "u"
                elif over_odds < under_odds:
                    Q20 = "o"
                else:
                    Q20 = "u" 

# Approximates the projection for the player using known limits and values for draftkings for steals projections
                R20 = line_value
                S20 = min(over_odds, under_odds)

                if R20 <= 15 and R20 % 1 == 0.5:
                    if R20 == 1.5:
                        Q21 = 250 if Q20 == "u" else 200
                    elif R20 == 2.5:
                        Q21 = 200 if Q20 == "u" else 175
                    elif R20 == 3.5:
                        Q21 = 175 if Q20 == "u" else 160
                    elif R20 == 4.5:
                        Q21 = 166 if Q20 == "u" else 160
                    elif R20 == 5.5:
                        Q21 = 160
                    elif R20 == 6.5:
                        Q21 = 160 if Q20 == "u" else 154
                    elif R20 == 7.5:
                        Q21 = 154
                    elif R20 == 8.5:
                        Q21 = 145
                    elif R20 == 9.5:
                        Q21 = 145
                    elif R20 == 10.5:
                        Q21 = 145
                    elif R20 == 11.5:
                        Q21 = 140 if Q20 == "u" else 135
                    elif R20 == 12.5:
                        Q21 = 135 if Q20 == "u" else 130
                    elif R20 >= 13.5:
                        Q21 = 130
                    elif R20 == 0.5:
                        Q4 = max(over_odds,under_odds)
                        P4 = min(over_odds,under_odds)
                        if Q20 == "o":
                            Q21 = 250
                       
                    else:
                        Q21 = None  
                else:
                    Q21 = None 

                if S20 > -115 and S20 < 115:
                    steal_calc = line_value 
                else:
                    if Q20 == "u":
                        if R20 == 0.5:
                            steal_calc = Q21 = (abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) / \
                   ((abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) + 
                    (abs(P4) / (abs(P4) + 100) if P4 < 0 else 100 / (P4 + 100)))
                        else:
                            steal_calc = (R20 - 0.5) + (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None
                    else:
                        steal_calc = (R20 + 0.5) - (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None

# Adds the steals calculation for each player                
                steal_calc = round(steal_calc,3)
                player_stats[player_name][4] = steal_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

finally:
    print("")

# Opens draftkings website to begin scraping the blocks projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-defense&subcategory=blocks-o%2Fu"
    driver.get(url)
    time.sleep(5) 

    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text


# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0, 0, 0, 0, 0, 0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-') 
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)


                if under_odds < over_odds:
                    Q20 = "u"
                elif over_odds < under_odds:
                    Q20 = "o"
                else:
                    Q20 = "u"  

# Approximates the projection for the player using known limits and values for draftkings for blocks projections
                R20 = line_value
                S20 = min(over_odds, under_odds)

                if R20 <= 15 and R20 % 1 == 0.5:
                    if R20 == 1.5:
                        Q21 = 250 if Q20 == "u" else 200
                    elif R20 == 2.5:
                        Q21 = 200 if Q20 == "u" else 175
                    elif R20 == 3.5:
                        Q21 = 175 if Q20 == "u" else 160
                    elif R20 == 4.5:
                        Q21 = 166 if Q20 == "u" else 160
                    elif R20 == 5.5:
                        Q21 = 160
                    elif R20 == 6.5:
                        Q21 = 160 if Q20 == "u" else 154
                    elif R20 == 7.5:
                        Q21 = 154
                    elif R20 == 8.5:
                        Q21 = 145
                    elif R20 == 9.5:
                        Q21 = 145
                    elif R20 == 10.5:
                        Q21 = 145
                    elif R20 == 11.5:
                        Q21 = 140 if Q20 == "u" else 135
                    elif R20 == 12.5:
                        Q21 = 135 if Q20 == "u" else 130
                    elif R20 >= 13.5:
                        Q21 = 130
                    elif R20 == 0.5:
                        Q4 = max(over_odds,under_odds)
                        P4 = min(over_odds,under_odds)
                        if Q20 == "o":
                            Q21 = 250
                       
                    else:
                        Q21 = None  
                else:
                    Q21 = None 

                if S20 > -115 and S20 < 115:
                    block_calc = line_value  
                else:
                    if Q20 == "u":
                        if R20 == 0.5:
                            block_calc = Q21 = (abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) / \
                   ((abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) + 
                    (abs(P4) / (abs(P4) + 100) if P4 < 0 else 100 / (P4 + 100)))
                        else:
                            block_calc = (R20 - 0.5) + (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None
                    else:
                        block_calc = (R20 + 0.5) - (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None

# Adds the blocks calculation for each player                
                block_calc = round(block_calc,3)
                player_stats[player_name][5] = block_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

finally:
    print("")

# Opens draftkings website to begin scraping the turnovers projections/stats for each player
try:
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-defense&subcategory=turnovers-o%2Fu"
    driver.get(url)
    time.sleep(5)  

    section_xpath = '//*[@id="root"]/section/section[2]/section'
    section = driver.find_element(By.XPATH, section_xpath)

    tables = section.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                player_name = row.find_element(By.XPATH, './th/div/a/span').text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                if player_name not in player_stats:
                    player_stats[player_name] = [player_name, 0, 0, 0, 0, 0, 0]

                line_value = float(row.find_element(By.XPATH, './td[1]/div/div/div/div[1]/span[3]').text)

                over_odds_str = row.find_element(By.XPATH, './td[1]/div/div/div/div[2]/div[2]/span').text
                under_odds_str = row.find_element(By.XPATH, './td[2]/div/div/div/div[2]/div[2]/span').text

                over_odds_str = over_odds_str.replace('−', '-')  
                under_odds_str = under_odds_str.replace('−', '-')

                over_odds = float(over_odds_str)
                under_odds = float(under_odds_str)

                if under_odds < over_odds:
                    Q20 = "u"
                elif over_odds < under_odds:
                    Q20 = "o"
                else:
                    Q20 = "u" 

# Approximates the projection for the player using known limits and values for draftkings for turnovers projections 
                R20 = line_value
                S20 = min(over_odds, under_odds)

                if R20 <= 15 and R20 % 1 == 0.5:
                    if R20 == 1.5:
                        Q21 = 250 if Q20 == "u" else 200
                    elif R20 == 2.5:
                        Q21 = 200 if Q20 == "u" else 175
                    elif R20 == 3.5:
                        Q21 = 175 if Q20 == "u" else 160
                    elif R20 == 4.5:
                        Q21 = 166 if Q20 == "u" else 160
                    elif R20 == 5.5:
                        Q21 = 160
                    elif R20 == 6.5:
                        Q21 = 160 if Q20 == "u" else 154
                    elif R20 == 7.5:
                        Q21 = 154
                    elif R20 == 8.5:
                        Q21 = 145
                    elif R20 == 9.5:
                        Q21 = 145
                    elif R20 == 10.5:
                        Q21 = 145
                    elif R20 == 11.5:
                        Q21 = 140 if Q20 == "u" else 135
                    elif R20 == 12.5:
                        Q21 = 135 if Q20 == "u" else 130
                    elif R20 >= 13.5:
                        Q21 = 130
                    elif R20 == 0.5:
                        Q4 = max(over_odds,under_odds)
                        P4 = min(over_odds,under_odds)
                        if Q20 == "o":
                            Q21 = 250
                       
                    else:
                        Q21 = None  
                else:
                    Q21 = None  

                if S20 > -115 and S20 < 115:
                    turnover_calc = line_value 
                else:
                    if Q20 == "u":
                        if R20 == 0.5:
                            turnover_calc = Q21 = (abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) / \
                   ((abs(Q4) / (abs(Q4) + 100) if Q4 < 0 else 100 / (Q4 + 100)) + 
                    (abs(P4) / (abs(P4) + 100) if P4 < 0 else 100 / (P4 + 100)))
                        else:
                            turnover_calc = (R20 - 0.5) + (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None
                    else:
                        turnover_calc = (R20 + 0.5) - (-abs(S20) + Q21) / (Q21 - 115) / 2 if Q21 else None

# Adds the turnovers calculation for each player                
                turnover_calc = round(turnover_calc,3)
                player_stats[player_name][6] = turnover_calc

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

finally:
    print("dk done")


# These url codes are examples, the user must go to Fliff and find the game codes manually
url_codes = ["269365","269364","269349","269362","269363","269352","269347","269355","269354","269358","269353","269348","269357"]
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

wait_counter = 0 # To ensure fliff is given enough time to load the first time

# Opens fliff for every game on the current NBA slate
for code in url_codes:
    url = f"https://sports.getfliff.com/markets/{code}_c_p_204_prematch?category=player-props"
    try:
        driver.get(url)
        if wait_counter == 0:
            time.sleep(40)
        else:  
            time.sleep(20)
        wait_counter += 1

        base_xpath = '//*[@id="root"]/div[1]/div[3]/div[{}]'
        label_xpath_suffix = '/span'
        section_index = 1  
        player_blocks_xpath = None

        game_xpath = "//*[@id=\"root\"]/div[1]/div[1]/div/div[1]/div/div[1]/span"
        game_value = driver.find_element(By.XPATH, game_xpath)

        while True:
            try:
                section_xpath = base_xpath.format(section_index)
                label_xpath = section_xpath + label_xpath_suffix

                label_element = driver.find_element(By.XPATH, label_xpath)
                label_text = label_element.text.strip()

                if label_text == "PLAYER BLOCKS":
                    player_blocks_xpath = section_xpath
                    break  

                section_index += 1  
            except NoSuchElementException:
                print("No more sections to check.")
                break

        if not player_blocks_xpath:
            print("No section with label 'PLAYER BLOCKS' found. Exiting script.")
        else:
            try:
                player_blocks_section = driver.find_element(By.XPATH, player_blocks_xpath)
                player_blocks_section.click()
                time.sleep(.5)  
            except NoSuchElementException:
                print("Main screen switch not found. Moving on...")

            base_table_xpath = '//*[@id="root"]/div[1]/div[3]'

            player_name_xpath_template = f'{base_table_xpath}/div[{{i}}]/p'

            line_xpath_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[2]/span'

            odds_xpath_1_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[3]/span'
            odds_xpath_2_template = f'{base_table_xpath}/div[{{i}}]/div[2]/div/div[3]/span'

            i = 7  
            player_data = []  

# Fliff Block Scraper
            while True:
                try:
                    player_name_xpath = player_name_xpath_template.format(i=i)
                    player_name_element = driver.find_element(By.XPATH, player_name_xpath)
                    player_name = player_name_element.text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                    if player_name not in player_stats:
                        player_stats[player_name] = [player_name, 0,0,0,0,0,0]

                    line_xpath = line_xpath_template.format(i=i)
                    line_element = driver.find_element(By.XPATH, line_xpath)
                    line_text = line_element.text  
                    line = float(line_text.split()[-1])  

                    odds_xpath_1 = odds_xpath_1_template.format(i=i)
                    odds_xpath_2 = odds_xpath_2_template.format(i=i)

                    odds_1_element = driver.find_element(By.XPATH, odds_xpath_1)
                    odds_1_text = odds_1_element.text.strip()
                    odds_1 = float(odds_1_text.replace('+', '').replace(' ','')) if odds_1_text else 0.0

                    odds_2_element = driver.find_element(By.XPATH, odds_xpath_2)
                    odds_2_text = odds_2_element.text.strip()
                    odds_2 = float(odds_2_text.replace('+', '').replace(' ','')) if odds_2_text else 0.0

                    odds = min(odds_1, odds_2) 
                    odds_alt = max(odds_1, odds_2)
                    if odds_1 > odds_2:
                        direction = "under"
                    else:
                        direction = "over"

# Calculates projected fliff blocks based off of historical data and limits
                    if line <= 15 and line % 1 == 0.5:
                        if line == 1.5:
                            maximum = 260 if direction == "under" else 210
                        elif line == 2.5:
                            maximum = 210 if direction == "under" else 195
                        elif line == 3.5:
                            maximum = 190 if direction == "under" else 185
                        elif line == 4.5:
                            maximum = 175 if direction == "under" else 170
                        elif line == 5.5:
                            maximum = 170 if direction == "under" else 165
                        elif line == 0.5:
                            if direction == "over":
                                maximum = 265
                            else:
                                maximum = None 
                        else:
                            maximum = None  
                    else:
                        maximum = None  
                    if direction == "under" and line == .5:
                        odds_ratio_1 = abs(odds_alt) / (abs(odds_alt) + 100) if odds_alt < 0 else 100 / (odds_alt + 100)
                        odds_ratio_2 = abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)
                        calc = odds_ratio_1 / (odds_ratio_1 + odds_ratio_2)
                    elif direction == "under" and line <= 5.5:
                        calc = (line - 0.5) + (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None
                    else:
                        calc = (line + 0.5) - (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None
                    calc = round(calc,3)

                    if player_stats[player_name][5] == 0:
                        player_stats[player_name][5] = calc


                    i += 1  
                except NoSuchElementException:
                    break 

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("")

    try:
        time.sleep(.5)  

        base_xpath = '//*[@id="root"]/div[1]/div[3]/div[{}]'
        label_xpath_suffix = '/span'
        section_index = 1  

        player_steals_xpath = None

        while True:
            try:
                section_xpath = base_xpath.format(section_index)
                label_xpath = section_xpath + label_xpath_suffix

                label_element = driver.find_element(By.XPATH, label_xpath)
                label_text = label_element.text.strip()


                if label_text == "PLAYER STEALS":
                    player_steals_xpath = section_xpath
                    break  

                section_index += 1  
            except NoSuchElementException:
                print("No more sections to check.")
                break

        if not player_steals_xpath:
            print("No section with label 'PLAYER STEALS' found. Exiting script.")
        else:
            try:
                player_steals_section = driver.find_element(By.XPATH, player_steals_xpath)
                player_steals_section.click()
                time.sleep(2)  
            except NoSuchElementException:
                print("Main screen switch not found. Moving on...")

            base_table_xpath = '//*[@id="root"]/div[1]/div[3]'

            player_name_xpath_template = f'{base_table_xpath}/div[{{i}}]/p'

            line_xpath_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[2]/span'

            odds_xpath_1_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[3]/span'
            odds_xpath_2_template = f'{base_table_xpath}/div[{{i}}]/div[2]/div/div[3]/span'

            i = 6  
            player_data = [] 

# Fliff Steal Scraper
            while True:
                try:
                    player_name_xpath = player_name_xpath_template.format(i=i)
                    player_name_element = driver.find_element(By.XPATH, player_name_xpath)
                    player_name = player_name_element.text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                    if player_name not in player_stats:
                        player_stats[player_name] = [player_name, 0,0,0,0,0,0]

                    line_xpath = line_xpath_template.format(i=i)
                    line_element = driver.find_element(By.XPATH, line_xpath)
                    line_text = line_element.text 
                    line = float(line_text.split()[-1])  

                    odds_xpath_1 = odds_xpath_1_template.format(i=i)
                    odds_xpath_2 = odds_xpath_2_template.format(i=i)

                    odds_1_element = driver.find_element(By.XPATH, odds_xpath_1)
                    odds_1_text = odds_1_element.text.strip()
                    odds_1 = float(odds_1_text.replace('+', '').replace(' ','')) if odds_1_text else 0.0

                    odds_2_element = driver.find_element(By.XPATH, odds_xpath_2)
                    odds_2_text = odds_2_element.text.strip()
                    odds_2 = float(odds_2_text.replace('+', '').replace(' ','')) if odds_2_text else 0.0

                    odds = min(odds_1, odds_2) 
                    odds_alt = max(odds_1, odds_2)
                    if odds_1 > odds_2:
                        direction = "under"
                    else:
                        direction = "over"

# Calculates projected fliff steals based off of historical data and limits
                    if line <= 15 and line % 1 == 0.5:
                        if line == 1.5:
                            maximum = 260 if direction == "under" else 210
                        elif line == 2.5:
                            maximum = 210 if direction == "under" else 195
                        elif line == 3.5:
                            maximum = 190 if direction == "under" else 185
                        elif line == 4.5:
                            maximum = 175 if direction == "under" else 170
                        elif line == 5.5:
                            maximum = 170 if direction == "under" else 165
                        elif line == 0.5:
                            if direction == "over":
                                maximum = 265
                            else:
                                maximum = None  
                        else:
                            maximum = None 
                    else:
                        maximum = None 
                    if direction == "under" and line == .5:
                        odds_ratio_1 = abs(odds_alt) / (abs(odds_alt) + 100) if odds_alt < 0 else 100 / (odds_alt + 100)
                        odds_ratio_2 = abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)
                        calc = odds_ratio_1 / (odds_ratio_1 + odds_ratio_2)
                    elif direction == "under" and line <= 5.5:
                        calc = (line - 0.5) + (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None
                    else:
                        calc = (line + 0.5) - (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None

                    calc = round(calc,3)

                    if player_stats[player_name][4] == 0:
                        player_stats[player_name][4] = calc

                    i += 1  
                except NoSuchElementException:
                    break  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("")

    try:
        time.sleep(.5)  

        base_xpath = '//*[@id="root"]/div[1]/div[3]/div[{}]'
        label_xpath_suffix = '/span'
        section_index = 1  

        player_turnovers_xpath = None

        while True:
            try:
                section_xpath = base_xpath.format(section_index)
                label_xpath = section_xpath + label_xpath_suffix

                label_element = driver.find_element(By.XPATH, label_xpath)
                label_text = label_element.text.strip()
            
                if label_text == "PLAYER TURNOVERS":
                    player_turnovers_xpath = section_xpath
                    break  
                section_index += 1 
            except NoSuchElementException:
                print("No more sections to check.")
                break

        if not player_turnovers_xpath:
            print("No section with label 'PLAYER TURNOVERS' found. Exiting script.")
        else:
            try:
                player_turnovers_section = driver.find_element(By.XPATH, player_turnovers_xpath)
                player_turnovers_section.click()
                time.sleep(2)  
            except NoSuchElementException:
                print("Main screen switch not found. Moving on...")

            base_table_xpath = '//*[@id="root"]/div[1]/div[3]'

            player_name_xpath_template = f'{base_table_xpath}/div[{{i}}]/p'

            line_xpath_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[2]/span'

            odds_xpath_1_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[3]/span'
            odds_xpath_2_template = f'{base_table_xpath}/div[{{i}}]/div[2]/div/div[3]/span'

            i = 4 
            player_data = []  

# Fliff Turnover Scraper
            while True:
                try:
                    player_name_xpath = player_name_xpath_template.format(i=i)
                    player_name_element = driver.find_element(By.XPATH, player_name_xpath)
                    player_name = player_name_element.text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                    if player_name not in player_stats:
                        player_stats[player_name] = [player_name, 0,0,0,0,0,0]

                    line_xpath = line_xpath_template.format(i=i)
                    line_element = driver.find_element(By.XPATH, line_xpath)
                    line_text = line_element.text  
                    line = float(line_text.split()[-1])  

                    odds_xpath_1 = odds_xpath_1_template.format(i=i)
                    odds_xpath_2 = odds_xpath_2_template.format(i=i)

                    odds_1_element = driver.find_element(By.XPATH, odds_xpath_1)
                    odds_1_text = odds_1_element.text.strip()
                    odds_1 = float(odds_1_text.replace('+', '').replace(' ','')) if odds_1_text else 0.0

                    odds_2_element = driver.find_element(By.XPATH, odds_xpath_2)
                    odds_2_text = odds_2_element.text.strip()
                    odds_2 = float(odds_2_text.replace('+', '').replace(' ','')) if odds_2_text else 0.0

                    odds = min(odds_1, odds_2)  
                    odds_alt = max(odds_1, odds_2)
                    if odds_1 > odds_2:
                        direction = "under"
                    else:
                        direction = "over"


# Calculates projected fliff turnovers based off of historical data and limits
                    if line <= 15 and line % 1 == 0.5:
                        if line == 1.5:
                            maximum = 260 if direction == "under" else 210
                        elif line == 2.5:
                            maximum = 210 if direction == "under" else 195
                        elif line == 3.5:
                            maximum = 190 if direction == "under" else 185
                        elif line == 4.5:
                            maximum = 175 if direction == "under" else 170
                        elif line == 5.5:
                            maximum = 170 if direction == "under" else 165
                        elif line == 0.5:
                            if direction == "over":
                                maximum = 265
                            else:
                                maximum = None 
                        else:
                            maximum = None  
                    else:
                        maximum = None 
                    if direction == "under" and line == .5:
                        odds_ratio_1 = abs(odds_alt) / (abs(odds_alt) + 100) if odds_alt < 0 else 100 / (odds_alt + 100)
                        odds_ratio_2 = abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)
                        calc = odds_ratio_1 / (odds_ratio_1 + odds_ratio_2)
                    elif direction == "under" and line <= 5.5:
                        calc = (line - 0.5) + (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None
                    else:
                        calc = (line + 0.5) - (-abs(odds) + maximum) / (maximum - 115) / 2 if maximum else None
                    calc = round(calc,3)

                    if player_stats[player_name][6] == 0:
                        player_stats[player_name][6] = calc

                    i += 1 
                except NoSuchElementException:
                    break  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("")

# Fliff Assist Scraper
    try:
        time.sleep(.5)  
        base_xpath = '//*[@id="root"]/div[1]/div[3]/div[{}]'
        label_xpath_suffix = '/span'
        section_index = 1  

        player_assists_xpath = None

        while True:
            try:
                section_xpath = base_xpath.format(section_index)
                label_xpath = section_xpath + label_xpath_suffix

                label_element = driver.find_element(By.XPATH, label_xpath)
                label_text = label_element.text.strip()
            
                if label_text == "PLAYER ASSISTS":
                    player_assists_xpath = section_xpath
                    break  

                section_index += 1 
            except NoSuchElementException:
                print("No more sections to check.")
                break

        if not player_assists_xpath:
            print("No section with label 'PLAYER ASSISTS' found. Exiting script.")
        else:
            try:
                player_assists_section = driver.find_element(By.XPATH, player_assists_xpath)
                player_assists_section.click()
                time.sleep(2)  
            except NoSuchElementException:
                print("Main screen switch not found. Moving on...")

            base_table_xpath = '//*[@id="root"]/div[1]/div[3]'

            player_name_xpath_template = f'{base_table_xpath}/div[{{i}}]/p'

            line_xpath_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[2]/span'

            odds_xpath_1_template = f'{base_table_xpath}/div[{{i}}]/div[1]/div/div[3]/span'
            odds_xpath_2_template = f'{base_table_xpath}/div[{{i}}]/div[2]/div/div[3]/span'

            i = 3  
            player_data = []  

            while True:
                try:
                    player_name_xpath = player_name_xpath_template.format(i=i)
                    player_name_element = driver.find_element(By.XPATH, player_name_xpath)
                    player_name = player_name_element.text

# Checks if player name is already in list, if not adds a new value to the player_stats list
                    if player_name not in player_stats:
                        player_stats[player_name] = [player_name, 0,0,0,0,0,0]

                    line_xpath = line_xpath_template.format(i=i)
                    line_element = driver.find_element(By.XPATH, line_xpath)
                    line_text = line_element.text  
                    line = float(line_text.split()[-1]) 

                    odds_xpath_1 = odds_xpath_1_template.format(i=i)
                    odds_xpath_2 = odds_xpath_2_template.format(i=i)

                    odds_1_element = driver.find_element(By.XPATH, odds_xpath_1)
                    odds_1_text = odds_1_element.text.strip()
                    odds_1 = float(odds_1_text.replace('+', '').replace(' ','')) if odds_1_text else 0.0

                    odds_2_element = driver.find_element(By.XPATH, odds_xpath_2)
                    odds_2_text = odds_2_element.text.strip()
                    odds_2 = float(odds_2_text.replace('+', '').replace(' ','')) if odds_2_text else 0.0

                    odds = min(odds_1, odds_2)  
                    odds_alt = max(odds_1, odds_2)
                    if odds_1 > odds_2:
                        direction = "under"
                    else:
                        direction = "over"

# Calculates projected fliff assists based off of historical data and limits
                    if line <= 15 and line % 1 == 0.5:
                        if line == 1.5:
                            maximum = 260 if direction == "under" else 210
                        elif line == 2.5:
                            maximum = 210 if direction == "under" else 195
                        elif line == 3.5:
                            maximum = 190 if direction == "under" else 185
                        elif line == 4.5:
                            maximum = 175 if direction == "under" else 170
                        elif line == 5.5:
                            maximum = 170 if direction == "under" else 165
                        elif line == 6.5:
                            maximum = 160 if direction == "under" else 155
                        elif line == 7.5:
                            maximum = 155
                        elif line == 8.5:
                            maximum = 155 if direction == "under" else 150
                        elif line == 9.5:
                            maximum = 150
                        elif line == 10.5:
                            maximum = 150   
                        elif line == 11.5:
                            maximum = 150 if direction == "under" else 140
                        elif line == 12.5:
                            maximum = 140
                        elif line == 13.5:
                            maximum = 140
                        elif line == 14.5:
                            maximum = 140
                        elif line == 0.5:
                            if direction == "over":
                                maximum = 265
                            else:
                                maximum = None 
                        else:
                            maximum = None  

                    calc = round(calc,3)

                    if player_stats[player_name][3] == 0:
                        player_stats[player_name][3] = calc

                    i += 1  
                except NoSuchElementException:
                    break  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"{game_value.text} Finished.")

# Can be changed based on stat weights
factors = [1, 1.2, 1.5, 3, 3, -1]


# Converts projected stats to a projected fantasy score for each player that has projections for all 6 stats
filtered_stats = {
    player: sum(float(stat) * factor for stat, factor in zip(stats[-6:], factors))  
    for player, stats in player_stats.items()
    if all(float(stat) != 0 for stat in stats[-6:])  
}

# Prints out list, with players and their fantasy score projections
for player, total in filtered_stats.items():
    total = round(total,3)
    print(f"{player}  {total}")