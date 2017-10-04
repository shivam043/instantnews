#!/usr/bin/env python
"""
Author:Shivam Singh
mail:shivam043@gmail.com
copyright@2017
"""


import os
import sys
import argparse
import webbrowser
import requests


# Global constants
API_URL = "https://newsapi.org/register"
BASE_URL = "https://newsapi.org/v1/articles"
SOURCE_URL = "https://newsapi.org/v1/sources"
VALID = ['y', 'n']
NEWS_CATEGORIES = [
    'business', 'entertainment', 'gaming',
    'general', 'music', 'politics',
    'science-and-nature', 'sport', 'technology'
    ]


# Global variable
news_codes = ['1', '2']
api_key = ""


def test_network_connection():
    """Test network connection"""
    try:
        response = requests.get("https://newsapi.org/")
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("There was issue connecting to the server. Please check your network connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def fetch_all_news_codes():
    """Fetch news codes from all sources"""
    response = requests.get(SOURCE_URL)
    json = response.json()
    global news_codes
    for source in json['sources']:
        news_codes.append(source['id'])


def load_config_key():
    """Load api key on a global api key and validate it"""
    try:
        global api_key
        api_key = os.environ['IN_API_KEY']
        if len(api_key) == 32:
            try:
                int(api_key, 16)
            except ValueError:
                print("Invalid API key")
    except KeyError:
        print('No API Token detected. '
              'Please visit {0} and get an API Token, '
              'which will be used by instantnews '
              'to get access to the data.'
              .format(API_URL))
        sys.exit(1)


def check_choice(choice):
    """Validate choice for yes or no"""
    if len(choice) > 1:
        return True
    if choice == "y" or choice == "n":
        return False


def show_sources_category(l):
    """Display news codes by category"""
    flag = 0
    if l in NEWS_CATEGORIES:
        flag = 1
    if flag == 0:
        print("Enter valid category")
        sys.exit(1)

    url = "?category={category_type}"
    response = requests.get((SOURCE_URL+url).format(category_type=l))
    json = response.json()
    for code in json['sources']:
        print(u"{0}: <{1}> {2}".format("News Code", code['id'], code['name']))


def show_sources_all():
    """Display all news codes"""
    response = requests.get(SOURCE_URL)
    json = response.json()
    for code in json['sources']:
        print(u"{0}: <{1}> {2}".format("News Code", code['id'], code['name']))


def show_news(l, BASE_URL):
    """Display news with respect to news id"""
    url = "?source={news_id}&apiKey="
    response = requests.get((BASE_URL+url+api_key).format(news_id=l))
    json = response.json()
    list_news = []
    c = 0

    for code in json['articles']:
        print('[{0}] {1}: {2}'.format(c, "Title", code['title']))
        print('{0}: {1}'.format("Author", code['author']))
        print('{0}: {1}'.format("Summary", code['description']))
        print('--------------------------------------------')
        list_news.append(code['url'])
        c = c+1

    print("Want to see the news that interests you/open in a webpage? Enter Y/N ")

    choice = (input()).lower()
    while check_choice(choice):
        print("Ooops that was wrong,Try again!")
        choice = input("Enter (y/n): ").lower()

    if choice == 'y':
        while choice == 'y':
            news_codes = input("Enter news code: ")
            while not news_codes.isdigit() or not 0 <= int(news_codes) <= c:
                print("Ooops that was wrong,Try again!")
                news_codes = input("Pick One: ")

            webbrowser.open(list_news[int(news_codes)])
            print("Want to exit? Enter Y/N ")
            choice = (input()).lower()
            if choice not in VALID:
                sys.exit()

            if choice == 'n':
                choice = 'y'
                continue
            else:
                break


def parser():
    """Parse arguments and call appropriate functions"""
    fetch_all_news_codes()
    load_config_key()

    if not sys.argv[1:]:
        print("Arguments need Type in --help/-h for help")
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--show", "-s", action="store",
                            help="Shows all the news channel codes category wise")
        parser.add_argument("--show_all", "-sa", action="store_true",
                            help="Shows all the news channel codes")
        parser.add_argument("--news", "-n", type=str, help="Shows news")
        args = parser.parse_args()

        if args.show_all:
            show_sources_all()
        elif args.show:
            show_sources_category(args.show)
        elif args.news:
            flag = 0
            l = args.news
            if l in news_codes:
                flag = 1
            if flag == 0:
                print("Enter valid newscode")
                sys.exit(1)
            show_news(args.news, BASE_URL)


def main():
    """Test network connection, then parse arguments"""
    test_network_connection()
    parser()


if __name__ == "__main__":
    main()
