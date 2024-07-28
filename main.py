import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup


def setup_driver(headless=True):
    """Setup Chrome WebDriver with specified options."""
    chromedriver_autoinstaller.install()
    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(options=options)
    return driver


def get_page_source(url, sleep_time=3):
    """Fetch page source after loading the given URL."""
    driver = setup_driver()
    driver.get(url)
    time.sleep(sleep_time)
    page_source = driver.page_source
    driver.quit()
    return page_source


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
