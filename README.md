# frustrated-stockfinder
## overview
Created a program that can search through websites of interest for stock in various products. My main targets were the XBOX Series X and 30 Series GPU.

Two main tools utilized for this program are requests and selenium. Selenium is a headless browser often used as a tool for website testing. The websites that are in sites.py have a key-value pair specifying which method would be preferable (requests or Selenium). 
It is important to download the necessary files and define the driver path for this program to work. To get started with selenium, I recommend using the following link: https://chromedriver.chromium.org/getting-started

## requests 
If the search method utilizes the requests library, it specifies the section and html attribute type where our target text is stored. It does this to filter out user reviews and comments that could also contain our keywords.
If sites.py stores just a single string in its key-value pair for target, it will search for that one word. If it contains a list of strings, it will iterate through all of them. This is useful for some websites that aren't consistent in how they display if an item is in stock.
These websites could just list: "3 Remaining", "Add to Cart", "Pick up in Store". Any of these would be of interest to us.

## selenium
Selenium just needs the attribute type for our target button (XPATH, Class, or ID) and the value for the key-value pairs. 

## notifications
Utilized pushover for notifications; However, I believe Twilio and Discord are also cost effective notification options. You will need to sign up on the pushover website and get a client name and token.

## diagnostics
The name of the game is improving the code and eliminating false positives and errors. To assist with this, the program will take a snapshot of the page html if we get a bite. This can be reviewed later to assist with improving the code.
