import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from datetime import datetime
import pymongo
import config
import pprint



def scrap_internshala(data_dict: dict, db_name):
    for name, url in data_dict.items():
        dbConn = pymongo.MongoClient(config.MONGO_CLIENT)
        db = dbConn[str(db_name)]
        table = db[name]
        url = url

        uClient = urlopen(url)
        internshala_page = uClient.read()
        uClient.close()

        page_beautify = bs4(internshala_page, "html.parser")

        total_no_pages = page_beautify.find("span", {"id":"total_pages"}).text

        try:
            for i in range(1, int(total_no_pages)+1):
                next_url = url+"/page-"+str(i)

                next_page_content = requests.get(next_url)
                beautify_nextPage = bs4(next_page_content.text, "html.parser")
                big_boxes = beautify_nextPage.find_all("div", {"class":"individual_internship"})

                for box in big_boxes:
                    try:
                        now = datetime.now()
                        date_time = now.strftime("%Y-%m-%d")
                    except :
                        date_time = None

                    try:
                        profile = box.find("div", {"class":"profile"}).a.text.strip().replace("\n", "")
                    except:
                        profile = None

                    try:
                        urls = box.find("div", {"class":"profile"}).a['href']
                        urls = "https://internshala.com/" + str(urls)
                    except:
                        urls = None

                    try:
                        company = box.find("div", {"class":"company_name"}).a.text.strip().replace("\n", "")
                    except :
                        company = None
                    
                    try:
                        location = box.find("a", {"class":"location_link"}).text.strip().replace("\n", "")
                    except:
                        location = None

                    try:
                        start_date = box.find("span", {"class":"start_immediately_desktop"}).text.strip().replace("\n", "")
                    except:
                        start_date = None

                    try:
                        stipend = box.find("span", {"class":"stipend"}).text.strip().replace("\n", "")
                    except:
                        stipend = None

                    try:
                        duration_row = box.find_all("div", {"class":"other_detail_item"})
                        duration = duration_row[1].find("div", {"class":"item_body"}).text.strip().replace("\n", "")
                    except:
                        duration = None

                    try:
                        apply_by = box.find("div", {"class":"apply_by"})
                        apply_by_date = apply_by.find("div", {"class":"item_body"}).text.strip().replace("\n", "")
                    except:
                        apply_by_date = None

                    try:
                        offer = box.find("div", {"class":"label_container label_container_mobile"}).text.strip().replace("\n", "")
                    except :
                        offer = None


                    myDict = {
                        "Date Time":date_time,
                        "url": urls,
                        "profile":profile, 
                        "company":company,
                        "Location":location,
                        "Start Date":start_date,
                        "Stipend":stipend,
                        'Duration':duration,
                        'Apply by Date':apply_by_date,
                        "Offer":offer
                        }

                    filters = {
                        "profile":profile,
                        "Location":location,
                        "company":company,
                    }
                    x = table.update_one(filters, {"$set":myDict}, upsert=True)
                    # x = table.insert_one(myDict, upsert=True)
        except Exception as e:
            print(e)
            print("Next")

    return table


# def scrap_indeed(data_dict: dict, db_name):
#     for name, url in data_dict.items():
#         dbConn = pymongo.MongoClient("mongodb://localhost:27017/")
#         db = dbConn[str(db_name)]
#         table = db[name]
#         url = url

#         uClient = urlopen(url)
#         indeed_page = uClient.read()
#         uClient.close()

#         page_beautify = bs4(indeed_page, "html.parser")

#         total_no_pages = page_beautify.find("div", {"id":"searchCountPages"}).text
#         try:
#             total_jobs = int(total_no_pages.strip().split()[3])
#             total_no_pages = (total_jobs // 15) - 5
#         except Exception as e:
#             print(e)

#         try:
#             for i in range(0, total_no_pages):
#                 next_url = url+"&start="+str(i)+"0"
#                 next_page_content = requests.get(next_url)
#                 beautify_nextPage = bs4(next_page_content.text, "html.parser")
#                 big_boxes = beautify_nextPage.find_all("div", {"class":"jobsearch-SerpJobCard"})
                
#                 for box in big_boxes:
#                     try:
#                         now = datetime.now()
#                         date_time = now.strftime("%Y-%m-%d")
#                     except :
#                         date_time = None

#                     try:
#                         profile = box.find("h2", {"class":"title"}).a.text.strip().replace("\n", "")
#                     except:
#                         profile = None
                    
#                     try:
#                         urls = box.find("h2", {"class":"title"}).a['href']
#                         urls = "https://in.indeed.com" + str(urls)
#                     except:
#                         urls = None

#                     try:
#                         company = box.find("span", {"class":"company"}).a.text.strip().replace("\n", "")
#                     except :
#                         company = None

#                     try:
#                         location_n_rating = box.find("div", {"class":"sjcl"}).div.text.strip().replace("\n", "")
#                         location = location_n_rating[:-3]
#                         rating = location_n_rating[-3:]
#                         location_n_rating = location + " " + rating

#                     except:
#                         location_n_rating = None

#                     try:
#                         date = box.find("span", {"class":"date"}).text.strip()
#                     except:
#                         date = None

#                     try:
#                         requirement = []
#                         reqs = box.find_all("div", {"class":"jobCardReqItem"})
#                         for req in reqs:
#                             a = req.text
#                             requirement.append(a)
#                     except:
#                         requirement = None

#                     myDict = {
#                         "Date Time":date_time,
#                         "url": urls,
#                         "profile":profile, 
#                         "company":company,
#                         "Location_n_rating":location_n_rating,
#                         "date":date,
#                     }

#                     filters = {
#                         "profile":profile,
#                         "Location_n_rating":location_n_rating,
#                         "company":company,
#                     }
#                     x = table.update_one(filters, {"$set":myDict}, upsert=True)
#                     # x = table.insert_one(myDict, upsert=True)
#         except Exception as e:
#             print(e)
#             print("Next")

# if __name__ == '__main__':
#     now = datetime.now()
#     date_time = now.strftime("%Y-%m-%d")
#     table = scrap_internshala(config.internshala_data_dict, config.INTERNSHALA_DB)
#     for post in table.find({"Date Time": date_time}):
#         pprint.pprint(post)
    # scrap_indeed(config.indeed_data_dict, config.INDEED_DB)
    
