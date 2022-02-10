from nis import cat
from unicodedata import category
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as trading
import os, json, datetime
from dotenv import load_dotenv
from markupsafe import re
from item_template import get_item
from optparse import OptionParser

load_dotenv()
EBAY_PRD_TOKEN = os.getenv('EBAY_PRD_TOKEN')
EBAY_PRD_APP_ID = os.getenv('EBAY_PRD_APP_ID')
EBAY_PRD_DEV_ID = os.getenv('EBAY_PRD_DEV_ID')
EBAY_PRD_CERT_ID = os.getenv('EBAY_PRD_CERT_ID')

def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")

    parser.add_option("-n", "--domain",
                      dest="domain", default='api.ebay.com',
                      help="Specifies the eBay domain to use (e.g. api.sandbox.ebay.com).")
    
    parser.add_option("-a", "--action",
                      dest="action", default='get_all_categories',
                      help="""Specifies action:
                      get_all_categories [CategorySiteID][LevelLimit]
                      get_category_specific_fields [CategoryID]
                      list_item (set item fields in item_template.py)
                      test_list_item (set item fields in item_template.py)
                      """)

    (opts, args) = parser.parse_args()
    return opts, args

def save_log(log_type, data):
    filepath = "./logs/{}_{}.json".format(log_type, datetime.datetime.now().strftime("%m_%d_%Y-%H_%M_%S"))
    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Complet exucution log: ", filepath)

def get_all_categories(api, args):
    category_site_id = 2
    levellimit = 4

    if len(args) == 2:
        category_site_id = args[0]
        levellimit = args[1]
    elif len(args) == 1:
        category_site_id = args[0]
    print("Running GetCategories eBay request. With params:")
    print(" DetailLevel: ReturnAll")
    print(" CategorySiteID: ", category_site_id)
    print(" LevelLimit': ", levellimit)

    response = api.execute("GetCategories", {'DetailLevel': 'ReturnAll',
                                             'CategorySiteID': category_site_id,
                                             'LevelLimit': levellimit})
    your_json = response.json()
    parsed = json.loads(your_json)
    save_log("get_all_categories", parsed)

def get_category_specific_fields(api, args):
    category_id = 607
    if len(args) == 1:
        category_id = args[0]

    print("Running GetCategorySpecifics eBay request. With params:")
    print(" CategoryID: ", category_id)

    response = api.execute("GetCategorySpecifics", {"CategoryID": category_id})
    your_json = response.json()
    parsed = json.loads(your_json)
    save_log("get_category_specific_fields", parsed)

def list_item(api):
    item = get_item()
    print("Running AddItem eBay request. With item_template")

    response = api.execute("AddItem", item)
    your_json = response.json()
    parsed = json.loads(your_json)
    save_log("get_item", parsed)

def test_list_item(api):
    item = get_item()
    print("Running VerifyAddItem eBay request. With item_template")

    response = api.execute("VerifyAddItem", item)
    your_json = response.json()
    parsed = json.loads(your_json)
    save_log("test_list_item", parsed)

if __name__ == "__main__":
    (opts, args) = init_options()

    try:
        api = trading(domain=opts.domain, appid=EBAY_PRD_APP_ID, devid=EBAY_PRD_DEV_ID,  certid=EBAY_PRD_CERT_ID,
                    token=EBAY_PRD_TOKEN, config_file=None)
        if opts.action == "get_all_categories":
            get_all_categories(api, args)
        elif opts.action == "get_category_specific_fields":
            get_category_specific_fields(api, args)
        elif opts.action == "list_item":
            list_item(api)
        elif opts.action == "test_list_item":
            test_list_item(api)
        else:
            print("Select valid action (use --help, to find more actions)")

    except ConnectionError as e:
        print(e)
