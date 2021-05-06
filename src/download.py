from typing import List
from utils.utils import login, download_manager, get_course_type, get_range
from utils.driver import Driver
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@download_manager
def download(driver: Driver, url: str) -> None:
    """
    Downloads the grade report
    """
    # visit the course page
    driver.get(url)

    # wait for download button
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-component='ActionMenu']"))).click()

    # download grade report
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Export']"))).click()


def run(driver: 'Driver', url: str, _range: 'range', course: 'Course'):
    # initialize
    course_links = course.get_links(driver, url, _range)
    
    # parse
    for course_link in course_links:
        download(driver, f"{course_link.link}/gradebook")


if __name__ == "__main__":
    # courses main page
    url = 'https://onramps.instructure.com/accounts/169964?'

    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('target_dir', nargs='?')
    args = parser.parse_args()

    # determine course type
    course = get_course_type()

    # get range
    _range = get_range()

    # initialize driver with target download directory
    driver = Driver.initialize(args.target_dir)
    login(driver, url)

    # begin scraping
    run(driver, url, _range, course)