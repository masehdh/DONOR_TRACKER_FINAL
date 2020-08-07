from bs4 import BeautifulSoup
import requests
from csv import writer
import csv
import pandas as pd
import urllib
import os.path
import json
import pymongo
import datetime

#Donor tracker site is different, headings are not links...

country_links = {'United States':'https://www.state.gov/press-releases/?results=30&gotopage=&total_pages=204&coll_filter_year=&coll_filter_month=&coll_filter_speaker=&coll_filter_country=&coll_filter_release_type=&coll_filter_bureau=&coll_filter_program=&coll_filter_profession=','United States2':'https://www.usaid.gov/coronavirus/fact-sheets','United Kingdom':'https://www.gov.uk/search/news-and-communications?keywords=&organisations%5B%5D=department-for-international-development','European Commission':'https://ec.europa.eu/commission/presscorner/home/en?keywords=coronavirus&dotyp=0#news-block','Switzerland':'https://www.eda.admin.ch/deza/en/home/news/news.html','Sweden':'https://www.sida.se/English/how-we-work/our-fields-of-work/health/sidas-response-to-covid-19/','Germany':'http://www.bmz.de/en/press/aktuelleMeldungen/index.html','Ireland':'https://dfa.ie/news-and-media/press-releases/','Norway':'https://www.regjeringen.no/en/whatsnew/finn-aktuelt2/id2415244/?topic=2692388','Netherlands':'https://www.government.nl/ministries/ministry-of-foreign-affairs/news','France':'https://www.afd.fr/en/actualites/communique-de-presse?field_date_value=&field_date_value_1=&field_region_country_target_id=All&field_theme_target_id=All&items_per_page=20','Japan':'https://www.mofa.go.jp/press/release/index.html','Japan2':'https://www.jica.go.jp/COVID-19/en/index.html#LatestNews','Japan3':'https://www.jica.go.jp/english/news/press/2020/index.html','CEPI':'https://cepi.net/news/','donor_tracker': 'https://donortracker.org/policy-updates?page=0'}
mlat_links = {'OCHA':'https://fts.unocha.org/appeals/952/donors?order=total_funding&sort=desc', 'WHO':'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/donors-and-partners/funding', 'UN MPTF':'http://mptf.undp.org/reports/portfolio_grid?output_format=print&title=Contributors/Partners%20Contributions&portfolio=donor&filter_year_from=2020&filter_year_to=2022&filter_month_to=&filter_month_from=&filter_fund=COV00&columns=donor%2Ccommitment%2Cpayment%2Cdeposit_rate'}

covid_terms = ['Covid-19', 'covid-19', 'COVID-19', '€', '$', 'aid', 'coronavirus', 'Coronavirus', 'COVID19', 'Covid19', 'covid19', 'Covid', 'COVID', 'covid', 'donor', 'pledge', 'pledges']
names = ['United Kingdom', 'United States', 'Australia', 'Japan', 'European Commission', "European Commission's Humanitarian Aid and Civil Protection Department", 'Norway', 'Germany', 'France', 'Sweden', 'Italy', 'Netherlands', 'NORWAY', 'NETHERLANDS']

def search_term_scraper(dict_of_links, search_terms):
    potential_links = []
    for site,link in dict_of_links.items():
        res = requests.get(link)
        
        parsed_url = urllib.parse.urlparse(link)
        base_url = f'{parsed_url[0]}://{parsed_url[1]}'
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            list_of_links = soup.select('a')
            for item in list_of_links:
                if any(term in item.text for term in search_terms):
                    if 'http' in item['href']:
                        potential_links.append({'country': site, 'title': item.text.strip().split('\n')[0],'link': item['href']})
                    else:
                        relative_path = item['href']
                        complete_url = f'{base_url}{relative_path}'
                        potential_links.append({'country': site, 'title': item.text.strip().split('\n')[0],'link': complete_url})
        else:
            print(f'Error {res.status_code}: {link}')

    # with open('results.csv','a+', encoding = 'utf-8', newline= '') as csv_file:
    #     csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
    #     csv_writer.writeheader()
    #     for country in potential_links:
    #         csv_writer.writerow(country)
    return potential_links

def list_to_csvs(scraper_results):
    if not(os.path.isfile('results.csv')):
        with open('results.csv', 'w', newline = '') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
            csv_writer.writeheader()

    oldlinks = []
    oldlinks2 = []
    with open('results.csv', 'r', encoding = 'utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            oldlinks.append(row['link'])
            oldlinks2.append(row['link'])

    with open('new_results.csv', 'w', encoding = 'utf-8', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
        csv_writer.writeheader()
        for result in scraper_results:
            if result['link'] not in oldlinks:
                csv_writer.writerow(result)
                oldlinks.append(result['link'])

    with open('results.csv', 'a+', encoding = 'utf-8', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
        for result in scraper_results:
            if result['link'] not in oldlinks2:
                csv_writer.writerow(result)
                oldlinks2.append(result['link'])

def mlat_scraper(dict_of_links, list_of_countries, filename = 'multilat'):
  list_of_tables = []
  list_of_countries = [country.lower() for country in names]
  today = datetime.datetime.now()
  date = today.strftime("%m-%d-%y")
  filename = f"{filename}.xlsx"
  for mlat in dict_of_links:
    res = requests.get(dict_of_links[mlat])
    if res.status_code == 200:
      df_list = pd.read_html(res.text.replace('&nbsp;',' '), match = ' G')
      df_table = df_list[0].iloc[:,[0,1]]
      for index, row in df_table.iterrows():
        if type(row[1]) != int:
          try:
            row[1] = row[1].replace(" ","")
            row[1] = int(row[1].replace(",",""))
          except:
            row[1] = row[1]
        if type(row[0]) is not str:
          df_table = df_table.drop(index)
      df_series = df_table.copy().iloc[:,0]
      for index, donor in enumerate(df_series):
        if any(country in donor.lower() for country in list_of_countries):
          df_series[index] = True
        else:
          df_series[index] = False
      countries_table = df_table[df_series]
      countries_table = countries_table.sort_values(by = countries_table.columns[0])
      if not(os.path.exists(filename)):
        countries_table.to_excel(filename, sheet_name=f'{mlat}-{date}', index=False)
      else:
        with pd.ExcelWriter(filename, mode='a') as writer:
          countries_table.to_excel(writer, sheet_name=f'{mlat}-{date}', index=False)
    else:
      print(f'Error {res.status_code}')
  return countries_table


# def mlat_csv_maker(dataframe, filename='multilat'):
  # today = datetime.datetime.now()
  # date = today.strftime("%m-%d-%y")
  # filename = f"{filename}.xlsx"

  # if not(os.path.exists(filename)):
  #       dataframe.to_excel(filename, sheet_name=f'{mlat}-{date}', index=False)
  # else:
  #   with pd.ExcelWriter(filename, mode='a') as writer:
  #     dataframe.to_excel(writer, sheet_name=f'{mlat}-{date}', index=False)

def articles_to_db(list_of_dicts):
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["donortrackerdb"]
  mycol = mydb["article_results"]

  indb_list = []
  notindb_list = []

  for document in mycol.find():
    indb_list.append(document['link'])
  
  for item in list_of_dicts:
    if item['link'] not in indb_list:
      notindb_list.append(item)

  try:
    mycol.insert_many(notindb_list)
  except Exception as e:
    print(e)

# def mlat_to_db(


results = search_term_scraper(country_links, covid_terms)
list_to_csvs(results)
articles_to_db(results)
mlat_results = mlat_scraper(mlat_links, names)
# mlat_csv_maker(mlat_results)
