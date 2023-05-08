
# Sears Ecommerce Bot

Sears Bot is a highly versatile and intelligent automation tool that utilizes the power of the Python programming language. It is designed to scrape all the target data from [Sear](https://www.sears.com/) website.
A Python bot designed for Sears website data scraping is a program that is written using the Python programming language. This bot is specifically created to scrape, or gather, information from the Sears website. This information can include product details, prices, and availability. This data can be useful for a variety of purposes, such as price comparison, inventory management, or market research. The bot can be designed to navigate through various pages of the Sears website, extract the desired data and save it to a file or database for further analysis. This type of bot can be useful for businesses and individuals looking to gain insights into the Sears website and its products.

## Functionalities

* GUI fields: Bot have a GUI that have 2 fields one is “Add files” and second one is “Output Folder”.

    * Add files: Here Bot will take input file which consist of sears link with category id.
    * Output Folder: Here the bot will select a directory where client want to store their data.

* GUI Validation: Bot GUI have strong validation.

    * Add files: if user not upload the file bot will show an error box to upload the file
    * Output folder: if user not selects the output directory the bot will show an error box to select the output directory.
    * Wrong input file: if user select wrong path bot will show an error to select the correct path file.

* List of Tuples: Bot will read all links with category id from input file and store it in a list of tupel variable.
* Display length of list: Bot will display how many links it have
* Lunch Browser:  Bot will launch the browser.
* Brand name folder: Bot will scrape brand name from sears webpage and make a folder with that name.
* Links scraping: Bot will create a csv file and check it if file not exist then bot will start products links scraping.
* Data Scraping: Bot will scrape the following data from sears website:

    * Product Name: Bot will scrape each product name.
    * Actual price: Bot will scrape each product actual price.
    * Regular price: Bot will scrape each product regular price.
    * Categories: Bot will scrape each product categories.
    * Short Description: Bot will scrape each product short description.

    * Long Description: Bot will scrape each product long description.
    * Variation SKU: Bot will scrape variation SKU of each product.
    * Product URL: Bot will scrape each product URL.
    * Item: Bot will scrape each product item number.
    * Category id: Bot will also store category id.
    * Images: Bot will scrape each product all images.

* Optional Data:  Bot will also store the option columns data like:

    * Type: it will store “simple” as a value.
    * Product_is_main: “Main” or “Variation” as a value.
    * Tags: it will be an empy column.
    * Attribute_id: it will be an empty column.
    * Attributes: it will be an empty column.
    * Option: it will be an empty column.

* Display counter: Bot will show counter on GUI that how many products are scraped.
* Execution Time: Bot will show an execution time on GUI after completing the scraping.
* Closing Browser: after completing all the scraping bot will close the browser.



