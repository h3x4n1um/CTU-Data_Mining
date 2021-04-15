from bs4 import BeautifulSoup, NavigableString, Tag

def textify(html_tag):
    if isinstance(html_tag, NavigableString):
        html_tag = html_tag.string.strip()
    elif isinstance(html_tag, Tag):
        html_tag = html_tag.text.strip()
    return html_tag

if __name__ == "__main__":
    with open("log_Da Nang_page_35.html", 'r', encoding="utf-8") as html_file:
        markup = html_file.read()
    soup = BeautifulSoup(markup, "lxml")
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

        # number of room
        number_of_rooms = hotel.find(class_="room_link").find("span").find("strong")
        if  number_of_rooms is not None:
            number_of_rooms = number_of_rooms.previous_sibling
            print("number_of_rooms:\t", number_of_rooms)
            print("number_of_rooms type:\t", type(number_of_rooms))

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

        hotel_info_dict["room_occupancy"] = occupancy
        print("occupancy:\t", occupancy)

        # hotel location features
        location_features = hotel.find(class_="pub_trans")
        if location_features is not None:
            print(location_features.prettify())
            location_features = location_features.find_all(class_="sr_card_address_line__dot-separator")
            hotel_location_features = []
            for feature in location_features:
                print("feature:\t", textify(feature))
                while textify(feature) == '':
                    feature = feature.next_sibling
                    print("feature:\t", textify(feature))
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