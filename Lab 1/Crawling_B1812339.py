import requests
import csv
from bs4 import BeautifulSoup



# circumvent anti-bot
headers = {
    "User-Agent": "Mozilla/5.0"
}

cnt = int(input("Input number of pages you want to crawl: "))

with open("Crawling_B1812339.csv", 'w', encoding="utf-8", newline='') as csvfile:
    crawl_writer = csv.DictWriter(csvfile, fieldnames=['', "country", "description", "designation", "points", "price", "province", "region_1", "region_2", "taster_name", "taster_twitter_handle", "title", "variety", "winery"])
    crawl_writer.writeheader()

    # index
    index = 0
    taster_twitter_handle_dict = dict()
    
    for c in range(1, cnt+1):
        response = requests.get("https://www.winemag.com/?s=&drink_type=wine&page="+str(c)+"&search_type=reviews", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        wine_table = soup.find("section", id="search-results")
        #print(wine_table)

        wine_list = wine_table.find_all('a', class_="review-listing")
        #print(wine_list)

        for wine_ele in wine_list:
            wine_page = requests.get(wine_ele.get("href"), headers=headers)
            wine_soup = BeautifulSoup(wine_page.content, "html.parser")

            wine_info_dict = dict()

            # index
            wine_info_dict[''] = index

            # title
            title = wine_soup.h1.get_text()
            #print(title)
            wine_info_dict["title"] = title

            # review-gate
            review_gate = wine_soup.find("div", id="review-gate")

            desc_n_taster = review_gate.find('p', class_="description")
            desc_n_taster_gen = desc_n_taster.stripped_strings

            # description
            description = next(desc_n_taster_gen)
            #print(description)
            wine_info_dict["description"] = description
                
            # taster_name
            taster_name = next(desc_n_taster_gen)
            #print(taster_name)
            wine_info_dict["taster_name"] = taster_name
            

            # taster_link
            taster_link = desc_n_taster.span.a.get("href")

            # taster_twitter_handle
            if taster_name not in taster_twitter_handle_dict:
                taster_page = requests.get(taster_link, headers=headers)
                taster_soup = BeautifulSoup(taster_page.content, "html.parser")
                twitter_handle = taster_soup.find("li", class_="twitter").get_text()
                taster_twitter_handle_dict[taster_name] = twitter_handle

            taster_twitter_handle = taster_twitter_handle_dict.get(taster_name)
            #print(taster_twitter_handle)
            wine_info_dict["taster_twitter_handle"] = taster_twitter_handle

            # primary-info
            primary_info = review_gate.find("ul", class_="primary-info")

            for primary_info_ele in primary_info.find_all("li"):
                info_label = primary_info_ele.find("div", class_="info-label").stripped_strings
                info_label = next(info_label).lower()

                info = primary_info_ele.find("div", class_="info")
                # change raing to points
                if info_label == "rating":
                    info_label = "points"
                    info = int(next(info.stripped_strings))
                    wine_info_dict[info_label] = info
                # remove $ and , in price
                elif info_label == "price":
                    info = next(info.stripped_strings).replace(',', '').replace('$', '')
                    if info.isnumeric():
                        info = int(info)
                        wine_info_dict[info_label] = info
                # split appellation into country, province, region_1 and region_2
                elif info_label == "appellation":
                    region_list = list(reversed(info.get_text().split(',')))
                    for i in range(len(region_list)):
                        region_list[i] = region_list[i].strip()
                        if i == 0:
                            wine_info_dict["country"] = region_list[i]
                        elif i == 1:
                            wine_info_dict["province"] = region_list[i]
                        elif i == 2:
                            wine_info_dict["region_1"] = region_list[i]
                        else:
                            wine_info_dict["region_2"] = region_list[i]
                    
                else:
                    info = next(info.stripped_strings)
                    wine_info_dict[info_label] = info

            print(wine_info_dict)

            # write csv
            crawl_writer.writerow(wine_info_dict)

            index = index + 1