from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import csv
import time

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url_USA = 'https://www.info-clipper.com/en/companies/united-states.us/groups.html'
url_UK='https://www.info-clipper.com/en/companies/united-kingdom.gb/groups.html'
url_Italia='https://www.info-clipper.com/en/companies/italy.it/groups.html'
url_Estonia='https://www.info-clipper.com/en/companies/estonia.ee/groups.html'


