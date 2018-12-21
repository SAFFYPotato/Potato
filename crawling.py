import re
import collections
import util
import urllib.request

from urllib import parse
from bs4 import BeautifulSoup

def tree(): return collections.defaultdict(tree)

def crawling_data_all():

    category_data = util.read_json('categoryData.json')
    region_data = category_data['region']

    naver_search_url = "https://search.naver.com/search.naver?"
    query_url = "where=nexearch&sm=tab_etc&query="
    query_option = "채소소매가"
    url = ''

    price_data = tree()
    crops = []
    units = []
    prices = []
    variances = []
    ratios = []

    for reg in region_data:
        url_decode = parse.urlparse(naver_search_url + query_url + reg + query_option)
        query = parse.parse_qs(url_decode.query)
        url_encode = parse.urlencode(query, doseq=True)
        url = naver_search_url + url_encode

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        for crop in soup.find_all("td", class_="first"):
            crop_temp = crop.get_text()
            crops.append(crop_temp)

        for td in soup.find_all("td", class_= ""):
            for unit in td.find_all(string=re.compile("\s/\s")):
                unit_temp = unit
                units.append(unit_temp)

        for price in soup.find_all("strong", class_={"up", "down", "stand"}):
            price_temp = int(price.get_text().replace(",", "").replace(" ", "").replace("원", ""))
            prices.append(price_temp)

        for variance in soup.find_all("span", class_={"up", "down", "stand"}):
            variance_temp = variance.get_text()
            variances.append(variance_temp)

        for ratio in soup.find_all("span", class_="percent"):
            ratio_temp = ratio.get_text()
            ratios.append(ratio_temp)

        for i in range(len(region_data)):
            for j in range(len(crops)):
                price_data[region_data[i]][crops[j]] = {'가격': prices[j],
                                                      '단위' : units[j],
                                                      '변동': variances[j],
                                                      '변동비': ratios[j]}

    #print(json.dumps(price_data, ensure_ascii=False))
    util.make_json(price_data, 'priceData.json')