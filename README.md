# UW-1
=============================
## Prerequirements
* ebaysdk==2.2.0
* python-dotenv==0.19.2
## Installation
```
git clone https://github.com/ilSerpente/UW-1.git
```
## Setup tokens
1) Open env_template file and set tokens
2) Rename file: 
```
mv env_template .env
```
## Running
Move to project folder:
```
cd UW-1
```
Run script:
```
python ebay.py
```
## Options
```
python3 ebay.py --help
Usage: ebay.py [options]

Options:
  -h, --help            show this help message and exit
  -d, --debug           Enabled debugging [default: False]
  -n DOMAIN, --domain=DOMAIN
                        Specifies the eBay domain to use (e.g.
                        api.sandbox.ebay.com).
  -a ACTION, --action=ACTION
                        Specifies action:
                        get_all_categories [CategorySiteID][LevelLimit]
                        get_category_specific_fields [CategoryID]
                        list_item (set item fields in item_template.py)
                        test_list_item (set item fields in item_template.py)
```

## Logs
After execution a command you will receive path to file with execution result:
```
python3 ebay.py -a get_all_categories 100 1
Running GetCategories eBay request. With params:
 DetailLevel: ReturnAll
 CategorySiteID:  100
 LevelLimit':  1
Complet exucution log:  ./logs/get_all_categories_02_10_2022-16_34_57.json
```
## Usage
1) Get all categories, you can select [eBay Global ID](https://developer.ebay.com/DevZone/merchandising/docs/Concepts/SiteIDToGlobalID.html) as first parameter and as second search depth in the category tree:
```
python3 ebay.py get_all_categories 2 1
```
2) After execution open log file and search for needed category ID:
![alt text](https://github.com/ilSerpente/UW-1/example_img/blob/main/example.png?raw=true)

3) Get category specitic fields:
```
python3 ebay.py -a get_category_specific_fields 617
Running GetCategorySpecifics eBay request. With params:
 CategoryID:  617
Complet exucution log:  ./logs/get_category_specific_fields_02_10_2022-17_11_59.json
```
4) Search for required fields in log file:
![alt text](https://github.com/ilSerpente/UW-1/example_img/blob/main/example2.png?raw=true)
You have to find all fields with "UsageConstraint": "Required" and save their names ("Name": "Movie/TV Title") in item_template.py

5) Adding fields:
![alt text](https://github.com/ilSerpente/UW-1/example_img/blob/main/example3.png?raw=true)

6) Listing item test:
```
python3 ebay.py -a test_list_item
Running VerifyAddItem eBay request. With item_template
Complet exucution log:  ./logs/test_list_item_02_10_2022-17_22_13.json
```
7) Real listing:
```
python3 ebay.py -a list_item 
Running AddItem eBay request. With item_template
Complet exucution log:  ./logs/get_item_02_10_2022-17_23_20.json
```