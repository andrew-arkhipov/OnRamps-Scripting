from time import sleep
from typing import List, Callable, Dict
from functools import wraps
from dataclasses import dataclass
from collections import defaultdict
from utils.courses.courses import HighSchoolCourse, CollegeCourse
import shutil
import pandas as pd
import os
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver, url):
    # get login page
    driver.get(url)

    # wait for manual login
    WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'UT COLLEGE')]")))


def download_manager(func):

    @wraps(func)
    def inner(*args, **kwargs):
        # preprocessing
        driver = args[0]
        size = len(os.listdir(driver.download_directory))

        # run scraper
        func(*args, **kwargs)

        # wait for download to start
        while len(os.listdir(driver.download_directory)) == size:
            sleep(0.05)

    return inner


def get_course_type():
    # get desired course type from stdin
    print()
    course_type = input("High school or college [HS/CO]: ").lower().strip()

    # error checking
    while course_type not in {'hs', 'co'}:
        print('Please enter a valid course type.')
        course_type = input("High school or college [HS/CO]: ").lower().strip()

    # assign course
    if course_type == 'hs':
        course = HighSchoolCourse()
    else:
        course = CollegeCourse()
    
    return course


def get_unit_number():
    # get unit number for grading purposes from stdin
    unit = input("Enter the unit number: ").strip()

    # error checking
    while not unit.isdigit():
        print('Please enter a valid unit number.')
        unit = input("Enter the unit number: ").strip()

    return unit


def get_survey_inputs():
    # get inputs from stdin
    inputs = {
        'url': input('Enter Qualtrics survey URL: '),
        'intro': input('Enter intro text: '),
        'finish': input('Enter finished text: ')
    }
    
    return inputs


@dataclass
class Assignment:
    name: str
    duration: int


def get_assignments():
    # prompt user
    print()
    print("Please enter the names and durations of the assignments you would like to add accommodations to exactly as they appear in Canvas.")
    print("Enter 'q' into the assignment name to indicate all assignments have been added.")
    print()

    # get first assignment
    name = input("Assignment name (e.g. Exam Unit 3: Part 2): ").strip()
    duration = int(input("Duration (e.g. 30): ").strip())
    print()
    res = [Assignment(name, duration)]

    # continue adding assignments as desired 
    while True:
        name = input("Assignment name: ").strip()
        if name == 'q':
            break
        duration = int(input("Duration: ").strip())
        print()
        res.append(Assignment(name, duration))

    return res


def get_range():
    # get range
    print()
    start = int(input("Enter the first page number of the desired courses: "))
    end = int(input("Enter the last page number of the desired courses: "))

    return range(start, end + 1)

@dataclass
class Student:
    first: str
    last: str
    multiplier: str


def get_students():
    # dictionary of students
    students = defaultdict(list)

    # get filename
    print()
    filename = input("Enter the filename of the accommodations csv: ")
    print()

    # get dataframe
    df = pd.read_csv(f"{os.path.dirname(sys.executable)}/{filename}")
    # df = pd.read_csv(filename)

    # parse through students
    for i, row in df.iterrows():
        if not row['Accommodation Request'].startswith("Extended time"):
            continue

        # parse through accommodation to get time multipler
        accom = row['Accommodation Request'].split(" ")
        multiplier = accom[5][1:-1]

        # create new instance of a student
        students[row['College Course']].append(Student(first=row['Student First Name'], last=row['Student Last Name'], multiplier=multiplier))

    return students