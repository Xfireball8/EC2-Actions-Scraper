FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY app ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy","crawl","actionsscraper", "-o",  "./res/res.json"]
