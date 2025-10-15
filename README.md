# NBA-Fantasy-Score-Predictor

## Overview

The function of this script is to help predict fantasy scores for NBA players based off of projections from primarily Draftkings and secondarily Fliff. This is useful for betting sites that have over/under lines for these players, where small edges can be found. It can also be used to find value on DFS sites where certain players may be under or overvalued. 

## Functionality

First, the script scrapes through the main DraftKings pages of each of the statistics for the NBA: points, rebounds, assists, steals, turnovers, and blocks. It creates a list for each player that contains the stat projections for each player, approximating for between lines using historical data from the site. After scraping all stats from DraftKings, it switches to Fliff, which will often have more if not all the lines for each player, filling in the blanks where needed. We scrape Draftkings first since it is known to be sharper, and Fliff is used to fill in mainly the steals, turnovers, and blocks odds. Once both sites have been fully scraped through, the script calculates projected fantasy scores for each player, only calculating a value if odds for all 6 stats are present. 

The factors that each stat is multiplied by can be adjusted easily in the code in the factors list. 

Note: Currently, the user will need to manually inspect the Fliff page to find the url_codes for each game, and manually input them. 
