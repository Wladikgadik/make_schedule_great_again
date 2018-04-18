import requests
from bs4 import BeautifulSoup

class pdf_table:
    def __init__(self, graduate, faculty_name, spec_code, spec_name, course_value, semester_value, group_name, link, time_period):
        self.graduate = graduate
        self.faculty_name = faculty_name
        self.spec_code = spec_code
        self.spec_name = spec_name
        self.course_value = course_value
        self.semester_value = semester_value
        self.group_name = group_name
        self.link = link
        self.time_period = time_period
try:
    full_time_page = requests.get('https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html')
    soup = BeautifulSoup(full_time_page.text, 'html.parser')
    rasp = soup.find('div', attrs={'class': 'column-center_rasp'})
    RASP_CONTENT = rasp.contents
    for each in range(len(RASP_CONTENT)):
        graduate = ''
        if rasp.contents[each].attrs['class'][0] == 'headerEduPrograms':
            graduate = rasp.contents[each].contents[0]
            rasp_table = rasp.contents[each+2]
except requests.RequestException:
    print('Something wrong, perhabs with vyatsu, not with your script, ofc')

print('')