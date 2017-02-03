import json
import os
import pickle
import re
import pprint

import wikipedia
import wikipedia_utils

DEBUG = False
NYT_BOOKS_LIST = list()
SUCCESS_BOOKS = dict()

def open_pickle(fname):
    obj = None
    if os.path.isfile(fname):
        with open(fname, "rb") as f:
            print("Loading " + fname)
            obj = pickle.load(f)
            print("Loaded.")
    else:
        print "File not found."
    return obj

def write_pickle(fname, obj):
    with open(fname, "wb") as f:
        print("Writing pickle file...")
        pickle.dump(obj, f)
        print("Wrote to " + fname)

def scrape_all_nyt_json(path):
    # print ("PATH: " + path)
    if os.path.exists(path):
        for d in os.listdir(path):
            if os.path.isdir(path + d):
                scrape_all_nyt_json(path + d + "/")
            else:
                scrape_one_nyt_json(path + d)

def scrape_one_nyt_json(file_path):
    week_data = None
    with open(file_path, 'r') as f:
        week_data = json.load(f)
    if week_data is None:
        return
    books_list = week_data["results"]["books"]
    for book in books_list:
        NYT_BOOKS_LIST.append(book)

def make_book_row(book_data):
    result_row = dict()
    try:
        result_row["title"] = book_data["title"]
        result_row["author"] = book_data["author"]
        result_row["image_link"] = book_data["book_image"]
        result_row["publisher"] = book_data["publisher"]
        result_row["isbn"] = book_data["primary_isbn13"]
        result_row["written_by"] = book_data["author"]
        result_row["description"] = book_data["description"]
        result_row["amazon_url"] = book_data["amazon_product_url"]
        return result_row
    except Exception as e:
        print(e)
        return None

def populate_books_table(b=False):
    pass

def get_publishers_details(pub_name):
    val = wikipedia_utils.GetWikipediaPage(pub_name)
    if val is None:
        return None  # => No wikipage found
    res = wikipedia_utils.ParseTemplates(val["text"])
    if len(res["templates"]) == 0:
        return None  # => No templates found on page
    infobox_class = ""
    for k in res["templates"]:
        assert len(k) == 2
        match = re.match("[iI]nfobox", k[0])
        if match:
            infobox_class = k[0]
            break
    if infobox_class is "":
        return None  # => No infobox template found

    infobox = dict(res["templates"]).get(infobox_class)
    if infobox is None:
        return None  # => Not sure, but something wrong
    else:
        this_data = get_publisher_infobox(infobox, pub_name)
        return this_data

def get_publisher_infobox(infobox, pub_name):
    info_dict = {"name": "", "image": "", "year_founded": "", "founder": "", "status": "", "country": ""}
   
    pn = re.sub("\(.+\)$", "", pub_name)
    info_dict["name"] = pn

    if "image" in infobox:
        pub = wikipedia.page(pub_name)
        if len(pub.images):
            info_dict["image"] = pub.images[0]
    elif "logo" in infobox:
        pub = wikipedia.page(pub_name)
        if len(pub.images):
            info_dict["image"] = pub.images[0]
    if "founded" in infobox:
        s = clean_text(infobox["founded"])
        match = re.match("(\d+)", s)
        if match:
            info_dict["year_founded"] = match.group(1)
    if "founder" in infobox:
        s = clean_text(infobox["founder"])
        # s = strip_wikimarkup(s)
        info_dict["founder"] = s
    if "status" in infobox:
        s = clean_text(infobox["status"])
        # s = strip_wikimarkup(s)
        info_dict["status"] = s
    if "country" in infobox:
        s = clean_text(infobox["country"])
        # s = strip_wikimarkup(s)
        info_dict["country"] = s

    # get other stuff next
    return info_dict

def get_author_details(author_name):
    val = wikipedia_utils.GetWikipediaPage(author_name)
    if val is None:
        return None  # => No wikipage found
    res = wikipedia_utils.ParseTemplates(val["text"])
    if len(res["templates"]) == 0:
        return None  # => No templates found on page
    infobox_class = ""
    for k in res["templates"]:
        assert len(k) == 2
        match = re.match("[iI]nfobox", k[0])
        if match:
            infobox_class = k[0]
            break
    if infobox_class is "":
        return None  # => No infobox template found

    infobox = dict(res["templates"]).get(infobox_class)
    if infobox is None:
        return None  # => Not sure, but something wrong
    else:
        this_data = get_author_infobox(infobox, author_name)
        return this_data

def get_author_infobox(infobox, author_name):
    wanted_data_keys = ["birth_date", "occupation", "nationality", "website"]
    info_d = {"name": author_name, "date_of_birth": "", "occupation":"", "nationality":"", "homepage_url":"", "image":""}
    if "image" in infobox:
        a = wikipedia.page(author_name)
        if len(a.images):
            info_d["image"] = a.images[0]
    if "birth_date" in infobox:
        s = clean_text(infobox["birth_date"])
        info_d["date_of_birth"] = s
    if "occupation" in infobox:
        s = clean_text(infobox["occupation"])
        info_d["occupation"] = s
    if "nationality" in infobox:
        s = clean_text(infobox["nationality"])
        info_d["nationality"] = s
    if "website" in infobox:
        s = clean_text(infobox["website"])
        info_d["homepage_url"] = s
    return info_d

