from bs4 import BeautifulSoup
from string import punctuation, maketrans
from generate import JSON_Writer
import fnmatch 
import sys,os
import pickle 

class Wrapper(object):
    """Manual Wrapper - to extract required fields from webpages"""

    def __init__(self, number_of_files):
        super(Wrapper, self).__init__()

        self.n = number_of_files

        # List of dicts to store extracted key,value pairs 
        self.extractions = [] 

        # to_extract - decided after experimentation 
        self.to_extract = set({'url','name','brand','color','measurements','likes','item','fabric', 'washlook', 'size'})

        self.price = set({'price', 'reduced_price'})

        # self.helper = Wrapper2()

    def raw(self, text):
        text = text.encode("ascii","ignore")
        return text.translate(maketrans("",""),punctuation).strip().lower()

    def extract(self, dirpath):
        for i in range(self.n):
            # print "Processing File : " + str(i) + ".html"
            soup = BeautifulSoup(open(dirpath+str(i)+".html"), "lxml")
            data = {} 

            tags = soup.find("div", class_ = "content clearfix")
            
            if tags:
                price = soup.find("div", class_ = "item-price-original-list")
                if price:
                    data['price'] = price.find("span").getText()
                    reduced = soup.find("div", class_ = "item-price reduced")
                    if reduced:
                        data['reduced_price'] = reduced.getText().split(":")[1].strip("\n").strip()
                else:
                    price = soup.find("div", class_ = "item-price")
                    if price:
                        data['price'] = price.getText().split(":")[1].strip()

                url = soup.find("meta", property = "og:url")
                data['url'] = url['content']

                # url = soup.find("link", rel = "canonical")
                # data['url'] = url['href']

                metas = tags.findAll("meta")

                for meta in metas:
                    field = meta['itemprop']
                    value = meta['content']
                    if field in self.to_extract and value:
                        data[field] = meta['content']

                loves = soup.find("div", class_ = "idp-love")
                if loves:
                    data['likes'] = loves.find("p").getText()

                details = soup.find("div", class_ = "item-details-content").findAll("div", class_= "row")
                # print details 
                for row in details:
                    pair = row.findAll("p")
                    key, value = self.raw(pair[0].getText()), pair[1].getText()
                    if key in self.to_extract and value:
                        data[key] = value 

                if data.keys():
                    self.extractions.append(data)
            else:
                print "Empty File : " + str(i) + ".html" 
                # self.helper.extract(soup)

    def validate(self):
        flag = True
        for x in self.extractions:
            for y in x.keys():
                if not x[y]:
                    print y, x[y] 
                    flag = False 
        return flag 

def dump(list_, filename):
    f = open(filename,"w+")
    pickle.dump(list_, f)
    f.close()

def count(dirpath):
    return len(fnmatch.filter(os.listdir(dirpath), '*.html'))

def write(filename):
    writer = JSON_Writer()
    writer.write(filename, "../extractions.json")

def main(dirpath, override):

    if override:
        number_of_files = count(dirpath)
        wrapper = Wrapper(number_of_files)
        wrapper.extract(dirpath)

        # Push the dump only if keys have non null values 
        if wrapper.validate():
            dump(wrapper.extractions, "dump")

    write("dump")

if __name__ == '__main__':

    dirpath = sys.argv[1]
    # Run wrapper again only if override is 1 
    override = int(sys.argv[2])

    main(dirpath, override)

""" 
Future work - different source schema 
class Wrapper2(object):
    def __init__(self):
        super(Wrapper2, self).__init__()
        
    def extract(self, soup):
        tags = soup.findAll("div", class_ = "item-body")
        if tags:
            for tag in tags:
                info = tag.findAll("p")
                print info[0].attrs
                exit()
        print len(tags)
        exit()
"""