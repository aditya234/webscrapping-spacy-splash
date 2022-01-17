import scrapy
from ..items import TripadvisorItem

class TripAdvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    start_urls = [
        "https://www.tripadvisor.in/Hotels-g294265-Singapore-Hotels.html"
    ]
    page_counter = 0

    def parse(self, response):
        item = TripadvisorItem()

        hotel_tiles = response.css("div.meta_listing")
        for hotel in hotel_tiles:
            item['hotel_name'] = hotel.css(".property_title::text").extract()
            item['price'] = hotel.css(".priceBlock .price::text").extract()
            item['features'] = hotel.css(".is-shown-at-tablet .text::text").extract()
            item['rating'] = hotel.css("a.bubble_45::attr(alt)").extract()
            item['review_count'] = hotel.css(".review_count::text").extract()
            item['comment'] = hotel.css(".popindex::text").extract()

            yield item

        page_count_str = "-oa" + str(TripAdvisorSpider.page_counter) if TripAdvisorSpider.page_counter > 0 else ''
        TripAdvisorSpider.page_counter += 30

        next_page = "https://www.tripadvisor.in/Hotels-g294265"+page_count_str+"-Singapore-Hotels.html"
        print(f"NEXT PAGE TO SCRAPE ---> {next_page}")
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)