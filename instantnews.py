#!/usr/bin/env python
import requests
import argparse
import webbrowser
from colored import fg,bg,attr
import sys
import os

API_URL="https://newsapi.org/register"
BASE_URL="https://newsapi.org/v1/articles"
SOURCE_URL="https://newsapi.org/v1/sources"
valid=['y','n']

def load_config_key():
    global apiKey
    try:
        apiKey=os.environ['IN_API_KEY']
        if len(apiKey)==32:
            try:
                int(apiKey,16)
            except ValueError:
                print("Invalid API key")
    
    except KeyError:
        print('No API Token detected. '
              'Please visit {0} and get an API Token, '
              'which will be used by Soccer CLI '
              'to get access to the data.'
             .format(API_URL))

def check_choice(choice):
    
    if len(choice)>1:
        return True
    
    if choice=="y" or choice=="n":
        return False

def show_sources_category(l):
    url="?category={category_type}"
    r=requests.get((SOURCE_URL+url).format(category_type=l))
    t=r.json()
    for i in t['sources']:
        print(((u"{0}:%s <{1}> %s%s{2}%s".format("Channel Code",i['id'],i['name'])))%(fg(1),attr(0),fg(3),attr(0)))

def show_sources_all():
    r=requests.get(SOURCE_URL)
    t=r.json()
    for i in t['sources']:
        print(((u"{0}:%s <{1}> %s%s{2}%s".format("Channel Code",i['id'],i['name'])))%(fg(1),attr(0),fg(3),attr(0)))

def show_news(l,BASE_URL):
    
    url="?source={news_id}&apiKey="
    if not apiKey:
        print('No API Token detected. '
              'Please visit {0} and get an API Token, '
              'which will be used by Soccer CLI '
              'to get access to the data.'
             .format(API_URL))
    
    r=requests.get((BASE_URL+url+apiKey).format(news_id=l))
    t=r.json()
    list_news=[]
    c=0
    
    for i in t['articles']:
        print(('%s [{0}] {1}: {2} %s'.format(c,"Title",i['title']))%(fg(3),attr(0)))
        print((('%s {0}: {1} %s'.format("Author",i['author'])))%(fg(5),attr(0)))
        print((('%s {0}: {1} %s'.format("Summary",i['description'])))%(fg(1),attr(0)))
        print('--------------------------------------------')
        list_news.append(i['url'])
        c=c+1
    
    print("Want to see the news that interests you/open in a webpage? Enter Y/N ")    
    
    choice=(input()).lower()
    while check_choice(choice):
          print("Ooops that was wrong,Try again!")
          choice=input("Enter (y/n): ").lower()

    
    if choice=='y':
        
        while choice=='y':
            
            news_code=input("Enter news code: ")
            while not(news_code.isdigit()) or not (0<=int(news_code)<=c):
                print("Ooops that was wrong,Try again!")
                news_code=input("Pick One: ")
            
            webbrowser.open(list_news[int(news_code)])
            print("Want to exit? Enter Y/N ")
            choice=(input()).lower()
            if choice not in valid:
               sys.exit()

            if choice=='n':
                choice='y'
                continue
            else:
                break
def parser():
    
    if not sys.argv[1:]:
        print("Arguments needed Type in --help/-h for help")
    else:
        load_config_key()
        parser=argparse.ArgumentParser()
    
    
        parser.add_argument("--show","-s",action="store",help="Shows all the channel codes category wise")
        parser.add_argument("--show_all","-sa",action="store_true",help="Shows all the channel codes")
        parser.add_argument("--news","-n",type=str,help="Shows news")
    
    
        args=parser.parse_args()
    
    
        if args.show_all:
            show_sources_all()
    
        elif args.show:
            show_sources_category(args.show)
   
        elif args.news:
            show_news(args.news,BASE_URL)   
    


def main():
    
    parser()

   
if __name__ == "__main__":
    main()    
