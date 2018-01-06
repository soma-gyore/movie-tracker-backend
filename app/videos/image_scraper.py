import json
import urllib.request
import PTN

from bs4 import BeautifulSoup


class ImageScraper(object):
    @staticmethod
    def get_soup(url, header):
        return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')

    def get_first_hit(self, searched_text):
        title = PTN.parse(searched_text)['title']
        query = title.split()
        query = '+'.join(query)
        url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
        header = {'User-Agent':
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

        soup = self.get_soup(url, header)
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, _ = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            return link