def clean_text(s):
    t = re.sub("\s+", " ", s)
    t = re.sub(r"\\n", "", t)
    t = re.sub("<!--.*?-->", "", t)
    t = re.sub("\<ref\>.+?\<\/ref\>", "", t)
    t = re.sub("\[\[(?:.*?\|)?(.*?)\]\]", r"\1", t)
    t = re.sub(r"\<br(?: \/)?\>", ", ", t)
    return t

def test_debug(debug=False):
    if debug:
        pass
        # print "Number of books in NYT json files" + str(len(NYT_BOOKS_LIST))

        # key_count = dict()
        # for b in NYT_BOOKS_LIST:
        #     for k in b.keys():
        #         if k not in key_count:
        #             key_count[k] = 1
        #         else:
        #             key_count[k] += 1
        # for k in key_count.keys():
        #     print(str(k) +"\t\t" + str(key_count[k]))

def scrape():
    # data paths
    nyt_json_files = "../nytimes/data/fetched/"
    nyt_pfile = "./new_p/nyt_list.p"
    books_pfile = "./new_p/books_table.p"

    # JSON Files
    # Go through these to get NYTIMES BOOKS
    # BOOKS will also have other data in there
    # as well as AUTHORS and PUBLISHERS associated
    # with them
    global NYT_BOOKS_LIST
    load_no_write = True
    if load_no_write:
        NYT_BOOKS_LIST = open_pickle(nyt_pfile)
    else:
        scrape_all_nyt_json(nyt_json_files)
        write_pickle(nyt_pfile, NYT_BOOKS_LIST)
    # NYT_BOOKS_LIST is now filled with data
    # Take that data, and make it look like a table
    load_no_write = True
    table_books = list()
    book_set = dict()
    authors_set = dict()

    # TODO: move to populate_books_table?
    if load_no_write:
        table_books = open_pickle(books_pfile)
        authors_set = open_pickle("./new_p/tmp_authors_set.p")
    else:
        for nyt_book in NYT_BOOKS_LIST:
            row = make_book_row(nyt_book)
            title = row["title"]
            author_name = row["written_by"]
            if row is not None and title not in book_set and author_name != "":
                table_books.append(row)
                book_set[title] = 1
                if author_name != "":
                    if author_name in authors_set:
                        authors_set[author_name] += 1
                    else:
                        authors_set[author_name] = 1

        ### Save later, as we will edit likely publishers
        # write_pickle(books_pfile, table_books)

    print("Number of books: "   + str(len(table_books)))
    print("Number of authors: " + str(len(authors_set.keys()))) 

    ### PUBLISHERS are given by NYT is bad
    ### Cannot search through them easily
    ### publishers_list.txt has an INCOMPLETE
    ### mapping of pubs given to good wiki pub pages

    with open("data/publisher-list.txt", "r") as f:
        pub_to_wikipage = json.load(f)
        for b in table_books:
            p = b["publisher"]
            if p in pub_to_wikipage:
                val = pub_to_wikipage[p]
                pn = re.sub("\(.+\)$", "", val)
                b["publisher"] = pn
            else:
                pass
                # table_books.remove(b)
        print("# of books after unknown publishers removed" + str(len(table_books)))

    write_pickle("./new_p/update_books_table.p", table_books)

        ### Get info for publishers
        # publisher_success_set = dict()
        # publisher_table = list()
        # for op in pub_to_wikipage.keys():
        #     val = pub_to_wikipage[op]
        #     if val not in publisher_success_set:
        #         info_d = get_publishers_details(val)
        #         if info_d is not None:
        #             publisher_table.append(info_d)
        #             publisher_success_set[info_d["name"]] = 1
        # print "# of publishers: " + str(len(publisher_table))
        # write_pickle("./new_p/publisher_table.p", publisher_table)

    # Authors are probably good but some of them won't have
    # wiki pages or their wiki pages are bad
    # If that's the case, we'll through out that author
    # and their books

    ### tmp_authors_set is a dict with author_name as key,
    ### number of books written as value
    # write_pickle("./new_p/tmp_authors_set.p", authors_set)
    author_success_set = dict()
    table_authors = list()
    for a in authors_set.keys():
        try:
            if a not in author_success_set:
                info_d = get_author_details(a)
                if info_d is not None:
                    table_authors.append(info_d)
                    author_success_set[info_d["name"]] = 1
        except IndexError as e:
            pass
        except KeyError as h:
            pass

    write_pickle("./new_p/tmp_authors_table.p", table_authors)
    # write_pickle(books_pfile, table_books)


    # TODO: If UnicodeEncodeError exists...just drop author?
    # Junot Diaz is one issue

    # TODO: Authors may have 'and', 'with', or commas

    test_debug(DEBUG)

if __name__ == "__main__":
    scrape()