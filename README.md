#Yeu cau cai dat:
sudo apt-get install libmysqlclient-dev python-dev

- pip install -r requirements.txt
- ChromeDriver dung version, download driver path in https://chromedriver.storage.googleapis.com/index.html

#ChromeDriver hien tai dang dung:
./chromedriver --version
ChromeDriver 75.0.3770.8

#RUN
python url_iframe.py

List domain  -> output_domain.txt
Filter: cat output_domain.txt |sort|uniq|less

Config:
- change path:  driver.get('https://vtv.vn/video/vtv-news/cong-nghe.htm')



for url in `cat output.txt | sort|grep -v javascript|uniq |grep -v mailto`;do echo  $url;curl -I $url;done

