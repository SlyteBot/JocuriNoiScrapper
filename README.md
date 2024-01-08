
# Web Scraper for Jocurinoi.ro

## Overview

This Python web scraper is designed to extract information from multiple product pages on a website. The scraper follows a three-step process: it first scrapes the links to individual product pages, then collects information from those pages, and finally, downloads thumbnails and uploads the gathered data to an SQL server.


## Features

*   **Multithreaded Scraping:** The scraper utilizes multithreading to improve efficiency, enabling simultaneous processing of multiple product pages.
    
*   **Beautiful Soup 4 Integration:** Beautiful Soup is used for parsing HTML and extracting relevant information from the web pages.
    
*   **MySQL Database Integration:** The scraper is configured to connect to a MySQL server to store the scraped data. Ensure you have a MySQL server set up and update the database connection details in the script.


## Usage

1.Clone the repository:
```
git clone https://github.com/SlyteBot/JocuriNoiScrapper.git
```
2.Setup your env file:
```
HOST="HOST"
USERNAME="USERNAME"
DATABASE="DATABASE"
PASSWORD="PASSWORD"
```
3.Make sure you have the following dependencies installed:
```
pip install -r requirements.txt
```
4.Run the scraper
```
python main.py
```
The scraper will start processing the game pages, collecting information, downloading thumbnails, and uploading data to the MySQL server.


## Disclaimer

This scraper is provided as-is and should be used responsibly and in compliance with the website's terms of service. Make sure to review and respect the website's robots.txt file and policies.


Feel free to customize and extend the code to fit your specific needs. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request. Happy scraping!
