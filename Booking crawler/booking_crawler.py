from bs4 import BeautifulSoup
from datetime import date, timedelta

import csv
import requests

def textify(html_tag):
    if html_tag is not None:
            html_tag = html_tag.text.strip()
    return html_tag

if __name__ == "__main__":
    checkin = date.today()
    checkout = checkin+timedelta(days=1) # max: 30 days

    city_name = input("Input city you want to crawl: ")

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"} # here's a little lesson in trickery

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
        crawl_writer = csv.DictWriter(csvfile, fieldnames=["hotel_name", "hotel_address", "hotel_distance_center", "hotel_room", "hotel_star", "hotel_score", "hotel_score_title", "hotel_number_reviews", "hotel_price", "hotel_offer"])
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
                hotel_info_dict["hotel_name"]=hotel_name

                # hotel address and distance from center
                address_line = hotel.find(class_="sr_card_address_line")

                hotel_address = address_line.find('a')
                if hotel_address is not None:
                    hotel_address = ','.join(reversed(hotel_address["data-coords"].split(',')))
                print(hotel_address)
                hotel_info_dict["hotel_address"]=hotel_address

                hotel_distance_center = textify(address_line.find(attrs={"data-bui-component": "Tooltip"}))
                print(hotel_distance_center)
                hotel_info_dict["hotel_distance_center"]=hotel_distance_center

                # hotel room
                hotel_room = textify(hotel.find(class_="room_link").find("span").find("strong"))
                print(hotel_room)
                hotel_info_dict["hotel_room"]=hotel_room

                # hotel rating
                hotel_star = hotel.find(class_="bui-rating")
                if hotel_star is not None:
                    hotel_star = hotel_star["aria-label"]
                print(hotel_star)
                hotel_info_dict["hotel_star"]=hotel_star

                # hotel review score
                hotel_score = textify(hotel.find(class_="bui-review-score__badge"))
                print(hotel_score)
                hotel_info_dict["hotel_score"]=hotel_score

                # hotel score title
                hotel_score_title = textify(hotel.find(class_="bui-review-score__title"))
                print(hotel_score_title)
                hotel_info_dict["hotel_score_title"]=hotel_score_title

                # hotel number reviews
                hotel_number_reviews = textify(hotel.find(class_="bui-review-score__text"))
                print(hotel_number_reviews)
                hotel_info_dict["hotel_number_reviews"]=hotel_number_reviews

                # hotel price
                hotel_price = textify(hotel.find(class_="bui-price-display__value"))
                print(hotel_price)
                hotel_info_dict["hotel_price"]=hotel_price

                # hotel offer
                offers = hotel.find_all(class_="sr_room_reinforcement")
                hotel_offer = ','.join([textify(offer) for offer in offers])
                print(hotel_offer)
                hotel_info_dict["hotel_offer"]=hotel_offer

                print("-------------------------------------------------")

                crawl_writer.writerow(hotel_info_dict)

            next_page_link = soup.find('a', class_="paging-next")
            if next_page_link is None:
                next_page = False
            else:
                r = requests.get("https://booking.com"+next_page_link['href'], headers=header)
                cnt = cnt+1