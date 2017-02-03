import json
import os
import pickle
import re

import wikipedia
import wikipedia_utils

"""
AUTHOR_DATA:  author_name = key : books_dict = dictionary
books_dict:   book_title = key  : details_dict = dictionary
details_dict: keys are: publisher, isbn10, isbn13, image_link
"""

AUTHOR_DATA = dict()
SUCCESS_TRACK = dict()
FAILURE_TRACK = dict()
MODEL_AUTHOR_LIST = list()
MODEL_BOOKS_LIST = list()
MODEL_PUBLISHER_LIST = list()


def get_author_infobox(info_d):
    wanted_data_keys = ["birth_date", "occupation", "nationality", "website"]
    info_dict = dict()
    for k in wanted_data_keys:
        if k in info_d.keys():
            s = replace_whitespace(info_d[k])
            s = strip_wikimarkup(s)
            if k is "birth_date":
                info_dict["date_of_birth"] = s
            elif k is "website":
                info_dict["homepage_URL"] = s
            else:
                info_dict[k] = s
    if "image" in info_d:
        pub = wikipedia.page(name)
        if len(pub.images):
            info_dict["image"] = pub.images[0]
    return info_dict


def get_publisher_infobox(info_d, name):
    # wanted_data_keys = ["image", "founded", "founder", "status", "country"]
    info_dict = {"name": name, "image": 0, "year_founded": "", "founder": "", "status": "", "country": ""}

    if "image" in info_d:
        pub = wikipedia.page(name)
        if len(pub.images):
            info_dict["image"] = pub.images[0]
    elif "logo" in info_d:
        pub = wikipedia.page(name)
        if len(pub.images):
            info_dict["image"] = pub.images[0]
    if "founded" in info_d:
        s = replace_whitespace(info_d["founded"])
        match = re.match("(\d+)", s)
        if match:
            info_dict["year_founded"] = match.group(1)
    if "founder" in info_d:
        s = replace_whitespace(info_d["founder"])
        s = strip_wikimarkup(s)
        info_dict["founder"] = s
    if "status" in info_d:
        s = replace_whitespace(info_d["status"])
        s = strip_wikimarkup(s)
        info_dict["status"] = s
    if "country" in info_d:
        s = replace_whitespace(info_d["country"])
        s = strip_wikimarkup(s)
        info_dict["country"] = s

    # get other stuff next
    return info_dict


def store_author_table(name, date_of_birth="", occupation="", nationality="", homepage_url="", **d):
    mine = dict()
    mine["name"] = name
    mine["date_of_birth"] = date_of_birth
    mine["occupation"] = occupation
    mine["nationality"] = nationality
    mine["homepage_url"] = homepage_url
    MODEL_AUTHOR_LIST.append(mine)


def replace_whitespace(s):
    t = re.sub("\s+", " ", s)
    u = re.sub(r"\\n", "", t)
    u = re.sub(r"\<br(?: \/)?\>", ", ", u)
    return u


def strip_wikimarkup(s):
    s = re.sub("<!--.*?-->", "", s)

    match = re.match("{{[URLurl]+\|(.+)}}", s)
    if match:
        return strip_wikimarkup(match.group(1))

    match = re.match("{{[bB]irth [dD]ate(?:.*)\|(\d+)\|(\d+)\|(\d+).*}}", s)
    if match:
        d = match.group(1) + "-" + match.group(2) + "-" + match.group(3)
        return strip_wikimarkup(d)

    match = re.match("{{[bB]irth [yY]ear(?:.*)\|(\d+).*}}", s)
    if match:
        d = match.group(1) + "-01-01"
        return strip_wikimarkup(d)

    match = re.match("{{flatlist", s)
    if match:
        a = s.split("*")
        b = [re.sub("\{|\}|flatlist\||\[|\]", "", i.strip()) for i in a]
        t = ', '.join(b[1:])
        return t

    match = re.match("\[\[.*?\]\]", s)
    if match:
        t = re.sub("\[\[(?:.*?\|)?(.*?)\]\]", r"\1", s)
        return strip_wikimarkup(t)
    return s
    # match = re.match(regex, s)
    # if match:
    #     print(match.group(1))


