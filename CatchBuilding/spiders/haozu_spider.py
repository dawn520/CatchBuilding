import scrapy


class HaozuSpider(scrapy.spiders.Spider):
    name = "haozu"
    allowed_domains = ["haozu.com"]
    start_urls = [
        "http://f.haozu.com/building/detail/?building_id=4859__house%2Fdetail11624951171020012123166215211867959004"
        "&cryp=eyJjaXR5X2lkIjoiMTciLCJkZXZpY2VJZCI6ImIzNWQ5ZDUwZjBkMzFmNjQiLCJwbGF0Zm9ybSI6IkFuZHJvaWQiLCJhcGlWZXJzaW9"
        "uIjoiMS4wLjAiLCJhcHBWZXJzaW9uIjoiMS4wIn0%253D"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
