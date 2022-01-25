class Restaurant:
    def __init__(self,data):
        self.name = data['name'] if 'name' in data else None
        self.cusines = data['cusines'] if 'cusines' in data else None
        self.total_reviews = []
        if ('reviews' in data) and data['reviews']:
            data_list = data['reviews'].split()
            self.total_reviews = int((data_list[0]).replace(',','')) if len(data_list)>0 else None

class Hotel:
    def __init__(self,data, city = ''):
        self.city = city
        self.name = data['hotel_name'] if 'hotel_name' in data else None

        self.rating = (float(data['rating']) if data['rating'] and data['rating'].isnumeric() else None) if 'rating' in data else None
        
        self.review_count = None
        if ('review_count' in data) and data['review_count']:
            data_list= data['review_count'].split()
            self.review_count = int(data_list[0]) if len(data_list)>0 and data_list[0].isnumeric() else None
            
        self.hotel_rank = None
        if ('hotel_rank' in data) and data['hotel_rank']:
            data_list = data['hotel_rank'].split()
            self.hotel_rank = int(data_list[0][1:]) if len(data_list)>0 and data_list[0].isnumeric() else None
        
        self.total_hotels = []
        if ('hotel_rank' in data) and data['hotel_rank']:
            data_list = data['hotel_rank'].split()
            self.total_hotels = int(data_list[2]) if len(data_list)>2 and data_list[2].isnumeric() else None
            
        self.best_price = (int(data['price']) if data['price'] else None) if 'price' in data else None
        self.restaurants_nearby = int(data['restraunts_nearby']) if ('restraunts_nearby' in data and data['restraunts_nearby'])  else None
        self.attractions_nearby = int(data['attractions_nearby']) if ('attractions_nearby' in data and data['attractions_nearby']) else None
        self.good_for_walkers_out_of_100 = int(data['good_for_walkers_out_of_100']) if ('good_for_walkers_out_of_100' in data and data['good_for_walkers_out_of_100']) else None
        
        self.amenities = data['amenities'] if 'amenities' in data else None
        self.languages = (data['languages'].split(", ") if data['languages'] else None) if 'languages' in data else None
        self.hotel_classes = data['hotel_class'] if 'hotel_class' in data else None
        self.best_price_source = data['best_price_source'] if 'best_price_source' in data else None
        self.top_cuisines = data['top_cuisines'] if 'top_cuisines' in data else None
        self.restaurants = []
        if ('restaurants' in data) and data['restaurants']:
            for restaurant in data['restaurants']:
                self.restaurants.append(Restaurant(restaurant))
                

class HotelList:
    def __init__(self):
        self.hotels = []
        self.filter_hotels_list = []
        
    def add_city_data(self, json_data, city):
        for hotel in json_data:
            self.hotels.append(Hotel(data = hotel, city= city))
        self.filter_hotels_list = self.hotels[:] #copying list by value
            
    def getHotels(self, cities, min_rating, max_hotel_price, cuisine, 
                  min_nearby_places, min_nearby_resturants, min_total_reviews, 
                  amenities_list, languages, hotel_classes):
        self.filter_hotels_list = []
        # filter loop 
        for hotel in self.hotels:
            if hotel.