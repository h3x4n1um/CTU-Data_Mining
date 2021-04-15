from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import date, timedelta

import csv
import requests
import os.path

def textify(html_tag):
    if isinstance(html_tag, NavigableString):
        html_tag = html_tag.string.strip()
    elif isinstance(html_tag, Tag):
        html_tag = html_tag.text.strip()
    return html_tag

def booking_crawler(city_name):
    checkin = date.today()
    checkout = checkin+timedelta(days=1) # max: 30 days

    # here's a little lesson in trickery
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}

    r = requests.get(
        "https://www.booking.com/searchresults.html?"+
            "ss="                   +city_name+
            "&checkin_year="        +str(checkin.year)+
            "&checkin_month="       +str(checkin.month)+
            "&checkin_monthday="    +str(checkin.day)+
            "&checkout_year="       +str(checkout.year)+
            "&checkout_month="      +str(checkout.month)+
            "&checkout_monthday="   +str(checkout.day),
            #"&order=price"
        headers = header
    )

    cnt = 1
    next_page = True
    with open("Booking_"+city_name+"_crawler.csv", 'w', encoding="utf-8", newline='') as csvfile:
        crawl_writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "hotel_name",
                "hotel_address",
                "hotel_distance_center",
                "hotel_location_features",
                "hotel_room",
                "number_of_rooms",
                "room_occupancy",
                "hotel_star",
                "hotel_score",
                "hotel_score_title",
                "hotel_number_reviews",
                "hotel_price",
                "hotel_offer"
            ]
        )
        crawl_writer.writeheader()
        while next_page:
            soup = BeautifulSoup(r.content, "lxml")

            with open("log_"+city_name+"_page_"+str(cnt)+".html", 'w', encoding="utf-8") as log_file:
                log_file.write(str(soup.prettify()))

            list_hotels = soup.find_all(class_="sr_item")
            for hotel in list_hotels:
                
                hotel_info_dict = dict()

                # hotel name
                hotel_name = textify(hotel.find(class_="sr-hotel__name"))
                print(hotel_name)
                hotel_info_dict["hotel_name"] = hotel_name

                # hotel address and distance from center
                address_line = hotel.find(class_="sr_card_address_line")

                hotel_address = address_line.find('a')
                if hotel_address is not None:
                    hotel_address = ','.join(reversed(hotel_address["data-coords"].split(',')))
                print(hotel_address)
                hotel_info_dict["hotel_address"] = hotel_address

                hotel_distance_center = textify(address_line.find(attrs={"data-bui-component": "Tooltip"}))
                print(hotel_distance_center)
                hotel_info_dict["hotel_distance_center"] = hotel_distance_center

                # hotel room
                hotel_room = textify(hotel.find(class_="room_link").find("span").find("strong"))
                print(hotel_room)
                hotel_info_dict["hotel_room"] = hotel_room

                # number of room
                number_of_rooms = hotel.find(class_="room_link").find("span").find("strong")
                if  number_of_rooms is not None:
                    number_of_rooms = textify(number_of_rooms.previous_sibling)
                print(number_of_rooms)
                hotel_info_dict["number_of_rooms"] = number_of_rooms

                # room occupancy
                occupancies = hotel.find_all(class_="c-occupancy-icons__multiplier-number")
                
                if len(occupancies) > 0:
                    occupancy = 0
                    for occupancy_ele in occupancies:
                        occupancy_ele = textify(occupancy_ele)
                        
                        if occupancy_ele.isnumeric():
                            occupancy = occupancy + int(occupancy_ele)
                else:
                    occupancy = len(hotel.find_all(class_="bicon"))

                hotel_info_dict["room_occupancy"] = str(occupancy)
                print(occupancy)

                # hotel location features
                hotel_location_features = None

                location_features = hotel.find(class_="pub_trans")
                if location_features is not None:
                    hotel_location_features = []
                    location_features = location_features.find_all(class_="sr_card_address_line__dot-separator")

                    for feature in location_features:
                        while textify(feature) == '':
                            feature = feature.next_sibling
                        hotel_location_features.append(textify(feature))

                    hotel_location_features = ','.join(hotel_location_features)
                
                print(hotel_location_features)
                hotel_info_dict["hotel_location_features"] = hotel_location_features

                # hotel rating
                hotel_star = hotel.find(class_="bui-rating")
                if hotel_star is not None:
                    hotel_star = hotel_star["aria-label"]
                print(hotel_star)
                hotel_info_dict["hotel_star"]=hotel_star

                # hotel review score
                hotel_score = textify(hotel.find(class_="bui-review-score__badge"))
                print(hotel_score)
                hotel_info_dict["hotel_score"] = hotel_score

                # hotel score title
                hotel_score_title = textify(hotel.find(class_="bui-review-score__title"))
                print(hotel_score_title)
                hotel_info_dict["hotel_score_title"] = hotel_score_title

                # hotel number reviews
                hotel_number_reviews = textify(hotel.find(class_="bui-review-score__text"))
                print(hotel_number_reviews)
                hotel_info_dict["hotel_number_reviews"] = hotel_number_reviews

                # hotel price
                hotel_price = textify(hotel.find(class_="bui-price-display__value"))
                print(hotel_price)
                hotel_info_dict["hotel_price"] = hotel_price

                # hotel offer
                offers = hotel.find_all(class_="sr_room_reinforcement")
                hotel_offer = ','.join([textify(offer) for offer in offers])
                print(hotel_offer)
                hotel_info_dict["hotel_offer"] = hotel_offer

                print("-------------------------------------------------")

                crawl_writer.writerow(hotel_info_dict)

            next_page_link = soup.find('a', class_="paging-next")
            if next_page_link is None:
                next_page = False
            else:
                r = requests.get("https://booking.com"+next_page_link['href'], headers=header)
                cnt = cnt+1

if __name__ == "__main__":
    user_input = input("Input file path or city you want to crawl: ")
    if os.path.isfile(user_input):
        print("\nFound file {}, attempt to crawl cities in file\n".format(user_input))
        with open(user_input, 'r', encoding="utf-8") as input_file:
            city_name = input_file.readline().strip()
            while city_name:
                print(city_name)
                booking_crawler(city_name)
                city_name = input_file.readline().strip()
    else:
        print("\nNot found file {}, use as search query\n".format(user_input))
        city_name = user_input
        print(city_name)
        booking_crawler(city_name)
