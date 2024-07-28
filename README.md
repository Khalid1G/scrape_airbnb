# Airbnb Property Data Scraper

This script scrapes property data from Airbnb using Selenium and BeautifulSoup. The extracted data includes property titles, ratings, prices, and prices with tax. The data is saved into a CSV file.

## Prerequisites

- Python 3.x
- Google Chrome

## Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

1. **Setup the WebDriver**

   The `setup_driver` function sets up the Chrome WebDriver. It uses the `chromedriver-autoinstaller` to automatically install the correct version of ChromeDriver.

   ```python
   def setup_driver(headless=True):
       """Setup Chrome WebDriver with specified options."""
       chromedriver_autoinstaller.install()
       options = Options()
       options.headless = headless
       driver = webdriver.Chrome(options=options)
       return driver
   ```

2. **Fetch Page Source**

   The `get_page_source` function loads the given URL and fetches the page source after a specified sleep time.

   ```python
   def get_page_source(url, sleep_time=3):
       """Fetch page source after loading the given URL."""
       driver = setup_driver()
       driver.get(url)
       time.sleep(sleep_time)
       page_source = driver.page_source
       driver.quit()
       return page_source
   ```

3. **Parse Property Data**

   The `parse_property_data` function parses the property data from the provided HTML elements.

   ```python
   def parse_property_data(all_data):
       """Parse property data from the provided HTML elements."""
       data_list = []
       for item in all_data:
           data = {}
           data["property-title"] = (
               item.find("div", {"data-testid": "listing-card-title"}).text.strip()
               if item.find("div", {"data-testid": "listing-card-title"})
               else None
           )
           data["rating"] = (
               item.find("div", {"class": "t1a9j9y7"}).text.split()[0]
               if item.find("div", {"class": "t1a9j9y7"})
               else None
           )
           data["price"] = (
               item.find("span", {"class": "_14y1gc"}).text.strip().split()[0]
               if item.find("span", {"class": "_14y1gc"})
               else None
           )
           data["price_with_tax"] = (
               item.find("div", {"class": "_i5duul"})
               .find("div", {"class": "_10d7v0r"})
               .text.strip()
               .split(" total")[0]
               if item.find("div", {"class": "_i5duul"})
               and item.find("div", {"class": "_i5duul"}).find(
                   "div", {"class": "_10d7v0r"}
               )
               else None
           )
           data_list.append(data)
       return data_list
   ```

4. **Main Function**

   The `main` function coordinates the scraping process: it fetches the page source, parses the property data, and saves it into a CSV file.

   ```python
   def main():
       url = "https://www.airbnb.fr/s/Europe/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-08-01&monthly_length=3&monthly_end_date=2024-11-01&price_filter_input_type=0&channel=EXPLORE&place_id=ChIJhdqtz4aI7UYRefD8s-aZ73I&date_picker_type=calendar&checkin=2024-08-08&checkout=2024-08-16&source=structured_search_input_header&search_type=filter_change"

       html_content = get_page_source(url)
       soup = BeautifulSoup(html_content, "html.parser")
       all_data = soup.find_all("div", {"itemprop": "itemListElement"})

       parsed_data = parse_property_data(all_data)

       df = pd.DataFrame(parsed_data)
       df.to_csv("airbnb.csv", index=False, encoding="utf-8")
       print(parsed_data)


   if __name__ == "__main__":
       main()
   ```

## Running the Script

To run the script, execute the following command:

```bash
python main.py
```

or

```bash
python3 main.py
```

## Output

The script will generate a `airbnb.csv` file containing the scraped property data.

## Note

- Make sure to have Google Chrome installed on your system.
- The script is set to run in headless mode by default. To see the browser in action, set `headless=False` in the `setup_driver` function.

## Disclaimer

This script is for educational purposes only. Make sure to comply with Airbnb's terms of service when scraping data from their site.
