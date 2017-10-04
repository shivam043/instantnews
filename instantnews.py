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


API_URL = "https://newsapi.org/register"
BASE_URL = "https://newsapi.org/v1/articles"
SOURCE_URL = "https://newsapi.org/v1/sources"
valid = ['y', 'n']
news_code = ['1', '2']
category_news = [
    'business', 'entertainment', 'gaming',
    'general', 'music', 'politics',
    'science-and-nature', 'sport', 'technology'
    ]


def test_network_connection():
    """Test network connection"""
    try:
        r = requests.get("https://newsapi.org/")
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("There was issue connecting to the server. Please check your network connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def fetch_all_news_code():
    """Fetch all news codes"""
    r = requests.get(SOURCE_URL)
    t = r.json()
    for i in t['sources']:
        news_code.append(i['id'])


def load_config_key():
    """Load api key on a global api key and validate it"""
    try:
        global apiKey
        apiKey = os.environ['IN_API_KEY']
        if len(apiKey) == 32:
            try:
                int(apiKey, 16)
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
    if l in category_news:
        flag = 1
    if flag == 0:
        print("Enter valid category")
        sys.exit(1)

    url = "?category={category_type}"
    r = requests.get((SOURCE_URL+url).format(category_type=l))
    t = r.json()
    for i in t['sources']:
        print(u"{0}: <{1}> {2}".format("News Code", i['id'], i['name']))


def show_sources_all():
    """Display all news codes"""
    r = requests.get(SOURCE_URL)
    t = r.json()
    for i in t['sources']:
        print(u"{0}: <{1}> {2}".format("News Code", i['id'], i['name']))


def show_news(l, BASE_URL):
    """Display news with respect to news id"""
    url = "?source={news_id}&apiKey="
    r = requests.get((BASE_URL+url+apiKey).format(news_id=l))
    t = r.json()
    list_news = []
    c = 0

    for i in t['articles']:
        print('[{0}] {1}: {2}'.format(c, "Title", i['title']))
        print('{0}: {1}'.format("Author", i['author']))
        print('{0}: {1}'.format("Summary", i['description']))
        print('--------------------------------------------')
        list_news.append(i['url'])
        c = c+1

    print("Want to see the news that interests you/open in a webpage? Enter Y/N ")

    choice = (input()).lower()
    while check_choice(choice):
        print("Ooops that was wrong,Try again!")
        choice = input("Enter (y/n): ").lower()

    if choice == 'y':
        while choice == 'y':
            news_code = input("Enter news code: ")
            while not news_code.isdigit() or not 0 <= int(news_code) <= c:
                print("Ooops that was wrong,Try again!")
                news_code = input("Pick One: ")

            webbrowser.open(list_news[int(news_code)])
            print("Want to exit? Enter Y/N ")
            choice = (input()).lower()
            if choice not in valid:
                sys.exit()

            if choice == 'n':
                choice = 'y'
                continue
            else:
                break


def parser():
    """Parse arguments and call appropriate functions"""
    fetch_all_news_code()
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
            if l in news_code:
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
