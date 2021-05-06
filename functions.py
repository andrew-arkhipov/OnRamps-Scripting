from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver):
    """
    Logs the user into OnRamps

    :param webdriver driver: standard selenium webdriver

    :return None
    """

    # get login page
    driver.get("https://onramps.instructure.com")

    # wait for manual login
    WebDriverWait(driver, 45).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Dashboard') or contains(text(), 'Courses')]")))


def get_college_course_links(driver, url, first_page=1, last_page=19):
    """
    Gets all college courses (can easily be adapted to high school)

    :param webdriver driver: standard selenium webdriver
    :param string url: the url string of the courses page for a given subject (e.g. College Algebra, Precalculus, etc.)
    :param integer first_page: the first page in the courses list that has college courses listed, should almost always be 1, defaults to 1
    :param integer last_page: the last page in the courses list that has college courses listed, it's okay if the page has some high school courses listed, 
                              defaults to 19 to avoid missing any pages

    :return list course_links: returns a list of the links for all college courses in a given subject
    """

    def _valid(element):
        """ 
        Helper function that determines if a link points to a valid college course

        :param WebElement element: standard selenium WebElement used for programmatic interaction

        :return bool: true or false based on given checks (feel free to change given the changes Canvas frequently makes)
        """

        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'UT COLLEGE' not in text: # 'UT COLLEGE' can be changed to 'HS' for high school courses
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def _parse_page(url):
        """
        Helper function that parses and scrapes the links of a single page in the list of pages of courses for a given subject

        :param string url: the url string of a single page in the list of pages of courses

        :return list courses: returns a list of of the links for all college courses on the given page
        """

        # get page
        driver.get(url)

        # wait for page to load
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr/td/a/span[contains(text(), 'COLLEGE')]")))
        except:
            # couldn't find any links
            return []

        # fetch all potential courses
        elements = [elem for elem in driver.find_elements_by_xpath("//a")]

        # filter links for valid course numbers
        courses = []
        for elem in elements:
            if _valid(elem):
                link = elem.get_attribute('href')
                courses.append(link)

        return courses

    # the actual code that uses the above helper functions
    course_links = []
    for page in range(first_page, last_page + 1):
        course_links.extend(_parse_page(driver, f"{url}page={str(page)}"))

    return course_links