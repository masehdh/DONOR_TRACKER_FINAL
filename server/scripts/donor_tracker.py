from bs4 import BeautifulSoup
import requests
from csv import writer
import csv
import urllib
import os.path
import pymongo

article_links = {'US1':'https://www.state.gov/press-releases/?results=30&gotopage=&total_pages=204&coll_filter_year=&coll_filter_month=&coll_filter_speaker=&coll_filter_country=&coll_filter_release_type=&coll_filter_bureau=&coll_filter_program=&coll_filter_profession=','US2':'https://www.usaid.gov/coronavirus/fact-sheets','UK':'https://www.gov.uk/search/news-and-communications?keywords=&organisations%5B%5D=department-for-international-development','EU':'https://ec.europa.eu/commission/presscorner/home/en?keywords=coronavirus&dotyp=0#news-block','Switzerland':'https://www.eda.admin.ch/deza/en/home/news/news.html','Sweden':'https://www.sida.se/English/how-we-work/our-fields-of-work/health/sidas-response-to-covid-19/','Germany':'http://www.bmz.de/en/press/aktuelleMeldungen/index.html','Ireland':'https://dfa.ie/news-and-media/press-releases/','Norway':'https://www.regjeringen.no/en/whatsnew/finn-aktuelt2/id2415244/?topic=2692388','Netherlands':'https://www.government.nl/ministries/ministry-of-foreign-affairs/news','France':'https://www.afd.fr/en/actualites/communique-de-presse?field_date_value=&field_date_value_1=&field_region_country_target_id=All&field_theme_target_id=All&items_per_page=20','Japan1':'https://www.mofa.go.jp/press/release/index.html','Japan2':'https://www.jica.go.jp/COVID-19/en/index.html#LatestNews', 'donor_tracker': 'https://donortracker.org/policy-updates?page=0', 'CEPI':'https://cepi.net/news/'}


covid_terms = ['Briefing', 'European', '€']

def article_scraper(search_terms, dict_of_links):
    potential_links = []
    for country, url in dict_of_links.items():
        res = requests.get(url)
        parsed_url = urllib.parse.urlparse(url)
        base_url = f'{parsed_url[0]}://{parsed_url[1]}'

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')

            list_of_links = soup.select('a')

            for link in list_of_links:
                if any(term in link.text for term in search_terms):
                    if 'http' in link['href']:
                        potential_links.append(
                            {
                                'country': country,
                                # for title, we get rid of unecessary white spaces, and only take the first line
                                'title': link.text.strip().split('\n')[0],
                                'link' : link['href']
                            }
                        )
                    else:
                        relative_path = link['href']
                        complete_url = f'{base_url}{relative_path}'
                        potential_links.append(
                            {
                                'country': country,
                                # for title, we get rid of unecessary white spaces, and only take the first line
                                'title': link.text.strip().split('\n')[0],
                                'link' : complete_url
                            }
                        )
        else:
            print(f'Error {res.status_code}: {url}')
    print("Search complete ...")
    return potential_links

def article_csv_maker(list_of_dicts):

    if not(os.path.exists('results.csv')):
        with open('results.csv', 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
            csv_writer.writeheader()

    # Read results.csv, store all of the links contained in a list
    oldlinks = []
    oldlinks2 = []
    with open('results.csv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            oldlinks.append(row['link'])
            oldlinks2.append(row['link'])


    # Write new-results.csv which only contains
    with open('new-results.csv','w', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
        csv_writer.writeheader()
        for result in list_of_dicts:
            if result['link'] not in oldlinks:
                csv_writer.writerow(result)
                oldlinks.append(result['link'])

    # Write a csv file containing results
    with open('results.csv','a+', newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = ['country', 'title', 'link'])
        for result in list_of_dicts:
            if not(result['link'] in oldlinks2):
                csv_writer.writerow(result)
                oldlinks2.append(result['link'])
    print("Results store in CSV files")

def store_to_db(list_of_dicts):
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    mydb = myclient["donortrackerdb"]
    mycol = mydb["article_results"]

    indb_list = []
    notindb_list = []

    for document in mycol.find():
        indb_list.append(document['link'])

    for item in list_of_dicts:
        if item['link'] not in indb_list:
            notindb_list.append(item)

    print(notindb_list)

    try:
        mycol.insert_many(notindb_list)
    except Exception as err:
        print(err)

# Store results (potential_links) of the article_scraper function in a variable, accepts search terms, and urls to search
results = article_scraper(covid_terms, article_links)
store_to_db(results)

# Stores the results (a list of dictionaries) into 2 csvs, one master list (results.csv) and one that only contains new results (new-results.csv)
# article_csv_maker(results)

