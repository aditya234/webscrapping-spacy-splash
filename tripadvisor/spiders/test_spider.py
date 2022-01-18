import scrapy
from scrapy_splash import SplashRequest


class SingaporeHotelSpier(scrapy.Spider):
    name = 'test'
    page_counter = 0

    def start_requests(self):
        url = "https://www.tripadvisor.in/Hotel_Review-g294265-d301803-Reviews-Sheraton_Towers_Singapore-Singapore.html"
        yield SplashRequest(url, self.parse,
                            args={'wait': 1, 'viewport': '1024x2480', 'timeout': 90, 'images': 0,
                                  'resource_timeout': 20},
                            )

    def parse(self, response):
        # iterating through all hotels in a given page
        hotel_name = response.css("#HEADING::text").get()
        covid_safety = response.css("ul li span.ctpJG").extract()

        yield {
            'name':hotel_name,
            'covid':covid_safety
        }
