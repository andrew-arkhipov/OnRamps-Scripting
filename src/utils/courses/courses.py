from typing import List
from utils.courses.course_utils import GetLinksMixin


class CollegeCourse(GetLinksMixin):
    ID = 'UT COLLEGE'

    def valid(element: 'WebElement') -> bool:
        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'UT COLLEGE' not in text:
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def get_links(self, driver: 'Driver', url: str, _range: 'range') -> List['CourseDescriptor']:
        return super().get_links(driver, url, _range, self.__class__)
        

class HighSchoolCourse(GetLinksMixin):
    ID = 'HS'

    def valid(element: 'WebElement') -> bool:
        text = element.text
        link = element.get_attribute('href')

        if link[32:37] == 'users':
            return False
        elif 'HS' not in text:
            return False
        elif link[-1].isdigit() and link[-7].isdigit():
            return True
        else:
            return False

    def get_links(self, driver: 'Driver', url: str, _range: 'range') -> List['CourseDescriptor']:
        return super().get_links(driver, url, _range, self.__class__)