def data_scrape_json(path):
    # print ("PATH: " + path)
    if os.path.exists(path):
        for d in os.listdir(path):
            if os.path.isdir(path + d):
                data_scrape_json(path + d + "/")
            else:
                scrap_json_helper(path + d)


def scrap_json_helper(file_path):
    week_data = None
    with open(file_path, 'r') as f:
        week_data = json.load(f)
    if week_data is None:
        return
    books_list = week_data["results"]["books"]

    for d in books_list:
        book_details = dict()
        books_dict = dict()
        book_title = d["title"]
        author_name = d["author"]
        if author_name in AUTHOR_DATA:
            books_dict = AUTHOR_DATA[author_name]
            if book_title in books_dict:
                continue
            else:
                pass  # author exists, but not book: add in book
        else:
            # author does not exist: add in author and book
            AUTHOR_DATA[author_name] = books_dict

        book_details["author"] = author_name
        book_details["image_link"] = d["book_image"]
        book_details["publisher"] = d["publisher"]
        book_details["isbn10"] = d["primary_isbn10"]
        book_details["isbn13"] = d["primary_isbn13"]
        book_details["description"] = d["description"]
        book_details["amazon_url"] = d["amazon_product_url"]
        books_dict[book_title] = book_details


def page_fail(s):
    FAILURE_TRACK[s] = 1


def page_success(s):
    SUCCESS_TRACK[s] = 1


def get_book_details(title):
    pass


def get_author_details(author_name):
    if author_name in SUCCESS_TRACK or author_name in FAILURE_TRACK:
        return 0
    val = wikipedia_utils.GetWikipediaPage(author_name)
    if val is None:
        page_fail(author_name)
        return -1
    res = wikipedia_utils.ParseTemplates(val["text"])
    if len(res["templates"]) == 0:
        page_fail(author_name)
        return -1

    infobox_class = ""
    for k in res["templates"]:
        assert len(k) == 2
        match = re.match("[iI]nfobox", k[0])
        if match:
            infobox_class = k[0]
            break
    if infobox_class is "":
        page_fail(author_name)
        return -1

    infobox = dict(res["templates"]).get(infobox_class)
    if infobox is None:
        page_fail(author_name)
        return -1
    else:
        # TODO: Parse through infobox!!!!
        this_data = get_author_infobox(infobox)
        this_data["name"] = author_name
        # this_data["book_list"] = list(AUTHOR_DATA[author_name].keys())
        store_author_table(**this_data)
        page_success(author_name)
        return 1


def get_publisher_details(pub_name):
    val = wikipedia_utils.GetWikipediaPage(pub_name)
    if val is None:
        return 101  # => No wikipage found
    res = wikipedia_utils.ParseTemplates(val["text"])
    if len(res["templates"]) == 0:
        return 102  # => No templates found on page
    infobox_class = ""
    for k in res["templates"]:
        assert len(k) == 2
        match = re.match("[iI]nfobox", k[0])
        if match:
            infobox_class = k[0]
            break
    if infobox_class is "":
        return 103  # => No infobox template found

    infobox = dict(res["templates"]).get(infobox_class)
    if infobox is None:
        return 104  # => Not sure, but something wrong
    else:
        this_data = get_publisher_infobox(infobox, pub_name)
        MODEL_PUBLISHER_LIST.append(this_data)
        return 0
        # pprint.pprint(this_data, indent=4)


