# -*- coding: utf-8 -*-

from datetime import date, timedelta

import csv
import json
import os
import requests
import uuid


def rand_uuid() -> str:
    return str(uuid.uuid4())


def get_response_json(r):
    res = None
    try:
        res = r.json()
    except json.JSONDecodeError:
        res = dict()
    return res


def write_json(js, file_path) -> None:
    # create dir b4 write
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding="utf-8") as json_file:
        json.dump(js, json_file, ensure_ascii=False, indent=4, sort_keys=True)


def booking_api(dest_name: str) -> None:
    # set request fields
    arrival_date    = (date.today()+timedelta(days=1)).strftime("%Y-%m-%d")
    departure_date  = (date.today()+timedelta(days=2)).strftime("%Y-%m-%d")

    # set header fields
    headers = {
        "User-Agent":       "Booking.App",
        "Authorization":    "Basic dGhlc2FpbnRzYnY6ZGdDVnlhcXZCeGdN"
    }

    # get dest_id from autocomplete
    find_dest_id_querry = requests.get(
        "https://iphone-xml.booking.com/json/mobile.autocomplete?"+
            "device_id="                    +rand_uuid()+
            "&user_version=27.1.1-android"  +
            "&text="                        +dest_name,
        headers=headers)
    dest_json = get_response_json(find_dest_id_querry)

    # dest_id, search_type
    dest_id = None
    search_type = None
    for cnt in dest_json:
        if cnt["dest_type"] == "city" or cnt["dest_type"] == "region":
            search_type = cnt["dest_type"]
            dest_id = cnt["dest_id"]
            dest_name = cnt["name"].strip()
            break

    # can't find city
    if dest_id is None:
        print("Error! Can't find city!!!")
        return
    
    # found city
    print("dest_name:\t{}\ndest_id:\t{}\nsearch_type:\t{}".format(dest_name, dest_id, search_type))

    write_json(dest_json, os.path.join("log", dest_name, "city_json.json"))

    # open csv file for write data
    csv_file = open('-'.join(["booking_api", dest_name])+".csv",
                    'w',
                    encoding="utf-8",
                    newline='')
    fieldnames = [
        # extract from search_json
        "hotel_id",
        "accommodation_type_name",
        "hotel_name",
        "address",
        "class",
        "review_nr",
        "review_score",
        "is_city_center",
        "latitude",
        "longitude",
        # extract from activity_json
        "activity",
        "room_service",
        "spa",
        "pool",
        # extract from hotel_json
        "price",
        "currency",
        "room_name",
        "room_count",
        "max_occupancy",
        "view",
        "refundable",
        "breakfast_included",
        "half_board",
        "free_parking"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    hotel_ids = set()
    cnt = 0
    stop_search = False
    previous_hotel_size, current_hotel_size = 0, 0
    while not stop_search:
        # search using dest_id
        offset = str(cnt*20)
        search_querry = requests.get(
            "https://iphone-xml.booking.com/json/mobile.searchResults?"+
                "device_id="                    +rand_uuid()+
                "&user_version=27.1.1-android"  +
                "&arrival_date="                +arrival_date+
                "&departure_date="              +departure_date+
                "&search_type="                 +search_type+
                "&dest_ids="                    +dest_id+
                "&offset="                      +offset,
            headers=headers)
        search_json = get_response_json(search_querry)
        write_json(search_json, os.path.join("log", dest_name, "search_json", '-'.join([dest_id, str(cnt)])+".json"))

        for result in search_json["result"]:
            # hotel_id
            hotel_ids.add(str(result["hotel_id"]))
            print("hotel_id:\t{}".format(result["hotel_id"]))

            # crawl activity data using hotel_id
            activity_querry = requests.get(
                "https://iphone-xml.booking.com/json/bookings.getHotelFacilities?"+
                    "device_id="                    +rand_uuid()+
                    "&user_version=27.1.1-android"  +
                    "&hotel_ids="                   +str(result["hotel_id"])+
                    "&use_new_code=1",
                headers=headers)
            activity_json = get_response_json(activity_querry)
            write_json(activity_json, os.path.join("log", dest_name, "activities", str(result["hotel_id"])+".json"))

            # activity, room_service, spa, pool
            activity = set()
            room_service = 0
            spa = 0
            pool = 0
            for activity_ele in activity_json:
                if activity_ele["facilitytype_name"] == "Activities":
                    activity.add(activity_ele["facility_name"])

                    if activity_ele["facilitytype_name"] == "Room service":
                        room_service = 1

                    if activity_ele["facilitytype_name"].lower().find("spa") != -1:
                        spa = 1

                    if activity_ele["facilitytype_name"].lower().find("pool") != -1:
                        pool = 1

            # extract data from result and activity
            hotel_info = {
                "hotel_id":                 result["hotel_id"],
                "accommodation_type_name":  result["accommodation_type_name"],
                "hotel_name":               result["hotel_name"],
                "address":                  result["address"],
                "class":                    result["class"],
                "review_nr":                result["review_nr"],
                "review_score":             result["review_score"],
                "is_city_center":           result["is_city_center"],
                "latitude":                 result["latitude"],
                "longitude":                result["longitude"],
                "activity":                 ", ".join(activity),
                "room_service":             room_service,
                "spa":                      spa,
                "pool":                     pool
            }

            # crawl hotel data from hotel_id
            hotel_querry = requests.get(
                "https://iphone-xml.booking.com/json/mobile.hotelPage?"+
                    "hotel_id="                     +str(result["hotel_id"])+
                    "&device_id="                   +rand_uuid()+
                    "&user_version=27.1.1-android"  +
                    "&arrival_date="                +arrival_date+
                    "&departure_date="              +departure_date,
                headers = headers)
            hotel_json = get_response_json(hotel_querry)
            write_json(hotel_json, os.path.join("log", dest_name, "hotels", str(result["hotel_id"])+".json"))

            # free parking
            free_parking = 0
            for top_ufi_benefits_json in hotel_json[0]["top_ufi_benefits"]:
                if top_ufi_benefits_json["icon"] == "icon_parkingfee":
                    free_parking = 1
            hotel_info["free_parking"] = free_parking

            for hotel_room_json in hotel_json[0]["block"]:
                # template from hotel_info
                hotel_room_info = hotel_info

                # iew
                view = set()
                for facilities in hotel_room_json["block_text"]["facilities"]:
                    if facilities.lower().find(" view") != -1:
                        view.add(facilities)

                # extract data from hotel_room_json
                hotel_room_info.update({
                    "price":                hotel_room_json["min_price"]["price"],
                    "currency":             hotel_room_json["min_price"]["currency"],
                    "room_name":            hotel_room_json["room_name"],
                    "room_count":           hotel_room_json["room_count"],
                    "max_occupancy":        hotel_room_json["max_occupancy"],
                    "view":                 ", ".join(view),
                    "refundable":           hotel_room_json["refundable"],
                    "breakfast_included":   hotel_room_json["breakfast_included"],
                    "half_board":           hotel_room_json["half_board"]
                })

                # write hotel_room_info to csv
                csv_writer.writerow(hotel_room_info)
        
        previous_hotel_size, current_hotel_size = current_hotel_size, len(hotel_ids)

        # if result not change then stop
        if previous_hotel_size == current_hotel_size:
            stop_search = True
        else:
            cnt = cnt + 1

    # number of hotels had been crawled
    print("hotel_ids size:\t{}".format(len(hotel_ids)))

    # close csv file
    csv_file.close()

if __name__ == "__main__":
    user_input = input("Input file path or city you want to crawl: ")
    if os.path.isfile(user_input):
        print("\nFound file {}, attempt to read and crawl cities in file\n".format(user_input))
        with open(user_input, 'r', encoding="utf-8") as input_file:
            dest_name = input_file.readline().strip()
            while dest_name:
                booking_api(dest_name)
                dest_name = input_file.readline().strip()
                print("-------------------------")
    else:
        print("\nNot found file {}, use as search query\n".format(user_input))
        dest_name = user_input
        booking_api(dest_name)