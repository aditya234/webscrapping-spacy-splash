import scrapy
from scrapy_splash import SplashRequest


class TokyoHotelSpier(scrapy.Spider):
    name = 'tokyo_hotels'
    page_counter = 0

    def start_requests(self):
        url = "https://www.tripadvisor.in/Hotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html"
        yield SplashRequest(url, self.parse,
                            args={'wait': 10, 'viewport': '1024x2480', 'timeout': 90,
                                  'resource_timeout': 20},
                            )

    def parse(self, response):
        # iterating through all hotels in a given page
        hotel_tiles = response.css("div.listItem")
        for hotel in hotel_tiles:
            next_page_route = hotel.css(".property_title::attr(href)").get()
            hotel_page = "https://www.tripadvisor.in/" + next_page_route
            if hotel_page is not None:
                yield response.follow(hotel_page, callback=self.parseHotelDetails)

        # going to another page through pagination
        page_count_str = "-oa" + str(TokyoHotelSpier.page_counter) if TokyoHotelSpier.page_counter > 0 else ''
        TokyoHotelSpier.page_counter += 30

        next_page = "https://www.tripadvisor.in/Hotels-g298184" + page_count_str + "-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html"
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseHotelDetails(self, response):
        item = {}
        item['hotel_name'] = response.css("#HEADING::text").get()
        # about tab
        about_tab = response.css("#ABOUT_TAB")
        # ratings and stuff
        items = about_tab.css("div.ui_column span::text").getall()

        if (items is not None) and (len(items) > 0):
            item['rating'] = items[0] if len(items) > 0 else None
            item['review_count'] = items[1] if len(items) > 1 else None
            item['hotel_rank'] = items[2] if len(items) > 2 else None

        item['amenities'] = about_tab.css('[data-test-target="amenity_text"]::text').getall()
        item['languages'] = about_tab.css(".ssr-init-26f .H::text").get()
        # commenting scraping of reviews because we don't need it as of
        # item['reviews'] = response.css(".H4 span::text").getall()
        item['hotel_class'] = response.css(".H~ .H::text").getall()
        item['price'] = response.css('.bookableOffer::attr(data-pernight)').get()
        item['best_price_source'] = response.css('.bookableOffer::attr(data-vendorname)').get()
        item['restraunts_nearby'] = response.css(".VyMdE::text").get()
        item['attractions_nearby'] = response.css(".eKwbS::text").get()
        item['good_for_walkers_out_of_100'] = response.css(".dfNPK::text").get()
        item['top_cuisines'] = response.css(".e:nth-child(2) .chXJi::text").getall()
        item['lat_long_link'] = response.css('#LOCATION .yYjkv::text').get()
        item['best_features_as_per_reviews'] = response.css('.bjRcr::text').getall()

        # get links to restaurants
        links = response.css('[class="seeNearby bBadB _R Mb S4 H3 b"]::attr(href)').getall()
        link_to_restaurants = "https://www.tripadvisor.in" + links[1] if len(links) > 1 else None
        link_to_tourist_attractions = "https://www.tripadvisor.in" + links[2] if len(links) > 2 else None

        if link_to_restaurants is not None:
            yield response.follow(link_to_restaurants,
                                  callback=self.parseRestaurants,
                                  meta={
                                      'items': item,
                                      'link_to_tourist_attractions': link_to_tourist_attractions
                                  }
                                )
        else:
            yield item

    def parseRestaurants(self, response):
        items = response.meta.get('items')
        restaurants_list = []

        restaurants = response.css('.near_listing')
        for restaurant in restaurants:
            restaurant_json = {}
            restaurant_json['name'] = restaurant.css('.location_name a::text').get()
            cusines = restaurant.css('.cuisine , .info-label+ span::text').getall()
            for index, cusine in enumerate(cusines):
                if '<a' in cusine:
                    cusines[index] = ''
            new_cusines = restaurant.css('[class ="item cuisine"]::text').getall()
            cusines.extend(new_cusines)
            restaurant_json['cusines'] = list(set(cusines))
            restaurant_json['reviews'] = restaurant.css('.more::text').get()
            restaurants_list.append(restaurant_json)

        items['restaurants'] = restaurants_list

        link_to_tourist_attractions = response.meta.get('link_to_tourist_attractions')
        if link_to_tourist_attractions is not None:
            yield response.follow(link_to_tourist_attractions,
                                  callback=self.parseAttractionsNearby,
                                  meta={
                                      'items': items,
                                  }
                                )
        else:
            yield items

    def parseAttractionsNearby(self, response):
        items = response.meta.get('items')
        yield items