def open_pickles(debug):
    if debug:
        with open("success.p", "rb") as f:
            global SUCCESS_TRACK
            SUCCESS_TRACK = pickle.load(f)
        with open("failure.p", "rb") as f:
            global FAILURE_TRACK
            FAILURE_TRACK = pickle.load(f)
        with open("authors_table.p", "rb") as f:
            global MODEL_AUTHOR_LIST
            MODEL_AUTHOR_LIST = pickle.load(f)
        with open("books_table.p", "rb") as f:
            global MODEL_BOOKS_LIST
            MODEL_BOOKS_LIST = pickle.load(f)


def write_pickles(debug):
    if debug:
        with open("author-data.p", "wb") as f:
            pickle.dump(AUTHOR_DATA, f)


def main():
    # Go through many json files, to get books titles and other data
    data_path = "../nytimes/data/fetched/"
    with open("author-data.p", "rb") as f:
            global AUTHOR_DATA
            AUTHOR_DATA = pickle.load(f)
    # data_scrape_json(data_path)
    # with open("author-data.p", "wb") as f:
    #     pickle.dump(AUTHOR_DATA, f)

    open_pickles(False)

    # details for books taken form nytimes; now get details for authors
    s_cnt = 0
    f_cnt = 0
    for author in AUTHOR_DATA:
        flag = get_author_details(author)
        if flag == 1:
            s_cnt += 1
        elif flag == -1:
            f_cnt += 1
        elif flag == 0:
            pass
        else:
            print
            "Unknown error"
            assert False

    # print("###################################")
    # print("Author Successes: " + str(s_cnt))
    # print("Author Failures:  " + str(f_cnt))
    # print("###################################")
    # with open("authors_table.p", "wb") as f:
    #     pickle.dump(MODEL_AUTHOR_LIST, f)
    # with open("success.p", "wb") as f:
    #     pickle.dump(SUCCESS_TRACK, f)
    # with open("failure.p", "wb") as f:
    #     pickle.dump(FAILURE_TRACK, f)

    # Create data table for books
    for author in AUTHOR_DATA.keys():
        # if author in SUCCESS_TRACK:
        for book_title in AUTHOR_DATA[author]:
            my_dict = dict()
            details = AUTHOR_DATA[author][book_title]
            my_dict["title"] = book_title
            my_dict["isbn"] = details["isbn13"]
            my_dict["written_by"] = details["author"]
            my_dict["publisher"] = details["publisher"]
            my_dict["image_link"] = details["image_link"]
            my_dict["description"] = details["description"]
            my_dict["amazon_url"] = details["amazon_url"]
            MODEL_BOOKS_LIST.append(my_dict)

    # with open("publisher-list.txt") as f:
    #     pub_to_wikipage = json.load(f)
    #     temp = dict()
    #     s_cnt, f_cnt = (0, 0)
    #     for p in pub_to_wikipage.keys():
    #         if pub_to_wikipage[p]:
    #             temp[pub_to_wikipage[p]] = 1
    #     for title in temp.keys():
    #         flag = get_publisher_details(title)
    #         if flag == 0:
    #             s_cnt += 1
    #         elif flag > 100:
    #             f_cnt += 1
    #         else:
    #             print
    #             "Unknown error"
    #             assert False
    #     # replace book's publisher
    #     for book in MODEL_BOOKS_LIST:
    #         p = book["publisher"]
    #         np = pub_to_wikipage[p]
    #         np = re.sub(" ?\(.+\)", "", np)
    #         book["publisher"] = np

    # print("###################################")
    # print("Publisher Successes: " + str(s_cnt))
    # print("Publisher Failures:  " + str(f_cnt))
    # print("###################################")

    # with open("publisher_table.p", "wb") as f:
    #     pickle.dump(MODEL_PUBLISHER_LIST, f)
    with open("books_table.p", "wb") as f:
        pickle.dump(MODEL_BOOKS_LIST, f)


if __name__ == "__main__":
    main()

# /w/api.php?action=query&format=json&prop=revisions&titles=Modern_Romance%3A_An_Investigation&rvprop=content

# TODO: Store data as a pickle file
# TODO: dictionary, where COLUMNS are keys
# TODO: try to get AUTHORS and BOOKS
