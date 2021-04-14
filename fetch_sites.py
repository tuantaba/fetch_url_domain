from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import html5lib
from urlparse import urlparse
from mysql.connector import MySQLConnection, Error 
from mysql_dbconfig import read_db_config
import os
import logging

logging.basicConfig(filename='app.log',level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def sql_insert(domain, url_crawler, subdomain, suburl):
#    print "domain is" + domain
#    print  "url_crawler is" + str(url_crawler)
#    print "subdomain is" +  str(subdomain)
#    print "suburl is" + str(suburl)
    query = "INSERT INTO domain(domain, url_crawler, subdomain, suburl) " \
            "VALUES(%s,%s,%s,%s)"
    args = (str(domain), str(url_crawler), str(subdomain), str(suburl))
    try:
        db_config=read_db_config()
        conn=None
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
            logging.info('last insert id' + str(cursor.lastrowid))
        else:
            print('last insert id not found')
            logging.error('Error: ' + str(domain) + str(e))

        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def fetch_domain_url(domain, url_crawler):
    if not os.path.exists(domain):
        os.makedirs(domain)
    #download driver path in https://chromedriver.storage.googleapis.com/index.html
    #refer: https://selenium-python.readthedocs.io/
    RAWOUTPUT_FILE = open(domain + "/urls_draw.txt","w")
    DOMAIN_FILE = open(domain + "/domain.txt", "w")
    URL_FILTER_FILE = open(domain + "/urls_filtered.txt", "w")

    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')

    driver_path = './chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
    driver.implicitly_wait(10)

    #driver.get('https://vtv.vn/video/vtv-news/giai-tri.htm')
    driver.get(url_crawler)
    try:
    #    time.sleep(1)
        iframe = driver.find_elements_by_tag_name('iframe')

        print ("length with iframe is", len(iframe))
        for i in range(0, len(iframe)):
            frame = driver.find_elements_by_tag_name('iframe')[i]
            print  ("frame is", frame)
            attr = frame.get_attribute('src')
            print attr
            RAWOUTPUT_FILE.write("%s\n" % attr)
            driver.switch_to.frame(frame)
            driver.switch_to_default_content()

    #Get href from a tags
        links = driver.find_elements_by_tag_name('a')
        for j in range(0, len(links)):
            link = driver.find_elements_by_tag_name('a')[j].get_attribute('href')
            print link

            RAWOUTPUT_FILE.write("%s\n" % link)              

        print ("scripting...")        
    #Get src from  script tags
        scripts = driver.find_elements_by_tag_name('script')
        for k in range(0, len(scripts)):
            script = driver.find_elements_by_tag_name('script')[k].get_attribute('src')
            print script

            RAWOUTPUT_FILE.write("%s\n" % script)      
        RAWOUTPUT_FILE.close()
    except:
        driver.quit();

    url_filtered = []
    domain_list = []

    try:
        FILEOPEN=open(domain + "/urls_draw.txt","r")
        urls = FILEOPEN.readlines()
        for each_url in urls:
#            print each_url
            if len(each_url.strip()) != 0 and "javascript" not in each_url and each_url not in url_filtered:

                url_filtered.append(each_url.strip())
                url_parsed = urlparse(each_url)
                #Write to domain file and domain_list variable
                if url_parsed.netloc not in domain_list:
                    DOMAIN_FILE.write("%s \r\n" % url_parsed.netloc )
                    domain_list.append(url_parsed.netloc)

        FILEOPEN.close()
    except Exception as e:
        print e

    return domain, url_crawler, domain_list, url_filtered
    
if  __name__ == '__main__':
    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("vtv.vn", "https://vtv.vn/truyen-hinh-truc-tuyen.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "VTV run error", e
        logging.error('Error: VTV run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("lotus.vn", "https://lotus.vn/w")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "Lotus run error", e
        logging.error('Error: Lotus run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("tuoitre.vn", "https://tuoitre.vn/thoi-su.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "Tuoitre run error", e
        logging.error('Error: Tuoitre run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("kenh14.vn", "https://kenh14.vn/star.chn")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "Kenh14 run error", e
        logging.error('Error: Kenh14 run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("nld.com.vn", "https://nld.com.vn/thoi-su.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "nld.com.vn run error", e
        logging.error('Error: nld.com.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("toquoc.vn", "http://toquoc.vn/thoi-su.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "Toquoc.vn run error", e
        logging.error('Error: Toquoc.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("soha.vn", "https://soha.vn/thoi-su.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "soha.vn run error", e
        logging.error('Error: soha.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("cafebiz.vn", "https://cafebiz.vn/thoi-su.chn")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "Cafebiz.vn run error", e
        logging.error('Error: Cafebiz.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("cafef.vn", "https://cafef.vn/thoi-su.chn")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "cafef.vn run error", e
        logging.error('Error: cafef.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("ictvietnam.vn", "https://ictvietnam.vn/tieu-diem.htm")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "ictvietnam.vn run error", e
        logging.error('Error: ictvietnam.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("autopro.com.vn", "https://autopro.com.vn/tin-tuc.chn")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "autopro.com.vn run error", e
        logging.error('Error: autopro.com.vn run' + str(e))

    try:
        domain, url_crawler, subdomain, suburl= fetch_domain_url("linkhay.com", "https://linkhay.com/link/stream/hot")
        sql_insert(domain, url_crawler, subdomain, suburl)
    except Exception as e:
        print "linkhay.com run error", e
        logging.error('Error: linkhay.com run' + str(e))
