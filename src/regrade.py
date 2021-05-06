from typing import List, Tuple
from time import sleep

from utils.driver import Driver
from utils.utils import login
from utils.courses.courses import CollegeCourse
from argparse import ArgumentParser

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def grade_student(driver: 'Driver') -> None:
    """
    Helper function to add fudge points to the student's grade for curving purposes
    """
    # wait for questions to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div/div/span[contains(text(), 'Question 1') or contains(text(), 'Pregunta 1')]")))

    question = driver.find_element_by_xpath("//div/div/span[contains(text(), 'Question 1') or contains(text(), 'Pregunta 1')]/../..")
    score = int(question.find_element_by_xpath("//div[@class='header']/span/div[@class='user_points']/input[@class='question_input']").get_attribute('value'))

    if score == 0:
        total = float(driver.find_element_by_xpath("//span[@class='score_value']").text)

        fudge = driver.find_element_by_xpath("//input[@id='fudge_points_entry']")
        current_fudge = float(fudge.get_attribute('value') or 0)

        fudge.clear()

        points = round(round((total - current_fudge) * 10/9, 2) - (total - current_fudge), 2)
        fudge.send_keys(str(points))

    # submit
    driver.find_element_by_xpath("//button[@class='btn btn-primary update-scores']").click()

    # next student
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()


def show_all_sections(driver) -> None:
    """
    Helper function that manually moves the mouse over the "show all sections" button in order to ensure all students are getting a curved grade
    """
    action = ActionChains(driver)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='students_selectmenu-button']")))
    dropdown = driver.find_element_by_xpath("//a[@id='students_selectmenu-button']")

    # click on dropdown menu
    action.move_to_element(dropdown).click(on_element=dropdown)

    # move mouse over to show all sections option
    # action.move_by_offset(0, 40).move_by_offset(-170, 0).click().perform()

    action.move_by_offset(0, 40).perform()
    action.move_by_offset(-170, 0).perform()
    action.click()

    action.perform()


def access_assignment(driver: 'Driver', url: str) -> int:
    """
    Accesses the specificed assignment, opens SpeedGrader, and gets the number of students to loop through
    """

    driver.get(url)

    try:
        # the XPath in this line can change in order to regrade other assignments
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '7 & 8')]"))).click()
    except:
        # not a valid high school course
        return 0

    # open survey tab
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a/i/span[contains(text(), 'SpeedGrader')]/../.."))).click()

    # switch to new tab
    driver.switch_to.window(driver.window_handles[1])

     # use actions to click on dropdown menu and show all sections
    show_all_sections(driver)

    # wait for speedgrader to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='x_of_x_students_frd' and contains(text(), '/')]")))

    student_fraction = driver.find_element_by_xpath("//div[@id='x_of_x_students_frd']")
    num_students = int(student_fraction.text.split("/")[1])

    return num_students


def run(driver: 'Driver', num_students: int) -> None:
    # parse
    for _ in range(num_students):
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='icon-arrow-right next']")))
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@id='this_student_does_not_have_a_submission' and @style='display: block;']")))
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='icon-arrow-right next']"))).click()
            continue
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='speedgrader_iframe']")))
            grade_student(driver)
        except:
            driver.switch_to.default_content()
            driver.find_element_by_xpath("//i[@class='icon-arrow-right next']").click()
            continue

def test():
    url = "https://onramps.instructure.com/courses/3018432/gradebook/speed_grader?assignment_id=28393321&student_id=11553403"

    driver = Driver.initialize()
    driver.get(url)
    sleep(30)

    run(driver, 71)


def main():
    url = "https://onramps.instructure.com/accounts/172690?" # college algebra

    driver = Driver.initialize()
    login(driver, url)

    course = CollegeCourse()

    # bad code, the range shouldn't be hard coded, can be adapted for any subject
    links = course.get_links(driver, url, range(1, 7))

    # run
    for link in links:
        num_students = access_assignment(driver, f"{link.link}/assignments")
        run(driver, num_students)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        

if __name__ == "__main__":
    main()