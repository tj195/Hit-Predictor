import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import csv

def Headers(soup):
  header = soup.find('tr', attrs={'class': 'colhead'})
  columns = [col.get_text() for col in header.find_all('td')]
  final_df = pd.DataFrame(columns=columns)
  return columns

def Batters(columns):
  final_df = None
  for i in range (1,331,50):
      url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2018/start/{}'.format(i)
      page = requests.get(url)
      soup = BeautifulSoup(page.text, 'html.parser')
      counter = 0
      players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
      
      for player in players:
          
          stats = [stat.get_text() for stat in player.find_all('td')]

          temp_df = pd.DataFrame(stats).transpose()
          temp_df.columns = columns

          final_df = pd.concat([final_df, temp_df], ignore_index=True)
  return final_df

def IdRemover():
  with open("output.csv", "r") as source:
    reader = csv.reader(source)
      
    with open("mlb_batter_stats.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
            del r[0]
            writer.writerow(r)

if __name__ == "__main__":
  url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2018/start/1'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  column = Headers(soup)
  batting_Stats = Batters(column)
  batting_Stats.to_csv("output.csv", index=False, sep=',', encoding='utf-8')
  IdRemover()